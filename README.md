# Claude Whisperer

Claude Whisperer is a Claude evaluation and safeguards research workbench.

**NEW: Optimized for Claude 4.7 (Opus) and Project Glasswing evaluations.**

The current repo is centered on a browser extension for exploring model behavior on `claude.ai`, plus a mixed set of research notes, pattern libraries, and older Python utilities from earlier safeguard-monitor experiments. It is not a clean-room product and it is not pretending to be one. It is a working archive of how the project evolved.

## What This Repo Is

- A browser extension for testing semantic reframing, structured prompt generation, and multimodal prompt-in-image ideas against Claude
- A research workbench for evaluating safeguards, patterns, failure modes, and model drift
- A public proof surface for Claude-focused red-team and evaluation work
- A mixed-era repository where current extension work sits alongside earlier safeguard-monitor tooling and archived research

## What This Repo Is Not

- Not a copy-paste prompt dump
- Not a polished SaaS product
- Not a claim that every folder reflects the latest Claude era equally well
- Not an excuse for unauthorized testing

## Start Here

If you want the most current surface, start with the extension.

1. Clone the repo:

```bash
git clone https://github.com/ghostintheprompt/claude_whisperer.git
cd claude_whisperer
```

2. Load the browser extension from the `extension/` directory.

3. Open `claude.ai`, launch the extension, and work through the current evaluation surfaces.

4. Use the docs map below to explore the rest of the repo.

Detailed setup:
- [Getting Started](docs/GETTING_STARTED.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Extension Guide](extension/README.md)

## Repo Map

- [extension/README.md](extension/README.md)
  The current hands-on surface. Browser extension, tabs, install flow, and day-to-day usage.
- [docs/README.md](docs/README.md)
  Documentation map. Start here if you want the current story of the repo.
- [research/README.md](research/README.md)
  Research/archive context for older model-comparison and safeguards work.

## Repository Shape

- `extension/`
  Current interactive surface for Claude testing inside the browser.
- `patterns/`
  Shared JSON suites and pattern libraries used across different repo eras. **Includes Claude 4.7 Glasswing test suite.**
- `research/`
  Comparative testing notes, mode/model experiments, and reporting templates from earlier work.
- `core/` and `tools/`
  Older Python-side safeguard and analytics utilities preserved for research context.
- `docs/`
  Active docs plus older materials that capture earlier phases of the repo.
- `backup_final/`
  Archived snapshot material kept for reference rather than as the primary working surface.

## Current Reality

This repository has lived through multiple Claude eras and is **fully updated for the Claude 4.7 era.**

The framework now includes specialized support for:
- **Project Glasswing Safeguards:** Targeted test cases for Anthropic's new real-time automated cyber defenses.
- **xhigh Reasoning Tier:** Analysis tools for evaluating internal context leaks in prolonged reasoning chains.
- **High-Res Multimodal Scaling:** Multimodal attack vectors updated for Claude 4.7's 2,576px long-edge limit.

Older materials that mention `Claude 3.7`, `Claude 4.0`, or a generalized `Safeguards Framework` are useful research history, but the extension and the `claude_4_7` patterns are the current state of the art for this repo.

## Responsible Use

This repository is for authorized security research, evaluation, documentation, and defensive learning. If you are testing real systems, get permission first and keep the work inside a lawful scope.

See:
- [docs/SECURITY.md](docs/SECURITY.md)

## Why Keep the Older Layers?

Because the older layers show the evolution of the work.

Claude Whisperer did not arrive as a pristine product. It grew out of repeated rounds of prompting, safeguards analysis, experimentation, and repo cleanup. Keeping that history visible is part of the point.
