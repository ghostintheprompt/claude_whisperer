# Punchlist

Current gaps and next implementation targets. Anything here is intentionally not
being claimed as finished runtime capability.

## High Priority

- Refactor the browser extension into a local-first review harness.
  - Remove browser-stored production API keys.
  - Add explicit authorization and risk-warning gates before live actions.
  - Make manual copy/review the default behavior.
  - Capture provider, exact model ID, interface, date, tool configuration, and
    attachment/retrieval context per run.

- Build session trajectory scoring.
  - Detect refusal-then-compliance patterns.
  - Track low-signal baseline erosion across turns.
  - Preserve staged setup turns in exported evidence.

- Add case-study export templates.
  - Raw private version.
  - Source-safe public version.
  - SOC handoff version with detections, logging, and escalation guidance.

- Refresh the vulnerability taxonomy for 2026.
  - Add decision preloading.
  - Add orchestration trust shift.
  - Add data-category hard stops.
  - Add legitimate-code camouflage.
  - Add MCP/tool-context risks.

## Medium Priority

- Add provider metadata adapters.
  - Anthropic.
  - OpenAI.
  - Gemini.
  - Local/offline fixtures.

- Build a safe fixture library.
  - No raw client material.
  - No operational payloads.
  - Mechanism-preserving examples for detection and regression tests.

- Add report generation.
  - Markdown evidence pack.
  - JSON findings export.
  - SOC summary.
  - Model/version matrix.

- Add code-review primitives for generated projects.
  - Network listeners.
  - Command execution.
  - Credential reads.
  - Session/token handling.
  - Persistence/process control.

## Lower Priority

- Add a dashboard once the data schema stabilizes.
- Add CI checks for detector tests and Markdown links.
- Decide which legacy exploit-generator files should stay private archive,
  become safe fixtures, or be removed from the public repo.

## Current Rule

Do not present items in this punchlist as completed features. The finished
capability today is the methodology plus the defensive detector.
