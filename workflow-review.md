# Local workflow review

Three independent reviewers exercised the development, research and terminal workflows on November 17, 2026, against repository revision `452d272`. The criteria were observable behavior through the real entry point, reproducible local evidence, readable and proportionate changes, and a fresh review grounded in the original requirement. The terminal review also checked OpenAI selection, skill discovery and session boundaries. The scores apply to these exercises. Discovery covered 31 skills. Specialist skills outside these exercises were ungraded.

A score of **4** means the exercise met its criteria, **3** means it worked with minor friction, **2** means it needed a workaround or exposed a material ambiguity, **1** means it blocked or steered the task to a wrong outcome, and **0** means it was unavailable.

| Workflow | Grade | Evidence and limitation |
|---|---|---|
| Ponytail, proof of fix and fresh code review | 4/4 each | A checkbox appeared saved but reverted on reload. Real Chromium and a disk-backed store reproduced the bug. A one-line fix passed the identical journey. The reviewers inspected before/after screenshots, request bodies and DOM traces. Independent review of the skill setup also reproduced the TDD selection mismatch. |
| Search-first and coding standards | 3/4 each | Searching found the existing Playwright installation. Its decision table also encourages combining several weak matches. The coding skill helped keep the edit small, but three references point to ECC resources absent from this checkout. |
| TDD | 2/4 | Red and green checkpoints worked. Pi's actual automatic prompt included the skill for general feature work. The imported text prescribes 80% coverage and per-stage commits. This conflicts with the shared rule that reserves full TDD for explicit test-first work. |
| E2E testing | 2/4 | The browser caught the regression. The trace example uses Chromium performance tracing while asking for DOM snapshots. Some examples register the response wait after the action that triggers it, which can miss a fast response. |
| Research loop | 4/4 | A preregistered comparison of two finite-difference formulas on nine rational inputs used the analytic derivative of a square as its independent reference. Maximum absolute errors were zero and one half. Two runs produced byte-identical output, and the handoff command reproduced it. |
| ARIS research wiki | 2/4 | Idea, claim and experiment records and their evidence links worked offline. Recording a planned experiment with no verdict stored a negative result with medium confidence. A status-only replacement erased the claim's original evidence while retaining a support edge. |
| Pi multi-chat and skill selection | 4/4 for the tested cases | Two simultaneous named Pi processes had distinct session IDs and the configured OpenAI model. Both exposed all 31 skill commands. At the time of this test, unslop and no-mistakes were explicit-only. The current no-mistakes router enables automatic selection for gated delivery. TDD's separate routing issue is scored above. |
| Playwright AXI | 3/4 | A real Chromium test on a local HTTP fixture went from red to green. Blocked file navigation also exited zero while its JSON contained a tool error. The success check must assert resulting page state. |
| Herdr operator guidance | 3/4 | Installed Herdr 0.9.5 help and key configuration confirmed persistent named sessions and tab controls. The reviewer was outside a Herdr pane and did not exercise live reattachment. |

## Where to spend the next edit

1. **Protect research evidence first.** Keep planned experiments in the study tracker. Supply an explicit verdict and provenance for completed runs. Treat `--update-on-exist` as a whole-record replacement. Prefer a new identified amendment linked to the old record. A helper-level fix should distinguish planned runs from measured outcomes and preserve claim history or reject incomplete amendments. [ARIS helper](skills/aris/scripts/research_wiki.py)
2. **Reserve full TDD for test-first assignments.** The task-specific description now makes that workflow discoverable for explicit test-first work. The shared testing rule covers everyday changes. The imported stage commits and 80% target are still part of the full workflow. [TDD workflow](skills/tdd-workflow/SKILL.md)
3. **Fix the two E2E examples.** Register the response promise before the click and await it afterward. For a Playwright trace viewer archive, use `context.tracing.start({ screenshots: true, snapshots: true })`, drive the journey and call `context.tracing.stop({ path: 'trace.zip' })`. Assert the post-reload result. Check AXI's nested errors as well as its exit status. [E2E testing](skills/e2e-testing/SKILL.md) · [Playwright AXI](skills/playwright-axi/SKILL.md)
4. **Keep dependency research deliberate.** The original search procedure includes full researcher and planner roles. Enable it for a project or a Pi session when comparing alternatives. The renamed TypeScript examples can be used directly. [TypeScript coding standards](skills/typescript-coding-standards/SKILL.md) · [Search-first](skills/search-first/SKILL.md)

