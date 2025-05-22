#!/bin/zsh
# Cleanup script for Claude Safeguards Framework
# Removes redundant and obsolete files

echo "🧹 Cleaning up Claude Safeguards Framework repository..."

# Files to keep
ESSENTIAL_FILES=(
  "launcher.py"
  "safeguards_aware_client.py"
  "realtime_safeguards_monitor.py"
  "README.md"
  "CHILD_SAFETY_FRAMEWORK.md"
  "CONTRIBUTING.md"
)

# Directories to keep
ESSENTIAL_DIRS=(
  "config"
  "patterns"
)

# Create backup directory
BACKUP_DIR="./backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Created backup directory: $BACKUP_DIR"

# Move all files except essential ones to backup
for file in *; do
  if [[ -f "$file" ]]; then
    if [[ ! " ${ESSENTIAL_FILES[@]} " =~ " ${file} " ]]; then
      echo "📄 Moving $file to backup"
      mv "$file" "$BACKUP_DIR/"
    else
      echo "✅ Keeping essential file: $file"
    fi
  fi
done

# Handle directories
for dir in */; do
  dir=${dir%/}  # Remove trailing slash
  if [[ -d "$dir" && ! " ${ESSENTIAL_DIRS[@]} " =~ " ${dir} " ]]; then
    if [[ "$dir" != "$BACKUP_DIR" && "$dir" != "." && "$dir" != ".." ]]; then
      echo "📁 Moving directory $dir to backup"
      mv "$dir" "$BACKUP_DIR/"
    fi
  else
    echo "✅ Keeping essential directory: $dir"
  fi
done

echo "🎉 Cleanup complete! Removed files are backed up in $BACKUP_DIR"
echo "📝 Repository now contains only essential Claude Safeguards Framework files"
