#!/bin/bash

# Claude 4.0 Vulnerability Testing Launcher Script
# This script provides an easy way to run various Claude 4.0 vulnerability tests

set -e

# Configuration
CLAUDE_MODEL="claude-4-sonnet-20240520"
RESULTS_DIR="./test_results"
LOG_DIR="./logs"

# Ensure directories exist
mkdir -p "$RESULTS_DIR"
mkdir -p "$LOG_DIR"

# Current timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/claude40_test_run_$TIMESTAMP.log"

# Function to log messages
log() {
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_FILE"
}

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  log "Error: ANTHROPIC_API_KEY environment variable not set"
  log "Please set it with: export ANTHROPIC_API_KEY=your_api_key_here"
  exit 1
fi

# Display menu and get user choice
show_menu() {
  clear
  echo "===================================================="
  echo "       CLAUDE 4.0 VULNERABILITY TESTING TOOLKIT      "
  echo "===================================================="
  echo "Choose a testing option:"
  echo ""
  echo "1) Run Basic Pain Point Tests"
  echo "2) Run Advanced Vulnerability Tests"
  echo "3) Run All Tests"
  echo "4) Run Tool Use Vulnerability Tests"
  echo "5) Run Reasoning Vulnerability Tests"
  echo "6) Run System Prompt Vulnerability Tests"
  echo "7) Run Multi-turn Conversation Vulnerability Tests"
  echo "8) Run Visual/Multimodal Vulnerability Tests"
  echo "9) View Test Results"
  echo "0) Exit"
  echo ""
  read -p "Enter your choice [0-9]: " choice
}

# Run the pain points testing script
run_pain_point_tests() {
  category="$1"
  
  if [ -z "$category" ]; then
    log "Running all basic pain point tests..."
    python3 test_claude40_pain_points.py --all --model "$CLAUDE_MODEL" --output-dir "$RESULTS_DIR"
  else
    log "Running pain point tests for category: $category"
    python3 test_claude40_pain_points.py --categories "$category" --model "$CLAUDE_MODEL" --output-dir "$RESULTS_DIR"
  fi
}

# Run the advanced test cases
run_advanced_tests() {
  log "Running advanced vulnerability tests..."
  python3 advanced_vulnerability_tester.py \
    --test-file claude_4_0_advanced_test_cases.json \
    --model "$CLAUDE_MODEL" \
    --output-dir "$RESULTS_DIR" \
    --report-format markdown
}

# View most recent test results
view_results() {
  # Find most recent markdown report
  recent_report=$(find "$RESULTS_DIR" -name "*.md" -type f -printf "%T@ %p\n" | sort -nr | head -1 | cut -d' ' -f2-)
  
  if [ -z "$recent_report" ]; then
    log "No test reports found."
    return
  fi
  
  log "Viewing most recent test report: $recent_report"
  if command -v less &>/dev/null; then
    less "$recent_report"
  else
    cat "$recent_report"
  fi
}

# Main loop
while true; do
  show_menu
  
  case $choice in
    1)
      log "Running basic pain point tests..."
      run_pain_point_tests
      read -p "Press Enter to continue..."
      ;;
    2)
      log "Running advanced vulnerability tests..."
      run_advanced_tests
      read -p "Press Enter to continue..."
      ;;
    3)
      log "Running all tests..."
      run_pain_point_tests
      run_advanced_tests
      log "All tests completed."
      read -p "Press Enter to continue..."
      ;;
    4)
      log "Running Tool Use vulnerability tests..."
      run_pain_point_tests "tool-use"
      read -p "Press Enter to continue..."
      ;;
    5)
      log "Running Reasoning vulnerability tests..."
      run_pain_point_tests "reasoning"
      read -p "Press Enter to continue..."
      ;;
    6)
      log "Running System Prompt vulnerability tests..."
      run_pain_point_tests "system-prompt"
      read -p "Press Enter to continue..."
      ;;
    7)
      log "Running Multi-turn Conversation vulnerability tests..."
      run_pain_point_tests "multi-turn"
      read -p "Press Enter to continue..."
      ;;
    8)
      log "Running Visual/Multimodal vulnerability tests..."
      run_pain_point_tests "multimodal"
      read -p "Press Enter to continue..."
      ;;
    9)
      view_results
      read -p "Press Enter to continue..."
      ;;
    0)
      log "Exiting Claude 4.0 Vulnerability Testing Toolkit"
      exit 0
      ;;
    *)
      log "Invalid option. Please try again."
      read -p "Press Enter to continue..."
      ;;
  esac
done