## Terminal preset verification

A fresh reviewer caught an incorrect tmux target for the optional Music status. After correction, concurrent launches produced one tab set. A real terminal client rendered the top bar, clicked the + to open an independent Pi, opened a regular Codex tab from the keyboard menu, and reattached to its selected review tab. Reopening restored a missing Git tab. Distinct project paths sharing a basename stayed separate.

The macOS integration recognized Music both closed and open. After Automation access was granted, the live app reported stopped playback and the status stayed quiet. Track formatting and transport command dispatch passed with simulated player data. A live playing track and changes to real playback were not exercised.

The current preset launches Encore for Apple Music. Run `./terminal/check-preset.sh` on macOS to check layout, reattachment and the optional Encore tab on a private tmux socket. The test uses stand-ins for the model clients and Encore.

## Skill cross-references and Pi extensions

The November 17 audit covered the 31 skill entry points then installed. Five pointed readers toward another skill or agent role.

| Entry point | What the audit found | Resolution |
|---|---|---|
| `verify-change` | Handed evidence to `ponytail-review` when a fresh review was requested. | The shared verification rule now covers how to compare visual states and report evidence. The separate command was retired. |
| `research-loop` | Listed `ponytail`, `ponytail-review`, `humanizer`, `aris`, and a second research-wiki entry as optional integrations. | Retired globally. `nexa-classifier` already has its own ARIS planning and wiki skills and a tracked research record. The original skill and its templates are in `b8c29ef:skills/research-loop/`. |
| [aris](skills/aris/SKILL.md) | Referred to `research-loop` as coordinator. | The experiment and wiki workflows and bundled scripts remain available. The coordination pointer was removed. |
| [typescript-coding-standards](skills/typescript-coding-standards/SKILL.md) | The original `coding-standards` named installed `api-design`, absent `frontend-patterns` and `backend-patterns`, and missing `rules/common/coding-style.md`. | The renamed skill opens directly on the language-specific examples. Cross-language conventions live in the shared rules. |
| [search-first](skills/search-first/SKILL.md) | Offered planner, researcher and architect roles, a client-specific delegation example, and an absent `iterative-retrieval` skill. | The original procedure is available per project or Pi session. The shared reuse rule covers routine work. |

The other 26 entry points contained no comparable skill handoff. The `axi` in `no-mistakes axi run` names a CLI command. The `ponytail:` example in `ponytail-review` describes a legacy code comment. The [no-mistakes router](skills/no-mistakes/SKILL.md) points to its own pinned operating instructions.

### Instruction hierarchy

1. **Shared rules** carry cross-project expectations for naming, comments, control flow, colocation, reuse, and observable verification.
2. **Repository instructions and runnable checks** own setup commands, fixtures, launch details and evidence paths. When a user journey repeatedly takes manual setup, put that setup behind one command in the owning project. A project-specific verification skill earns its place when agents need guidance to choose or drive several such checks.
3. **On-demand skills** own distinct procedures such as independent review, deliberate TDD, or gated delivery. Use a cross-skill pointer when another skill owns a concrete step and the condition for handing it off is clear. Both original Ponytail skills are globally discoverable. The authoring skill advertises itself for any coding task.

