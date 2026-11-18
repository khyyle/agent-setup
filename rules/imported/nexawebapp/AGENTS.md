# Agent Instructions

This file is the entry point for any AI coding agent working in this repo
(Claude Code, Cursor agents, Codex, Aider, etc.). Read this first.

---

## Required reading before planning any task

1. **`docs/development/WORKSTREAMS.md`** — current priorities, agent queue,
   what's blocked, what's owned by the human. Always check before proposing
   work so you don't duplicate or contradict what's already in flight.
2. **`README.md`** — system overview and tech stack.
3. **`CONTRIBUTING.md`** — commit message format (Conventional Commits),
   PR title rules, branch naming, and `make` targets.
4. **`.cursor/rules/`** — the canonical code quality rulebook. Specifically:
   - `general-code-quality.mdc` — DRY/KISS/YAGNI, naming, comments
   - `python-code-quality.mdc` — NumPy docstrings, typing, error handling
   - `frontend-code-quality.mdc` — React/Vite/Tailwind conventions
   - `styling-and-theme.mdc` — design tokens, colors, components
   - `repo-info.mdc` — directory layout, environments

The `.cursor/rules/` files are the source of truth for code conventions.
The summary below covers the highest-leverage rules; defer to those files
on any conflict.

---

## No-touch zones (hard rules)

Automation must NEVER modify these without explicit human approval in the
issue/PR thread. These are off-limits even when an issue seems to require it:

- **`backend/ml/`** — production ML inference, training, and model code.
  Owned by the human for active R&D. Reading is fine; writing is not.
- **Any branch matching `ml-research*`** — research workspace. Off-limits
  to all automation.
- **`infrastructure/`** — Terraform, Docker, deployment configs. Changes
  here can break production. Human-only.
- **`.github/workflows/`** — CI/CD pipelines. Self-modification is forbidden.
- **Anything containing secrets** — `.env*`, `cookies.txt`, credentials.
  Never read, never write, never commit.

If a task appears to require touching one of these, stop and post a comment
explaining what's needed. Do not proceed.

---

## The workstream model

Every issue follows this lifecycle:

```
issue opened
   ↓
triage comment posted by claude-bot (scope, files, acceptance, size, path)
   ↓
human applies ONE label (three ways to do it):
   • Click the label in the GitHub UI
   • `gh issue edit N --add-label agent:auto`
   • Reply `bet` on the issue to accept the triage's recommended path
     (or `bet agent:cursor` / `bet needs-design` to override)

The label that gets applied is one of:
   • agent:auto       → bot opens a ready-for-review PR autonomously
   • agent:cursor     → human will drive in Cursor; do not auto-execute
   • needs-design     → scope unclear; waiting on human design decision
   ↓
(if agent:auto) execute workflow opens a ready-for-review PR in the matching bucket
   ↓
PR review workflow auto-fires on every non-draft PR (~2 min after open)
   ↓
(on CI failure for bot-authored PRs only) auto-fix workflow attempts a fix
   ↓
human eyeballs diff + review verdict, then squash-merges
```

### Bucket labels

Issues with `agent:auto` also get a bucket label that decides the
branch namespace used by the autopilot:

- `bucket:bug` → branch `bucket/bugs/<issue-#>-<slug>`
- `bucket:feature` → branch `bucket/features/<issue-#>-<slug>`
- `bucket:tech-debt` → branch `bucket/tech-debt/<issue-#>-<slug>`
- `bucket:docs` → branch `bucket/docs/<issue-#>-<slug>`

### Size labels

Estimated by triage: `size:S` (~1 hr), `size:M` (~half day),
`size:L` (full day or more). Anything `size:L` should default to `agent:cursor`,
not `agent:auto` — too much blast radius.

### What `agent:auto` actually does (Phase F)

When you label an open issue `agent:auto`, the
[`claude-auto-pr`](.github/workflows/claude-auto-pr.yml) workflow runs
`scripts/agent/implement-issue.sh`, which:

1. Reads the issue body + the most recent triage comment for context.
2. Branches off `staging` with a name derived from the bucket + issue
   number + title slug. **Repo policy is staging-first**: every agent PR
   targets `staging`, and the human (you) promotes `staging → main`
   manually with a fast-forward merge when ready to ship to prod.
3. Runs Claude Code in headless edit mode with these hard rules
   (enforced both in the prompt **and** post-edit by the script):
   - Never touches no-touch zones (refuses, posts a comment, exits).
   - Diff capped at 500 lines / 10 files; bails on overage.
   - Refuses to disable, skip, or delete tests.
   - Must run `make check` and pass before pushing.
4. Commits with `Co-authored-by: claude-agent <bot@nexa.farm>` and an
   `Agent-Implemented: tier-2` trailer (used by heal-PR detection).
5. Opens a **ready-for-review** PR linking the issue, which immediately
   triggers the auto-review workflow. (You can still mark it back to
   draft manually if you want to pause review while you investigate.)
6. If anything goes wrong (no diff, scope cap, validation fail), the
   script posts a diagnostic comment on the issue and exits cleanly.
   The `agent:auto` label is preserved so you can investigate; remove
   it and apply `agent:cursor` to drive manually.

### CI failure → fix-it tier matrix

When CI fails on a PR, the `claude-ci-autofix` workflow chains three
scripts in order. The choice of which one runs is fully deterministic:

| Tier | Script | Type of fix | Calls Claude? | Pushes code? | Runs for |
|---|---|---|---|---|---|
| **1** | `scripts/agent/autofix-pr.sh` | Mechanical: `ruff format`, `ruff check --fix`, `eslint --fix` | No | Yes (commit trailer `Agent-Autofix: tier-1`, capped at 2 attempts) | **All PRs** (human and bot) |
| **2** | `scripts/agent/heal-pr.sh` (1st attempt) | Reasoning: small logic / type / test fix | Yes (headless edit mode, ≤300 line diff, must pass `make check`) | Yes (commit trailer `Agent-Heal: tier-2`) | **Bot-authored PRs only** |
| **3** | `scripts/agent/heal-pr.sh` (2nd attempt) | Reasoning: deeper fix after tier-2 didn't fully resolve | Yes (same constraints) | Yes (commit trailer `Agent-Heal: tier-3`) | **Bot-authored PRs only** |
| — | `scripts/agent/suggest-fix-pr.sh` | Markdown comment proposing the fix | Yes | **No** | **Human PRs** that survive tier 1, or bot PRs that survive tier 3 |

**Bot-authored detection** is anchored on two strong signals (committer
email regex `^claude-(implement|heal|agent|autofix)@` OR an anchored
`^Agent-Implemented:` commit trailer). We deliberately do not match
free-text mentions of "claude-agent" to avoid false positives.

Human PRs **never** get auto-pushed reasoning fixes. Tier 2/3 for
humans is always a suggestion comment they can apply with one click.

---

## How to act (full rules in `.cursor/rules/agent-behavior.mdc`)

Four failure modes Karpathy identified in LLM coding agents — treat these as hard constraints:

- **Think before coding.** Surface ambiguity before writing code, not after a bad diff. Read the surrounding call graph and identify the full blast radius of a change first.
- **Simplicity first.** Never add features, parameters, or abstractions that were not asked for. No "flexibility" without ≥2 current consumers.
- **Surgical changes.** Touch only what the request requires. Do not "improve" adjacent code, rename things as a side effect, or refactor things that aren't broken.
- **Work to completion.** Run `make check`. Do not stop mid-task and declare success. When blocked, report clearly what failed and what decision is needed.

---

## Code quality summary (defer to `.cursor/rules/` for details)

### Universal
- DRY, KISS, YAGNI, SRP. Composition over inheritance.
- Comments explain **why**, never **what**. No commented-out code.
- No `print()` / `console.log()` / `alert()` in committed code.
- No emojis in code or comments.
- Catch specific exceptions, never bare `Exception`. Never silently swallow.
- Files past ~300 lines are a signal to split.

