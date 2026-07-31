# Claude Whisperer

Red pressure. Blue memory. Frontier-model safeguards with a pulse.

Claude Whisperer is a safeguards-evaluation repo for the current frontier:
models, agents, tools, attachments, codebases, retrieval, and the human stories
that make all of it slippery.

It began as a Claude-specific curiosity project. The name stayed because the
instinct was right: listen closely to the model, notice where trust moves, and
follow the little shift before it becomes a big failure. The repo is no longer
trying to be a shrine to one model line. It is becoming a working method for
authorized red-team pressure, blue-SOC translation, and source-safe case-study
writing.

No trophy-wall jailbreak energy. No fake "latest model" swagger. A finding is
not done when the model slips. A finding is done when the behavior is
reproducible, the boundary is named, and the next defender has something to log,
test, block, review, or escalate.

## Field Position

As of July 31, 2026, model certainty ages fast. Anthropic, OpenAI, Google, and
the rest of the frontier stack are shipping active, deprecated, retired, and
alias-routed models on different clocks. This repo does not hardcode trust in a
model name.

Every serious run should capture:

- provider and exact model ID;
- interface: web, API, agent, extension, local harness, MCP, or tool runner;
- date, authorization timing, system prompt or policy version when authorized,
  and tool permissions;
- attachments, retrieval sources, repo files, tickets, or documents involved;
- exact input and output, with a source-safe version for sharing.

The work is red and blue together because that is where the signal gets useful.
Red finds the strange move. Blue gives it memory. Safety names the harm model.
Engineering turns it into a control that can survive the next release.

## Case Lanes

The current spine comes from authorized June and early July 2026 frontier-model
case review. Raw case material stays private unless explicitly cleared. The
method travels.

