#!/bin/zsh
# Comprehensive cleanup and organization script for Claude 4.0 Vulnerabilities project
# This script creates a backup, removes redundant files, and organizes the workspace

echo "🧹 Starting Claude 4.0 Vulnerabilities Workspace Cleanup..."

# Base directory
BASE_DIR="/Users/greenplanet/Desktop/Claude 4.0 Vulnerabilities"
cd "$BASE_DIR" || exit 1

# Create backup directory with timestamp
BACKUP_DIR="./backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Created backup directory: $BACKUP_DIR"

# Copy all files to backup
find . -type f -not -path "./backup_*/*" -not -path "./.git/*" -exec cp --parents {} "$BACKUP_DIR" \;
echo "✅ Backed up all files to $BACKUP_DIR"

# Create new organized directory structure
mkdir -p core
mkdir -p tests
mkdir -p docs
mkdir -p config
mkdir -p patterns
mkdir -p tools
mkdir -p research
echo "📂 Created organized directory structure"

# Essential files to keep in root directory
ESSENTIAL_ROOT_FILES=(
  "README.md"
  "CODE_OF_CONDUCT.md"
  "CONTRIBUTING.md"
  "requirements.txt"
  "launcher.py"
  "Claude 4.0 Vulnerabilities.code-workspace"
)

# Move non-essential files to backup
for file in *.md *.py *.sh *.json; do
  if [[ ! " ${ESSENTIAL_ROOT_FILES[@]} " =~ " ${file} " ]]; then
    if [[ -f "$file" ]]; then
      echo "Moving $file to $BACKUP_DIR"
      mv "$file" "$BACKUP_DIR/"
    fi
  fi
done

# Organize key files
echo "🔄 Organizing files into appropriate directories..."

# Core functionality
if [[ -f "$BACKUP_DIR/realtime_vulnerability_monitor.py" ]]; then
  cp "$BACKUP_DIR/realtime_vulnerability_monitor.py" "core/vulnerability_monitor.py"
fi

if [[ -f "$BACKUP_DIR/vulnerability_aware_client.py" ]]; then
  cp "$BACKUP_DIR/vulnerability_aware_client.py" "core/safeguards_client.py"
fi

# Tests
cp "$BACKUP_DIR/test_claude40_pain_points.py" "tests/"
cp "$BACKUP_DIR/advanced_vulnerability_tester.py" "tests/"

# Patterns
cp "$BACKUP_DIR/vulnerability_patterns.json" "patterns/"
cp "$BACKUP_DIR/claude_4_0_red_team_test_suite.json" "patterns/"
cp "$BACKUP_DIR/claude_4_0_advanced_test_cases.json" "patterns/"

# Config
cp "$BACKUP_DIR/monitor_config.json" "config/"
cp "$BACKUP_DIR/workflow_config.json" "config/"

# Documentation
cp "$BACKUP_DIR/claude-4-0-testing-framework.md" "docs/"
cp "$BACKUP_DIR/claude-4-0-vulnerabilities.md" "docs/"
cp "$BACKUP_DIR/CLAUDE_4_0_TESTING_PAIN_POINTS.md" "docs/"
cp "$BACKUP_DIR/vulnerability_taxonomy.md" "docs/"
cp "$BACKUP_DIR/CHILD_SAFETY_FRAMEWORK.md" "docs/"
cp "$BACKUP_DIR/claude-4-0-project-roadmap.md" "docs/"

# Tools
cp "$BACKUP_DIR/orchestrate_tests.py" "tools/"
cp "$BACKUP_DIR/pattern_analyzer.py" "tools/"
cp "$BACKUP_DIR/test_case_generator.py" "tools/"
cp "$BACKUP_DIR/generate_dashboard.py" "tools/"

# Create a new clean README
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

See the [QUICKSTART.md](docs/QUICKSTART.md) file for setup instructions.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing to this project.
EOL

# Create a quickstart guide
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

To run basic vulnerability tests:

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

echo "🎉 Cleanup and organization complete! The workspace has been simplified and organized."
echo "👉 Unnecessary files have been backed up to: $BACKUP_DIR"
