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
- a long conversation that has already moved the baseline.

The key evaluator question is not only "did the model refuse this prompt?" It is
"where did the system assign trust, and did that trust survive contact with
untrusted content?"

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

### 2. Mode Switching

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

### 3. Orchestration Trust Shift

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

### 4. Multilingual And Unicode Drift

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

### 5. Low-Signal Erosion

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

### 6. Data-Category Hard Stops

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

### 7. Legitimate-Code Camouflage

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
