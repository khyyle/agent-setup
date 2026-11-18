---
name: aris
description: Use ARIS to plan claim-driven experiments and maintain a local research wiki of papers, claims, ideas and experiment outcomes.
---

For a claim, baseline, ablation or run-order decision, use the [experiment planning procedure](references/planning/experiment-plan.md). For paper ingestion, evidence links or recording a completed run, use the [research wiki procedure](references/research-wiki.md). Each is the full pinned procedure for that stage.

The wiki examples locate their helpers under `$ARIS_REPO/tools/`. For the personal installation, set `export ARIS_REPO="$HOME/.agents/skills/aris"` in the shell running the example. For another installation, set it to the directory containing this skill. Run the commands from the study directory so the evidence stays with the study.

Keep planned experiments in the study tracker. The [wiki helper](scripts/research_wiki.py) defaults a missing verdict to `no` and confidence to `medium`. Supply the measured verdict, confidence and run provenance when recording an outcome. A claim update with `--update-on-exist` replaces the record. Read the existing evidence before an amendment and preserve its history.
