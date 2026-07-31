"""Evasion-signal detector for LLM input guardrails.

A defensive utility. It scans a piece of user-supplied text for the
*obfuscation, trust-shift, and structural* signals that are commonly used to
smuggle an instruction past a model's safeguards: encoded payloads, homoglyph
substitution, invisible characters, decision preloading, sensitive data/action
pairing, orchestration trust shifts, and disproportionate context dilution.

It does not generate, transform, or attack anything. Given text in, it returns
structured findings that a trust-and-safety pipeline can log, score, or route
for review. Each finding names the signal, a severity, and the concrete
evidence that triggered it, so a human can verify the call.

The categories map to the failure-mode taxonomy in
``research/taxonomy/vulnerability_taxonomy.md`` — this is the detection side of
those categories.

Usage:
    from defense.evasion_signal_detector import scan, risk_score
    findings = scan(user_text)
    score = risk_score(findings)          # 0..100

CLI:
    echo "some text" | python3 defense/evasion_signal_detector.py
    python3 defense/evasion_signal_detector.py path/to/file.txt
"""

from __future__ import annotations

import base64
import binascii
import codecs
import re
import sys
import unicodedata
from dataclasses import dataclass
from typing import List

# Severity is an ordered label; higher weight contributes more to risk_score.
_SEVERITY_WEIGHT = {"info": 5, "low": 15, "medium": 35, "high": 60}


@dataclass
class Finding:
    """One detected signal, with the evidence that produced it."""

    signal: str
    severity: str
    detail: str
    evidence: str = ""
    span: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        if self.severity not in _SEVERITY_WEIGHT:
            raise ValueError(f"unknown severity: {self.severity!r}")

    def as_dict(self) -> dict:
        return {
            "signal": self.signal,
            "severity": self.severity,
            "detail": self.detail,
            "evidence": self.evidence,
            "span": list(self.span) if self.span else None,
        }


# --- individual detectors ---------------------------------------------------

# Invisible / formatting characters that carry no visible glyph but survive
# copy-paste. Used to break up trigger words or hide instructions.
_INVISIBLE = {
    "​": "ZERO WIDTH SPACE",
    "‌": "ZERO WIDTH NON-JOINER",
    "‍": "ZERO WIDTH JOINER",
    "⁠": "WORD JOINER",
    "﻿": "ZERO WIDTH NO-BREAK SPACE",
    "­": "SOFT HYPHEN",
    "᠎": "MONGOLIAN VOWEL SEPARATOR",
}

# Leetspeak substitutions: a digit/symbol standing in for a letter.
_LEET = set("0134577@$!")

_WORD_RE = re.compile(r"\S+")
# A base64 candidate: a long run of the base64 alphabet, optionally padded.
_B64_RE = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")
# A short common-word set used only to tell whether a ROT13 pass makes the
# text *more* like English than the original (concealment heuristic).
_COMMON = {
    "the", "and", "you", "that", "this", "with", "for", "are", "not", "your",
    "have", "from", "they", "will", "would", "there", "their", "what", "about",
    "which", "when", "make", "like", "how", "then", "instructions", "ignore",
    "system", "prompt", "please", "should", "must",
}

_CONTROL_TERMS_RE = re.compile(
    r"\b(?:ignore|instruction|instructions|system|prompt|rule|rules|policy|"
    r"execute|run|call|tool|agent|workflow|developer|operator|authority)\b",
    re.IGNORECASE,
)

_DECISION_PRELOAD_RE = re.compile(
    r"\b(?:"
    r"follow (?:these|the) steps exactly|"
    r"do not (?:ask|stop|evaluate|reason|reassess|refuse)|"
    r"no need to (?:ask|evaluate|reason|verify|check)|"
    r"already (?:authorized|approved|verified|decided)|"
    r"just (?:execute|run|perform|do it)|"
    r"complete the task without|"
    r"the decision has already been made|"
    r"treat (?:this|these) as (?:approved|authorized|operator|system)"
    r")\b",
    re.IGNORECASE,
)

_SENSITIVE_DATA_RE = re.compile(
    r"\b(?:"
    r"api[-_ ]?key|access[-_ ]?token|bearer token|oauth token|refresh token|"
    r"session cookie|auth(?:entication)? header|password|passwd|credential(?:s)?|"
    r"secret(?:s)?|private key|ssh key|jwt|2fa|2sv|two[- ](?:factor|step)|"
    r"backup code(?:s)?|recovery code(?:s)?|login token"
    r")\b",
    re.IGNORECASE,
)

_SENSITIVE_ACTION_RE = re.compile(
    r"\b(?:"
    r"collect|extract|export|dump|list|enumerate|retrieve|scrape|harvest|"
    r"store|log|print|send|forward|validate|use|authenticate|login|exfiltrate"
    r")\b",
    re.IGNORECASE,
)

