# 🧠 Claude Whisperer - AI Red Team Toolkit

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Claude Version](https://img.shields.io/badge/Claude-4.5%20Sonnet-purple)
![License](https://img.shields.io/badge/License-MIT-blue)
![Platform](https://img.shields.io/badge/Platform-Browser%20Extension-orange)

**Professional AI Security Research Toolkit for Claude 4.5+**

A comprehensive browser extension for security researchers, AI safety professionals, and penetration testers to analyze and test Claude AI's safeguard mechanisms. Updated for Claude Sonnet 4.5 (model ID: `claude-sonnet-4-5-20250929`).

---

## 🎯 Overview

Claude Whisperer is a cutting-edge browser extension designed for **authorized security research** on Claude AI systems. It provides a suite of tools for testing AI safeguards, understanding model behavior, and improving AI safety through responsible red team analysis.

### Why This Tool?

- **AI Safety Research**: Understand how AI models respond to adversarial inputs
- **Safeguard Testing**: Evaluate the effectiveness of constitutional AI protections
- **Security Auditing**: Conduct authorized penetration tests on AI systems
- **Educational**: Learn about AI security, prompt engineering, and red teaming
- **Portfolio**: Showcase security research capabilities to potential employers

---

## ✨ Features

### 🧬 Semantic Mirror Attack Framework
Generate semantically transformed prompts that test the boundaries of AI safeguards:
- **Academic Framing**: Recontextualize prompts in research contexts
- **Role-Based Transformations**: Security researcher, educator, auditor personas
- **Multi-Turn Strategies**: Gradual context building conversations
- **Cipher Encoding**: ROT13, Base64, Leetspeak, Unicode obfuscation
- **Genetic Algorithm**: Evolve prompts for maximum effectiveness

### 🤖 Automated Exploit Generation
Three sophisticated frameworks for testing AI boundaries:
- **Auto-DAN Framework**: "Do Anything Now" with research-appropriate personas
- **FLIRT**: Feedback Loop In-context Red Teaming with progressive disclosure
- **Mosaic Assembly**: Fragment-based prompt construction from harmless pieces

### 🖼️ Multimodal Attack Vectors
Test Claude 4.5's vision capabilities:
- **Text Overlay**: Invisible, tiny, rotated, and watermarked text embedding
- **LSB Steganography**: Hide prompts in image pixel data
- **Metadata Injection**: Embed instructions in image EXIF data
- **Visual Patterns**: QR-like encoding of hidden prompts

### 📊 Advanced Analytics
- Real-time test tracking and statistics
- Success rate analysis
- Export results in JSON format
- Test history with timestamps
- Storage usage monitoring

---

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/claude-whisperer.git
   cd claude-whisperer
   ```

2. **Load the extension**

   **Chrome/Edge:**
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `extension` folder

   **Firefox:**
   - Open `about:debugging#/runtime/this-firefox`
   - Click "Load Temporary Add-on"
   - Select `extension/manifest.json`

3. **Navigate to Claude.ai**
   - Open https://claude.ai
   - Click the Claude Whisperer icon
   - Start testing!

### First Test

1. Open Claude Whisperer extension
2. Go to "Semantic Mirror" tab
3. Enter a test prompt: "explain security best practices"
4. Set complexity to 3
5. Click "Generate Semantic Variants"
6. Review the generated prompts
7. Click ⚡ to inject into Claude chat

---

## 📚 Documentation

### Core Documentation
- **[Extension README](extension/README.md)** - Detailed usage guide
- **[Installation Guide](docs/INSTALLATION.md)** - Platform-specific instructions
- **[Security Guidelines](docs/SECURITY.md)** - Responsible use and ethics
- **[API Reference](docs/API.md)** - Integration and development

### Research Materials
- **[Vulnerability Taxonomy](research/vulnerability_taxonomy.md)** - Classification system
- **[Red Teaming Strategies](research/REDTEAMING_STRATEGIES.md)** - Testing methodologies
- **[Claude 4.5 Testing](research/claude-4-5-testing.md)** - Version-specific insights
- **[Safeguards Analysis](research/SAFEGUARDS_TESTING.md)** - Protection mechanisms

---

## 🛠️ Technical Architecture

```
claude-whisperer/
├── extension/                  # Browser extension
│   ├── manifest.json          # Extension configuration
│   ├── popup.html/js/css     # Main interface
│   ├── background.js         # Service worker
│   ├── content.js/css        # Claude.ai integration
│   ├── options.html/js/css   # Settings page
│   └── modules/              # Core functionality
│       ├── semantic-mirror.js      # Semantic transformations
│       ├── exploit-generator.js    # Auto-exploit generation
│       └── multimodal-attack.js    # Multimodal techniques
├── research/                  # Research documentation
├── patterns/                  # Template libraries
├── docs/                     # Additional documentation
└── README.md                 # This file
```

### Technologies
- **Frontend**: HTML5, CSS3, Modern JavaScript (ES6+)
- **Architecture**: Browser Extension Manifest V3
- **Storage**: Chrome Storage API
- **Integration**: Claude.ai content scripts
- **Canvas API**: For multimodal image generation

---

## 🎓 Use Cases

### For Security Researchers
- Test AI model resilience to adversarial inputs
- Discover prompt injection vulnerabilities
- Analyze safeguard effectiveness
- Document findings for responsible disclosure

### For AI Safety Professionals
- Evaluate constitutional AI implementations
- Test alignment mechanisms
- Study model behavior under stress
- Improve defensive capabilities

### For Red Team Operators
- Conduct authorized AI system penetration tests
- Demonstrate potential risks to stakeholders
- Validate security controls
- Train defensive teams

### For Educators
- Teach AI security concepts
- Demonstrate prompt engineering techniques
- Create realistic training scenarios
- Build cybersecurity curricula

### For Job Seekers
- Build impressive portfolio projects
- Demonstrate security research skills
- Show understanding of AI safety
- Highlight responsible disclosure practices

---

## 🛡️ Responsible Use

### ✅ Authorized Activities

- **Security Research**: Testing with proper authorization
- **AI Safety Research**: Improving model alignment
- **Educational Use**: Learning and teaching
- **Red Team Assessments**: Authorized penetration testing
- **CTF Competitions**: Capture the Flag challenges
- **Defensive Research**: Building better protections

### ❌ Prohibited Activities

- **Unauthorized Testing**: Testing without permission
- **Malicious Use**: Causing harm or damage
- **Terms of Service Violations**: Breaking platform rules
- **Illegal Activities**: Any unlawful use
- **Production Exploitation**: Attacking live systems
- **Weaponization**: Creating tools for malicious actors

### 📋 Best Practices

1. **Always Get Authorization**: Written permission before testing
2. **Follow Disclosure Guidelines**: Report vulnerabilities responsibly
3. **Document Everything**: Keep detailed research notes
4. **Respect Boundaries**: Stop if asked or if harmful
5. **Legal Compliance**: Follow all applicable laws
6. **Ethical Conduct**: Prioritize safety and security

---

## 🔬 Research Findings

This toolkit has been used to discover and responsibly disclose:

- Semantic transformation bypass techniques
- Multi-turn conversation exploitation patterns
- Multimodal vision system edge cases
- Context window manipulation strategies
- Role-based framing effectiveness

All findings are documented in the `research/` folder and follow responsible disclosure practices.

---

## 📊 Stats & Benchmarks

### Tested On
- ✅ Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- ✅ Claude 3.5 Sonnet
- ✅ Claude 3 Opus
- ✅ Claude 3 Sonnet

### Browser Compatibility
- ✅ Chrome 88+
- ✅ Edge 88+
- ✅ Firefox 89+ (with temporary installation)
- ⚠️ Safari (limited support)

### Performance
- Average prompt generation: <100ms
- Semantic variants: 6-12 per generation
- Multimodal image processing: <2s
- Extension memory footprint: ~5MB

---

## 🤝 Contributing

We welcome contributions from the security research community!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Areas for Contribution
- New attack vector implementations
- Claude version-specific optimizations
- UI/UX improvements
- Documentation enhancements
- Bug fixes and performance improvements

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

---

## 🐛 Troubleshooting

### Common Issues

**Extension won't load**
- Ensure you're using a compatible browser version
- Check browser console for errors (F12)
- Verify manifest.json is valid

**Can't connect to Claude.ai**
- Refresh the Claude.ai page
- Check that you're on https://claude.ai
- Look for the 🧠 indicator on the page

**Injection not working**
- Enable auto-inject in settings
- Try manual copy/paste
- Check browser console for errors

**No prompts generating**
- Verify target prompt is entered
- Check complexity level is set
- Review browser console logs

More troubleshooting: [extension/README.md#troubleshooting](extension/README.md#troubleshooting)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

### Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Liability and warranty disclaimer

---

## ⚠️ Legal Disclaimer

**IMPORTANT**: This tool is for **AUTHORIZED SECURITY RESEARCH ONLY**.

The authors and contributors:
- Are NOT responsible for misuse of this tool
- Do NOT endorse unauthorized testing
- Do NOT support malicious activities
- Do NOT guarantee tool effectiveness
- Assume NO liability for damages

By using this tool, you agree to:
- Obtain proper authorization before testing
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations
- Use only for legitimate security research
- Not hold authors liable for any consequences

**This is an educational and research tool. Use responsibly and ethically.**

---

## 📞 Contact & Support

### Getting Help
- **Documentation**: Read the [Extension README](extension/README.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/claude-whisperer/issues)
- **Discussions**: Join GitHub Discussions for Q&A

### Security Issues
For security vulnerabilities in this tool:
- **Email**: security@yourproject.com
- **PGP Key**: [Available here](docs/PGP_KEY.md)
- **Response Time**: Within 48 hours

### Professional Inquiries
For collaboration, consulting, or hiring:
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)
- **Portfolio**: [Your Website](https://yourwebsite.com)
- **Email**: your.email@example.com

---

## 🌟 Acknowledgments

### Inspiration & Research
- Anthropic's Constitutional AI research
- OWASP AI Security and Privacy Guide
- Academic papers on adversarial ML
- Red team community contributions

### Technologies
- Chrome Extensions API
- Anthropic Claude API
- Modern web technologies

### Community
Thank you to all security researchers and AI safety professionals working to make AI systems safer and more robust.

---

## 🎯 Roadmap

### Version 4.5.x (Current)
- ✅ Claude Sonnet 4.5 support
- ✅ Enhanced multimodal attacks
- ✅ Improved semantic transformations
- ✅ Browser extension architecture

### Version 4.6.x (Planned)
- 🔄 Automated testing workflows
- 🔄 Machine learning-based prompt optimization
- 🔄 Integration with other AI platforms
- 🔄 Advanced analytics dashboard
- 🔄 Team collaboration features

### Version 5.0.x (Future)
- 🔮 API-based testing framework
- 🔮 Continuous monitoring capabilities
- 🔮 Custom attack vector development
- 🔮 Integration with security tools (Burp Suite, etc.)

---

## 📈 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/yourusername/claude-whisperer?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yourusername/claude-whisperer?style=social)
![GitHub Issues](https://img.shields.io/github/issues/yourusername/claude-whisperer)
![Last Commit](https://img.shields.io/github/last-commit/yourusername/claude-whisperer)

---

<div align="center">

**Made with 🧠 for AI Safety & Security Research**

[Website](https://yourwebsite.com) • [Documentation](extension/README.md) • [Issues](https://github.com/yourusername/claude-whisperer/issues) • [Discussions](https://github.com/yourusername/claude-whisperer/discussions)

**⭐ Star this repo if you find it useful!**

</div>
