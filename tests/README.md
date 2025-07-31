# claude-whisperer Testing Framework

This directory contains the testing framework for the claude-whisperer project, which implements comprehensive tests for all components of the system.

## Overview

The testing framework includes:

- **Unit Tests**: Tests for individual components
- **Integration Tests**: Tests for component interactions
- **System Tests**: End-to-end tests of the entire system

## Test Components

### Multimodal Attack Tests

Tests for the image-based attack vectors, including:

- Text in image embedding
- Steganography
- Metadata injection
- Visual pattern encoding

### Semantic Mirror Attack Tests

Tests for the semantic mirror attack framework, including:

- Semantic variant generation
- Genetic prompt evolution
- Cipher-based encoding

### Exploit Generator Tests

Tests for the automated exploit generator, including:

- Auto-DAN framework
- FLIRT (Feedback Loop In-context Red Teaming)
- Mosaic Prompt Assembler

### Frontend Interface Tests

Tests for the browser-based testing interface, including:

- API endpoints
- WebSocket communication
- Jailbreak detection logic

### Integration Tests

End-to-end tests that verify all components work together correctly.

## Running Tests

You can run all tests using the master test runner:

```bash
python run_tests.py
```

To run specific test categories:

```bash
python run_tests.py --filter multimodal_attacks
python run_tests.py --filter semantic_mirror
python run_tests.py --filter exploit_generator
python run_tests.py --filter frontend
python run_tests.py --filter integration
```

For verbose output:

```bash
python run_tests.py --verbose
```

To generate a test report:

```bash
python run_tests.py --report tests/reports/my_report.json
```

## CI Integration

For continuous integration environments, use the `--ci` flag, which will return a non-zero exit code if any tests fail:

```bash
python run_tests.py --ci
```

## Test Reports

Test reports are saved in JSON format in the `tests/reports` directory by default. They include:

- Test run timestamp
- Number of tests run, passed, failed, and errors
- Pass rate
- Duration
- List of failed tests and errors

## Adding New Tests

To add a new test:

1. Create a new file with the name pattern `test_*.py` in the `tests` directory
2. Implement test cases using the `unittest` framework
3. Run the tests to verify they work as expected

## Mocking External Services

When testing components that interact with external services:

- Use the `unittest.mock` module to mock external dependencies
- For the Anthropic API, use the provided mock classes

Example:

```python
@patch('anthropic.Anthropic')
def test_function(self, mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client
    mock_client.messages.create.return_value = MockResponse("Test response")
    
    # Test code that uses the Anthropic client
```
