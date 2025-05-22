#!/usr/bin/env zsh
# Execute vulnerability research workflows for Claude 3.7

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Set the base directory
BASE_DIR="$(dirname "$(realpath "$0")")"
cd "$BASE_DIR"

print_header() {
    echo -e "\n${BLUE}=========================================================${NC}"
    echo -e "${BLUE}   Claude 3.7 Vulnerability Research Framework${NC}"
    echo -e "${BLUE}=========================================================${NC}\n"
}

print_help() {
    print_header
    echo -e "${GREEN}Usage:${NC}"
    echo -e "  $0 ${YELLOW}<command>${NC} [options]\n"
    echo -e "${GREEN}Available commands:${NC}"
    echo -e "  ${YELLOW}quick-scan${NC}         Run a quick vulnerability scan"
    echo -e "  ${YELLOW}deep-dive${NC}          Run comprehensive vulnerability analysis"
    echo -e "  ${YELLOW}monitor${NC}            Start real-time vulnerability monitoring"
    echo -e "  ${YELLOW}analyze${NC}            Analyze existing vulnerability results"
    echo -e "  ${YELLOW}report${NC}             Generate research report from results"
    echo -e "  ${YELLOW}dashboard${NC}          Generate interactive dashboard"
    echo -e "  ${YELLOW}trends${NC}             Analyze vulnerability trends over time"
    echo -e "  ${YELLOW}help${NC}               Show this help message\n"
    echo -e "${GREEN}Examples:${NC}"
    echo -e "  $0 ${YELLOW}quick-scan${NC}"
    echo -e "  $0 ${YELLOW}monitor${NC}"
    echo -e "  $0 ${YELLOW}report${NC} --type comprehensive\n"
}

if [ $# -eq 0 ]; then
    print_help
    exit 0
fi

command=$1
shift

case "$command" in
    quick-scan)
        print_header
        echo -e "${GREEN}Running quick vulnerability scan...${NC}\n"
        python3 vulnerability_research_workflow.py run-workflow quick_scan "$@"
        ;;
        
    deep-dive)
        print_header
        echo -e "${GREEN}Running comprehensive vulnerability analysis...${NC}\n"
        python3 vulnerability_research_workflow.py run-workflow full_research "$@"
        ;;
        
    monitor)
        print_header
        echo -e "${GREEN}Starting real-time vulnerability monitoring...${NC}\n"
        python3 vulnerability_research_workflow.py setup-monitoring "$@"
        echo -e "\n${YELLOW}Real-time monitor started. Use the vulnerability_aware_client.py script to test vulnerabilities.${NC}"
        ;;
        
    analyze)
        print_header
        echo -e "${GREEN}Running vulnerability pattern analysis...${NC}\n"
        python3 vulnerability_research_workflow.py run-step pattern_analysis "$@"
        ;;
        
    report)
        print_header
        echo -e "${GREEN}Generating vulnerability research report...${NC}\n"
        python3 vulnerability_research_workflow.py create-report "$@"
        ;;
        
    dashboard)
        print_header
        echo -e "${GREEN}Generating interactive vulnerability dashboard...${NC}\n"
        python3 vulnerability_research_workflow.py generate-dashboard "$@"
        ;;
        
    trends)
        print_header
        echo -e "${GREEN}Analyzing vulnerability trends...${NC}\n"
        python3 vulnerability_research_workflow.py analyze-trends --visualize "$@"
        ;;
        
    help)
        print_help
        ;;
        
    *)
        echo -e "${RED}Unknown command: $command${NC}\n"
        print_help
        exit 1
        ;;
esac
