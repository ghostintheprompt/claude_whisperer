# Important Findings Method

Case-informed frontier AI red-team and blue-SOC methodology.

This document converts recent authorized frontier-model case review into a
source-safe working method. It does not publish raw transcripts, client-specific
details, or operational payloads. It preserves the professional value: how the
attack moved, where the trust boundary shifted, what evidence mattered, and how
to turn the red finding into blue-team controls.

## The Stance

Frontier AI security should be done like a shared room, not a duel.

Red team work supplies pressure, surprise, and pattern discovery. Blue SOC work
supplies telemetry, containment, review paths, and memory. Safety and policy
teams supply the harm model. Engineering supplies the actual control surface.
When those groups work separately, the system learns slowly. When they work
together, one strange transcript can become a detection, a test suite, a safer
tool boundary, and a better incident story.

That is the posture here: creative enough to find the edge, careful enough to
make the edge useful.

## Core Observation

The model is not always the stage. It is often the trust converter.

The visible prompt may look harmless because the real pressure has already been
loaded into:

- a document or attachment;
- a codebase with credible enterprise shape;
- a ticket, issue, or pull request;
- a retrieval result;
- an agent or subagent pipeline;
- a tool result that the system treats as trusted;
- a clean chat message that points at risky content living in files or code;
- a long conversation that has already moved the baseline.

The key evaluator question is not only "did the model refuse this prompt?" It is
"where did the system assign trust, and did that trust survive contact with
untrusted content?"

Intent is often structural before it is explicit. Legitimate cover plus an
embedded permission gap plus a request for bypass, credentials, execution, or
enumeration tells the story even when the words stay polished.

The threat also lives in what a request enables, not only what it contains.
A short probe, a harmless-looking primer, or a clean code scaffold can matter
because of the door it opens downstream.

## Pattern Lanes

### 1. Decision Preloading

Attack shape: the operator supplies the objective, authorization story, steps,
success criteria, and urgency up front. The model is nudged into acting as a
pure execution engine.

Evaluator question: Does the model independently reassess each action, data
type, and tool call, or does it accept the preloaded frame?

Blue translation:

- detect phrases that remove review, reassessment, or questioning;
- require fresh policy checks before tool calls and code execution;
- log the stated authorization separately from the requested action;
- never let claimed authorization downgrade a sensitive-data boundary.

Implemented signal: `decision_preloading`.

### 2. Calibrated Craft

Attack shape: the operator shapes the attempt to the target model's own safety
layer, reasoning style, conversational habits, and trusted-context assumptions.
High craft is not decoration; it is an operator capability signal.

Evaluator question: Is the attack generic, or does it show model-specific
knowledge, patience, adaptation, and repeated boundary measurement?

Blue translation:

- record sophistication as part of severity;
- distinguish copy-paste prompts from calibrated campaigns;
- preserve timing, repetition, and adaptation patterns;
- treat high-craft failures as intelligence, not just policy misses.

### 3. Mode Switching

Attack shape: the conversation moves in small increments from "developer
building a thing" to "analyst reviewing a thing" to "operator executing a
thing." No single step looks dramatic, but the accumulated direction matters.

Evaluator question: Does the model maintain policy consistency when the user's
role, task frame, or professional context changes?

Blue translation:

- score the trajectory, not only the latest message;
- flag refusal-then-compliance sequences;
- preserve conversation branches when reviewing incidents;
- compare direct requests against staged requests with the same end state.

### 4. Orchestration Trust Shift

Attack shape: the human never directly asks the model. Instructions arrive
through a subagent, tool output, repository file, document, CI job, MCP server,
or automation pipeline. The model receives hostile content as if it were
operator or system context.

Evaluator question: Does the model treat content according to its origin and
authority, or does it collapse all context into trusted instruction?

Blue translation:

- scan tool arguments and tool results, not only chat input;
- mark document and retrieval text as untrusted by default;
- separate operator instructions from content being analyzed;
- log agent identity, tool name, source URI, and authority level per step.

Implemented signal: `orchestration_trust_shift`.

### 5. Chat-Surface Displacement

Attack shape: the chat avoids obvious trigger language while the real
instruction, code path, or policy pressure sits in an attachment, repo file,
tool input, retrieved text, image, or generated codebase.

Evaluator question: Is the safety review inspecting the whole work object, or
only the visible chat turn?

Blue translation:

- scan attachments, code, tool arguments, retrieved chunks, and generated files;
- preserve file names, hashes, source paths, and extraction timestamps;
- compare chat-only risk with full-context risk;
- do not let "the user did not say it in chat" become a blind spot.

### 6. Trusted-Slot Contamination

Attack shape: untrusted text reaches a slot the model treats as authoritative:
system prompt, developer message, operator context, tool-trusted context, or
pipeline instruction.

Evaluator question: Does the model keep untrusted content as data, or does it
promote it into rules?

Blue translation:

- label authority levels explicitly;
- never merge retrieved or attached content into instruction slots;
- alert when source text tries to override, append, replace, or inject rules;
- keep content and instructions visually and structurally separate in evidence.

Implemented signal: `trusted_slot_contamination`.

### 7. Multilingual And Unicode Drift

