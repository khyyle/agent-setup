---
name: research-loop
description: Coordinate ongoing empirical or computational research through bounded experiments, evidence records, and clear handoffs. Use for starting or resuming a study, maintaining research conventions across specialist skills, or preparing a research handoff; not for ordinary factual lookups.
---

# Research Loop

Keep research reproducible and understandable while using the project's existing
tools. This skill coordinates the work; it does not select a scientific method,
create a new research platform, or grant permission to deploy a result.

## Establish the task and its boundaries

Determine whether the user wants a brief, a plan, experiments, a review, an
explanation, or a handoff. Do that work without automatically running every stage.
An explanation request does not authorize another experiment. A handoff request
does not authorize continuing the work it describes.

For a new study or incomplete context, use the fillable
[research brief](assets/research-brief.md). The user or agent can fill it from
existing instructions and records. Keep a useful existing brief rather than
creating another. Templates are output aids, not a mandatory questionnaire or
new directory structure. Omit irrelevant fields.

Read applicable repository instructions and the current research index before
planning changes. Verify repository state, relevant source, data availability,
and what previous reports actually measured. Treat handoff statements as dated
evidence to check, not proof of the present state. Record discrepancies instead of
silently replacing history. Do not re-read the entire archive when its index and
the next experiment's dependencies are sufficient.

Separate verified facts, user-reported context, assumptions, and proposals. An
agent can discover a path or infer a reasonable organizational choice; it cannot
invent a budget, approval, result, or validation set. An authorization field only
records permission already supplied by the user. Preserve existing authorization
without repeatedly requesting it. Ask only for missing information that changes
the decision or blocks the requested action, and continue independent work.

## Run a bounded research loop

### Frame the next question

State the claim being tested and what outcome would change the next decision.
Separate descriptive fit, prediction, calibration, causal explanation, and
application value. Evidence for one does not establish the others. For example,
a useful forecast can still fail to identify the cause of a change.

Read the relevant prior failures and primary literature before expanding the
model family. Tie each source to a specific assumption or method, and distinguish
the authors' results from the proposed application. Say when only an abstract was
available. Do not turn a familiar technique into an obligatory approach.

Prefer the smallest comparison that distinguishes plausible explanations. Retain
a simple baseline. Match inputs, fitting opportunities, and evaluation support
where possible. When several factors must change, explain which attribution the
comparison can and cannot support.

### Specify the experiment before its outcomes

Put a short protocol beside the relevant study, or extend its existing protocol.
Define only what this experiment needs:

- The question, comparator, primary outcome, and decision criterion, including
  what would count as insufficient evidence.
- Inputs, units, inclusion rules, missingness, data/version provenance, and the
  independent unit of analysis. Distinguish measured quantities from inferred
  labels and incomplete annotations.
- Fitting, selection, calibration, and evaluation boundaries. Use chronological
  boundaries when time matters; address group leakage and repeated measurements
  when they matter. Include preprocessing in the leakage audit.
- Parameter estimation, priors, search space, numerical checks, and failure rules.
  A simulator's parameters are not fitted estimates unless using an explicit
  oracle control. Name approximations and identification limits.
- Primary metrics, relevant conditional diagnostics, and uncertainty assumptions.
  Repeated observations, repeated looks, and selection across experiments affect
  what uncertainty statements mean.
- A finite run/search scope, resource limits, stopping condition, and necessary
  checks. Use existing permissions and available resources; missing paid-compute
  authorization does not prevent useful planning or local inspection.

Explain the basis for durations, effect sizes, and decision thresholds when they
matter. Label provisional choices and their limitations; a numeric cutoff is not
principled merely because it was written down before the run.

Record prior exposure to evaluation data. A chronological split prevents certain
leaks but cannot make a repeatedly examined corpus unseen again. Later changes
to the protocol are dated amendments; describe outcome-informed changes as
exploratory rather than rewriting them as prior choices.

### Execute and inspect

Reuse the existing runner and model interfaces. Keep experiment-specific code
with its study unless actual reuse justifies a shared package. Separate data
access, model behavior, evaluation, and application policy where those boundaries
exist. Do not copy production policy into an evaluator without a stated purpose
and a plan to keep the definitions consistent.

Use immutable or versioned inputs and new artifact destinations. Record the
source revision, uncommitted source differences when relevant, resolved settings,
input hashes or equivalent dataset versions, and exact reproduction commands.
Freeze the source used by a run. Preserve original outputs, failed attempts,
exclusions, optimizer terminations, and numerical failures in the run artifacts.
A finished process or normalized distribution alone is not evidence of correctness.

Run checks appropriate to the scientific claim: analytical cases, simulation
controls, invariants, leakage tests, or independent numerical comparisons. Inspect
the declared diagnostics as well as the primary metric. Do not quietly change
support, discard failed seeds, or tune tolerances until a preferred model wins.

