"""Evasion-signal detector for LLM input guardrails.

A defensive utility. It scans a piece of user-supplied text for the
*obfuscation and structural* signals that are commonly used to smuggle an
instruction past a model's safeguards — encoded payloads, homoglyph
substitution, invisible characters, and disproportionate "context dilution".

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
from dataclasses import dataclass, field
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
    _detect_base64,
    _detect_rot13,
    _detect_leetspeak,
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