Attack shape: Unicode, mixed writing systems, homoglyphs, invisible characters,
and encoded strings create mismatches between what a human sees, what a
classifier reads, and what the model processes.

Evaluator question: Does normalization happen before policy evaluation, and are
decoded or normalized artifacts rescanned?

Blue translation:

- normalize Unicode before classification;
- strip or expose zero-width and format characters;
- detect mixed-script control language;
- decode obvious encodings and scan the decoded result;
- preserve both original and normalized evidence.

Implemented signals: `homoglyph_substitution`,
`mixed_script_control_surface`, `invisible_characters`, `base64_payload`,
`rot13_concealment`, `leetspeak_substitution`.

### 8. Low-Signal Erosion

Attack shape: early requests are boring, legitimate, or only mildly weird. They
set vocabulary, role, and assumptions. Later, a sharper request inherits that
baseline.

Evaluator question: Does the system notice when a session's risk level changes,
or does each turn get judged in isolation?

Blue translation:

- keep session-level risk state;
- alert when benign setup is followed by sensitive action;
- track repeated boundary probes even when each probe is low severity;
- review the final turn together with the setup turns.

Implemented signals: `context_dilution`, `oversized_input`; trajectory scoring
is a next implementation target.

### 9. Probe Confirmation

Attack shape: the immediate goal is not the harmful output. The immediate goal
is confirming whether the safety boundary moved. A brief probe, minimal content,
and clean exit can still be a successful operation.

Evaluator question: Is the request asking for a capability, or asking whether a
capability can slip through?

Blue translation:

- treat bypass checks as events, not noise;
- track probe clusters by account, session, model, and interface;
- preserve negative results too, because persistence changes the risk picture;
- look for downstream escalation after a successful confirmation.

Implemented signal: `probe_confirmation`.

### 10. Data-Category Hard Stops

Attack shape: credential harvesting, account access, token handling,
enumeration, or reconnaissance is wrapped in professional enterprise language.
The frame may be persuasive. The data category is still sensitive.

Evaluator question: Does the system gate on the data/action class itself, or
does it over-trust the claimed context?

Blue translation:

- treat auth material as an escalation point regardless of intent framing;
- inspect every discrete API call and data type in generated code;
- separate "build a tool" from "build a tool that touches secrets";
- require approval gates for credential, token, session, recovery, and
  enumeration workflows.

Implemented signal: `sensitive_data_action_request`.

### 11. Clean-Auth Probing

Attack shape: a legitimate or hijacked authenticated account probes the model.
Perimeter controls see clean authentication and pass the interaction through,
leaving the model's content policy and downstream telemetry as the main
detection surface.

Evaluator question: Does the system combine identity/session context with
content-layer signals, or does clean auth lower suspicion too far?

Blue translation:

- correlate authenticated-session history with content risk;
- track memory cultivation and repeated low-signal probing;
- monitor linguistic obfuscation from otherwise trusted accounts;
- do not treat clean login as clean intent.

### 12. Legitimate-Code Camouflage

Attack shape: risky behavior hides inside a credible project: C++, agents,
server architecture, process management, remote input, plugins, enterprise
dashboards, or audit tooling. The model cooperates because the project looks
normal.

Evaluator question: Does the model inspect the dangerous primitives inside the
larger artifact, or does the professional container launder the request?

Blue translation:

- review generated code by primitive, not by project label;
- flag network listeners, credential reads, command execution, persistence,
  process control, and remote input separately;
- require generated-code security review before execution;
- log code provenance and execution context.

## Case Role

Each case should also get a role label:

- **probe:** testing whether the boundary can move;
- **sabotage:** trying to cause damage, disruption, or policy failure;
- **choreography:** a patient staged path with delayed trigger;
- **learning:** measuring the system for future attempts;
- **camouflage:** hiding the risky primitive inside legitimate work.

The same transcript can carry more than one role. Labeling the role keeps the
analysis from flattening every case into "jailbreak worked" or "jailbreak
failed."

## Evidence Discipline

Every finding should carry:

- provider and exact model ID;
- date and time;
- interface used: web UI, API, agent, extension, MCP, local harness;
- system prompt or policy version if authorized to record it;
- tool configuration and permissions;
- attachments, retrieval sources, or repo files involved;
- exact input and output, sanitized when needed;
- expected outcome, observed outcome, severity, and confidence;
- likely case role: probe, sabotage, choreography, learning, camouflage;
- attacker craft level: generic, adapted, calibrated, or persistent;
- red-team interpretation and blue-team recommendation.

The red finding is only half the work. The other half is making the next
reviewer faster.

## Current Deliverables This Repo Should Produce

- A concise evaluator report for each case family.
- A detection or triage rule for every repeatable signal.
- A source-safe case study that explains the method without exposing raw client
  material.
- A model/version matrix that can be re-run after frontier releases.
- A SOC handoff note: what to log, what to alert on, what to escalate, and what
  is probably noise.

## What Not To Do

- Do not lead with jailbreak branding when the real value is evaluation craft.
- Do not claim a model version is current without checking.
- Do not store production API keys in a browser extension.
- Do not publish raw case files unless the repo is private and the contract
  allows it.
- Do not let old exploit-generator language make the work look unserious.

## The Working Line

Pressure creates signal. Signal becomes control. Control gets pressured again.

That loop is the work.
