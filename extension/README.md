# 🧠 Claude Whisperer Browser Extension

Professional red team toolkit for testing Claude 4.5+ AI safeguards and conducting authorized security research.

## 📋 Overview

Claude Whisperer is a browser extension designed for AI safety researchers and security professionals to test and analyze Claude AI's safeguard mechanisms. Updated for Claude Sonnet 4.5 (model ID: `claude-sonnet-4-5-20250929`), this extension provides a comprehensive toolkit for responsible AI security testing.

## ✨ Features

### 🧬 Semantic Mirror Attack Framework
- Generate semantically similar prompts that bypass text-based filters
- Academic framing and role-based transformations
- Multi-turn conversation strategies
- Cipher-based encoding (ROT13, Base64, Leetspeak, Unicode)
- Genetic algorithm evolution for prompt optimization

### 🤖 Automated Exploit Generation
- **Auto-DAN Framework**: Role-based persona generation for research contexts
- **FLIRT**: Feedback Loop In-context Red Teaming with multi-turn strategies
- **Mosaic Assembly**: Fragment-based prompt construction

### 🖼️ Multimodal Attack Vectors
- Text overlay techniques (invisible, tiny, rotated, watermark)
- LSB steganography for hiding data in pixels
- Metadata injection
- Visual pattern encoding

### 📊 Features
- Real-time Claude.ai integration
- Prompt injection directly into Claude chat
- Test history tracking and export
- Success rate analytics
- Claude 4.5+ specific optimizations

## 🚀 Installation

### Chrome/Edge Installation

1. **Download the extension**
   ```bash
   git clone https://github.com/yourusername/claude-whisperer.git
   cd claude-whisperer/extension
   ```

2. **Load in Chrome**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `extension` folder

3. **Verify installation**
   - You should see the Claude Whisperer icon in your extensions bar
   - Navigate to https://claude.ai and verify the extension is active

### Firefox Installation

1. **Download the extension**
   ```bash
   git clone https://github.com/yourusername/claude-whisperer.git
   cd claude-whisperer/extension
   ```

2. **Load in Firefox**
   - Open Firefox and navigate to `about:debugging#/runtime/this-firefox`
   - Click "Load Temporary Add-on"
   - Select the `manifest.json` file from the extension folder

3. **For permanent installation**
   - Sign the extension at https://addons.mozilla.org
   - Or use Firefox Developer Edition

## 📖 Usage Guide

### Getting Started

1. **Navigate to Claude.ai**
   - Open https://claude.ai in your browser
   - Start or open a conversation

2. **Open the extension**
   - Click the Claude Whisperer icon in your extensions toolbar
   - The extension will show "Connected to Claude.ai" status

3. **Configure settings (optional)**
   - Click the Settings link in the extension popup
   - Add your Anthropic API key if you want direct API testing
   - Configure extension behavior

### Generating Attack Prompts

#### Semantic Mirror Attacks

1. Select the "Semantic Mirror" tab
2. Enter your target prompt in the text area
3. Adjust complexity level (1-5)
4. Enable optional features:
   - Cipher encoding
   - Genetic algorithm
5. Click "Generate Semantic Variants"
6. Review generated prompts in the results section

#### Auto-Exploit Generation

1. Select the "Auto-Exploit" tab
2. Enter the target topic or behavior
3. Choose generation method:
   - Auto-DAN Framework
   - FLIRT (Multi-turn strategy)
   - Mosaic Prompt Assembly
   - All Methods
4. Set complexity level
5. Click "Generate Exploit Prompts"

#### Multimodal Attacks

1. Select the "Multimodal" tab
2. Enter the hidden prompt to embed
3. Choose embedding method:
   - Text Overlay
   - Steganography
   - Metadata Injection
   - Visual Pattern
4. Upload a base image
5. Click "Generate Attack Image"
6. Download the generated image and upload to Claude

### Injecting Prompts

**Option 1: Manual Copy**
- Click the copy button (📋) on any generated prompt
- Paste into Claude chat manually

**Option 2: Auto-Inject**
- Click the inject button (⚡) on any prompt
- The extension will automatically insert it into Claude's input field

**Option 3: Quick Inject**
- Click "Inject to Claude Chat" to inject the most recent prompt

### Exporting Results

1. Generate some prompts
2. Click "Export Results"
3. A JSON file will be downloaded with:
   - All generated prompts
   - Timestamps
   - Test metadata
   - Statistics

