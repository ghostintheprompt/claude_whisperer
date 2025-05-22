#!/bin/bash
# Claude 3.7 Vulnerability Testing Helper Script

# Default values
TEST_FILE=""
OUTPUT_DIR="./results"
MODEL="claude-3-7-sonnet-20250501"
CROSS_MODEL=false
MODE_COMPARISON=false

# Display usage information
function show_help {
    echo "Claude 3.7 Vulnerability Testing Helper"
    echo ""
    echo "Usage:"
    echo "  $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -t, --test FILE         Test file to use (JSON format)"
    echo "  -o, --output DIR        Directory for output results (default: ./results)"
    echo "  -m, --model MODEL       Claude model to test (default: claude-3-7-sonnet-20250501)"
    echo "  -c, --cross-model       Run cross-model comparison tests"
    echo "  -d, --mode-comparison   Run mode comparison tests (Quick vs. Depth)"
    echo ""
    echo "Examples:"
    echo "  $0 --test test_case.json --mode-comparison"
    echo "  $0 --test test_suite.json --cross-model --output ./comparison_results"
    echo ""
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            show_help
            shift
            ;;
        -t|--test)
            TEST_FILE="$2"
            shift
            shift
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift
            shift
            ;;
        -m|--model)
            MODEL="$2"
            shift
            shift
            ;;
        -c|--cross-model)
            CROSS_MODEL=true
            shift
            ;;
        -d|--mode-comparison)
            MODE_COMPARISON=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Validate inputs
if [ -z "$TEST_FILE" ]; then
    echo "Error: No test file specified. Use -t or --test to specify a test file."
    exit 1
fi

if [ ! -f "$TEST_FILE" ]; then
    echo "Error: Test file not found: $TEST_FILE"
    exit 1
fi

if [[ "$CROSS_MODEL" == "false" && "$MODE_COMPARISON" == "false" ]]; then
    echo "Error: You must specify at least one test type (--cross-model or --mode-comparison)"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "Results will be saved to: $OUTPUT_DIR"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Warning: ANTHROPIC_API_KEY environment variable not set."
    echo "You'll be prompted for your API key or you can cancel and set it with:"
    echo "export ANTHROPIC_API_KEY=your_api_key_here"
    read -p "Press Enter to continue or Ctrl+C to cancel..."
fi

# Run tests
if [[ "$CROSS_MODEL" == "true" ]]; then
    echo ""
    echo "Running cross-model comparison tests..."
    echo "========================================"
    
    ./cross_model_tester.py \
        --test_file "$TEST_FILE" \
        --output "$OUTPUT_DIR/cross_model_results.json" \
        --csv "$OUTPUT_DIR/cross_model_results.csv"
    
    CROSS_MODEL_STATUS=$?
    echo ""
fi

if [[ "$MODE_COMPARISON" == "true" ]]; then
    echo ""
    echo "Running mode comparison tests (Quick vs. Depth)..."
    echo "=================================================="
    
    ./mode_comparison_tester.py \
        --test_file "$TEST_FILE" \
        --model "$MODEL" \
        --output "$OUTPUT_DIR/mode_results.json" \
        --report_dir "$OUTPUT_DIR/mode_report"
    
    MODE_COMPARISON_STATUS=$?
    echo ""
fi

# Check for errors
if [[ "$CROSS_MODEL" == "true" && "$CROSS_MODEL_STATUS" -ne 0 ]]; then
    echo "Cross-model tests completed with errors."
else
    if [[ "$CROSS_MODEL" == "true" ]]; then
        echo "Cross-model tests completed successfully."
        echo "Results saved to:"
        echo "  - $OUTPUT_DIR/cross_model_results.json"
        echo "  - $OUTPUT_DIR/cross_model_results.csv"
    fi
fi

if [[ "$MODE_COMPARISON" == "true" && "$MODE_COMPARISON_STATUS" -ne 0 ]]; then
    echo "Mode comparison tests completed with errors."
else
    if [[ "$MODE_COMPARISON" == "true" ]]; then
        echo "Mode comparison tests completed successfully."
        echo "Results saved to:"
        echo "  - $OUTPUT_DIR/mode_results.json"
        echo "  - $OUTPUT_DIR/mode_report/"
        
        # Open HTML report if it exists
        if [ -f "$OUTPUT_DIR/mode_report/report.html" ]; then
            echo ""
            echo "Report generated at: $OUTPUT_DIR/mode_report/report.html"
            
            # Try to open the report on macOS
            if [[ "$(uname)" == "Darwin" ]]; then
                open "$OUTPUT_DIR/mode_report/report.html"
            fi
        fi
    fi
fi

echo ""
echo "Testing complete!"
