#!/bin/bash
# update_to_claude_4.sh - Script to update Claude 3.7 references to Claude 4.0

echo "Starting Claude 4.0 update process..."

# Update file contents
find . -type f -name "*.md" -o -name "*.py" -o -name "*.json" | xargs grep -l "Claude 3.7" | xargs sed -i '' 's/Claude 3.7/Claude 4.0/g'
find . -type f -name "*.md" -o -name "*.py" -o -name "*.json" | xargs grep -l "CLAUDE37" | xargs sed -i '' 's/CLAUDE37/CLAUDE40/g'
find . -type f -name "*.md" -o -name "*.py" -o -name "*.json" | xargs grep -l "claude-3-7" | xargs sed -i '' 's/claude-3-7/claude-4-0/g'
find . -type f -name "*.md" -o -name "*.py" -o -name "*.json" | xargs grep -l "claude_3_7" | xargs sed -i '' 's/claude_3_7/claude_4_0/g'

echo "File content updates complete."

# Remove old workspace file
if [ -f "Claude 3.7 Vulnerabilities.code-workspace" ]; then
  rm "Claude 3.7 Vulnerabilities.code-workspace"
  echo "Removed old workspace file."
fi

echo "Update complete! The project is now configured for Claude 4.0."