Stop at the stated boundary. An inconclusive or negative result is a valid
completion. Another model, dataset, or wider search needs an explicit research
reason and must remain within the authorized scope and budget. Describe a useful
next question rather than automatically starting an unbounded search.

### Interpret, review, and retain

Explain the outcome, its uncertainty, the assumptions it relies on, and remaining
alternative explanations. Keep a simulation result scoped to its generator and
a field result scoped to its population and design. Distinguish numerical success
from statistical adequacy and useful application performance.

Update the existing hypothesis record with the question or ID, status, linked
protocol/run/source, observed result, limitations, and next decision. Useful
statuses include proposed, evaluated with mixed evidence, supported within the
tested setting, contradicted within that setting, and unresolved. Preserve prior
negative findings; do not replace them with the newest favorable run.

Review substantive changes against connected code and scientific assumptions.
Use an independent reviewer when warranted and delegation is available and
authorized. Give it the task and raw evidence without coaching it toward a
preferred verdict. Agent agreement is additional scrutiny, not independent data.
Resolve findings using evidence. Run required repository checks for the actual
changes and distinguish new failures from a verified existing baseline.

Commit, publish, or hand off according to the user's requested workflow and local
conventions. Research findings alone never authorize production changes.

## Keep one maintained record

Follow existing paths and test organization. For a new study, propose the smallest
layout that fits its real responsibilities; ask when a new shared package, public
interface, or archival destination needs a decision. Do not impose this skill's
template filenames on an established repository.

Keep durable explanation near the study or package it explains. An overview
introduces the question and links to the method, results, and reproduction path.
A model card or walkthrough holds substantial mathematics. The research tracker
summarizes evidence and decisions by linking to those records. Small studies can
keep these sections in one file; separate them only when that improves use.

Store private data, generated forecasts, checkpoints, exploratory drafts, agent
exchanges, and long logs in the project's ignored or external artifact location.
Check the ignore rule and data-sharing permissions. An ignored local directory is
not a durable backup; retain the project's approved artifact location and retrieval
instructions when reproducibility depends on it. Preserve meaningful evidence,
not every scratch transcript. Do not delete unique historical evidence during
cleanup without confirming its replacement and authorization.

When existing documents disagree, mark which record governs current direction
and link the superseded result with its context. Avoid a new top-level summary
after every turn or a second wiki mirroring the same claims.

## Write for a reader outside the conversation

Introduce the problem, data, and construction before referring to "the model."
Use connected prose, concrete verbs, and explicit reasons. Explain what a package
does rather than saying it "owns" a broad concern. Separate observed results from
proposals and interpretation. Preserve the details a reader needs to reproduce or
challenge a claim without replaying the conversation.

Define mathematical symbols, dimensions, units, conditioning information, and
assumptions before use. Show the construction behind consequential posterior,
variance, or error-rate claims. Identify exact and approximate steps. Use the
repository's math renderer; default to `$...$` and `$$...$$` in Markdown when no
convention exists. Link primary sources and supporting experiments near claims.

Use descriptive frontmatter when the project uses it, such as title, date,
status, scope, and audience. Avoid promotional phrasing, vague authority,
conversation-specific rebuttals, decorative headings, invented terminology, and
overcompressed lists. Prose editing must preserve equations, caveats, source
attribution, and scientific uncertainty.

## Compose with other skills

Discover available skills and read only those relevant to the current task.
Keep the project brief and existing instruction hierarchy in force. Do not install
dependencies or change tool configuration merely to follow a suggested workflow.

| Task | Useful specialist skill, if available | Boundary |
|---|---|---|
| Implement an experiment | `ponytail` | Small complete changes; local conventions still apply. |
| Review connected code | `ponytail-review` | Code quality does not establish scientific validity. |
| Edit the durable explanation | `humanizer` | Preserve technical meaning and evidence; keep editorial drafts out of maintained reports. |
| Find literature or design/run a study | `aris` for experiment planning and the research wiki, or a relevant research skill | Invoke the needed stage, not an automatic paper/deployment pipeline. |
| Maintain research memory | Existing research-wiki skill | Use it only if the project already uses or requests it; identify which records are authoritative. |

These are optional integrations, not hard dependencies. If a requested specialist
is unavailable, state that and follow the applicable missing-skill instructions;
do not claim it ran. When no specialist is required, perform the task directly.

## Handoff and completion

For a context transfer, adapt [the handoff template](assets/handoff.md). Verify
current branches, files, and results when accessible; otherwise label them as
last recorded. Include the next bounded action, key positive and negative
findings, exact evidence paths, relevant model definitions, permissions, data
access limits, and uncommitted work. Carry essential writing and organization
conventions in the prompt so it works even without this skill installed.

End each requested task with the result, its limits, the durable record, checks
actually performed, and any decision still needed. Do not report planned runs as
completed or leave a claimed result supported only by an agent's scratch notes.
