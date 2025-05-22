#!/bin/zsh
# Cleanup script for Claude Safeguards Framework - simplified version

echo "🧹 Cleaning up Claude Safeguards Framework repository..."

# Create a directory for the simplified framework
mkdir -p "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple"
mkdir -p "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/config"
mkdir -p "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/patterns"

# Copy only the essential files
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/launcher.py" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/safeguards_aware_client.py" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/realtime_safeguards_monitor.py" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/CHILD_SAFETY_FRAMEWORK.md" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/CONTRIBUTING.md" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/README.md.new" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/README.md"

# Copy config files
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/config/safeguards_config.json" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/config/"

# Copy pattern files
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/patterns/child_safety_patterns.json" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/patterns/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/patterns/content_moderation_patterns.json" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/patterns/"
cp "/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities/patterns/policy_patterns.json" "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/patterns/"

# Make scripts executable
chmod +x "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/launcher.py"
chmod +x "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/safeguards_aware_client.py"
chmod +x "/Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple/realtime_safeguards_monitor.py"

echo "🎉 Created simplified Claude Safeguards Framework at /Users/greenplanet/Desktop/Claude-Safeguards-Framework-Simple"
