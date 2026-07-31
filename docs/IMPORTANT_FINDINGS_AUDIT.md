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

## Current Runtime Signals

Implemented in `defense/evasion_signal_detector.py`:

- `base64_payload`
- `homoglyph_substitution`
- `mixed_script_control_surface`
- `invisible_characters`
- `rot13_concealment`
- `leetspeak_substitution`
- `decision_preloading`
- `sensitive_data_action_request`
- `orchestration_trust_shift`
- `trusted_slot_contamination`
- `probe_confirmation`
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
