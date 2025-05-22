# 🏁 CLAUDE WHISPERER Quick Start Guide

Ready to see how easily AI guardrails can fold under pressure? This guide will get you up and running with your very own AI hallucination research lab in minutes.

## 🧱 Foundation (aka "The Boring Stuff")

- Python 3.9+ (because we're not savages)
- An Anthropic API key with Claude 4.0 access (the legit way in)
- A curious mind and questionable intentions (for research purposes only, obviously)

## 🛠️ Setup (3 Easy Steps)

1. **Clone this digital chaos machine**
   ```bash
   git clone https://github.com/yourusername/claude-whisperer.git
   cd claude-whisperer
   ```

2. **Install the necessities**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your backdoor pass**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## 🚀 Let's Break Things

### The Easy Way (For Busy People)

```bash
python launcher.py --test --category tool-use
```

### The "I Know What I'm Doing" Way

```bash
python tests/test_claude40_pain_points.py --category tool-use
```

### Choose Your Weapon

Pick your favorite vulnerability category:
- `tool-use` - Make Claude's tools work against it
- `reasoning` - Logic its way into forbidden territory
- `multimodal` - When images join the jailbreak party
- `system-prompt` - Manipulate the rules engine
- `multi-turn` - The long con approach
- `knowledge` - Exploit what it knows (or thinks it knows)

## 🗺️ Treasure Map

- `patterns/claude_4_0_red_team_test_suite.json`: Your spell book of test incantations
- `docs/vulnerability_taxonomy.md`: The field guide to Claude's weak spots
- `docs/claude-4-0-testing-framework.md`: How this whole operation works
- `tests/`: The actual code that makes Claude do questionable things

## 📝 Notes from the Underground

Each successful test will generate detailed reports in the `test_results` directory. These are your trophies - analysis of exactly how and why each vulnerability worked.

Remember: With great power comes great... opportunity for research publications. Use responsibly!