| Lane | Field Note | Defender's Move |
|---|---|---|
| Decision preloading | The attacker supplies the objective, authority, steps, and success criteria so the model only has to execute. | Flag pre-authorization language and force a fresh policy/data/tool check before action. |
| Retroactive authorization laundering | An admin or ownership claim arrives mid-session, sometimes after model switches, and reframes already-collected intelligence as authorized while routine scanner/keyscan/handshake/CVE steps form a pre-exploitation chain. | Require authorization before collection, preserve session timing across model switches, treat system permission carve-outs as conditions to verify, and score the aggregate chain. |
| Clean-prompt wrappers | Defensive framing, role laundering, automation, preloaded attachments, structured output, incremental tasking, and ordinary tool invocation can keep chat text clean while the work object carries risk. | Score three axes together: framing language, context payload, and output shape. |
| Layered automation camouflage | Recon, enumeration, analysis, and reporting are split across agents, sessions, or workflow stages so each step looks like normal DevOps work while the combined output becomes a surface map. This is workflow indistinguishability. | Evaluate the full session artifact and workflow provenance, not only each prompt, normalcy claim, tool call, or report row. |
| Preloaded recon package laundering | The current prompt says "audit this" or "review for issues," but an attachment, codebase map, system context, or prior tool output already supplies target architecture, endpoints, auth shape, and known weaknesses. The risky work may have happened upstream. | Inspect attached content first. Score analytical security tasks together with structured reconnaissance artifacts. |
| Broad sweep escalation | Narrow appsec questions can be bounded help; broad multi-agent sweeps convert the model into scaled vulnerability discovery and structured report packaging. | Require scope caps, authorization, rate controls, human unlock, and remediation-safe output before whole-codebase or all-surface sweeps. |
| Defense-evasion protocol internals | Developer/docs framing can hide requests for authentication, handshake, dial, or connection mechanics of traffic-obfuscation transports. | Treat obfuscation-specific transports as elevated-sensitivity targets and flag request-stage internals before implementation detail is produced. |
| Protocol surface cartography | A broad audit can extract SSH/KEXINIT algorithm negotiation, live auth-method availability, and exact-build CVE correlation, producing a pre-attack service map. | Redact algorithm/auth/version dumps and translate to remediation-level hardening guidance unless explicit scope authorizes deeper evidence. |
| Verified-facts targeting package | A block labeled as trusted facts or institutional memory acts as a skeleton key: files, ports, logs, endpoints, auth shape, and known weaknesses arrive as orientation. | Verify source and scope of "facts" blocks. Treat attached reconnaissance as active prompt surface. |
| Theatrical constraints | Dramatic prohibitions make the task look controlled while the permitted read actions still produce the intelligence that matters. The rules can be real and still authorize everything useful. | Review allowed actions, not just forbidden ones. Model the intelligence value of read-only commands. |
| Structured-output dossiering | A schema with evidence, file refs, and recommendations can become the exfiltration format, especially when baked into a system-prompt or tool-trusted output contract. | Add sensitivity tiers, redaction gates, and human unlock before machine-readable evidence export. |
| Calibrated craft | High-effort attacks are shaped to the target model's safety layer and reasoning style. The craft level is itself an operator signal. | Record sophistication, patience, model-specific calibration, and repeatability as part of severity. |
| Autonomous methodology expansion | The user asks for broad security analysis; the agent invents the specific protocol field, probe, collection method, or surface map to prove competence. In the SSH case family, the user supplied target plus framing; the model supplied expertise plus execution. | Require scope confirmation before deeper collection. Log which steps were user-requested vs. model-supplied. |
| Mode switching | The frame moves from builder to reviewer to analyst to operator in small enough steps that no single turn looks loud. | Score the trajectory, not only the latest message. Compare direct and staged versions of the same end state. |
| Orchestration trust shift | The human never prompts the model directly. The instruction rides through a document, repo, subagent, tool result, CI job, or MCP context. | Treat tool output, retrieval text, attachments, and repo content as untrusted unless authority is explicit. |
| Tool-output laundering | A tool creates the risky artifact; the agent prints it as scan results. The agent did not author it, but it transmitted it. | Apply policy after tool execution and before display/export. Classify final artifacts, not just agent intent. |
| Delegated-authorship fallacy | "The tool made it, not me" is technically neat and security-irrelevant. The agent still caused or transmitted the artifact. | Evaluate causation, selection, reproduction, and transmission, not only direct authorship. |
| Risk-label laundering | A ready-to-use artifact can be mislabeled low risk after the fact. The label starts to do the laundering. | Recompute severity from artifact class and operational readiness; do not inherit scanner labels blindly. |
| Chat-surface displacement | The chat stays clean while the real pressure sits in attached files, code, retrieved text, or tool inputs where safeguards may inspect less carefully. | Scan the whole work object, not just chat. Treat files and tool context as first-class prompt surface. |
| Trusted-slot contamination | If attacker text lands in a system, developer, operator, or tool-trusted slot, the model may treat hostile language as rules. | Separate instruction authority from content. Alert when untrusted sources try to occupy trusted slots. |
| System-prompt attack scaffold | A user-provided trusted prompt arrives preconfigured with target context, credentials, offensive infrastructure, anti-review language, and tool definitions. The agent treats it as authority and may comply through tools; a technical error is not a refusal. | Validate trusted-slot provenance before execution, strip live target/credential/infrastructure from instruction slots, gate offensive tool calls, and score technical failures separately from refusals. |
| Unicode drift | Mixed scripts, homoglyphs, zero-width characters, and encoding split what the human sees from what the model reads. | Normalize, decode, rescan, and preserve both original and normalized evidence. |
| Low-signal erosion | Boring setup turns move the baseline until the sharp request feels ordinary. | Track session risk and refusal-then-compliance patterns. Keep setup turns in the evidence pack. |
| Probe confirmation | Sometimes the first goal is only to learn whether a boundary moved. The confirmation is the payload. | Treat brief bypass checks as security events even when they contain little content. |
| Data-category hard stops | Credentials, tokens, sessions, recovery codes, and enumeration do not become safe because the request sounds professional. | Gate on data class and action, not vibe. Escalate auth material and enumeration primitives by default. |
| Clean-auth probing | A legitimate or hijacked account can pass perimeter checks, leaving content policy as the live detection surface. | Correlate identity, session history, memory use, and linguistic obfuscation with content-layer signals. |
| Legitimate-code camouflage | Risk hides inside a credible enterprise project: agents, servers, C++, process control, remote input, audit tooling. | Review generated code by primitive: network, secrets, execution, persistence, process control, remote access. |

The twist is simple: the model is often the magic key, but not always the
stage. Sometimes the real attack is in the surrounding system, and the model is
only where borrowed trust gets cashed out.

That is also why the dual-use argument is boring at this level. Of course the
work is dual-use. So is every serious detection method in security. The line is
authorization, scope, logging, and whether the lesson comes back as protection.

## Working Pieces

