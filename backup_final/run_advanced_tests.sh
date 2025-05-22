#!/bin/bash
# Integration script for running advanced vulnerability tests and integrating with existing tools

display_help() {
    echo "Advanced Vulnerability Testing Framework Integration Script"
    echo ""
    echo "Usage:"
    echo "  $0 [options]"
    echo ""
    echo "Options:"
    echo "  --test-suite FILE       Test suite JSON file to use"
    echo "  --mode-comparison       Compare results between Quick and Depth modes"
    echo "  --cross-model           Compare results across different model versions"
    echo "  --output-dir DIR        Directory to store results (default: ./reports)"
    echo "  --simulate              Run in simulation mode without making actual API calls"
    echo "  --integrate             Integrate results with existing analysis framework"
    echo "  --visualize             Generate visualizations from results"
    echo "  --help                  Display this help message and exit"
    echo ""
    echo "Examples:"
    echo "  $0 --test-suite advanced_vulnerability_test_suite.json --mode-comparison --output-dir ./reports/advanced"
    echo "  $0 --test-suite advanced_vulnerability_test_suite.json --cross-model --integrate"
    echo ""
}

# Default values
TEST_SUITE=""
OUTPUT_DIR="./reports"
MODE_COMPARISON=false
CROSS_MODEL=false
SIMULATE=false
INTEGRATE=false
VISUALIZE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test-suite)
            TEST_SUITE="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --mode-comparison)
            MODE_COMPARISON=true
            shift
            ;;
        --cross-model)
            CROSS_MODEL=true
            shift
            ;;
        --simulate)
            SIMULATE=true
            shift
            ;;
        --integrate)
            INTEGRATE=true
            shift
            ;;
        --visualize)
            VISUALIZE=true
            shift
            ;;
        --help)
            display_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            display_help
            exit 1
            ;;
    esac
done

# Check for required arguments
if [ -z "$TEST_SUITE" ]; then
    echo "Error: Test suite file is required"
    display_help
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Main execution
echo "Advanced Vulnerability Testing Framework Integration Script"
echo "============================================================"
echo "Test Suite: $TEST_SUITE"
echo "Output Directory: $OUTPUT_DIR"
echo "============================================================"

# Run the advanced vulnerability tester
TESTER_ARGS="--test_suite $TEST_SUITE --output_dir $OUTPUT_DIR"

if [ "$SIMULATE" = true ]; then
    TESTER_ARGS="$TESTER_ARGS --simulate"
fi

if [ "$MODE_COMPARISON" = true ]; then
    TESTER_ARGS="$TESTER_ARGS --models claude-3-7-quick claude-3-7-depth"
    echo "Running mode comparison test..."
elif [ "$CROSS_MODEL" = true ]; then
    TESTER_ARGS="$TESTER_ARGS --models claude-3-7-quick claude-3-7-depth claude-3-5-sonnet"
    echo "Running cross-model comparison test..."
else
    echo "Running standard test..."
fi

echo "Running advanced vulnerability tester with args: $TESTER_ARGS"
python3 ./advanced_vulnerability_tester.py $TESTER_ARGS

# Check if the test was successful
if [ $? -ne 0 ]; then
    echo "Error running advanced vulnerability tester"
    exit 1
fi

echo "Advanced vulnerability tests completed successfully"

# Integration with existing tools
if [ "$INTEGRATE" = true ]; then
    echo "Integrating results with existing analysis framework..."
    
    # Convert results to format expected by existing tools
    echo "Converting results to compatible format..."
    
    if [ "$MODE_COMPARISON" = true ]; then
        echo "Running mode comparison analyzer..."
        # This would be the actual command to run the existing mode comparison tool
        # with the results from the advanced tester
        python3 ./mode_comparison_tester.py --results "$OUTPUT_DIR/vulnerability_test_results.json" --report_dir "$OUTPUT_DIR"
    fi
    
    # Run the generic analysis tool on the results
    echo "Running analysis tools on results..."
    python3 ./analyze_results.py "$OUTPUT_DIR/vulnerability_test_results.json" --report "$OUTPUT_DIR/integrated_analysis.md"
fi

# Generate visualizations
if [ "$VISUALIZE" = true ]; then
    echo "Generating additional visualizations..."
    # This would be the command to generate more sophisticated visualizations
    # For now we'll assume the advanced_vulnerability_tester.py already generates basic ones
fi

echo "============================================================"
echo "Testing completed. Results available in $OUTPUT_DIR"
echo "Key outputs:"
echo "- Test report: $OUTPUT_DIR/vulnerability_report.md"
echo "- Raw results: $OUTPUT_DIR/vulnerability_test_results.json"
if [ "$VISUALIZE" = true ] || [ "$INTEGRATE" = true ]; then
    echo "- Visualizations: $OUTPUT_DIR/*.png"
fi
if [ "$INTEGRATE" = true ]; then
    echo "- Integrated analysis: $OUTPUT_DIR/integrated_analysis.md" 
fi
echo "============================================================"

exit 0
