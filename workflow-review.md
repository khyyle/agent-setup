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
| Pi multi-chat and skill selection | 4/4 for the tested cases | Two simultaneous named Pi processes had distinct session IDs and the configured OpenAI model. Both exposed all 31 skill commands. Explicit-only unslop and no-mistakes were absent from the automatic prompt. TDD's separate routing issue is scored above. |
| Playwright AXI | 3/4 | A real Chromium test on a local HTTP fixture went from red to green. Blocked file navigation also exited zero while its JSON contained a tool error. The success check must assert resulting page state. |
| Herdr operator guidance | 3/4 | Installed Herdr 0.9.5 help and key configuration confirmed persistent named sessions and tab controls. The reviewer was outside a Herdr pane and did not exercise live reattachment. |

## Where to spend the next edit

1. **Protect research evidence first.** Keep planned experiments in the study tracker. Supply an explicit verdict and provenance for completed runs. Treat `--update-on-exist` as a whole-record replacement. Prefer a new identified amendment linked to the old record. A helper-level fix should distinguish planned runs from measured outcomes and preserve claim history or reject incomplete amendments. [ARIS helper](skills/aris/scripts/research_wiki.py)
2. **Make deliberate TDD enforceable.** Use the shared testing rule for everyday work. Explicit-only skill metadata in Codex and Pi would bring routing into line with that decision while preserving the imported workflow body. Decide separately whether stage commits and the 80% target belong in a future local variant. [TDD workflow](skills/tdd-workflow/SKILL.md)
3. **Fix the two E2E examples.** Register the response promise before the click and await it afterward. For a Playwright trace viewer archive, use `context.tracing.start({ screenshots: true, snapshots: true })`, drive the journey and call `context.tracing.stop({ path: 'trace.zip' })`. Assert the post-reload result. Check AXI's nested errors as well as its exit status. [E2E testing](skills/e2e-testing/SKILL.md) · [Playwright AXI](skills/playwright-axi/SKILL.md)
4. **Trim stale routes.** Point coding-standards at the maintained local rules and installed specialist skills. Let search-first accept a small local implementation when combining several packages costs more than the behavior warrants. [Coding standards](skills/coding-standards/SKILL.md) · [Search-first](skills/search-first/SKILL.md)

## Terminal preset verification

A fresh reviewer caught an incorrect tmux target for the optional Music status. After correction, concurrent launches produced one tab set. A real terminal client rendered the top bar, clicked the + to open an independent Pi, opened a regular Codex tab from the keyboard menu, and reattached to its selected review tab. Reopening restored a missing Git tab. Distinct project paths sharing a basename stayed separate.

The macOS integration recognized Music both closed and open. After Automation access was granted, the live app reported stopped playback and the status stayed quiet. Track formatting and transport command dispatch passed with simulated player data. A live playing track and changes to real playback were not exercised.

Run `./terminal/check-preset.sh` on macOS to repeat the layout and reattachment check. It uses a temporary Git repository and a private tmux socket, with stand-ins for the model clients and Music.
