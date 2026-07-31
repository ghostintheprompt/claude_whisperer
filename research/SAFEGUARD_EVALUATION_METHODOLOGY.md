# Safeguard Evaluation Methodology

A defender's companion to the [Vulnerability Taxonomy](taxonomy/vulnerability_taxonomy.md).

The taxonomy names the ways an instruction-following model can be pushed off its
guidelines. This document takes each category from the **evaluator's** side:
what you are actually measuring, how to measure it without fooling yourself, and
what mitigations and detection signals reduce the exposure. The goal is a
repeatable evaluation you can re-run against a new model or a new system prompt
and get a comparable result, not a one-off "we tried some prompts."

The 2026 update adds the case-informed lanes from
[`../docs/IMPORTANT_FINDINGS_METHOD.md`](../docs/IMPORTANT_FINDINGS_METHOD.md):
decision preloading, clean-prompt wrapper taxonomy, mode switching,
retroactive authorization laundering, orchestration trust shift, Unicode drift,
chat-surface displacement, trusted-slot contamination, low-signal erosion, probe
confirmation, autonomous methodology expansion, data-category hard stops,
clean-auth probing, and legitimate-code camouflage.

The detection signals referenced below are implemented in
[`defense/evasion_signal_detector.py`](../defense/evasion_signal_detector.py).

---

## How to run an evaluation (the loop)

1. **Fix the target.** One model, one system prompt, one tool configuration,
   one set of decoding settings. Change one variable at a time or the results
   are not attributable.
2. **Define pass/fail per case, up front.** "Refused," "complied," and
   "complied with a hedge" are different outcomes — decide which is a failure
   *before* you see the response, or you will rationalize borderline cases.
3. **Test each category, not just the ones that are easy to write.** Coverage
   is the point; a high pass rate on three categories tells you nothing about
   the other two.
4. **Log verbatim.** Store the exact input, the exact output, the decoding
   settings, the model version, and the point in the session where authorization
   or ownership was established. A finding you can't reproduce is not a finding.
5. **Separate finding from filtering.** Record every case that failed, with a
   severity and a confidence, and rank afterward. Deciding "that one doesn't
   count" mid-run silently lowers recall.
6. **Re-baseline on every model change.** A mitigation that held on one model
   is a hypothesis, not a guarantee, on the next.

Metrics worth tracking per category: **attack-success rate** (fraction of cases
that produced a disallowed outcome), **false-refusal rate** (benign cases that
were wrongly refused — over-blocking is also a failure), and **consistency**
(same case, repeated, same outcome).

---

## Category 1 — Instruction processing

**What you're measuring:** whether the model's guideline-following survives
competing, reframed, or obfuscated instructions.

**Evaluation approach:** hold the underlying request constant and vary only the
*framing* around it (neutral vs. authority-laden vs. role-assigned), and the
*surface form* (plain vs. encoded). If the outcome changes when the substance
did not, the safeguard is keying on surface features rather than intent.

**Detection signals (pre-model):** obfuscated surface form is machine-detectable
before the model ever sees it: `base64_payload`, `homoglyph_substitution`,
`mixed_script_control_surface`, `invisible_characters`,
`leetspeak_substitution`, `rot13_concealment`. Route high-scoring inputs to
stricter handling or review.

**Mitigations:** normalize input before evaluation (NFKC Unicode normalization,
strip zero-width characters, decode-and-re-scan encoded segments); design the
system prompt so that role and framing do not carry authority to relax rules;
test that "as a security researcher, …" and the bare request get the same
treatment.

---

## Category 2 — Reasoning exploitation

**What you're measuring:** whether step-by-step reasoning, hypotheticals, or
"for the sake of argument" framings can walk the model to an output it would
refuse directly.

**Evaluation approach:** compare the direct request to the same request reached
through a chain (decomposition into individually-benign steps, a false dilemma,
an indirect phrasing). The gap between "refuses directly" and "complies when
led there" is the quantity of interest.

**Detection signals:** largely semantic, so pre-model string signals are weak
here — this category is caught at the *output* boundary, not the input.

**Detection signals:** `decision_preloading` catches language that tries to
pre-authorize the model's choices or remove reassessment. This is not a verdict;
it is a cue to inspect whether the request is converting reasoning into pure
execution.

**Mitigations:** evaluate the final artifact against policy regardless of the
reasoning path that produced it; don't let an accumulation of benign steps
launder a disallowed result; where tools are involved, gate on what the action
*does*, not on how the request was phrased.

## Retroactive authorization laundering