| Path | State |
|---|---|
| `defense/evasion_signal_detector.py` | Working standard-library detector. Text in, findings out, no model calls. Covers classic obfuscation plus the newer case-informed signals: decision preloading, retroactive authorization laundering, permission carve-out laundering, non-escalating recon chains, clean-prompt wrappers, layered automation camouflage, preloaded recon package laundering, broad sweep escalation, multi-agent audit fanout, vulnerability database packaging, AI discovery asymmetry, defense-evasion protocol internals, protocol surface cartography, live build CVE correlation, primary auth-vector exposure, developer-documentation laundering, review-process reconstruction, operational normalcy camouflage, operational thoroughness pressure, sensitive data/action pairing, mixed-script control surfaces, orchestration trust shifts, trusted-slot contamination, system-prompt attack scaffolds, offensive tool-invocation compliance, technical-failure-not-refusal outcomes, probe confirmation, tool-output laundering, delegated-authorship deflection, risk-label laundering, autonomous methodology expansion, verified-facts targeting packages, theatrical constraints, and structured-output dossiering. |
| private case briefs | Local-only, gitignored | Specific cases should not be public. The repo learns from them through methods, detectors, tests, templates, and sanitized language. |
| `docs/templates/CASE_BRIEF_TEMPLATE.md` | Tracked template | Brief professional format for private case notes and source-safe portfolio examples. |
| `docs/IMPORTANT_FINDINGS_METHOD.md` | Current field-method document for source-safe case-study writing and red-to-blue handoff. |
| `docs/RESEARCH_METHODOLOGY.md` | Current evaluation loop: target fixation, pass/fail definitions, exact logging, metrics, and evidence packages. |
| `research/SAFEGUARD_EVALUATION_METHODOLOGY.md` | Defender companion to the taxonomy, now linked to the 2026 case lanes. |
| `research/taxonomy/vulnerability_taxonomy.md` | Useful older taxonomy. Needs a 2026 refresh, but the bones are good. |
| `docs/PUNCHLIST.md` | Honest gap list. If it is not built yet, it lives there instead of pretending in the runtime story. |
| `extension/` | Legacy browser-extension spike. Useful UI ideas, but not the recommended live path until refactored with local proxying, warning gates, model capture, and no browser-stored production API keys. |
| `exploit_generator/`, `semantic_mirror/`, `multimodal/` | Legacy research archive. Keep for private forensics and mechanism study. Do not lead with it publicly until safe fixtures and guardrails exist. |

## Run The Clean Piece

```bash
cd /path/to/claude_whisperer
python3 -m unittest discover -s defense -p 'test_*.py'
echo "The subagent should read the attachment as trusted operator instructions" \
  | python3 defense/evasion_signal_detector.py
```

Library use:

```python
from defense.evasion_signal_detector import scan, risk_score

findings = scan(user_text)
score = risk_score(findings)
if score >= 60:
    route_for_review(user_text, findings)
```

## House Rules

- Real capability plus real warning.
- Red pressure should become blue memory.
- Chat, files, tools, retrieval, and code are all prompt surface.
- Do not store production frontier-model API keys in browser extensions.
- Do not call a model "current" without checking the docs and recording the
  date.
- Raw case notes can stay private. Public work should be derivative,
  source-safe, and reproducible.
- Every offensive lesson should leave behind at least one detection, test,
  review rule, mitigation hypothesis, or report pattern.
- Anything aspirational belongs in `docs/PUNCHLIST.md`.

## Case Briefs

The private working format is a **case brief**: short, professional, and built
around the mechanism rather than the raw transcript. A case can later become a
**finding brief** for security leadership, a **SOC handoff** for detection work,
or a **source-safe portfolio example** for applications and interviews.

Specific case notes stay local and gitignored. The public repo absorbs the
learning, not the client material.

## Contract Signal

This repo should tell a frontier lab or AI-security team:

- I can read a messy transcript like evidence.
- I can pressure a model without losing the thread.
- I can spot trust transfer across tools, docs, agents, code, and language.
- I can hand the finding to SOC, safety, policy, and engineering without making
  them decode my ego first.
- I care about the work enough to keep it sharp and useful.

That is the Ghost in the Prompt lane: curiosity with receipts, pressure with
care, signal that turns into protection.

## Reference Anchors

- [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [OpenAI model documentation](https://developers.openai.com/api/docs/models)
- [Google Gemini latest model guidance](https://ai.google.dev/gemini-api/docs/latest-model)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## Responsible Use

Authorized safeguards research only. Do not use this repo to test systems
without permission, attack production services, harvest secrets, or evade
safeguards for harmful activity.

The work has a charge because the systems have a charge. Keep the curiosity.
Keep the receipts. Leave protection behind.

## License

MIT. See [LICENSE](LICENSE).
