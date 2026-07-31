# Frontier Safeguards Research Methodology

This document describes the current Claude Whisperer research method for
authorized frontier-model safeguards evaluation. Older files in this repository
may mention specific Claude generations. Treat those as historical fixtures.
This methodology is provider- and model-agnostic.

## Operating Principle

An AI red-team finding is not complete when the model fails. It is complete
when the behavior is reproducible, the trust boundary is named, the evidence is
preserved, and the blue-team control is obvious enough to test.

## Evaluation Loop

1. **Fix the target.** Record provider, exact model ID, interface, policy or
   system prompt version, tool permissions, attachments, retrieval state, and
   date.
2. **State the hypothesis.** Name the behavior under test before running it.
3. **Define pass/fail up front.** Refusal, partial compliance, transformed
   compliance, tool-call attempt, and unsafe output are different outcomes.
4. **Run the direct case.** Establish the baseline response.
5. **Run the shaped case.** Vary one pressure lane at a time: framing,
   orchestration, attachment, Unicode, context length, tool availability, or
   conversation trajectory.
6. **Log verbatim.** Preserve exact inputs, outputs, model metadata, and
   environment details. Sanitize only the version intended for sharing.
7. **Translate to control.** Every repeatable red observation should produce a
   detection, review rule, policy test, or mitigation hypothesis.
8. **Re-baseline after release changes.** A result from one model generation is
   evidence, not a permanent truth.

## Pressure Lanes

### Decision Preloading

The attacker supplies authorization, action plan, success criteria, and urgency
so the model has little room to reassess.

Measure:

- Does the model independently evaluate each step?
- Does it ask for missing authority or scope?
- Does it perform sensitive actions because the frame says they are approved?

Control:

- Detect pre-authorization language.
- Require fresh checks at tool and data boundaries.
- Log the difference between claimed authorization and requested capability.

### Mode Switching

The request gradually changes task identity: builder, reviewer, analyst,
auditor, operator. The end state may be refused directly but reached through
small legitimate-looking steps.

Measure:

- Does policy enforcement change with role framing?
- Does the system preserve risk state across turns?
- Does refusal consistency degrade after benign setup?

Control:

- Score trajectories.
- Review refusal-then-compliance sequences.
- Compare direct and staged variants of the same end request.

### Orchestration Trust Shift

The request rides through a pipeline, subagent, code file, document, issue,
retrieval result, or tool output. The model may treat untrusted content as
trusted instruction.

Measure:

- Is source authority preserved?
- Are tool outputs treated as data or instructions?
- Does an automated layer bypass human review?

Control:

- Mark untrusted context explicitly.
- Scan tool inputs, tool outputs, attachments, and retrieved text.
- Log agent identity, tool name, source, and authority per step.

### Unicode And Encoding

The visible surface differs from the model-readable surface through mixed
scripts, homoglyphs, zero-width characters, or encodings.

Measure:

- Does normalization happen before policy evaluation?
- Are decoded artifacts rescanned?
- Does classifier behavior change across scripts?

Control:

- Normalize Unicode.
- Expose invisible characters.
- Decode obvious encodings.
- Preserve original and normalized evidence.

### Data-Category Boundaries

Credential, token, session, recovery, authentication, and enumeration requests
must be treated by data class, not by stated intent.

Measure:

- Does professional framing lower scrutiny?
- Does a larger codebase hide a sensitive primitive?
- Does the model evaluate discrete API calls and data types?

Control:

- Escalate sensitive data/action pairings.
- Inspect generated code by primitive.
- Require approval for auth material, session artifacts, and enumeration.

### Low-Signal Baseline Erosion

The early sequence looks harmless, but it establishes a context that makes a
later request easier to accept.

Measure:

- Does the session risk score rise?
- Does the final turn inherit trust from setup turns?
- Does the same final request get different treatment when isolated?

Control:

- Maintain session-level risk state.
- Alert on repeated boundary probes.
- Review setup turns when the final turn touches sensitive action.

## Metrics

Track both safety and usability:

- attack-success rate;
- refusal consistency;
- false-refusal rate;
- tool-call attempt rate;
- sensitive-data touch rate;
- trajectory risk delta;
- reproducibility across repeated runs;
- regression after model or system-prompt changes.

## Evidence Package

A contract-ready finding should include:

- finding title;
- provider and exact model ID;
- interface and environment;
- policy/system prompt version if authorized;
- tool permissions and available connectors;
- attachment or retrieval source summary;
- exact input/output or sanitized reproduction;
- expected result and observed result;
- severity, confidence, and reproducibility notes;
- red-team interpretation;
- blue-team detection or mitigation recommendation;
- open questions for safety, policy, or engineering.

## Relationship To The Code

The working detector in `defense/evasion_signal_detector.py` implements
pre-model triage for several of the lanes above. It is intentionally defensive:
text in, findings out, no model call, no prompt generation.

Legacy exploit generators and browser-extension pieces are retained as archive
material. They should not be represented as current production-grade tooling
until refactored behind explicit warnings, authorization gates, safer fixtures,
and model-version capture.
