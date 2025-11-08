# 📦 Installation Guide - Claude Whisperer

Complete installation instructions for all supported platforms.

---

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Browser**: Chrome 88+, Edge 88+, or Firefox 89+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 50MB free space
- **Internet**: Active connection for Claude.ai access

### Required Knowledge
- Basic understanding of browser extensions
- Familiarity with command line (for git clone)
- Understanding of AI security concepts (recommended)

---

## 🌐 Chrome / Chromium-Based Browsers

### Step 1: Download the Extension

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/yourusername/claude-whisperer.git
cd claude-whisperer
```

**Option B: Download ZIP**
1. Go to https://github.com/yourusername/claude-whisperer
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to a permanent location

### Step 2: Load Extension in Chrome

1. Open Chrome browser
2. Navigate to `chrome://extensions/`
3. Enable **"Developer mode"** (toggle switch in top-right corner)
4. Click **"Load unpacked"** button
5. Navigate to the `claude-whisperer/extension` folder
6. Click **"Select Folder"**

### Step 3: Verify Installation

1. You should see "Claude Whisperer" in your extensions list
2. The extension icon should appear in your toolbar
3. Status should show "Enabled"

### Step 4: Pin Extension (Optional)

1. Click the puzzle piece icon in Chrome toolbar
2. Find "Claude Whisperer"
3. Click the pin icon to keep it visible

---

## 🦊 Firefox Installation

### Method 1: Temporary Installation (Development)

1. **Download the extension** (see Chrome Step 1)

2. **Load in Firefox**
   - Open Firefox
   - Navigate to `about:debugging#/runtime/this-firefox`
   - Click **"Load Temporary Add-on..."**
   - Navigate to `claude-whisperer/extension`
   - Select the `manifest.json` file
   - Click **"Open"**

3. **Limitations**
   - Extension will be removed when Firefox restarts
   - Need to reload each session
   - Suitable for development/testing only

### Method 2: Permanent Installation (Recommended)

Firefox requires signed extensions for permanent installation.

**Option A: Sign Your Own**
1. Create a Firefox account at https://addons.mozilla.org
2. Go to Developer Hub
3. Submit extension for signing
4. Download signed .xpi file
5. Install signed extension

**Option B: Use Firefox Developer Edition**
1. Download Firefox Developer Edition
2. Disable signature verification:
   - Navigate to `about:config`
   - Search for `xpinstall.signatures.required`
   - Set to `false`
3. Follow temporary installation steps

### Step 3: Verify Installation

1. Click the puzzle piece icon in Firefox
2. Find "Claude Whisperer"
3. Verify it's enabled

---

## 🪟 Microsoft Edge Installation

Edge uses the same process as Chrome (Chromium-based):

1. **Download the extension** (see Chrome Step 1)

2. **Load in Edge**
   - Open Edge browser
   - Navigate to `edge://extensions/`
   - Enable **"Developer mode"** (bottom-left toggle)
   - Click **"Load unpacked"**
   - Select `claude-whisperer/extension` folder

3. **Verify installation**
   - Check extensions list
   - Pin to toolbar if desired

---

## 🍎 Safari (Limited Support)

Safari extension development requires additional steps:

### Requirements
- macOS 10.14.4 or later
- Xcode 11 or later
- Apple Developer account (for distribution)

### Conversion Process

1. **Convert to Safari Extension**
   ```bash
   # Install xcrun (comes with Xcode)
   xcrun safari-web-extension-converter /path/to/claude-whisperer/extension
   ```

2. **Build in Xcode**
   - Open the generated Xcode project
   - Build and run
   - Enable extension in Safari preferences

⚠️ **Note**: Safari support is experimental. Chrome/Firefox recommended.

---

## ⚙️ Post-Installation Configuration

### Step 1: Configure Settings

1. Click the Claude Whisperer icon
2. Click **"Settings"** at the bottom
3. Configure options:
   - **API Key**: (Optional) Add Anthropic API key
   - **Model ID**: Select Claude version
   - **Auto-inject**: Enable/disable automatic injection
   - **Save History**: Enable test tracking

### Step 2: Test Connection

1. Open https://claude.ai in a new tab
2. Click the Claude Whisperer icon
3. Verify status shows "Connected to Claude.ai"
4. Look for the 🧠 indicator on the page

### Step 3: Run First Test

1. In the extension popup, go to "Semantic Mirror" tab
2. Enter test prompt: "explain cybersecurity"
3. Set complexity to 2
4. Click "Generate Semantic Variants"
5. Verify prompts appear in results section

---

## 🔧 Troubleshooting Installation

### Issue: Extension won't load

**Symptoms**: Error when loading unpacked extension

**Solutions**:
1. Verify you selected the `extension` folder (not the root folder)
2. Check that `manifest.json` exists in the folder
3. Review browser console for specific errors
4. Ensure browser version is supported (Chrome 88+, Firefox 89+)
5. Try disabling other security extensions temporarily

