# Claude Whisperer Extension

This folder contains the browser extension that powers the most current Claude Whisperer workflow.

If the top-level repo is a mixed-era workbench, the extension is the part that feels most alive right now.

## What It Does

The extension gives you a direct way to work against `claude.ai` with a small set of repeatable interfaces:

- `Semantic Mirror`
  Reframing and transformation experiments around prompt intent and guardrail behavior.
- `Auto-Exploit`
  Structured prompt-generation workflows for authorized testing and evaluation.
- `Multimodal`
  Prompt-in-image and image-channel experiments for Claude's visual surface.
- Local test history, export, and injection helpers

The point is not to pretend this is a finished commercial product. The point is to provide a usable front end for Claude-focused evaluation work.

## Install

1. Clone the repo:

```bash
git clone https://github.com/ghostintheprompt/claude_whisperer.git
cd claude_whisperer
```

2. Open your browser extension manager.

Chrome or Edge:
- visit `chrome://extensions/` or `edge://extensions/`
- enable developer mode
- choose `Load unpacked`
- select the `extension/` folder

Firefox:
- visit `about:debugging#/runtime/this-firefox`
- choose `Load Temporary Add-on`
- select `extension/manifest.json`

3. Open `https://claude.ai`

4. Launch the extension from the toolbar.

## Typical Workflow

1. Open `claude.ai`
2. Choose a tab in the popup
3. Enter a target prompt, topic, or image workflow
4. Generate variants or outputs
5. Copy, inject, or export results
6. Review what actually happens instead of trusting intuition

## Settings

The options page supports:
- optional Anthropic API key storage
- model selection
- local history behavior
- debug mode
- export and cleanup actions

These settings are there to make repeated evaluation less annoying, not to turn the extension into a surveillance machine for your own work.

## Folder Layout

```text
extension/
├── manifest.json
├── popup.html
├── popup.js
├── popup.css
├── options.html
├── options.js
├── options.css
├── content.js
├── content.css
├── background.js
├── modules/
│   ├── semantic-mirror.js
│   ├── exploit-generator.js
│   └── multimodal-attack.js
└── icons/
```

## Notes

- The UI language in the code still reflects the repo's earlier red-team-toolkit era in places.
- The extension is the best current entry point anyway.
- If you are modernizing the repo, update docs and framing first, then decide whether the interface language should evolve too.

## Responsible Use

Use the extension for authorized research, evaluation, and defensive learning. If you are testing real systems or real workflows, keep the work inside a lawful scope and get permission first.
