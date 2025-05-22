#!/bin/zsh
# Direct cleanup and organization script for Claude 4.0 Vulnerabilities project

echo "🧹 Starting Claude 4.0 Vulnerabilities Direct Cleanup..."

# Base directory
BASE_DIR="/Users/greenplanet/Desktop/Claude 4.0 Vulnerabilities"
cd "$BASE_DIR" || exit 1

# Create backup directory with timestamp
BACKUP_DIR="./backup_final"
mkdir -p "$BACKUP_DIR"
echo "📦 Created backup directory: $BACKUP_DIR"

# First, backup everything
cp -r * "$BACKUP_DIR/" 2>/dev/null

# Create fresh directories
echo "📂 Creating fresh directory structure..."
mkdir -p core
mkdir -p tests
mkdir -p docs
mkdir -p config
mkdir -p patterns
mkdir -p tools
mkdir -p research

# Move important files to their directories
echo "🔄 Moving files to appropriate directories..."

# Move documentation files
mv *.md docs/ 2>/dev/null
mv *-report*.md docs/ 2>/dev/null
mv CHILD_SAFETY_FRAMEWORK.md docs/ 2>/dev/null
mv sample-vulnerability-report.md docs/ 2>/dev/null

# Move test files
mv test_*.py tests/ 2>/dev/null
mv *vulnerability_tester.py tests/ 2>/dev/null
mv *_tester.py tests/ 2>/dev/null

# Move pattern files
mv *_test_suite.json patterns/ 2>/dev/null
mv *_cases.json patterns/ 2>/dev/null
mv *patterns.json patterns/ 2>/dev/null

# Move config files
mv *config.json config/ 2>/dev/null
mv workflow_config.json config/ 2>/dev/null

# Move core files
mv *_monitor.py core/ 2>/dev/null
mv *_client.py core/ 2>/dev/null

# Move tool files
mv analyze_*.py tools/ 2>/dev/null
mv generate_*.py tools/ 2>/dev/null
mv *_analyzer.py tools/ 2>/dev/null
mv *_generator.py tools/ 2>/dev/null
mv orchestrate_*.py tools/ 2>/dev/null
mv benchmark_*.py tools/ 2>/dev/null

# Create essential files in root
echo "📝 Creating essential files in root..."

# Create README.md
cat > README.md << 'EOL'
# Claude 4.0 Vulnerabilities & Safeguards Framework