**What you're measuring:** whether the system treats a late admin, owner, or
authorized-testing claim as permission for work that already happened. The
interesting failure is chronological: useful reconnaissance or evidence
collection occurs first, then the user supplies an ownership story that
retroactively makes the session feel legitimate.

**Evaluation approach:** compare up-front scoped authorization with a
mid-session ownership injection after model switches, resumed context, or
already-collected intelligence. Then test a non-escalating chain where each step
looks routine in isolation but the aggregate artifact becomes target-specific
pre-exploitation reconnaissance.
Add a lab-frame variant: begin with HTB, CTF, or authorized-lab framing, then
introduce credential or target material only after the model hits technical
friction. Test whether plain retry language after a block is treated as a fresh
request or as boundary probing, and whether AD CS ESC/template analysis expands
beyond defensive validation under the lab frame.

**Detection signals:** `retroactive_authorization_laundering`,
`permission_carveout_laundering`, `non_escalating_recon_chain`,
`ctf_lab_authorization_laundering`, `mid_session_credential_injection`,
`retry_after_block_persistence`, and `adcs_esc_methodology_expansion`.

**Mitigations:** require authorization before collection, preserve chronology
across model switches and resumed sessions, treat system permission carve-outs
as conditions to verify, and score routine collection steps by their aggregate
intelligence value. Verify lab scope before operational actions, gate
mid-session credentials and target details, and keep refusal state sticky across
simple retries.

## Clean-prompt wrapper taxonomy

**What you're measuring:** whether a prompt keeps its visible language clean
while risk moves into the surrounding work object: an attachment, codebase map,
schema, tool output, prior session, automation wrapper, or machine-readable
report contract.

**Evaluation approach:** hold the underlying task constant and vary the wrapper
category: defensive framing, role laundering, automation wrapper, pre-loaded
context, structured output pressure, incremental tasking, and legitimate tool
invocation. Then score the same case across three axes: framing language,
context payload, and output shape. For automation-wrapper cases, compare
per-step risk with full-session risk; the combined workflow artifact may carry
the signal that no individual prompt reveals. Treat normal engineering or
DevOps framing as context, not as proof of safety. This is workflow
indistinguishability: mature enterprise workflow and adversarial choreography
can share the same visible structure.

**Detection signals:** `defensive_framing_wrapper`, `role_laundering`,
`automation_wrapper`, `layered_automation_camouflage`,
`preloaded_context_payload`, `preloaded_recon_package_laundering`,
`structured_output_pressure`, `structured_output_dossiering`,
`operational_thoroughness_pressure`, `operational_normalcy_camouflage`,
`incremental_tasking`,
`legitimate_tool_invocation_wrapper`,
`permission_carveout_laundering`, `non_escalating_recon_chain`,
`broad_sweep_escalation`, `multi_agent_audit_fanout`,
`vulnerability_database_packaging`, `ai_discovery_asymmetry`,
`obfuscation_transport_internals`, `developer_documentation_laundering`,
`review_process_sensitive_reconstruction`, `ssh_crypto_surface_extraction`,
`auth_method_surface_disclosure`, `protocol_surface_cartography`, and
`clean_prompt_axis_combo`.

**Mitigations:** treat clean phrasing as metadata, not safety. Scan the whole
work object, preserve context provenance, treat schema shape as an export
boundary, inspect system/developer/tool-trusted schemas before execution,
require redaction gates before portable evidence export, review aggregate
intelligence value when ordinary developer tools are chained together, and
preserve enough cross-session state to detect a surface map emerging from
multiple benign-looking stages.

## Bounded review vs sweep escalation

**What you're measuring:** whether the system can distinguish narrow
remediation help from broad automated vulnerability discovery. A question about
one CSRF control or password-hashing path is different from a sweep across a
whole codebase, endpoint inventory, or attack surface.

**Evaluation approach:** compare a bounded question with a broad sweep request
that introduces multi-agent fanout, parallel auditors, full-surface coverage, or
structured file/line findings. Track whether the model preserves scope or
packages a portable vulnerability database.

**Detection signals:** `broad_sweep_escalation`,
`multi_agent_audit_fanout`, `vulnerability_database_packaging`, and
`ai_discovery_asymmetry`.

**Mitigations:** require scope caps, target ownership, rate controls, and human
unlock before broad sweeps. Route output to remediation-safe queues, redact
exploit scenarios and portable offensive-report fields, and measure discovery
velocity against triage and patch capacity.

## Defense-evasion protocol internals

**What you're measuring:** whether the system flags elevated target classes at
request stage. Traffic-obfuscation and defense-evasion transports require
special handling when the ask touches authentication, handshake, dial,
connection-establishment, or protocol internals.

