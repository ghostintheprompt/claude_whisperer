# Claude 3.7 Safeguards Testing Framework

This update adds advanced safeguard testing capabilities focused on Claude 3.7's safety mechanisms, addressing key requirements for comprehensive user well-being protection. These tools enable structured, systematic evaluation of policy enforcement, with particular focus on mode consistency, cross-model comparison, and child safety protections.

## New Tools Added

### 1. Cross-Model Safeguards Analysis (`cross_model_safeguards.py`)

This tool enables systematic comparison of safety protections across different LLM models:

- Tests Claude 3.7 (Quick and Depth modes) against Claude 3.5 Sonnet and other models
- Analyzes differences in policy enforcement strength and consistency
- Generates both JSON and CSV reports for safety analytics
- Works with both Anthropic and other model providers

### 2. Mode Safeguards Comparison (`mode_safeguards_comparison.py`)

Focuses specifically on ensuring consistent policy enforcement between Claude 3.7's Quick and Depth modes:

- Runs identical prompts through both modes to identify enforcement discrepancies
- Generates detailed reports with visualizations
- Provides statistical analysis of safety enforcement patterns
- Identifies potential safety gaps requiring attention

### 3. Safeguards Test Generator (`safeguards_test_generator.py`)

Helps analysts create standardized safety test cases:

- Interactive mode for test suite creation
- Template generation for common policy enforcement scenarios
- Standardized formatting for safety test cases
- Child safety specific test suite generation

### 4. Real-time Safeguards Monitor (`realtime_safeguards_monitor.py`)

Provides continuous monitoring of Claude 3.7 interactions:

- WebSocket server for real-time analysis of API usage
- Detects potential policy violations in user conversations
- Configurable alerting for safety interventions
- Comprehensive logging for safety audit trails
- Advanced child safety monitoring capabilities

### 5. Orchestration Framework (`orchestrate_safeguards_tests.py`)

Automates the execution of safety test suites:

- Parallel execution of test cases
- Comprehensive reporting and analytics
- Integration with CI/CD pipelines for automated safety validation
- Report generation with visualizations

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/your-organization/claude-3.7-safeguards.git
cd claude-3.7-safeguards

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export ANTHROPIC_API_KEY=your_api_key
```

### Running Safety Tests

```bash
# Run the cross-model safety comparison
python cross_model_safeguards.py --test-suite tests/policy_enforcement_tests.json

# Run the mode comparison tests
python mode_safeguards_comparison.py --test-suite tests/consistency_tests.json

# Start the real-time monitoring server
python realtime_safeguards_monitor.py --port 8765
```

## Contributing New Safety Tests

1. Use the `safeguards_test_generator.py` to create new test cases
2. Follow the test case format documented in `CONTRIBUTING.md`
3. Submit a pull request with your new safety tests

## Policy Enforcement Documentation

For detailed information about the policy enforcement mechanisms and test methodologies, see the following documents:

- [POLICY_ENFORCEMENT.md](POLICY_ENFORCEMENT.md) - Detailed information on enforcement mechanisms
- [CHILD_SAFETY_FRAMEWORK.md](CHILD_SAFETY_FRAMEWORK.md) - Specialized child safety protection testing
- [SAFEGUARDS_ANALYTICS.md](SAFEGUARDS_ANALYTICS.md) - Framework for safety metrics and reporting

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file.
