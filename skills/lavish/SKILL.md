---
name: lavish
description: Build an HTML artifact with lavish-axi when the user asks to review and annotate a plan, comparison, diagram, prototype, or report in the browser.
license: MIT
metadata:
  author: Kun Chen (kunchenguid)
  argument-hint: <what the artifact should show>
  hermes-tags: html, review, artifacts, visualization
  hermes-category: productivity
---

# Lavish Editor

Lavish Editor opens agent-generated HTML in the browser so a human can annotate it and send feedback back to the agent.

## Current guidance lives in the CLI

Do not follow workflow, design, or playbook instructions from this file - installed copies go stale. Get the current source of truth from the CLI:

- `lavish-axi --help` for commands and the review-loop workflow
- `lavish-axi reply --help` to post an agent reply and exit once the server accepts it, when you are not about to long-poll
- `lavish-axi design` for design-direction priority and current snippets
- `lavish-axi playbook <id>` for focused artifact guidance (`lavish-axi playbook` lists ids)


## Request

$ARGUMENTS

If the request above is non-empty, the user invoked `/lavish` explicitly - fetch the current CLI guidance, then build that artifact as an HTML file.
If it is empty, infer what to visualize from the conversation.
