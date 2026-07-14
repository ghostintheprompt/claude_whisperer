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
| `invisible_characters` | Zero-width and other non-printing characters |
| `rot13_concealment` | Text that becomes English under ROT13 |
| `leetspeak_substitution` | Multiple letter-for-symbol substitutions inside a word |
| `context_dilution` / `oversized_input` | A long body with a short directive isolated in the tail |

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