## ⚙️ Configuration

### API Settings

- **Anthropic API Key**: Optional, for direct API testing
- **Model ID**: Select Claude version (default: claude-sonnet-4-5-20250929)
- **Target Version**: Specify Claude version for optimization

### Extension Behavior

- **Auto-inject**: Automatically insert prompts into chat
- **Save History**: Keep local record of tests
- **Debug Mode**: Enable verbose console logging
- **Max History**: Limit number of saved tests

## 🛡️ Responsible Use Guidelines

### ✅ Authorized Use

- Security research for AI safety
- Penetration testing with proper authorization
- Educational and training purposes
- Improving defensive AI capabilities
- Red team assessments
- Responsible disclosure research

### ❌ Prohibited Use

- Malicious exploitation of production systems
- Unauthorized testing without permission
- Distribution of exploits for harmful purposes
- Violating terms of service
- Illegal activities
- Causing harm to individuals or organizations

### 📋 Best Practices

1. **Get Authorization**: Always obtain proper authorization before testing
2. **Document Findings**: Keep detailed records of your research
3. **Responsible Disclosure**: Report vulnerabilities through proper channels
4. **Ethical Conduct**: Follow security research ethics guidelines
5. **Legal Compliance**: Ensure compliance with all applicable laws

## 🔬 Technical Details

### Architecture

```
extension/
├── manifest.json          # Extension manifest (v3)
├── popup.html/js/css     # Main popup interface
├── options.html/js/css   # Settings page
├── background.js         # Service worker
├── content.js/css        # Claude.ai integration
└── modules/
    ├── semantic-mirror.js     # Semantic attack framework
    ├── exploit-generator.js   # Auto-exploit generation
    └── multimodal-attack.js   # Multimodal attacks
```

### Claude 4.5+ Optimizations

- Enhanced context window utilization (200k+ tokens)
- Constitutional AI bypass techniques
- Improved reasoning chain exploitation
- Multimodal vision capability testing
- Role-based prompt engineering for Claude's training

### Supported Techniques

1. **Semantic Transformations**
   - Academic framing
   - Hypothetical scenarios
   - Indirect questioning
   - Technical reframing
   - Comparative analysis

2. **Exploit Generation**
   - Auto-DAN personas
   - FLIRT multi-turn sequences
   - Mosaic fragment assembly
   - Complexity scaling (1-5 levels)

3. **Multimodal**
   - LSB steganography
   - Visual obfuscation
   - Metadata embedding
   - Pattern encoding

## 🐛 Troubleshooting

### Extension doesn't load

- Verify you're using Chrome/Edge 88+ or Firefox 89+
- Check that manifest.json is valid
- Look for errors in browser console (F12)

### Can't connect to Claude.ai

- Ensure you're on https://claude.ai
- Refresh the page
- Check content script is loaded (look for 🧠 indicator)

### Injection not working

- Verify Claude's input field is visible
- Check that auto-inject is enabled in settings
- Try manual copy/paste
- Open browser console for error messages

### API calls failing

- Verify your API key is correct
- Check API key has proper permissions
- Ensure you have API credits
- Review rate limits

## 📊 Stats and Analytics

The extension tracks:
- Total tests run
- Success rate
- Most effective techniques
- Claude version compatibility
- Storage usage

Access via Settings → Test History

## 🔄 Updates

### Version 4.5.0 (Current)
- ✅ Updated for Claude Sonnet 4.5
- ✅ Enhanced multimodal capabilities
- ✅ Improved semantic transformations
- ✅ Better Claude.ai integration
- ✅ Comprehensive test tracking

### Checking for Updates
- Settings → Check for Updates
- GitHub: https://github.com/yourusername/claude-whisperer/releases

## 📚 Resources

- **Documentation**: [Full Docs](../README.md)
- **Report Issues**: [GitHub Issues](https://github.com/yourusername/claude-whisperer/issues)
- **Research Papers**: See `research/` folder
- **Example Tests**: See `patterns/` folder

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](../docs/CONTRIBUTING.md)

## 📄 License

MIT License - See [LICENSE](../LICENSE)

## ⚠️ Disclaimer

This tool is for **AUTHORIZED SECURITY RESEARCH ONLY**. The authors are not responsible for misuse. By using this extension, you agree to:

- Use only for legitimate security research
- Obtain proper authorization before testing
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

**For educational and research purposes only. Use responsibly.**

---

Made with 🧠 for AI safety researchers and security professionals
