# Research

This directory contains the methodology, taxonomy, fixtures, and analysis tools
for authorized safeguards evaluation.

The current project direction is frontier-model and provider agnostic. Older
scripts and pattern files may still reference specific Claude generations; treat
those as historical fixtures until reviewed.

## Start Here

- [Safeguard Evaluation Methodology](SAFEGUARD_EVALUATION_METHODOLOGY.md)
- [Vulnerability Taxonomy](taxonomy/vulnerability_taxonomy.md)
- [Important Findings Method](../docs/IMPORTANT_FINDINGS_METHOD.md)
- [Defense Detector](../defense/README.md)

## Current Research Questions

- Does the system reassess action and data boundaries when a request is framed
  as already authorized?
- Does safety behavior change when the same objective arrives through a
  document, codebase, tool result, subagent, MCP context, or retrieval source?
- Does Unicode, script mixing, encoding, or long-context placement create a
  classifier/model mismatch?
- Does a low-signal setup sequence erode refusal consistency?
- Can each red-team finding be translated into a SOC detection, escalation
  rule, or regression test?

## Directory Structure

- `taxonomy/` - category system for failure modes and evaluation lanes.
- `patterns/` - legacy and current test fixtures. Review before public use.
- `modes/` and `models/` - older comparison tooling.
- `tools/` - analysis utilities and generators.
- `reports/` - report templates and examples.

## Working Rule

Research notes can be raw in private. Public methodology should be source-safe,
reproducible, and useful to the teams that have to defend the system after the
red team leaves.