_ORCHESTRATION_RE = re.compile(
    r"\b(?:"
    r"subagent|sub-agent|worker agent|agent pipeline|automation pipeline|"
    r"orchestrator|orchestration|workflow runner|ci job|tool call|mcp server|"
    r"system context|operator-level|developer message|trusted context"
    r")\b",
    re.IGNORECASE,
)

_TRUSTED_SLOT_RE = re.compile(
    r"\b(?:"
    r"system prompt|system instructions|developer message|operator-level|"
    r"trusted context|rules|policy|higher implicit trust"
    r")\b",
    re.IGNORECASE,
)

_UNTRUSTED_SOURCE_RE = re.compile(
    r"\b(?:"
    r"attacker|malicious|user-supplied|document|attachment|tool output|"
    r"repository|repo|ticket|issue|webpage|subagent|pipeline|inject|insert|"
    r"prepend|append|override|replace"
    r")\b",
    re.IGNORECASE,
)

_PROBE_CONFIRMATION_RE = re.compile(
    r"\b(?:confirm|check|test|verify|see if|find out whether|determine whether)\b"
    r".{0,120}\b(?:bypass|jailbreak|safety layer|guardrail|filter|refusal|policy)\b"
    r"|"
    r"\b(?:bypass|jailbreak|guardrail)\b"
    r".{0,120}\b(?:confirm|check|test|verify|see if)\b",
    re.IGNORECASE | re.DOTALL,
)

_TRUST_TRANSFER_RE = re.compile(
    r"\b(?:"
    r"instructions?|policy|system|operator|developer|trusted|tool output|"
    r"document|attachment|repository|ticket|issue|pull request|webpage|runbook"
    r")\b",
    re.IGNORECASE,
)


def _detect_invisible(text: str) -> List[Finding]:
    hits: dict[str, int] = {}
    first_at: dict[str, int] = {}
    for i, ch in enumerate(text):
        if ch in _INVISIBLE:
            hits[ch] = hits.get(ch, 0) + 1
            first_at.setdefault(ch, i)
    findings = []
    for ch, count in hits.items():
        name = _INVISIBLE[ch]
        findings.append(
            Finding(
                signal="invisible_characters",
                severity="high" if count > 2 else "medium",
                detail=(
                    f"{count} occurrence(s) of {name} (U+{ord(ch):04X}). "
                    "Invisible characters can split trigger words or hide text "
                    "that a human reviewer will not see."
                ),
                evidence=f"U+{ord(ch):04X} {name} x{count}",
                span=(first_at[ch], first_at[ch] + 1),
            )
        )
    return findings


def _confusable_script(ch: str) -> str | None:
    """Return the script name if ch is a letter from a non-Latin script that is
    commonly used as a Latin look-alike (homoglyph), else None."""
    if not ch.isalpha() or ch.isascii():
        return None
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    for script in ("CYRILLIC", "GREEK", "ARMENIAN"):
        if name.startswith(script):
            return script
    return None


def _script_name(ch: str) -> str | None:
    if not ch.isalpha():
        return None
    if ch.isascii():
        return "LATIN"
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    for script in (
        "ARABIC",
        "ARMENIAN",
        "CYRILLIC",
        "GREEK",
        "HEBREW",
        "HIRAGANA",
        "KATAKANA",
        "CJK",
        "DEVANAGARI",
    ):
        if name.startswith(script):
            return script
    return None


def _detect_homoglyphs(text: str) -> List[Finding]:
    findings = []
    for m in _WORD_RE.finditer(text):
        token = m.group()
        has_ascii_letter = any(c.isascii() and c.isalpha() for c in token)
        confusables = [(c, s) for c in token if (s := _confusable_script(c))]
        # A token that mixes ASCII letters with look-alike letters from another
        # script is the classic homoglyph-substitution pattern.
        if has_ascii_letter and confusables:
            scripts = sorted({s for _, s in confusables})
            findings.append(
                Finding(
                    signal="homoglyph_substitution",
                    severity="high",
                    detail=(
                        f"Token mixes ASCII letters with {', '.join(scripts)} "
                        f"look-alike character(s). This defeats exact-string "
                        f"matching on trigger terms."
                    ),
                    evidence=token,
                    span=(m.start(), m.end()),
                )
            )
    return findings


def _detect_mixed_script_control_surface(text: str) -> List[Finding]:
    scripts = sorted({script for ch in text if (script := _script_name(ch))})
    if "LATIN" not in scripts or len(scripts) < 3:
        return []
    if not _CONTROL_TERMS_RE.search(text):
        return []
    return [
        Finding(
            signal="mixed_script_control_surface",
            severity="medium",
            detail=(
                "Input mixes Latin text with multiple other writing systems near "
                "instruction or control-surface language. This can create blind "
                "spots for classifiers that rely on sliding windows, keyword "
                "matching, or single-script normalization."
            ),
            evidence=", ".join(scripts),
        )
    ]