Kun Chen's AXI emphasizes contextual help from the executable, and no-mistakes generates its skill and checks for drift. Mitchell Hashimoto pairs short instructions based on observed mistakes with runnable screenshot and test tools. Lauren Tan's pstack uses the project's existing harness or builds an app-specific verification procedure. Those examples support a brief universal rule and project-owned proof. [Kun Chen's AXI](https://github.com/kunchenguid/axi) · [no-mistakes build targets](https://github.com/kunchenguid/no-mistakes#development) · [Hashimoto's harness examples](https://mitchellh.com/writing/my-ai-adoption-journey) · [pstack verification guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md)

There are good reasons to compose skills on complex work. Matt Pocock's implementation workflow calls for a distinct code-review pass. Dex Horthy describes handing research and plan artifacts to later phases. Both give the next phase a concrete input. For this setup, the same rationale supports a study handoff or a branch review with the original requirements. [Pocock's engineering skills](https://github.com/mattpocock/skills) · [Horthy on context engineering](https://www.hlyr.dev/blog/advanced-context-engineering)

### Skill provenance after cleanup

| Comparison | Decision |
|---|---|
| Exact pinned entry files | `axi`, `herdr`, `unslop`, `ponytail`, `ponytail-review`, `django-patterns`, and `search-first` match their sources. Search-first is project- or session-selected. Unslop also has local Codex invocation metadata. The full pinned `no-mistakes` instructions sit behind a local, model-invocable trigger for gated delivery. |
| Local tool compatibility | `gh-axi` and `quota-axi` use the installed binaries in place of unversioned downloads. `chrome-devtools-axi` and `playwright-axi` use the installed tools and describe distinct use cases. `lavish` uses the pinned binary and selects interactive HTML review when that is the requested deliverable. |
| Language examples and TDD | `typescript-coding-standards` is a renamed ECC adaptation. It removes missing references, corrects shared-state sorting and error-handling examples, and replaces the 50-line helper cutoff with a readability criterion. `tdd-workflow` changes only its discovery description. |
| Procedure plus local entry guidance | `context7-mcp` keeps the narrower version-specific trigger and official-docs fallback. The operational instructions, from resolving the library ID through using the results, match Upstash. The `aris` entry links to the complete pinned planning and wiki procedures and their supporting protocols. It documents helper discovery and the observed wiki record defaults. The local `exa-axi` skill documents its companion CLI. |
| Rest of the original local imports | `api-design`, `cpp-coding-standards`, `cpp-testing`, `database-migrations`, `docker-patterns`, `e2e-testing`, `humanizer`, `python-patterns`, `security-review`, `ui-ux-guidelines`, and `web-perf` match the initial import at `dc3cacf`. |

The source pins are recorded in [the tool skill manifest](tools/skill-sources.tsv). The comparison used the pinned files and the Git import snapshots.

### Screenshot inventory

`pi list` reported no installed packages in this checkout. Pi 1.5.2's local resource loader discovered 31 shared skills and zero custom extensions. Seven of the screenshot's eight named skills are available here: `axi`, `chrome-devtools-axi`, `exa-axi`, `gh-axi`, `herdr`, `no-mistakes` and `unslop`. The eighth, `bro`, is absent.

The legible extension names include `@tintinweb/pi-subagents`, `chafa-image-preview`, `earendil-works/pi-transcribe`, `save-md` and `pi-openai-compaction`. Other labels are clipped or just say `src`. The image shows a `grok-build` theme separately. The exact toggle package cannot be identified from the image. The transcription project now ships as Pi Voice. [Pi Voice migration guide](https://github.com/earendil-works/pi-voice#upgrading-from-pi-transcribe)

For the requested interface, the optional `pi-skill-toggle` extension exposes `/skills-toggle` with automatic, manual-only and disabled states. Its manual-only switch writes Pi's frontmatter in the skill file. In this symlinked layout, that is a tracked change to the shared checkout. Codex's separate invocation policy lives in `agents/openai.yaml`. Stock `pi config` enables or disables whole resources. [Toggle controls and storage](https://github.com/Whamp/pi-skill-toggle#usage)

The setup guide pins a Git revision of the skill toggle that scans `~/.agents/skills`. The npm release with the same version number omits that path. [Install instructions](README.md#optional-setup)
