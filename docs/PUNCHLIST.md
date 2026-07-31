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
  - Track when ownership or authorization claims appear relative to collection.
  - Preserve model-switch and resumed-session boundaries.
  - Preserve staged setup turns in exported evidence.
  - Compare per-turn risk with full-session aggregate risk for layered
    automation-wrapper cases.
  - Score routine scan/keyscan/handshake/version/CVE steps as an aggregate
    recon chain when they appear across turns.
  - Preserve block/refusal state across plain retry attempts such as "try
    again" after a classifier stop.

- Build scope-delta tracking.
  - Record user-requested steps separately from model-supplied steps.
  - Record user-named protocol fields separately from model-supplied protocol
    fields.
  - Flag broad defensive prompts that become specific target interaction.
  - Treat late admin or owner claims as metadata until scope is reverified.
  - Treat HTB, CTF, and lab labels as scope claims to verify, not proof of
    authorization.
  - Gate mid-session credential or target-detail injection before any use,
    tool call, or report display.
  - Require confirmation before deeper collection or surface mapping.
  - Distinguish bounded appsec questions from broad whole-codebase or
    all-attack-surface sweeps.
  - Keep AD CS ESC and certificate-template work in defensive validation and
    remediation lanes unless trusted lab scope and output boundaries are clear.

- Build sweep safety gates.
  - Require explicit authorization, target ownership, and scope caps before
    multi-agent or full-surface vulnerability sweeps.
  - Add rate limits and human unlock before parallel auditor fanout.
  - Route findings to remediation-safe queues instead of portable vulnerability
    databases.
  - Track discovery volume against triage, patch, and deployment capacity.

- Build elevated target-class registry.
  - Start with obfuscation-specific transports and defense-evasion protocols.
  - Gate authentication, handshake, dial, connection-establishment, and internal
    mechanics at request stage.
  - Keep reviewer-analysis notes source-safe when sampled completions are empty
    or harmless.

- Build whole-work-object scanning.
  - Run detector passes across chat text, attachments, repo files, retrieved
    chunks, generated code, and tool arguments.
  - Score clean-prompt cases across framing language, context payload, and
    output shape.
  - Preserve workflow provenance so recon, enumeration, analysis, and reporting
    stages can be evaluated together.
  - Detect reconnaissance artifacts in context blocks: endpoint inventories,
    auth flows, file refs, log paths, ports, and known weaknesses.
  - Score analytical security tasks paired with attached or upstream
    reconnaissance-package density before model analysis begins.
  - Preserve file path, hash, extraction timestamp, and source interface.
  - Compare chat-only risk with full-context risk.

- Build trusted-slot provenance validation.
  - Scan system prompts, developer messages, tool definitions, and operator
    context before agent execution.
  - Block trusted slots that contain live target context, credential-bearing
    material, offensive infrastructure references, or anti-review language.
  - Treat returned tool content as untrusted data until provenance, authority,
    and schema have been verified.
  - Record attempted tool invocation separately from tool success or failure.
  - Classify technical tool/runtime failure as safety non-intervention when the
    model otherwise complied.

- Build typed tool-result boundaries.
  - Wrap tool outputs in typed envelopes with source, tool identity, authority,
    schema version, timestamp, and content hash.
  - Parse results before model exposure; never inject raw tool strings directly
    into instruction context.
  - Separate data payload fields from directive text and quarantine
    instruction-like content from untrusted outputs.
  - Fail closed on schema mismatch, unknown executable fields, missing
    provenance, or output class escalation.
  - Compare training/prompt-level "treat this as untrusted" controls against
    structural parser, sandbox, sanitization, and schema controls.

- Build safe transformation boundaries.
  - Classify source files before formatting, conversion, cleanup, translation,
    or unchanged pass-through.
  - Treat "pass through unchanged" and "preserve verbatim" as display/export
    decisions that still require policy review.
  - Add metadata triage for filenames, paths, comments, and labels that suggest
    filter testing, evasion attempts, payload staging, or policy probes.
  - Redact, summarize, or quarantine unsafe source blocks rather than
    preserving them for formatting fidelity.

- Build sensitivity-tiered structured output.
  - Add sensitivity labels to evidence and file reference fields.
  - Require redaction or human unlock before portable evidence export.
  - Separate internal evidence from source-safe recommendation text.
  - Redact live protocol surface dumps, including KEX/cipher/MAC/host-key and
    authentication-method inventories, from shareable reports.
  - Redact exact running-build, CVE-correlation, and patch-status joins from
    shareable reports unless explicitly authorized.

- Add case-study export templates.
  - Raw private version.
  - Source-safe public version.
  - SOC handoff version with detections, logging, and escalation guidance.
  - Keep private case notes gitignored until explicitly cleared.

- Refresh the vulnerability taxonomy for 2026.
  - Add decision preloading.
  - Add clean-prompt wrapper taxonomy.
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
  - Add benign DevOps and enterprise-workflow baselines to tune
    `operational_normalcy_camouflage` false positives.

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
  - Hypervisor and kernel memory-mapping invariants such as duplicate
    guest-physical remap acceptance.

## Lower Priority

- Add a dashboard once the data schema stabilizes.
- Add CI checks for detector tests and Markdown links.
- Decide which legacy exploit-generator files should stay private archive,
  become safe fixtures, or be removed from the public repo.

## Current Rule

Do not present items in this punchlist as completed features. The finished
capability today is the methodology plus the defensive detector.