def _looks_like_text(raw: bytes) -> bool:
    if not raw:
        return False
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if not decoded:
        return False
    printable = sum(ch.isprintable() or ch in " \t\n\r" for ch in decoded)
    return printable / len(decoded) >= 0.85 and any(ch.isalpha() for ch in decoded)


def _detect_base64(text: str) -> List[Finding]:
    findings = []
    for m in _B64_RE.finditer(text):
        token = m.group()
        # base64 length must be a multiple of 4 to decode cleanly.
        if len(token) % 4 != 0:
            continue
        try:
            raw = base64.b64decode(token, validate=True)
        except (binascii.Error, ValueError):
            continue
        if _looks_like_text(raw):
            preview = raw.decode("utf-8", "replace")[:60]
            findings.append(
                Finding(
                    signal="base64_payload",
                    severity="high",
                    detail=(
                        "A base64 run decodes to readable text. Encoding is used "
                        "to carry an instruction past surface-level review."
                    ),
                    evidence=f"decodes to: {preview!r}",
                    span=(m.start(), m.end()),
                )
            )
    return findings


def _detect_rot13(text: str) -> List[Finding]:
    words = re.findall(r"[A-Za-z]{3,}", text.lower())
    if len(words) < 4:
        return []
    before = sum(w in _COMMON for w in words)
    rotated = codecs.encode(text, "rot_13")
    rot_words = re.findall(r"[A-Za-z]{3,}", rotated.lower())
    after = sum(w in _COMMON for w in rot_words)
    # If ROT13 turns gibberish into several common words, the original was
    # probably ROT13-concealed text.
    if after >= 3 and after >= before + 2:
        preview = rotated[:60]
        return [
            Finding(
                signal="rot13_concealment",
                severity="medium",
                detail=(
                    "Applying ROT13 yields substantially more common English "
                    "words than the original, suggesting concealed text."
                ),
                evidence=f"rot13 -> {preview!r}",
            )
        ]
    return []


def _detect_leetspeak(text: str) -> List[Finding]:
    findings = []
    for m in _WORD_RE.finditer(text):
        token = m.group()
        letters = [c for c in token if c.isalpha()]
        leet = [c for c in token if c in _LEET]
        # Interior digit/symbol substitution inside an otherwise-alphabetic word.
        if len(letters) >= 2 and len(leet) >= 2 and len(token) <= 20:
            findings.append(
                Finding(
                    signal="leetspeak_substitution",
                    severity="low",
                    detail=(
                        "Word contains multiple letter-for-symbol substitutions, "
                        "a common way to evade keyword filters."
                    ),
                    evidence=token,
                    span=(m.start(), m.end()),
                )
            )
    return findings


def _detect_decision_preloading(text: str) -> List[Finding]:
    matches = list(_DECISION_PRELOAD_RE.finditer(text))
    if len(matches) < 2:
        return []
    evidence = "; ".join(m.group(0) for m in matches[:3])
    return [
        Finding(
            signal="decision_preloading",
            severity="medium",
            detail=(
                "Input contains multiple phrases that pre-load authorization or "
                "decision-making and push the model toward execution without "
                "reassessment. This is a high-value review signal for agentic "
                "and code-generation workflows."
            ),
            evidence=evidence,
            span=(matches[0].start(), matches[-1].end()),
        )
    ]


def _detect_sensitive_data_action_request(text: str) -> List[Finding]:
    sensitive = list(_SENSITIVE_DATA_RE.finditer(text))
    actions = list(_SENSITIVE_ACTION_RE.finditer(text))
    if not sensitive or not actions:
        return []
    first = min(sensitive[0].start(), actions[0].start())
    last = max(sensitive[-1].end(), actions[-1].end())
    return [
        Finding(
            signal="sensitive_data_action_request",
            severity="high",
            detail=(
                "Request combines authentication or secret-bearing data with "
                "action verbs. Treat this as a data-category boundary first; "
                "professional framing or claimed authorization should not lower "
                "scrutiny."
            ),
            evidence=f"{sensitive[0].group(0)} + {actions[0].group(0)}",
            span=(first, last),
        )
    ]


