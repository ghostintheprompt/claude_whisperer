#!/usr/bin/env python3
"""
Master test runner for the claude-whisperer test suite.

This script runs all the unit and integration tests, and generates a report of the results.
"""

import os
import sys
import unittest
import time
import json
from datetime import datetime
import argparse

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)


def run_tests(test_filter=None, verbose=False, report_path=None):
    """
    Run the test suite and generate a report.
    
    Args:
        test_filter: Optional filter to run specific tests
        verbose: Whether to print verbose output
        report_path: Path to save the test report
    
    Returns:
        unittest.TestResult: The test result object
    """
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover tests
    start_dir = os.path.join(project_root, 'tests')
    if test_filter:
        pattern = f'test_{test_filter}.py'
    else:
        pattern = 'test_*.py'
    
    print(f"🔍 Discovering tests in {start_dir} with pattern {pattern}")
    suite = loader.discover(start_dir, pattern=pattern)
    
    # Run tests
    print("\n🧪 Running tests...")
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Calculate metrics
    total_tests = result.testsRun
    passed_tests = total_tests - len(result.errors) - len(result.failures)
    pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    duration = end_time - start_time
    
    # Print summary
    print("\n📊 Test Summary:")
    print(f"  - Total tests run: {total_tests}")
    print(f"  - Passed: {passed_tests}")
    print(f"  - Failed: {len(result.failures)}")
    print(f"  - Errors: {len(result.errors)}")
    print(f"  - Pass rate: {pass_rate:.2f}%")
    print(f"  - Duration: {duration:.2f} seconds")
    
    # Generate report
    if report_path:
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": len(result.failures),
            "errors": len(result.errors),
            "pass_rate": pass_rate,
            "duration": duration,
            "failures": [f"{test_case}.{test_method}" for test_case, _ in result.failures],
            "errors": [f"{test_case}.{test_method}" for test_case, _ in result.errors]
        }
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📝 Test report saved to {report_path}")
    
    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Claude Whisperer Test Runner")
    parser.add_argument('--filter', type=str, help='Only run tests matching this filter')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print verbose output')
    parser.add_argument('--report', type=str, help='Path to save the test report')
    parser.add_argument('--ci', action='store_true', help='Run in CI mode (exits with error code on test failure)')
    
    args = parser.parse_args()
    
    # Set default report path if not provided
    if args.report is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.report = os.path.join(project_root, 'tests', 'reports', f'test_report_{timestamp}.json')
    
    # Run tests
    result = run_tests(args.filter, args.verbose, args.report)
    
    # Exit with error code if in CI mode and tests failed
    if args.ci and (result.failures or result.errors):
        sys.exit(1)


if __name__ == '__main__':
    print("🧠 claude-whisperer: Test Runner")
    print("=" * 60)
    main()
