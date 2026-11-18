---
name: aris
description: Use ARIS to plan claim-driven experiments and maintain a local research wiki of papers, claims, ideas and experiment outcomes.
---

These are the experiment-plan and research-wiki stages of ARIS. Select the stage that advances the study. The research-loop skill coordinates runs, verification and handoffs.

## Plan an experiment

Read the study's current question, proposal, existing evidence and compute or data limits. State the primary claim, a plausible competing explanation and the minimum evidence that would distinguish them. Pair each essential experiment with its strongest applicable baseline, fixed dataset/split, metric, budget and decision criterion. Include a simpler variant or an ablation if it isolates the claimed contribution. Record what a negative result would imply.

Start with a data and metric sanity check, then the baseline and the smallest decisive comparison. Set a stop/go condition before expensive runs. Put the plan and run IDs in the study's existing tracker. Keep proposed results distinct from observations.

## Maintain a research wiki

Use a wiki when the study benefits from finding relationships across papers, claims and runs. Read the current index before adding an entry. Keep provenance, conditions, uncertainty and contradictory evidence with each claim. Keep raw traces and large outputs in the owning study and link to them. Use the existing study record for routine progress.

The bundled [wiki CLI](scripts/research_wiki.py) runs with Python's standard library. Use the installed skill directory below or resolve `scripts/` relative to this file. Set `wiki` to the study's wiki directory. These commands illustrate an offline, manually sourced entry.

```sh
helper=~/.agents/skills/aris/scripts/research_wiki.py
python3 "$helper" init "$wiki"
python3 "$helper" ingest_paper "$wiki" --title "$paper_title" --authors "$authors" --year "$year" --thesis "$thesis"
python3 "$helper" rebuild_index "$wiki"
python3 "$helper" stats "$wiki"
```

Use `add_claim --help`, `upsert_idea --help` or `add_experiment --help` for typed records and links. Supply evidence and run provenance when advancing a claim's status. Ingest skips an existing paper by default. Inspect an existing page before requesting an overwrite. When curating raw session text, run the bundled [capture filter](scripts/capture_filter.py) on candidate excerpts and verify the source before saving them.
