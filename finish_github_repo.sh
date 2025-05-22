#!/bin/bash
# Script to finalize the claude-whisperer repository before pushing to GitHub

# Define paths
TEMP_DIR="/tmp/claude-whisperer"
REPO_URL="https://github.com/MdrnDme/claude-whisperer.git"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== Finalizing claude-whisperer Repository =====${NC}"

# Check if temp directory exists
if [ ! -d "$TEMP_DIR" ]; then
  echo -e "${RED}Error: Temporary directory not found. Please run prepare_github_repo.sh first.${NC}"
  exit 1
fi

# Change to temp directory
cd "$TEMP_DIR" || exit 1

# Make sure all references to "CLAUDE WHISPERER" or "Claude Whisperer" are changed to "claude-whisperer"
echo -e "${YELLOW}Checking for remaining uppercase references...${NC}"
grep -r "CLAUDE WHISPERER\|Claude Whisperer" --include="*.py" --include="*.md" --include="*.txt" .

# Make final commit for name changes
echo -e "${YELLOW}Making final commits...${NC}"
git add .
git commit -m "Finalize renaming to claude-whisperer"

# Instructions for pushing
echo -e "${GREEN}===== Repository Ready to Push =====${NC}"
echo -e "To push to GitHub, run the following commands:"
echo -e "${YELLOW}cd $TEMP_DIR${NC}"
echo -e "${YELLOW}git push -u origin main${NC}"

echo -e "${GREEN}===== Complete =====${NC}"