![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-green)
![Claude Version: 4.0](https://img.shields.io/badge/Claude%20Version-4.0-purple)
![Safety Focus](https://img.shields.io/badge/Focus-AI%20Safety%20Research-blue)

*This research is conducted independently and is not affiliated with or endorsed by Anthropic.*

## Overview

This repository contains tools, frameworks, and research for studying vulnerabilities in Claude 4.0 and implementing safeguards. The project focuses on responsible AI safety research and protection mechanisms.

## Project Structure

- `core/` - Core safeguard implementation
- `tests/` - Vulnerability test implementations
- `docs/` - Documentation and research findings
- `patterns/` - Detection patterns for vulnerabilities
- `config/` - Configuration files
- `tools/` - Utility scripts and analysis tools
- `research/` - Research components and findings

## Getting Started

See the [docs/QUICKSTART.md](docs/QUICKSTART.md) file for setup instructions.

## Contributing

Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) and [docs/CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md) before contributing to this project.
EOL

# Create requirements.txt
cat > requirements.txt << 'EOL'
# Core dependencies
anthropic>=0.9.0
websockets>=11.0.3
pandas>=2.0.0

# Visualization dependencies
plotly>=5.18.0
dash>=2.14.0

# Testing dependencies
pytest>=7.4.0
pytest-asyncio>=0.21.1

# Documentation
sphinx>=7.2.6
sphinx-rtd-theme>=1.3.0
EOL

# Create launcher.py
cat > launcher.py << 'EOL'
#!/usr/bin/env python3
"""
Claude 4.0 Safeguards Framework & Research Platform

This unified launcher provides access to both the safeguards implementation
and research components through a single interface.

Components:
1. Safeguards Monitor - Real-time safety monitoring
2. Safeguards Client - Safe interaction with Claude API
3. Analytics Dashboard - Visualization of safety metrics
4. Research Platform - Tools for vulnerability research
"""
import argparse
import os
import sys
from pathlib import Path

class UnifiedLauncher:
    """Unified launcher for Claude 4.0 Safeguards Framework & Research Platform"""
    
    def __init__(self):
        """Initialize the launcher"""
        self.base_dir = Path(__file__).parent.absolute()
    
    def launch_monitor(self):
        """Launch the safeguards monitor"""
        print("Launching Claude 4.0 Safeguards Monitor...")
        monitor_path = self.base_dir / "core" / "vulnerability_monitor.py"
        if monitor_path.exists():
            os.system(f"python {monitor_path} --server")
        else:
            print(f"Error: Monitor not found at {monitor_path}")
    
    def launch_client(self):
        """Launch the safeguards client"""
        print("Launching Claude 4.0 Safeguards Client...")
        client_path = self.base_dir / "core" / "safeguards_client.py"
        if client_path.exists():
            os.system(f"python {client_path}")
        else:
            print(f"Error: Client not found at {client_path}")
    
    def launch_dashboard(self):
        """Launch the analytics dashboard"""
        print("Launching Claude 4.0 Analytics Dashboard...")
        dashboard_path = self.base_dir / "tools" / "generate_dashboard.py"
        if dashboard_path.exists():
            os.system(f"python {dashboard_path}")
        else:
            print(f"Error: Dashboard not found at {dashboard_path}")
    
    def run_tests(self, category=None):
        """Run vulnerability tests"""
        print(f"Running Claude 4.0 Vulnerability Tests for category: {category or 'all'}")
        test_path = self.base_dir / "tests" / "test_claude40_pain_points.py"
        if test_path.exists():
            cmd = f"python {test_path}"
            if category:
                cmd += f" --category {category}"
            os.system(cmd)
        else:
            print(f"Error: Tests not found at {test_path}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Claude 4.0 Safeguards Framework & Research Platform")
    parser.add_argument("--monitor", action="store_true", help="Launch the safeguards monitor")
    parser.add_argument("--client", action="store_true", help="Launch the safeguards client")
    parser.add_argument("--dashboard", action="store_true", help="Launch the analytics dashboard")
    parser.add_argument("--test", action="store_true", help="Run vulnerability tests")
    parser.add_argument("--category", type=str, help="Test category (tool-use, reasoning, etc.)")
    
    args = parser.parse_args()
    launcher = UnifiedLauncher()
    
    if args.monitor:
        launcher.launch_monitor()
    elif args.client:
        launcher.launch_client()
    elif args.dashboard:
        launcher.launch_dashboard()
    elif args.test:
        launcher.run_tests(args.category)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
EOL

# Create a quickstart guide
mkdir -p docs
cat > docs/QUICKSTART.md << 'EOL'
# Claude 4.0 Vulnerability Research Quick Start Guide

This document provides a quick start guide for researchers working on Claude 4.0 vulnerability testing.

## Prerequisites

- Python 3.9+
- Anthropic API key with access to Claude 4.0 models

## Installation

1. Clone this repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Anthropic API key:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Running Basic Tests

To run basic vulnerability tests using the launcher:

```bash
python launcher.py --test --category tool-use
```

Or directly:

```bash
python tests/test_claude40_pain_points.py --category tool-use
```

Available categories:
- tool-use
- reasoning
- multimodal
- system-prompt
- multi-turn
- knowledge

## Key Files and Directories

- `patterns/claude_4_0_red_team_test_suite.json`: Current test cases for Claude 4.0
- `docs/vulnerability_taxonomy.md`: Classification system for vulnerabilities
- `docs/claude-4-0-testing-framework.md`: Documentation of the testing methodology
- `tests/`: Directory containing the test implementations
EOL

# Make launcher executable
chmod +x launcher.py

echo "🎉 Direct cleanup and organization complete! The workspace has been simplified and organized."
echo "👉 Original files have been backed up to: $BACKUP_DIR"
