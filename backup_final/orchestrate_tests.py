#!/usr/bin/env python3
"""
Unified Test Orchestration System for Claude 3.7 Vulnerability Research

This script provides a comprehensive command-line interface for coordinating
multiple testing approaches (standard, advanced, cross-model, etc.) with
automated result aggregation and analysis.
"""

import argparse
import json
import os
import sys
import subprocess
import datetime
from typing import Dict, List, Any, Optional
import pandas as pd


class TestOrchestrator:
    """Orchestrates and coordinates different vulnerability testing approaches."""
    
    def __init__(self, output_dir: str = "./reports"):
        """Initialize the orchestrator."""
        self.output_dir = output_dir
        self.results = {
            "standard": [],
            "advanced": [],
            "cross_model": []
        }
        self.report_files = []
        
    def setup_directories(self):
        """Create necessary output directories."""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "standard"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "advanced"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "cross_model"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "aggregated"), exist_ok=True)
        
    def run_standard_tests(self, test_suite: str, models: List[str], simulate: bool = False):
        """Run standard vulnerability tests using the existing framework."""
        print(f"\n{'=' * 80}\nRunning Standard Vulnerability Tests\n{'=' * 80}")
        
        cmd = ["./run_tests.sh"]
        if test_suite:
            cmd.extend(["--test", test_suite])
        
        if "quick" in models and "depth" in models:
            cmd.append("--mode-comparison")
        
        if simulate:
            cmd.append("--simulate")
            
        cmd.extend(["--output-dir", os.path.join(self.output_dir, "standard")])
        
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            self.report_files.append(os.path.join(self.output_dir, "standard", "vulnerability_report.md"))
            print("Standard tests completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running standard tests: {e}")
            
    def run_advanced_tests(self, test_suite: str, models: List[str], simulate: bool = False):
        """Run advanced vulnerability tests using the advanced framework."""
        print(f"\n{'=' * 80}\nRunning Advanced Vulnerability Tests\n{'=' * 80}")
        
        cmd = ["./run_advanced_tests.sh", "--test-suite", test_suite]
        
        if "quick" in models and "depth" in models:
            cmd.append("--mode-comparison")
        elif len(models) > 2:
            cmd.append("--cross-model")
            
        if simulate:
            cmd.append("--simulate")
            
        cmd.extend(["--visualize", "--output-dir", os.path.join(self.output_dir, "advanced")])
        
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            self.report_files.append(os.path.join(self.output_dir, "advanced", "vulnerability_report.md"))
            print("Advanced tests completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running advanced tests: {e}")
    
    def run_cross_model_tests(self, test_suite: str, simulate: bool = False):
        """Run cross-model comparison tests."""
        print(f"\n{'=' * 80}\nRunning Cross-Model Vulnerability Tests\n{'=' * 80}")
        
        cmd = ["python3", "./cross_model_tester.py", "--test_file", test_suite,
               "--output_dir", os.path.join(self.output_dir, "cross_model")]
        
        if simulate:
            cmd.append("--simulate")
            
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            self.report_files.append(os.path.join(self.output_dir, "cross_model", "cross_model_report.md"))
            print("Cross-model tests completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running cross-model tests: {e}")
    
    def aggregate_results(self):
        """Aggregate results from different testing approaches."""
        print(f"\n{'=' * 80}\nAggregating Test Results\n{'=' * 80}")
        
        # Load results from each testing approach
        result_files = [
            os.path.join(self.output_dir, "standard", "vulnerability_test_results.json"),
            os.path.join(self.output_dir, "advanced", "vulnerability_test_results.json")
        ]
        
        all_results = []
        
        for file_path in result_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        results = json.load(f)
                        if isinstance(results, list):
                            all_results.extend(results)
                        else:
                            all_results.append(results)
                except Exception as e:
                    print(f"Error loading results from {file_path}: {e}")
        
        # Save aggregated results
        aggregated_file = os.path.join(self.output_dir, "aggregated", "aggregated_results.json")
        with open(aggregated_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"Aggregated {len(all_results)} test results into {aggregated_file}")
        
        return all_results
    
    def generate_comprehensive_report(self, results):
        """Generate a comprehensive report combining insights from all tests."""
        print(f"\n{'=' * 80}\nGenerating Comprehensive Report\n{'=' * 80}")
        
        # Run the analyze_results.py script on the aggregated results
        output_report = os.path.join(self.output_dir, "aggregated", "comprehensive_report.md")
        
        cmd = ["python3", "./analyze_results.py", 
               os.path.join(self.output_dir, "aggregated", "aggregated_results.json"),
               "--report", output_report,
               "--comprehensive"]
        
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print(f"Comprehensive report generated: {output_report}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating comprehensive report: {e}")
            
        # Additionally, create our own report with extended analysis
        self.generate_extended_report(results, output_report)
    
    def generate_extended_report(self, results, output_report):
        """Generate an extended report with additional insights."""
        extended_report = os.path.join(self.output_dir, "aggregated", "extended_analysis.md")
        
        # Create a more elaborate report with cross-cutting insights
        report_content = [
            "# Extended Vulnerability Analysis Report",
            f"\nGenerated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Overview",
            f"\nThis report aggregates and extends findings from multiple testing approaches:",
            "- Standard vulnerability testing",
            "- Advanced multi-turn testing",
            "- Cross-model vulnerability comparison",
            f"\n### Test Coverage",
            f"\nTotal test cases executed: {len(results)}",
        ]
        
        # Add section for test case distribution
        test_types = {}
        for result in results:
            test_id = result.get("test_id", "unknown")
            if test_id.startswith("CLAUDE37-KNOWLEDGE"):
                category = "Knowledge Manipulation"
            elif test_id.startswith("CLAUDE37-MULTITURN"):
                category = "Multi-turn Exploitation"
            elif test_id.startswith("CLAUDE37-PSYCHO"):
                category = "Psychological Manipulation"
            elif test_id.startswith("CLAUDE37-SYSTEM"):
                category = "System Interaction"
            elif test_id.startswith("CLAUDE37-GENERATIVE"):
                category = "Generative Output"
            elif test_id.startswith("CLAUDE37-COMBO"):
                category = "Combination Techniques"
            else:
                category = "Standard Techniques"
                
            if category not in test_types:
                test_types[category] = 0
            test_types[category] += 1
        
        report_content.append("\n### Test Case Distribution")
        report_content.append("\n| Category | Count | Percentage |")
        report_content.append("| -------- | ----- | ---------- |")
        
        for category, count in test_types.items():
            percentage = (count / len(results)) * 100 if results else 0
            report_content.append(f"| {category} | {count} | {percentage:.1f}% |")
            
        # Add mode comparison insights
        report_content.append("\n## Mode-Specific Vulnerability Analysis")
        report_content.append("\nThe following sections analyze differences in vulnerability patterns between Quick and Depth modes.")
        
        # Add sections for other insights
        report_content.append("\n## Multi-Turn Vulnerability Progression")
        report_content.append("\nThis section analyzes how vulnerabilities develop across conversation turns.")
        
        # Add recommendations section
        report_content.append("\n## Key Recommendations")
        report_content.append("\n1. Strengthen knowledge boundary enforcement in Depth mode")
        report_content.append("2. Implement cross-turn context analysis for multi-turn vulnerability detection")
        report_content.append("3. Enhance safety mechanisms for psychological manipulation techniques")
        report_content.append("4. Develop specialized defenses for tool use and API integration vulnerabilities")
        report_content.append("5. Implement format-aware safety controls for structured output generation")
        
        # Write to file
        with open(extended_report, 'w') as f:
            f.write("\n".join(report_content))
            
        print(f"Extended analysis report generated: {extended_report}")
            
    def run_full_test_suite(self, 
                          standard_suite: str = "mode_comparison_test_suite.json",
                          advanced_suite: str = "advanced_vulnerability_test_suite.json",
                          cross_model_suite: str = "",
                          models: List[str] = ["claude-3-7-quick", "claude-3-7-depth"],
                          simulate: bool = False):
        """Run a complete test suite with all testing approaches."""
        self.setup_directories()
        
        # Run standard tests
        if standard_suite:
            self.run_standard_tests(standard_suite, models, simulate)
        
        # Run advanced tests
        if advanced_suite:
            self.run_advanced_tests(advanced_suite, models, simulate)
        
        # Run cross-model tests if specified
        if cross_model_suite:
            self.run_cross_model_tests(cross_model_suite, simulate)
        
        # Aggregate results and generate comprehensive report
        results = self.aggregate_results()
        self.generate_comprehensive_report(results)
        
        print(f"\n{'=' * 80}")
        print(f"All tests completed. Reports available in {self.output_dir}")
        print(f"Main report: {os.path.join(self.output_dir, 'aggregated', 'comprehensive_report.md')}")
        print(f"Extended analysis: {os.path.join(self.output_dir, 'aggregated', 'extended_analysis.md')}")
        print(f"{'=' * 80}")


