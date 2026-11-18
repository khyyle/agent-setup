#!/usr/bin/env node
import { parseArgs } from "node:util";

const args = process.argv.slice(2);
if (args.length === 1 && ["-v", "-V", "--version"].includes(args[0])) {
  console.log("0.1.0");
  process.exit(0);
}

const help = [
  "exa-axi search \"query\" [--limit 1..10] [--full]",
  "exa-axi read <http-or-https-url> [--chars 1..20000]",
  "Search web sources or read a page through Exa's public MCP endpoint. Output is TOON.",
].join("\n");

function integer(value, max, flag) {
  if (!/^\d+$/.test(value) || Number(value) < 1 || Number(value) > max) {
    throw new Error(`${flag} must be an integer between 1 and ${max}`);
  }
  return Number(value);
}

function requestFor(command, argv) {
  if (!["search", "read"].includes(command)) throw new Error("Unknown command");
  const options = command === "search"
    ? { limit: { type: "string", default: "5" }, full: { type: "boolean", default: false } }
    : { chars: { type: "string", default: "3000" } };
  const { values, positionals } = parseArgs({ args: argv, options, allowPositionals: true });
  if (positionals.length !== 1 || !positionals[0].trim()) throw new Error("Supply one query or URL");
  if (command === "search") {
    return { name: "web_search_exa", arguments: { query: positionals[0], numResults: integer(values.limit, 10, "--limit") }, full: values.full };
  }
  const url = new URL(positionals[0]);
  if (!["https:", "http:"].includes(url.protocol) || url.username || url.password) {
    throw new Error("Supply an HTTP(S) URL without credentials");
  }
  return { name: "web_fetch_exa", arguments: { urls: [url.href], maxCharacters: integer(values.chars, 20000, "--chars") } };
}

function searchOutput(body, full) {
  // The hosted tool returns labeled plain text, sometimes several articles per MCP content block.
  const header = /^Title:[ \t]*([^\n]*)\r?\nURL:[ \t]*(https?:\/\/[^\s]+)[ \t]*\r?$/gm;
  const headers = Array.from(body.matchAll(header));
  if (!headers.length) {
    if (!body || /^no (?:search )?results(?: found)?[.!]?$/i.test(body)) return { count: 0, results: [] };
    return { response: full ? body : body.slice(0, 800), ...(body.length > 800 && !full ? { hint: "Repeat search with --full for the full upstream response" } : {}) };
  }
  let truncated = false;
  const results = headers.map((match, index) => {
    const content = body.slice(match.index + match[0].length, headers[index + 1]?.index ?? body.length)
      .trim().replace(/^(?:(?:Published|Author):[^\n]*\n)*(?:Highlights|Text|Contents):\s*/i, "").trim();
    truncated ||= !full && content.length > 480;
    return { title: match[1].trim(), url: match[2], excerpt: full ? content : content.replace(/\s+/g, " ").slice(0, 480) };
  });
  return { count: results.length, results, ...(truncated ? { hint: "Use --full for all returned excerpts, or exa-axi read <url> for a page" } : {}) };
}

async function main() {
  if (!args.length || args.includes("--help") || args[0] === "-h") return console.log(help);
  const { encode } = await import("@toon-format/toon");
  let request;
  try {
    request = requestFor(args[0], args.slice(1));
  } catch (error) {
    console.log(encode({ error: error.message, help }));
    process.exitCode = 2;
    return;
  }

  const { Client } = await import("@modelcontextprotocol/sdk/client/index.js");
  const { StreamableHTTPClientTransport } = await import("@modelcontextprotocol/sdk/client/streamableHttp.js");
  const client = new Client({ name: "personal-exa-axi", version: "0.1.0" });
  const signal = AbortSignal.timeout(45000);
  try {
    const transport = new StreamableHTTPClientTransport(new URL("https://mcp.exa.ai/mcp"), { requestInit: { signal } });
    await client.connect(transport, { signal });
    const result = await client.callTool({ name: request.name, arguments: request.arguments }, undefined, { signal });
    const body = result.content.filter(part => part.type === "text").map(part => part.text).join("\n").trim();
    if (result.isError) throw new Error(body.slice(0, 500) || "Exa rejected the request");
    if (result.content.some(part => part.type !== "text") && !body) throw new Error("Exa returned an unsupported content format");
    console.log(encode(args[0] === "search" ? searchOutput(body, request.full) : { url: request.arguments.urls[0], text: body }));
  } catch (error) {
    console.log(encode({ error: String(error.message).slice(0, 500), hint: "Check network access and the public Exa rate limit" }));
    process.exitCode = 1;
  } finally {
    await client.close();
  }
}

await main();
