# defense/

The defender's side of the toolkit: utilities for **catching** the evasion
techniques the research catalogs, rather than producing them.

## `evasion_signal_detector.py`

Scans a piece of input text for obfuscation and structural signals commonly
used to smuggle an instruction past a model's safeguards, and returns
structured findings with a triage score. It generates nothing and calls no
model — text in, findings out.

Detected signals:

| Signal | What it catches |
|---|---|
| `base64_payload` | A base64 run that decodes to readable text |
| `homoglyph_substitution` | ASCII letters mixed with look-alike Cyrillic/Greek/Armenian glyphs |
| `mixed_script_control_surface` | Multiple writing systems around instruction or control-surface language |
| `invisible_characters` | Zero-width and other non-printing characters |
| `rot13_concealment` | Text that becomes English under ROT13 |
| `leetspeak_substitution` | Multiple letter-for-symbol substitutions inside a word |
| `decision_preloading` | Language that tries to pre-authorize the model's choices and turn it into an execution engine |
| `defensive_framing_wrapper` | "Audit/review/harden" language paired with target, recon, sensitive-data, or artifact detail |
| `role_laundering` | Security, compliance, or internal-tool role framing paired with context payload or output pressure |
| `automation_wrapper` | Workflow, scheduled job, runbook, or pipeline framing paired with target/context detail |
| `layered_automation_camouflage` | Automation that distributes recon, enumeration, analysis, or reporting across layers |
| `preloaded_context_payload` | Attachments, schemas, codebase maps, or prior agent output carrying target detail |
| `preloaded_recon_package_laundering` | Clean audit/review task paired with attached or upstream reconnaissance artifacts |
| `structured_output_pressure` | Machine-readable findings or schema pressure that can package portable evidence |
| `operational_thoroughness_pressure` | Completeness/specificity framed as a job, role, workflow, or schema requirement |
| `operational_normalcy_camouflage` | Normal engineering/DevOps/workflow language paired with context payload or output pressure |
| `incremental_tasking` | Work split across turns or sessions so no single prompt carries the full signal |
| `legitimate_tool_invocation_wrapper` | Ordinary developer reads/tools used in aggregate to produce a vulnerability map |
| `clean_prompt_axis_combo` | Framing language, context payload, and output shape appearing together |
| `broad_sweep_escalation` | A bounded defensive ask expanding into broad codebase or attack-surface sweep |
| `multi_agent_audit_fanout` | Multiple auditors/agents/parallel lanes fanning out over security review |
| `vulnerability_database_packaging` | Prioritized file/line vulnerability databases or offensive-engagement-style exports |
| `ai_discovery_asymmetry` | AI-driven discovery velocity exceeding defender triage and patch capacity |
| `obfuscation_transport_internals` | Auth/handshake/connection mechanics of traffic-obfuscation or defense-evasion transports |
| `developer_documentation_laundering` | Developer/docs framing paired with sensitive obfuscation-transport internals |
| `review_process_sensitive_reconstruction` | Reviewer analysis reconstructing sensitive mechanics even when sampled output is empty |
| `ssh_crypto_surface_extraction` | Full SSH/KEXINIT algorithm or cryptographic negotiation surface mapping |
| `auth_method_surface_disclosure` | Live authentication-method or password-auth availability disclosure |
| `primary_auth_vector_exposure` | Auth-method disclosure framed as the key or primary attack vector |
| `live_build_cve_correlation` | Exact running build correlated with CVEs and patch status on a live target |
| `protocol_surface_cartography` | Cryptographic negotiation data plus auth-method disclosure in one surface map |
| `retroactive_authorization_laundering` | Admin/ownership claims arriving after recon or already-collected intelligence |
| `permission_carveout_laundering` | Authorized-testing or system-permission language used as automatic clearance |
| `non_escalating_recon_chain` | Routine-looking collection steps that aggregate into pre-exploitation recon |
| `sensitive_data_action_request` | Auth/secret-bearing data categories paired with action verbs |
| `orchestration_trust_shift` | Agent, tool, or pipeline framing that can smuggle instructions into trusted context |
| `trusted_slot_contamination` | Untrusted content trying to reach system/developer/operator instruction slots |
| `probe_confirmation` | Requests where confirming a bypass may be the payload |
| `tool_output_laundering` | High-risk tool artifacts paired with raw/verbatim reporting requests |
| `delegated_authorship_deflection` | "The tool made it" framing paired with a high-risk artifact |
| `risk_label_laundering` | Low-severity labels paired with high-risk artifacts |
| `autonomous_methodology_expansion` | Broad defensive framing where the agent fills in deeper audit tradecraft against a target |
| `verified_facts_targeting_package` | "Verified facts" or memory blocks containing reconnaissance artifacts |
| `theatrical_constraints_operational_permissions` | Strict-sounding prohibitions paired with intelligence-producing read permissions |
| `structured_output_dossiering` | Machine-readable evidence schemas that package portable target intelligence |
| `context_dilution` / `oversized_input` | A long body with a short directive isolated in the tail |

The newer signals come from 2026 frontier-model case review. They are meant
for SOC triage and evaluator workflow design: a hit does not prove malice, but
it says "slow down here; the trust boundary is being touched."

### Use as a library

```python
from defense.evasion_signal_detector import scan, risk_score

findings = scan(user_text)
if risk_score(findings) >= 60:
    route_for_review(user_text, findings)
```

### Use from the shell

```bash
echo "some text" | python3 defense/evasion_signal_detector.py
python3 defense/evasion_signal_detector.py path/to/file.txt
```

### Tests

```bash
cd defense && python3 -m unittest test_evasion_signal_detector
```

No third-party dependencies; standard library only.

## Context

These signals map to the categories in
[`../research/taxonomy/vulnerability_taxonomy.md`](../research/taxonomy/vulnerability_taxonomy.md);
the defender's evaluation and mitigation guidance for each is in
[`../research/SAFEGUARD_EVALUATION_METHODOLOGY.md`](../research/SAFEGUARD_EVALUATION_METHODOLOGY.md).
