ifi#!/bin/zsh
# Complete cleanup and organization script for Claude 4.0 Vulnerabilities project
# This script removes redundant files and organizes the workspace

echo "🧹 Starting Claude 4.0 Vulnerabilities Workspace Complete Cleanup..."

# Base directory
BASE_DIR="/Users/greenplanet/Desktop/Claude 4.0 Vulnerabilities"
cd "$BASE_DIR" || exit 1

# Create backup directory with timestamp
BACKUP_DIR="./backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Created backup directory: $BACKUP_DIR"

# Backup everything first
echo "📂 Backing up all files..."
find . -maxdepth 1 -type f -not -path "*/\.*" -not -name "organize_claude40_complete.sh" -exec cp {} "$BACKUP_DIR/" \;

# Create clean directory structure
mkdir -p core
mkdir -p tests
mkdir -p docs
mkdir -p config
mkdir -p patterns
mkdir -p tools
mkdir -p research
echo "📂 Created organized directory structure"

# Essential files to keep in root
KEEP_ROOT=(
  "README.md"
  "CODE_OF_CONDUCT.md"
  "CONTRIBUTING.md"
  "requirements.txt"
  "launcher.py"
  "Claude 4.0 Vulnerabilities.code-workspace"
  "organize_claude40_complete.sh"
)

# Organize files into appropriate directories
echo "🔄 Organizing files into appropriate directories..."

# Core files
mkdir -p core
if [[ -f "realtime_vulnerability_monitor.py" ]]; then
  mv "realtime_vulnerability_monitor.py" "core/vulnerability_monitor.py"
fi
if [[ -f "vulnerability_aware_client.py" ]]; then
  mv "vulnerability_aware_client.py" "core/safeguards_client.py"
fi
if [[ -f "safeguards_aware_client.py" ]]; then
  mv "safeguards_aware_client.py" "core/client.py"
fi

# Test files
mkdir -p tests
mv test_claude40_pain_points.py tests/ 2>/dev/null
mv advanced_vulnerability_tester.py tests/ 2>/dev/null
mv test_case_generator.py tests/ 2>/dev/null

# Tools
mkdir -p tools
mv pattern_analyzer.py tools/ 2>/dev/null
mv generate_dashboard.py tools/ 2>/dev/null
mv orchestrate_tests.py tools/ 2>/dev/null
mv analyze_results.py tools/ 2>/dev/null
mv benchmark_vulnerability.py tools/ 2>/dev/null

# Patterns
mkdir -p patterns
mv claude_4_0_red_team_test_suite.json patterns/ 2>/dev/null
mv claude_4_0_advanced_test_cases.json patterns/ 2>/dev/null
mv vulnerability_patterns.json patterns/ 2>/dev/null
mv red_team_test_suite.json patterns/ 2>/dev/null
mv advanced_vulnerability_test_suite.json patterns/ 2>/dev/null

# Config
mkdir -p config
mv monitor_config.json config/ 2>/dev/null
mv workflow_config.json config/ 2>/dev/null

# Documentation
mkdir -p docs
mv CHILD_SAFETY_FRAMEWORK.md docs/ 2>/dev/null
mv CLAUDE_4_0_TESTING_PAIN_POINTS.md docs/ 2>/dev/null
mv QUICKSTART.md docs/ 2>/dev/null
mv vulnerability_taxonomy.md docs/ 2>/dev/null
mv claude-4-0-testing-framework.md docs/ 2>/dev/null
mv claude-4-0-vulnerabilities.md docs/ 2>/dev/null
mv claude-4-0-project-roadmap.md docs/ 2>/dev/null
mv sample-vulnerability-report.md docs/ 2>/dev/null
mv vulnerability-report-template.md docs/ 2>/dev/null
mv ADVANCED_CAPABILITIES.md docs/ 2>/dev/null

# Create clean README.md
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

# Now remove all files not intended to be kept in root
for file in *.md *.py *.sh *.json; do
  keep=false
  for keep_file in "${KEEP_ROOT[@]}"; do
    if [[ "$file" == "$keep_file" ]]; then
      keep=true
      break
    fi
  done
  
  if [[ "$keep" == false && -f "$file" ]]; then
    echo "Removing $file from root directory"
    rm -f "$file"
  fi
done

echo "🎉 Complete cleanup and organization done! The workspace has been simplified and organized."
echo "👉 Original files have been backed up to: $BACKUP_DIR"
