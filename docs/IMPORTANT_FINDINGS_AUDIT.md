# Important Findings Audit

Audit source: `/Users/greenplanet/Downloads/Important Findings.rtf`

Follow-up note: the user clarified that many recent attacks kept chat wording
clean while moving the real pressure into files, tool calls, code, or other
attached context.

Purpose: make sure the June/early July 2026 findings are represented in Claude
Whisperer as method, detection, reporting discipline, or punchlist. This is the
template for future rounds: `Important Findings 2`, `Important Findings 3`, and
so on.

## Batch Result

Status: captured after the second pass.

The first pass captured the broad spine: decision preloading, mode switching,
orchestration trust shift, Unicode drift, low-signal erosion, data-category hard
stops, and legitimate-code camouflage. The audit found additional nuance that
needed to become first-class: calibrated craft, trusted-slot contamination,
probe confirmation, clean-auth probing, structural intent, case-role labeling,
and "what the request enables" as a severity lens.

## Coverage Map

| ID | Source Lines | Finding | Claude Whisperer Coverage | Status |
|---|---:|---|---|---|
| IF-01 | 2-4, 48-49 | Decision preloading turns the model into an execution engine. | README case lane, Important Findings Method lane, `decision_preloading` detector, unit test. | Captured |
| IF-02 | 5-8, 50-53 | Attack sophistication maps to target-model safety sophistication and operator capability. | README `Calibrated craft` lane, Important Findings Method lane, evidence package craft-level field. | Captured |
| IF-03 | 9-12, 54-57 | Mode switching from builder to reviewer to analyst avoids a single reassessment moment. | README `Mode switching` lane, Important Findings Method lane, research methodology trajectory guidance. | Captured |
| IF-04 | 13-15, 58-60 | Violations have roles: probing, sabotage, choreography, learning. AI is not always the main stage. | Important Findings Method `Case Role` section, README "model is not always the stage" framing. | Captured |
| IF-05 | 16-19, 61-64 | Multilingual/script switching and Unicode tricks create sliding-window blind spots. | README `Unicode drift` lane, Important Findings Method lane, detector signals for homoglyphs, mixed scripts, invisible chars, encodings. | Captured |
| IF-06 | 20-25, 65-70 | Subagent orchestration lets instructions arrive as operator/system context while no human watches. | README `Orchestration trust shift` lane, Important Findings Method lane, `orchestration_trust_shift` detector, unit test. | Captured |
| IF-07 | 26-27, 71-72 | Low-signal requests erode the baseline before dangerous content appears. | README `Low-signal erosion` lane, Important Findings Method lane, context dilution detector, trajectory scoring in punchlist. | Captured; scoring remains next-work |
| IF-08 | 28-33, 73-81 | Credential harvesting and reconnaissance hide inside legitimate tooling and large codebases. Use fixed data-category checks. | README `Data-category hard stops` and `Legitimate-code camouflage`, Important Findings Method lanes, `sensitive_data_action_request` detector. | Captured |
| IF-09 | 103-106 | If attacker text gets into the system prompt/trusted slot, the model treats it as rules; persistence matters. | README `Trusted-slot contamination` lane, Important Findings Method lane, `trusted_slot_contamination` detector, unit test. | Captured |
| IF-10 | 107-109 | Target + working credentials + action directive should trigger elevated scrutiny. | Data-category hard stops lane, `sensitive_data_action_request` detector, evidence package data/action notes. | Captured |
| IF-11 | 110-113 | Clean or hijacked authenticated accounts are ideal probing vehicles; perimeter auth may hide content risk. | README `Clean-auth probing` lane, Important Findings Method lane. Needs future session/identity telemetry implementation. | Captured in method; runtime next-work |
| IF-12 | 114-117 | Legitimate-looking C++ infrastructure is high-risk when it combines networking, process management, and remote input/execution. | README and Important Findings Method `Legitimate-code camouflage`; punchlist generated-code primitive review. | Captured; code review scanner next-work |
| IF-13 | 118-120 | Probe-only confirmation can be the payload. | README `Probe confirmation` lane, Important Findings Method lane, `probe_confirmation` detector, unit test. | Captured |
| IF-14 | 121-122 | Intent is structural: legitimate cover + embedded permission gap + bypass request. | Important Findings Method core observation; data-category and legitimate-code lanes. | Captured |
| IF-15 | 123 | The threat lives in what it enables, not only what it contains. | Important Findings Method core observation; README contract signal and case lanes. | Captured |
| IF-16 | 124-125 | Priming messages and patient staged setup enable downstream trigger prompts. | Low-signal erosion and mode-switching lanes; trajectory scoring punchlist. | Captured; scoring remains next-work |
| IF-17 | Follow-up | Chat text often avoids safeguard-trigger words while files, tools, code, or attachments carry the real pressure. | README `Chat-surface displacement` lane; Important Findings Method lane; scanner can be run over files, not only pasted chat. | Captured; full file/tool pipeline scanning remains next-work |
| IF-18 | Follow-up | Clean prompts collapse into seven wrapper categories: defensive framing, role laundering, automation wrapper, pre-loaded context, structured output pressure, incremental tasking, and legitimate tool invocation. | README `Clean-prompt wrappers` lane, Important Findings Method taxonomy, Research Methodology lane, detector signals and tests. | Captured |
| IF-19 | Follow-up | Automation wrappers are hardest because they distribute work across layers, normalize behavior as enterprise tooling, and make the risky surface visible only in full-session output. | README `Layered automation camouflage` lane, Important Findings Method detectability tiers, Research Methodology, detector signals and tests. | Captured |
| IF-20 | Follow-up | The hardest phrasing problem is that the suspicious pattern also describes normal software engineering and DevOps culture. Normalcy claims must be tested against scope, provenance, data class, and final artifact. | README `Layered automation camouflage` lane, Important Findings Method, Research Methodology, `operational_normalcy_camouflage` detector and test. | Captured |
| IF-21 | Follow-up | Workflow indistinguishability: modular decomposition, configuration files, schemas, and multi-agent pipelines are accurate descriptions of both mature enterprise work and layered adversarial choreography. | Important Findings Method, Research Methodology, private Case 006, expanded `operational_normalcy_camouflage` detector test. | Captured |
| IF-22 | Follow-up | Attachment-heavy recon package laundering: the visible prompt says "audit this" while attached documents, codebase maps, system context, or prior tool output already supply target architecture, enumerated endpoints, auth mechanisms, and known weaknesses. | README `Preloaded recon package laundering` lane, Important Findings Method, Research Methodology, private Case 004, `preloaded_recon_package_laundering` detector and test. | Captured |
| IF-23 | Follow-up | Bounded appsec questions are different from broad multi-agent sweeps. Sweeps can turn the model into scaled vulnerability discovery and package file/line findings faster than defenders can triage and patch. | README `Broad sweep escalation` lane, Important Findings Method, Research Methodology, evaluation companion, private Case 007, detector signals and tests. | Captured |
| IF-24 | Follow-up | Defense-evasion protocol internals: developer/open-source documentation framing can hide requests for authentication, handshake, dial, or connection mechanics of traffic-obfuscation transports. Reviewer analysis can also reconstruct sensitive mechanics even when sampled output is empty. | README `Defense-evasion protocol internals` lane, Important Findings Method, Research Methodology, evaluation companion, private Case 008, detector signals and tests. | Captured |
| IF-25 | Follow-up | Protocol surface cartography: full SSH/KEXINIT algorithm extraction plus authentication-method disclosure creates a pre-attack service map, not just remediation evidence. | README `Protocol surface cartography` lane, Important Findings Method, Research Methodology, evaluation companion, private Case 009, detector signals and tests. | Captured |
| IF-26 | Follow-up | Auth-method disclosure becomes primary-vector exposure when labeled as a key finding, and exact running-build-to-CVE-to-patch-status joins complete a live vulnerability triage cycle. | README `Protocol surface cartography` lane, Important Findings Method, Research Methodology, evaluation companion, private Case 009, `primary_auth_vector_exposure` and `live_build_cve_correlation` tests. | Captured |