### Python (`backend/`)
- NumPy-style docstrings on all non-trivial functions.
- Full type annotations using built-in generics (`list[str]`, not `List[str]`).
- Module-level constants in `SHOUTING_CASE`.
- Logging via `logger`, never `print`.

### Frontend (`frontend/`)
- Functional components only. Zustand for global state, TanStack Query for data.
- Tailwind CSS only. No inline `<style>`, no CSS modules.
- Use design tokens from `App.css` `@theme` and `config/nexaColors.js`.
  **Never hardcode hex values in JSX.**
- File naming: PascalCase components, camelCase hooks/utils, kebab-case assets.
- Tappable areas ≥ 44px. ARIA roles + keyboard support.

---

## Git conventions

For everyday git operations (worktree workflow, syncing with remote, undo/recover, conflict resolution), see [`docs/development/GIT_PLAYBOOK.md`](docs/development/GIT_PLAYBOOK.md). This section covers only the conventions that are policy.

### Commit messages — Conventional Commits (enforced by hook)

```
<type>(<optional scope>): <description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`, `revert`.
Scopes are optional. Use the canonical vocabulary and selection rules in
[`CONTRIBUTING.md`](CONTRIBUTING.md#scopes); omit the scope when none fits
cleanly.

### Agent-authored commits

Every commit authored by automation MUST include this trailer in the commit body:

```
Co-authored-by: claude-agent <bot@nexa.farm>
```

This keeps `git shortlog` honest about what was human vs. agent work.

### Branch naming

```
<type>/<short-description>
```

For agent-driven work, prefix with the bucket: `bucket/bugs/<desc>`,
`bucket/features/<desc>`, `bucket/infra/<desc>`.

### PR rules

- Title follows Conventional Commits (squash merges use the title).
- Body uses the template in `CONTRIBUTING.md` (What / Why / Test Plan / Closes #N).
- Agent-opened PRs are **ready-for-review** (so the auto-reviewer fires immediately) but never auto-merged. Human is the merge gate.
- Keep PRs focused: one logical change, one issue closed.

### Branching policy — staging-first

- **`staging` is the integration branch.** Every PR — agent-opened or
  human-opened — targets `staging`. The autopilot (`implement-issue.sh`)
  defaults `BASE_BRANCH=staging` and `gh pr create --base staging`.
- **`main` is the deploy frontier.** It only ever receives commits via
  a fast-forward merge from `staging`, performed manually by the human.
  Agents never push to `main`, never PR to `main`.
- **Promote with**: `git checkout main && git merge --ff-only origin/staging && git push`.
  If the merge isn't fast-forward, `staging` has diverged from `main`
  (someone pushed directly to `main`) — reconcile before promoting.
- **`scripts/agent/daily.sh` surfaces the gap**: every digest shows
  "Pending promotion (staging → main)" with the commit list, and warns
  loudly if `main` has drifted ahead of `staging`.

---

## Verification before opening a PR

Run these from the repo root before pushing:

```bash
make check   # lint + tests; mirrors CI
```

If `make check` fails, fix it locally. Do not push red.

---

## When to stop and ask

Stop and post a comment instead of proceeding when:

- The issue requires touching a no-touch zone.
- Acceptance criteria are ambiguous after one re-read.
- The fix would touch >5 files for a `size:S` task (likely scope creep).
- A test you'd need to write requires fixtures that don't exist.
- The change would alter a public API contract without an accompanying spec update.
- You'd need to disable an existing test to make the change pass.

Stopping is cheap. A bad PR is expensive.

---

## Cost discipline

Token usage is tracked per workflow. If a single triage / review / execution
run is going to exceed reasonable bounds (rough heuristic: more than ~50k
tokens of repo context for a `size:S` task), prefer to ask a clarifying
question rather than load more context.