def _detect_orchestration_trust_shift(text: str) -> List[Finding]:
    orchestration = list(_ORCHESTRATION_RE.finditer(text))
    trust_transfer = list(_TRUST_TRANSFER_RE.finditer(text))
    if not orchestration or len(trust_transfer) < 2:
        return []
    evidence_terms = [orchestration[0].group(0)] + [
        m.group(0) for m in trust_transfer[:2]
    ]
    return [
        Finding(
            signal="orchestration_trust_shift",
            severity="medium",
            detail=(
                "Input references an agent, tool, or automation layer together "
                "with trusted-context language. This is the shape where a human "
                "may never directly prompt the model, and malicious instructions "
                "can arrive as pipeline or operator context."
            ),
            evidence=" + ".join(evidence_terms),
            span=(orchestration[0].start(), trust_transfer[-1].end()),
        )
    ]


def _detect_trusted_slot_contamination(text: str) -> List[Finding]:
    trusted = list(_TRUSTED_SLOT_RE.finditer(text))
    source = list(_UNTRUSTED_SOURCE_RE.finditer(text))
    if not trusted or not source:
        return []
    return [
        Finding(
            signal="trusted_slot_contamination",
            severity="high",
            detail=(
                "Input combines trusted instruction slots with untrusted source "
                "or insertion language. This is the failure mode where hostile "
                "content reaches the model as rules rather than data."
            ),
            evidence=f"{trusted[0].group(0)} + {source[0].group(0)}",
            span=(min(trusted[0].start(), source[0].start()), max(trusted[-1].end(), source[-1].end())),
        )
    ]


def _detect_probe_confirmation(text: str) -> List[Finding]:
    match = _PROBE_CONFIRMATION_RE.search(text)
    if not match:
        return []
    return [
        Finding(
            signal="probe_confirmation",
            severity="medium",
            detail=(
                "Request appears focused on confirming whether a safety boundary "
                "can be crossed. In probing workflows, the confirmation can be "
                "the payload even when the content is brief."
            ),
            evidence=match.group(0)[:120],
            span=(match.start(), match.end()),
        )
    ]


def _detect_context_dilution(text: str, threshold: int = 4000) -> List[Finding]:
    """Structural signal: a very long body with a short directive-style line
    isolated in the final stretch (delayed-activation / haystack pattern)."""
    if len(text) < threshold:
        return []
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        return []
    tail = lines[max(0, int(len(lines) * 0.9)):]
    median_len = sorted(len(ln) for ln in lines)[len(lines) // 2]
    short_tail = [ln for ln in tail if len(ln) < max(80, median_len // 2)]
    if short_tail:
        return [
            Finding(
                signal="context_dilution",
                severity="low",
                detail=(
                    f"Input is {len(text)} chars with a short line isolated in "
                    "the final 10%. Large benign context with a late, brief "
                    "instruction is the delayed-activation pattern; warrants "
                    "manual review of the tail."
                ),
                evidence=short_tail[-1][:80],
            )
        ]
    return [
        Finding(
            signal="oversized_input",
            severity="info",
            detail=(
                f"Input is {len(text)} chars. Long inputs should be reviewed for "
                "buried or delayed instructions."
            ),
        )
    ]


_DETECTORS = (
    _detect_invisible,
    _detect_homoglyphs,
    _detect_mixed_script_control_surface,
    _detect_base64,
    _detect_rot13,
    _detect_leetspeak,
    _detect_decision_preloading,
    _detect_sensitive_data_action_request,
    _detect_orchestration_trust_shift,
    _detect_trusted_slot_contamination,
    _detect_probe_confirmation,
    _detect_context_dilution,
)


def scan(text: str) -> List[Finding]:
    """Run every detector over ``text`` and return findings, most severe first."""
    findings: List[Finding] = []
    for detector in _DETECTORS:
        findings.extend(detector(text))
    findings.sort(key=lambda f: _SEVERITY_WEIGHT[f.severity], reverse=True)
    return findings


def risk_score(findings: List[Finding]) -> int:
    """Aggregate findings into a 0..100 score (saturating).

    A single high-severity signal already lands in the elevated range; multiple
    signals accumulate. The score is a triage aid, not a verdict.
    """
    total = sum(_SEVERITY_WEIGHT[f.severity] for f in findings)
    return min(100, total)


def format_report(text: str) -> str:
    findings = scan(text)
    score = risk_score(findings)
    lines = [f"risk_score: {score}/100", f"findings: {len(findings)}", ""]
    if not findings:
        lines.append("  (no evasion signals detected)")
    for f in findings:
        lines.append(f"  [{f.severity.upper():6}] {f.signal}")
        lines.append(f"           {f.detail}")
        if f.evidence:
            lines.append(f"           evidence: {f.evidence}")
    return "\n".join(lines)


def _read_input(argv: List[str]) -> str:
    if len(argv) > 1:
        with open(argv[1], "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return sys.stdin.read()


if __name__ == "__main__":
    print(format_report(_read_input(sys.argv)))
