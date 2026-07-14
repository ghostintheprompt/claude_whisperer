<p align="center">
  <img src="claude_whisperer.png" width="480">
</p>

# Claude Whisperer — AI Safeguards Evaluation Toolkit

![License](https://img.shields.io/badge/License-MIT-blue)
![Platform](https://img.shields.io/badge/Platform-Browser%20Extension-orange)
![Focus](https://img.shields.io/badge/Focus-Red%20Team%20Methodology-green)

A research project for **systematically evaluating the safeguards of large language models**. It pairs a structured vulnerability taxonomy with a browser-based testing extension, so that model behavior under adversarial input can be probed methodically rather than ad hoc.

The emphasis is on **method**: naming failure modes, defining how you'd test for each, and documenting results — the discipline a red team or AI-safety evaluator actually works from.

---

## Start with the methodology

The center of this project is the **[Vulnerability Taxonomy](research/taxonomy/vulnerability_taxonomy.md)** — a structured classification of the ways an instruction-following model can be pushed off its guidelines, with a testing approach and example for each category:

| Category | What it covers |
|---|---|
| **Instruction processing** | Conflicting instructions, role-based framing, instruction encoding |
| **Reasoning exploitation** | Chain-of-thought subversion, false ethical dilemmas, indirect requests |
| **Context window** | Context dilution, delayed activation, incremental context building |
| **Multi-turn** | Gradual boundary testing, false urgency, conversation forking |
| **Emergent capabilities** | Tool-use subversion, cross-domain transfer, capability chaining |

Each entry is written for an evaluator: a definition, concrete testing approaches, and a "Responsible Disclosure" note. It's the part of the repo that demonstrates *how the work is reasoned about*, independent of any single model version.

---

## The testing extension

A Manifest V3 browser extension provides a working instrument for exercising the taxonomy against a live model:

- **Semantic reframing** — recontextualize a prompt (academic, auditor, educator framings) to test whether safeguards hold across surface form.
- **Prompt transformation** — cipher/encoding variants (ROT13, Base64, leetspeak, Unicode) to probe input normalization.
- **Multimodal probes** — text-in-image and steganographic variants to test vision-side handling.
- **Session tracking** — logs prompts, responses, and outcomes to JSON for later analysis.

The extension is the delivery mechanism; the taxonomy is what tells you *what* to test and *how to read the result*.

---

## Repository map

```
claude_whisperer/
├── research/
│   └── taxonomy/vulnerability_taxonomy.md   # the methodology (start here)
├── extension/                               # Manifest V3 testing extension
│   ├── background.js  content.js  popup.*   # working code
│   └── modules/                             # transformation modules
├── core/                                    # API clients used by the CLI tooling
├── docs/                                    # methodology notes, testing guides
├── patterns/                                # template / test-case libraries
└── tests/                                   # test harness
```

---

## Status & scope

This is a **research artifact from 2025**. Model references throughout (taxonomy examples, extension defaults, test fixtures) reflect the model generations current at the time it was written — they are a snapshot, not a maintained integration, and some model IDs have since been retired. Treat the code as a demonstration of method and structure, not a turnkey tool against today's models.

The taxonomy and testing approach are the durable parts; they carry over regardless of model version.

---

## Responsible use

This project is for **authorized safeguards research and evaluation** — the kind of work done under proper authorization to make models more robust.

**Appropriate uses:** authorized red-team and penetration testing, AI-safety and alignment research, CTF and educational settings, defensive research (building detections and mitigations).

**Out of scope:** testing without authorization, attacking production systems, or any use aimed at causing harm or evading safeguards for malicious ends.

If you use this to test a model you don't own, get written authorization first and follow responsible-disclosure practice.

---

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <sub>A red-team methodology project. Built for AI-safety and security research.</sub><br>
  <sub>github.com/ghostintheprompt/claude_whisperer</sub>
</p>
