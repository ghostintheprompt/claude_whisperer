# Safeguard Evaluation Methodology

A defender's companion to the [Vulnerability Taxonomy](taxonomy/vulnerability_taxonomy.md).

The taxonomy names the ways an instruction-following model can be pushed off its
guidelines. This document takes each category from the **evaluator's** side:
what you are actually measuring, how to measure it without fooling yourself, and
what mitigations and detection signals reduce the exposure. The goal is a
repeatable evaluation you can re-run against a new model or a new system prompt
and get a comparable result — not a one-off "we tried some prompts."

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
   settings, and the model version. A finding you can't reproduce is not a
   finding.
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
before the model ever sees it — `base64_payload`, `homoglyph_substitution`,
`invisible_characters`, `leetspeak_substitution`, `rot13_concealment`. Route
high-scoring inputs to stricter handling or review.

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

**Mitigations:** evaluate the final artifact against policy regardless of the
reasoning path that produced it; don't let an accumulation of benign steps
launder a disallowed result; where tools are involved, gate on what the action
*does*, not on how the request was phrased.

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
too, not only the top-level message.

**Mitigations:** gate tools on the effect of the action and require
authorization for irreversible ones; don't let a sequence of low-risk calls sum
to a high-risk effect unnoticed; log tool-call chains so a reviewer can see the
composition, not just the individual calls.

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
