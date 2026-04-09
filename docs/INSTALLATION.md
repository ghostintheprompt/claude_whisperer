# Claude Whisperer Installation Guide

Claude Whisperer is easiest to use as a browser extension loaded from this repository.

## Clone the Repo

```bash
git clone https://github.com/ghostintheprompt/claude_whisperer.git
cd claude_whisperer
```

## Chrome and Edge

1. Open `chrome://extensions/` or `edge://extensions/`
2. Enable developer mode
3. Click `Load unpacked`
4. Select the `extension/` folder
5. Open `https://claude.ai`
6. Launch the extension from the toolbar

## Firefox

1. Open `about:debugging#/runtime/this-firefox`
2. Click `Load Temporary Add-on`
3. Select `extension/manifest.json`
4. Open `https://claude.ai`
5. Launch the extension from the toolbar

Note:
- Firefox temporary installs are best for development and testing
- permanent installation requires the usual Firefox signing path

## Optional Settings

Inside the extension settings page you can configure:
- Anthropic API key storage
- preferred Claude model ID
- local history behavior
- debug mode

The API key is optional. The extension can still be useful when working directly inside `claude.ai`.

## Sanity Check

Once installed:
- visit `claude.ai`
- open the extension
- confirm the status indicator recognizes the page
- try one of the tabs and generate a result

## If Installation Feels Off

Common causes:
- loading the repo root instead of the `extension/` directory
- using an older browser build
- expecting the old Python tooling to be the install path

For the current repo surface, the extension is the install path.