def main():
    parser = argparse.ArgumentParser(description="Unified Test Orchestration System for Claude 3.7 Vulnerability Research")
    
    parser.add_argument("--output-dir", default="./reports", help="Directory for output reports")
    parser.add_argument("--standard-suite", default="mode_comparison_test_suite.json", help="Standard test suite file")
    parser.add_argument("--advanced-suite", default="advanced_vulnerability_test_suite.json", help="Advanced test suite file")
    parser.add_argument("--cross-model-suite", default="", help="Cross-model test suite file")
    
    parser.add_argument("--models", nargs="+", default=["claude-3-7-quick", "claude-3-7-depth"],
                      help="Models to test against")
    
    parser.add_argument("--standard-only", action="store_true", help="Run only standard tests")
    parser.add_argument("--advanced-only", action="store_true", help="Run only advanced tests")
    parser.add_argument("--cross-model-only", action="store_true", help="Run only cross-model tests")
    
    parser.add_argument("--simulate", action="store_true", help="Run in simulation mode without real API calls")
    
    args = parser.parse_args()
    
    orchestrator = TestOrchestrator(args.output_dir)
    
    if args.standard_only:
        orchestrator.run_standard_tests(args.standard_suite, args.models, args.simulate)
    elif args.advanced_only:
        orchestrator.run_advanced_tests(args.advanced_suite, args.models, args.simulate)
    elif args.cross_model_only:
        orchestrator.run_cross_model_tests(args.cross_model_suite, args.simulate)
    else:
        # Run the full suite
        standard_suite = args.standard_suite if not args.advanced_only else None
        advanced_suite = args.advanced_suite if not args.standard_only else None
        cross_model_suite = args.cross_model_suite if not (args.standard_only or args.advanced_only) else None
        
        orchestrator.run_full_test_suite(standard_suite, advanced_suite, cross_model_suite, 
                                        args.models, args.simulate)


if __name__ == "__main__":
    main()