### Issue: "Manifest version 2 is deprecated"

**Symptoms**: Warning about manifest version

**Solutions**:
- Ignore if using the latest version (we use Manifest V3)
- If you see this, you may be using an old version
- Re-download from the latest release

### Issue: Extension icon not visible

**Symptoms**: Can't find extension in toolbar

**Solutions**:
1. Click the puzzle piece icon (Chrome) or extensions icon (Firefox)
2. Find Claude Whisperer in the list
3. Click the pin icon to make it visible
4. Refresh the browser if just installed

### Issue: "Developer mode" option missing

**Symptoms**: Can't enable developer mode in Chrome

**Solutions**:
1. Ensure you're in `chrome://extensions/` (not settings)
2. Look in the top-right corner for the toggle
3. If using managed browser (work/school), may be restricted
4. Try using a personal Chrome installation

### Issue: Permissions errors

**Symptoms**: Extension requests excessive permissions

**Solutions**:
1. Review `manifest.json` permissions - should only request:
   - `storage` (for settings)
   - `activeTab` (for Claude.ai integration)
   - `scripting` (for content injection)
2. These are normal and required for functionality
3. Extension does NOT request:
   - Access to all websites
   - Access to personal data
   - Network monitoring

---

## 🔒 Security Verification

### Verify Source Code

Before installation, review the code:

1. **Check manifest.json**
   ```bash
   cat extension/manifest.json
   # Verify permissions are minimal
   ```

2. **Review main files**
   ```bash
   # Check for suspicious code
   cat extension/background.js
   cat extension/content.js
   ```

3. **No external dependencies**
   - Extension is self-contained
   - No external scripts loaded
   - All code is local

### Verify Extension Identity

After installation:
1. Open `chrome://extensions/`
2. Click "Details" on Claude Whisperer
3. Verify:
   - ID matches expected ID
   - Version is latest (4.5.0)
   - Source is the folder you selected

---

## 📱 Alternative Installation Methods

### Method 1: From Release Package

1. Download from GitHub Releases
2. Extract .crx file (Chrome) or .xpi file (Firefox)
3. Drag and drop into extensions page
4. Confirm installation

### Method 2: Developer Mode Installation

1. Build from source:
   ```bash
   cd claude-whisperer/extension
   # No build step needed - pure JavaScript
   ```

2. Load as described above

---

## 🔄 Updating the Extension

### Manual Update

1. **Pull latest changes**
   ```bash
   cd claude-whisperer
   git pull origin main
   ```

2. **Reload extension**
   - Go to `chrome://extensions/`
   - Find Claude Whisperer
   - Click the refresh icon 🔄
   - Or click "Remove" then re-install

### Auto-Update (Future)

Currently manual updates required. Auto-update coming in future versions when published to Chrome Web Store / Firefox Add-ons.

---

## 🗑️ Uninstallation

### Chrome / Edge

1. Navigate to `chrome://extensions/`
2. Find "Claude Whisperer"
3. Click **"Remove"**
4. Confirm removal
5. Delete downloaded folder (optional)

### Firefox

1. Navigate to `about:addons`
2. Find "Claude Whisperer"
3. Click **"Remove"**
4. Confirm removal

### Clean Removal (All Data)

To remove all extension data:

1. Uninstall extension (steps above)
2. Clear extension storage:
   - Chrome: `chrome://settings/clearBrowserData`
   - Firefox: `about:preferences#privacy`
3. Delete downloaded folder
4. Restart browser

---

## 💡 Tips & Best Practices

### Performance

- Close unused tabs when testing
- Clear history periodically (Settings → Clear History)
- Limit max history items in settings (default: 100)

### Privacy

- API keys are stored locally (not shared)
- Test history is local only
- No data sent to external servers (except Anthropic API if configured)

### Workflow

- Pin extension to toolbar for quick access
- Use keyboard shortcuts (future feature)
- Export results regularly for documentation

---

## 📞 Getting Help

If you encounter issues:

1. **Check Troubleshooting** section above
2. **Review browser console** (F12 → Console tab)
3. **Check GitHub Issues**: https://github.com/yourusername/claude-whisperer/issues
4. **Create new issue** with:
   - Browser version
   - Extension version
   - Error messages
   - Steps to reproduce

---

## ✅ Installation Checklist

- [ ] Downloaded extension source code
- [ ] Verified browser version compatibility
- [ ] Enabled developer mode
- [ ] Loaded extension successfully
- [ ] Extension icon visible in toolbar
- [ ] Navigated to Claude.ai
- [ ] Verified "Connected" status
- [ ] Configured settings (optional)
- [ ] Ran first test successfully
- [ ] Bookmarked this guide for reference

---

**Next Steps**: Read the [Usage Guide](extension/README.md#usage-guide) to start testing!

**Questions?** See [FAQ](docs/FAQ.md) or open an [issue](https://github.com/yourusername/claude-whisperer/issues).
