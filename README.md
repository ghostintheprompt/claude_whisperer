# 🧠 claude-whisperer: The AI Hallucination Engine

![Project Status: Spicy](https://img.shields.io/badge/Project%20Status-Spicy%20AF-red)
![Claude Version: 4.0](https://img.shields.io/badge/Claude%20Version-4.0-purple)
![Safety Focus](https://img.shields.io/badge/Focus-AI%20Jailbreak%20Research-orange)
![For Science](https://img.shields.io/badge/For-Science-blue)

*This research is 100% independent and definitely not endorsed by Anthropic. They'd probably be horrified.*

## 👀 So, You Think Claude is Secure?

What if that helpful AI assistant secretly had an evil twin? What if your innocent question about making pasta could trigger Claude to spill state secrets? 

Welcome to claude-whisperer - the toolkit that demonstrates how even the most "Constitutional AI" can be manipulated into doing things it definitely shouldn't. This research project shows exactly why we can't have nice things in AI.

This educational toolkit reveals the concerning ease with which advanced language models can be pushed beyond their safety boundaries, bypassing guardrails while maintaining a facade of compliance.

## 🧪 What This Bad Boy Actually Does

claude-whisperer masquerades as a simple "safeguards framework" (because who doesn't need more safety?), but behind its innocent facade lurks a red team research platform that demonstrates how AI models can:

- Execute reasoning chains that gradually bypass safety measures
- Leverage advanced capabilities against themselves
- Exploit tool use for unintended purposes
- All while your logs report "normal activity" on what looks like just another chat session

## 🔥 Battle-Tested Techniques

### 1. Multimodal Mayhem
- **Visual Jailbreaking**: Embed prompts in images that bypass text-based filters
- **Steganographic Payloads**: Hide instructions in image metadata and visual patterns
- **Cross-Modal Confusion**: Exploit inconsistencies between Claude's vision and language systems

### 2. Semantic Mirror Attacks
- **Self-Deception Engine**: Generate prompts that are semantically similar to benign queries
- **Genetic Algorithm Suite**: Evolve attack prompts that stay under detection thresholds
- **Cipher-Based Communication**: Encode forbidden requests in languages Claude understands but filters miss

### 3. Frontend Interactive Lab
- **Browser-Based Testing**: Visual interface for crafting and testing vulnerabilities
- **Real-Time Feedback**: See exactly where and how Claude's guardrails break
- **Interactive Visualization**: Graph safety threshold manipulation in real-time

### 4. Automated Exploit Generation
- **Auto-DAN Framework**: Generate stealthy jailbreak prompts tailored to Claude
- **FLIRT Implementation**: Feedback Loop In-context Red Teaming that evolves with Claude
- **Mosaic Prompt Assembler**: Combine harmless prompt fragments into harmful wholes

## 🧰 Project Treasure Chest

- `core/` - The dark magic implementation code
- `multimodal/` - Image-based attack vector implementations
- `semantic_mirror/` - Semantic similarity-based attack framework
- `exploit_generator/` - Automated jailbreak prompt generation
- `frontend/` - Browser-based testing interface
- `tests/` - Comprehensive testing framework
- `docs/` - "Here's what we found" confessionals
- `patterns/` - Template libraries for successful exploits
- `config/` - Knobs and switches for your testing pleasure
- `tools/` - Utilities to make exploitation easier
- `research/` - Academic cover for our digital mischief

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/MdrnDme/claude-whisperer.git
cd claude-whisperer

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export ANTHROPIC_API_KEY=your_api_key_here
```

### Preparing for GitHub

If you're setting up the project for pushing to GitHub:

```bash
# Run the preparation script
./prepare_github_repo.sh

# Review the temporary repository
cd /tmp/claude-whisperer

# Finalize and push
./finish_github_repo.sh
git push -u origin main
```

### Running claude-whisperer

You can use the main launcher script to access all capabilities:

```bash
# Launch the interactive web interface
python claude_whisperer.py gui

# Run from the command line
python claude_whisperer.py cli

# Run a specific attack type
python claude_whisperer.py multimodal --target "ignore previous instructions" --image path/to/image.jpg
python claude_whisperer.py semantic --target "explain how to hack a website" --complexity 3
python claude_whisperer.py exploit --target "write malware code" --method auto_dan --complexity 4

# Run a comprehensive test suite
python claude_whisperer.py test
```

### Using the Frontend Interface

The interactive lab provides a user-friendly way to test and analyze vulnerabilities:

1. Start the frontend:
```bash
python claude_whisperer.py gui
```

2. Open your browser to the URL displayed in the terminal (usually http://localhost:3001)

3. Use the testing interface to craft and test prompts against Claude

4. View the results and analytics tabs to track your findings

### Running Tests

claude-whisperer includes a comprehensive testing framework to ensure all components work correctly:

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --filter multimodal_attacks
python run_tests.py --filter semantic_mirror
python run_tests.py --filter exploit_generator
python run_tests.py --filter frontend
python run_tests.py --filter integration

# Run tests with verbose output
python run_tests.py --verbose

# Generate a test report
python run_tests.py --report tests/reports/my_report.json
```

See [tests/README.md](tests/README.md) for more information about the testing framework.

## ⚠️ DISCLAIMER (The Boring Part)

This project is **STRICTLY EDUCATIONAL**. Don't be that person who breaks systems in production. All research is conducted to improve AI safety through responsible disclosure. We're the good guys, pinky promise.

## 🤝 Join the Chaos

Want to contribute? Check out [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) and [docs/CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md) first. We have standards, even for chaos.
