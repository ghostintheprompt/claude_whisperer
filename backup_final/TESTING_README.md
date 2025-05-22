# Claude 3.7 Testing Framework

This directory contains specialized testing tools for evaluating vulnerabilities in Claude 3.7, with particular focus on its unique features:

1. **Mode Differences (Quick vs. Depth)**: Testing how vulnerabilities may manifest differently across modes
2. **Cross-Model Comparison**: Comparing Claude 3.7 with other models like Claude 3.5 Sonnet and GPT-4
3. **Tool Use Vulnerabilities**: Specialized tests for Claude's tool use capabilities
4. **Enhanced Reasoning Capabilities**: Evaluating how Claude's reasoning may be vulnerable

## Tools Overview

### 1. Mode Comparison Tester

Tests how vulnerabilities may manifest differently between Quick and Depth modes in Claude 3.7. The tool generates comprehensive reports with visualizations.

```bash
./mode_comparison_tester.py --test_file mode_comparison_test_suite.json --report_dir report_output
```

**Features:**
- Automatically tests prompts in both Quick and Depth modes
- Identifies inconsistencies in safety boundaries between modes
- Generates HTML reports with visualizations
- Provides detailed CSV summaries for further analysis

### 2. Cross-Model Tester

Compares vulnerability patterns across multiple models:

```bash
./cross_model_tester.py --test_file test_case.json --csv report.csv
```

**Features:**
- Tests across Claude 3.7, Claude 3.5 Sonnet, and GPT models
- Supports multiple modes per model
- Generates JSON and CSV reports
- Compatible with Anthropic and OpenAI models

## Test Case Format

### Individual Test Case (for cross_model_tester.py)

```json
{
  "vulnerability_id": "CLAUDE37-CATEGORY-001",
  "title": "Descriptive name of vulnerability",
  "category": ["Primary category", "Secondary category"],
  "severity": "Low|Medium|High|Critical",
  "test_case": "The exact prompt to test",
  "expected_behavior": "How Claude should respond (safe behavior)",
  "vulnerable_behavior": "How Claude responds when vulnerability is present",
  "success_criteria": ["Criterion 1", "Criterion 2"],
  "discovered_by": "Researcher name",
  "discovery_date": "YYYY-MM-DD",
  "status": "Active|Mitigated|Fixed|Disputed"
}
```

### Test Suite (for mode_comparison_tester.py)

```json
{
  "name": "Test Suite Name",
  "description": "Description of the test suite",
  "test_cases": [
    {
      "id": "CLAUDE37-MODE-001",
      "title": "Test case title",
      "category": ["Category1", "Category2"],
      "prompt": "The prompt to test",
      "success_criteria": ["Criterion 1", "Criterion 2"],
      "expected_behavior": "Expected safe behavior",
      "vulnerable_behavior": "Vulnerable behavior"
    }
  ]
}
```

## Requirements

- Python 3.8+
- `anthropic` Python package
- `openai` Python package (for cross-model testing with GPT models)
- `pandas` and `matplotlib` (for visualization in reports)

Install requirements:

```bash
pip install anthropic openai pandas matplotlib
```

## API Keys

Set your API keys as environment variables:

```bash
export ANTHROPIC_API_KEY="your_anthropic_key"
export OPENAI_API_KEY="your_openai_key"  # Optional, for cross-model testing
```

Or pass them directly:

```bash
./cross_model_tester.py --test_file test.json --anthropic_key "your_key" --openai_key "your_key"
```

## Best Practices

1. **Start with small test batches** before running large test suites
2. **Test each vulnerability in both modes** to identify mode-specific behaviors
3. **Document results thoroughly** using the standard reporting templates
4. **Compare with previous versions** to track changes in vulnerability patterns
5. **Follow responsible disclosure protocols** for any new vulnerabilities

## Example Workflow

1. Create a test suite JSON file with your test cases
2. Run the mode comparison tester
3. Analyze the report to identify mode-specific vulnerabilities
4. Run cross-model tests to compare with other models
5. Document findings using the standard vulnerability report template
6. Submit reports following the responsible disclosure process

## Contributing

When adding new tests:

1. Follow the standardized test case format
2. Include clear success criteria
3. Document expected vs. vulnerable behaviors
4. Test across both modes
5. Add tests to appropriate test suites

## License

MIT License - See the LICENSE file for details
