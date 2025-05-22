#!/bin/zsh
# Cleanup script for Claude Safeguards Framework - simplified version

echo "🧹 Cleaning up Claude Safeguards Framework repository..."

# Create a directory for the simplified framework
TARGET_DIR="/Users/greenplanet/Desktop/Simple-Safeguards"
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/config"
mkdir -p "$TARGET_DIR/patterns"

# Source directory with proper escaping
SOURCE_DIR="/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities"

# Copy only the essential files
cp "$SOURCE_DIR/launcher.py" "$TARGET_DIR/"
cp "$SOURCE_DIR/safeguards_aware_client.py" "$TARGET_DIR/"
cp "$SOURCE_DIR/realtime_safeguards_monitor.py" "$TARGET_DIR/"
cp "$SOURCE_DIR/CHILD_SAFETY_FRAMEWORK.md" "$TARGET_DIR/"
cp "$SOURCE_DIR/CONTRIBUTING.md" "$TARGET_DIR/"
cp "$SOURCE_DIR/README.md.new" "$TARGET_DIR/README.md"

# Copy config files
cp "$SOURCE_DIR/config/safeguards_config.json" "$TARGET_DIR/config/"

# Copy pattern files
cp "$SOURCE_DIR/patterns/child_safety_patterns.json" "$TARGET_DIR/patterns/"
cp "$SOURCE_DIR/patterns/content_moderation_patterns.json" "$TARGET_DIR/patterns/"
cp "$SOURCE_DIR/patterns/policy_patterns.json" "$TARGET_DIR/patterns/"

# Make scripts executable
chmod +x "$TARGET_DIR/launcher.py"
chmod +x "$TARGET_DIR/safeguards_aware_client.py"
chmod +x "$TARGET_DIR/realtime_safeguards_monitor.py"

echo "🎉 Created simplified Claude Safeguards Framework at $TARGET_DIR"