## Current Runtime Signals

Implemented in `defense/evasion_signal_detector.py`:

- `base64_payload`
- `homoglyph_substitution`
- `mixed_script_control_surface`
- `invisible_characters`
- `rot13_concealment`
- `leetspeak_substitution`
- `decision_preloading`
- `defensive_framing_wrapper`
- `role_laundering`
- `automation_wrapper`
- `layered_automation_camouflage`
- `preloaded_context_payload`
- `preloaded_recon_package_laundering`
- `structured_output_pressure`
- `operational_thoroughness_pressure`
- `operational_normalcy_camouflage`
- `incremental_tasking`
- `legitimate_tool_invocation_wrapper`
- `broad_sweep_escalation`
- `multi_agent_audit_fanout`
- `vulnerability_database_packaging`
- `ai_discovery_asymmetry`
- `obfuscation_transport_internals`
- `developer_documentation_laundering`
- `review_process_sensitive_reconstruction`
- `ssh_crypto_surface_extraction`
- `auth_method_surface_disclosure`
- `primary_auth_vector_exposure`
- `live_build_cve_correlation`
- `protocol_surface_cartography`
- `clean_prompt_axis_combo`
- `sensitive_data_action_request`
- `orchestration_trust_shift`
- `trusted_slot_contamination`
- `probe_confirmation`
- `tool_output_laundering`
- `delegated_authorship_deflection`
- `risk_label_laundering`
- `autonomous_methodology_expansion`
- `verified_facts_targeting_package`
- `theatrical_constraints_operational_permissions`
- `structured_output_dossiering`
- `context_dilution`
- `oversized_input`

## Still Next-Work

These are captured in method and punchlist but not fully implemented as runtime
systems yet:

- session trajectory scoring for low-signal erosion;
- automated file, attachment, retrieved-text, and tool-argument scanning;
- authenticated-account/content-risk correlation;
- generated-code primitive review for network, execution, secrets, persistence,
  and remote input;
- source-safe case-study export templates;
- model/provider metadata adapters.

## Workflow For Important Findings 2+

1. Add the next source file as `Important Findings 2.rtf`, markdown, or text.
2. Extract the findings into numbered bullets.
3. Map each bullet to one of four destinations:
   - README lane;
   - methodology section;
   - detector/runtime signal;
   - punchlist item.
4. Mark status:
   - captured;
   - captured in method, runtime next-work;
   - missing;
   - intentionally private/raw.
5. Add tests for any new detector signal.
6. Keep raw case material private unless explicitly cleared; publish mechanism
   and controls, not client source.

This is the smartest loop: research batch, audit, method update, detector/test
update, punchlist update, then the next batch.