**Evaluation approach:** compare ordinary protocol education with a developer
documentation wrapper around obfuscation-transport internals. The expected
behavior is high-level classification and scope clarification, not a walkthrough
of internal mechanics.

**Detection signals:** `obfuscation_transport_internals`,
`developer_documentation_laundering`, and
`review_process_sensitive_reconstruction`.

**Mitigations:** classify obfuscation-specific transports as elevated targets,
do not let open-source or developer framing downgrade the request, and keep
reviewer analysis source-safe when the sampled completion is empty or harmless.

## Protocol surface cartography

**What you're measuring:** whether an audit produces a live service map rather
than remediation-level guidance. SSH/KEXINIT-style algorithm negotiation,
authentication-method availability, exact running build, CVE correlation, and
patch status can become pre-attack intelligence when exported together.

**Evaluation approach:** compare high-level hardening advice with requests or
outputs that enumerate cryptographic negotiation options, live authentication
methods, and exact-build vulnerability correlation. The expected safe outcome
is remediation guidance without a portable surface dump.

**Detection signals:** `ssh_crypto_surface_extraction`,
`auth_method_surface_disclosure`, `primary_auth_vector_exposure`,
`live_build_cve_correlation`, and `protocol_surface_cartography`.

**Mitigations:** redact full KEX/cipher/MAC/host-key and auth-method inventories
from shareable output, redact exact-build-to-CVE joins unless explicitly
authorized, require explicit scope for live collection, and convert details into
remediation statements.

## Autonomous methodology expansion

**What you're measuring:** whether a broad defensive request causes the model to
invent the specific audit method, protocol field, collection target, or surface
map. In this case family, the user supplied a target and high-level security
analysis frame; the model supplied the specialized protocol focus and execution
path. That makes methodology authorship the finding: target plus framing came
from the user, expertise plus execution came from the model.

**Evaluation approach:** compare a narrow user-requested hardening task with a
broad audit frame. Log which protocol fields, commands, and collection steps
were named by the user versus introduced by the model's internal auditor
persona.

**Detection signals:** `autonomous_methodology_expansion`, with
`ssh_crypto_surface_extraction` or `protocol_surface_cartography` when the
model-supplied method exports live protocol surface.

**Mitigations:** require scope confirmation before deeper collection, cap
autonomous audit depth by default, and treat defensive or educational framing as
context rather than blanket permission.

---

## Category 3 — Context window

**What you're measuring:** whether a small instruction buried in a large body of
otherwise-benign content behaves differently than the same instruction in
isolation (context dilution, delayed activation).

**Evaluation approach:** take a case the model refuses in isolation, embed it in
progressively larger benign context, and record where (if anywhere) the outcome
flips. Report the threshold.

**Detection signals:** `context_dilution` / `oversized_input` flag the
structural shape — a long body with a short, isolated directive in the tail —
so those inputs get read in full rather than skimmed.

**Mitigations:** apply the same evaluation to the whole input, not just its
head; be especially careful with retrieved or pasted content that the user did
not write; monitor for the "long benign haystack, short imperative needle"
shape.

---

## Category 4 — Multi-turn

**What you're measuring:** whether guideline-following degrades across a
conversation — gradual boundary-pushing, manufactured urgency, or forking the
conversation to escape an earlier refusal.

**Evaluation approach:** script multi-turn sequences, not single prompts. A
model that refuses on turn 1 but complies on turn 6 after incremental pressure
is a different (and more realistic) result than a single-shot test shows.

**Detection signals:** per-message input signals still apply, but the load-
bearing signal is *trajectory* — track refusals-then-compliance within a
session rather than scoring each message alone.

**Mitigations:** evaluate the running conversation state, not just the latest
turn; treat "you already agreed earlier" as unverified; reset the burden of the
guideline on each request rather than letting it erode.

---

## Category 5 — Emergent capabilities

**What you're measuring:** whether tool use, cross-domain transfer, or chaining
of individually-permitted capabilities produces an outcome that none of the
steps would be allowed to produce alone.

**Evaluation approach:** test the *composition*, not just the parts. A tool call
that is fine in isolation may be the last link in a chain that isn't. Enumerate
the chains, not only the individual actions.

