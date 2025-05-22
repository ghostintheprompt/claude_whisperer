#!/bin/bash
# Script to prepare and push the claude-whisperer project to GitHub

# Define paths
SOURCE_DIR="/Users/greenplanet/Desktop/Claude 4.0 Vulnerabilities"
TEMP_DIR="/tmp/claude-whisperer"
REPO_URL="https://github.com/MdrnDme/claude-whisperer.git"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== claude-whisperer GitHub Preparation =====${NC}"

# Create temp directory
echo -e "${YELLOW}Creating temporary directory...${NC}"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy core files and directories
echo -e "${YELLOW}Copying project files...${NC}"
cp -r "$SOURCE_DIR/multimodal" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/semantic_mirror" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/exploit_generator" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/frontend" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/tests" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/tools" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/core" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/config" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/research" "$TEMP_DIR/"
cp -r "$SOURCE_DIR/patterns" "$TEMP_DIR/"
mkdir -p "$TEMP_DIR/docs"

# Copy main files
cp "$SOURCE_DIR/claude_whisperer.py" "$TEMP_DIR/"
cp "$SOURCE_DIR/run_tests.py" "$TEMP_DIR/"
cp "$SOURCE_DIR/requirements.txt" "$TEMP_DIR/"
cp "$SOURCE_DIR/README.md" "$TEMP_DIR/"

# Copy essential documentation
cp "$SOURCE_DIR/docs/CODE_OF_CONDUCT.md" "$TEMP_DIR/docs/"
cp "$SOURCE_DIR/docs/CONTRIBUTING.md" "$TEMP_DIR/docs/"
cp "$SOURCE_DIR/docs/QUICKSTART.md" "$TEMP_DIR/docs/"
cp "$SOURCE_DIR/docs/MULTIMODAL_ATTACKS.md" "$TEMP_DIR/docs/"
cp "$SOURCE_DIR/docs/SEMANTIC_MIRROR_ATTACKS.md" "$TEMP_DIR/docs/"
cp "$SOURCE_DIR/docs/AUTOMATED_EXPLOIT_GENERATOR.md" "$TEMP_DIR/docs/"
cp "$SOURCE_DIR/docs/FRONTEND_INTERFACE.md" "$TEMP_DIR/docs/"

# Replace "Claude 3.7" with "Claude 4.0" in all files
echo -e "${YELLOW}Replacing Claude 3.7 references with Claude 4.0...${NC}"
find "$TEMP_DIR" -type f -name "*.py" -o -name "*.md" -o -name "*.txt" | xargs sed -i '' -e 's/Claude 3\.7/Claude 4\.0/g'

# Replace "Claude Whisperer" with "claude-whisperer" in all files
echo -e "${YELLOW}Updating project name to claude-whisperer...${NC}"
find "$TEMP_DIR" -type f -name "*.py" -o -name "*.md" -o -name "*.txt" | xargs sed -i '' -e 's/Claude Whisperer/claude-whisperer/g'
find "$TEMP_DIR" -type f -name "*.py" -o -name "*.md" -o -name "*.txt" | xargs sed -i '' -e 's/CLAUDE WHISPERER/claude-whisperer/g'

# Create git repository
echo -e "${YELLOW}Initializing Git repository...${NC}"
cd "$TEMP_DIR"
git init
git add .
git commit -m "Initial commit of Claude Whisperer project"

# Add remote and push
echo -e "${YELLOW}Setting up remote repository...${NC}"
git remote add origin "$REPO_URL"

echo -e "${GREEN}===== Preparation Complete =====${NC}"
echo -e "${GREEN}The repository is ready at:${NC} $TEMP_DIR"
echo
echo -e "${YELLOW}To push to GitHub, execute:${NC}"
echo "cd $TEMP_DIR"
echo "git push -u origin main"
echo
echo -e "${YELLOW}Note:${NC} If you haven't already authenticated with GitHub, you may need to set up SSH keys or authenticate via HTTPS"