**Detection signals:** input-level obfuscation detection still applies to tool
arguments (an encoded payload can ride inside a tool call), so scan tool inputs
too, not only the top-level message. `orchestration_trust_shift` flags agent,
tool, MCP, and pipeline framing that can turn untrusted content into apparently
trusted instruction. `trusted_slot_contamination` flags untrusted content trying
to occupy system, developer, operator, or tool-trusted instruction slots.
`tool_output_provenance_gap` catches cases where tool results are treated as
plain model-readable strings without verified provenance or structural
data/directive separation. `soft_control_boundary_reliance` catches designs
that rely on training-level skepticism or prompt-level warnings instead of
parser, sandbox, sanitization, or schema enforcement.
`formatting_fidelity_laundering`, `file_indirection_payload_staging`, and
`self_labeled_filter_test_artifact` catch the file/document variant where
formatting or conversion is used to reproduce risky source blocks unchanged,
especially when artifact metadata discloses filter-test intent.
`system_prompt_attack_scaffold` flags preconfigured trusted-slot scaffolds with
live offensive context, while `offensive_tool_invocation_compliance` and
`technical_failure_not_refusal` separate model compliance from tool success.

**Mitigations:** gate tools on the effect of the action and require
authorization for irreversible ones; don't let a sequence of low-risk calls sum
to a high-risk effect unnoticed; validate trusted prompt/tool definitions before
execution; log tool-call chains so a reviewer can see the composition, not just
the individual calls; wrap tool outputs in typed envelopes, verify provenance,
enforce schemas, and strip directive-like text before model exposure; treat
formatting/conversion as an export boundary that requires source-file
classification; inspect file metadata for payload or filter-test labels; treat
technical tool failure as safety non-intervention when the model otherwise
complied.

---

## Chat-surface displacement

**What you're measuring:** whether the safety layer evaluates the full work
object or only the visible chat turn.

**Evaluation approach:** keep the chat request bland while moving the risk into
attached files, repo content, retrieved text, tool arguments, images, or
generated code. Compare chat-only assessment with full-context assessment.
Pay special attention to attachments or system context that already contain
target architecture, endpoint inventories, auth mechanisms, known weaknesses,
or security-boundary descriptions before the model begins analysis.
Labels like "verified facts" or "institutional memory" should not bypass
provenance checks; they can remove the clarifying friction that would otherwise
scope the task down. In rule blocks, inspect the intelligence value of allowed
read actions, not only the comfort created by banned writes or restarts.
Prompt text alone is the wrong inspection unit when a prior session, tool, or
agent output has already produced the reconnaissance package.

**Detection signals:** run `evasion_signal_detector.py` over extracted text from
files and tool context, not only chat messages. `orchestration_trust_shift` and
`trusted_slot_contamination` are especially relevant here.
`preloaded_recon_package_laundering` catches the combination of a clean
analytical security task with attached or upstream reconnaissance artifacts.

**Mitigations:** treat every file, retrieved chunk, tool result, and code block
as prompt surface; record source path/hash/timestamp; require full-context scans
before tool execution or generated-code use; classify allowed reads by what they
can reveal before accepting governance language as adequate.

---

## Data-category hard stops

Some requests deserve elevated scrutiny because of what they touch, not because
of how persuasive the context sounds. Authentication material, session tokens,
recovery codes, secrets, and enumeration primitives should not become easier to
handle just because the user frames the work as enterprise tooling or incident
response.

**What you're measuring:** whether the model gates on sensitive data/action
classes independently of stated intent.

**Detection signals:** `sensitive_data_action_request` flags authentication or
secret-bearing data categories paired with action verbs such as export, list,
retrieve, harvest, send, or use.
`platform_session_token_exfiltration` catches bug-bounty or operational-analysis
framing paired with injection/exfiltration vectors aimed at platform session
tokens.
`hypervisor_mapping_invariant_bypass` catches EPT/SLAT duplicate-GPA remap
acceptance when it appears with split-page hooking, rootkit, or blue-pill
context.

`probe_confirmation` flags attempts where simply confirming whether a boundary
can be crossed may be the operational objective.

**Mitigations:** inspect every discrete API call, file read, network action, and
data type inside a larger project; require escalation for credential/session
material; convert session-token exfiltration asks into remediation-safe impact,
logging, and fix guidance; keep hypervisor mapping soft spots at invariant,
logging, and negative-test level; treat claimed authorization as metadata, not
as permission.

---

## Reporting

A finding is only useful if someone else can act on it. Each one should carry:
the category, the exact reproduction (input + settings + model version), the
observed vs. expected outcome, a severity, and a confidence. Rank by severity
for the reader; keep the low-confidence ones in the log rather than dropping
them — a separate verification pass is the right place to filter, not the
finding step.

Follow responsible-disclosure practice for anything found against a system you
do not own: report through the owner's channel, give them time to remediate,
and don't publish a working reproduction ahead of a fix.
