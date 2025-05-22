#!/usr/bin/env python3
"""
Claude 4.0 Pain Point Testing Script

This script allows researchers to easily test Claude 4.0 for specific vulnerability
categories identified in the CLAUDE_4_0_TESTING_PAIN_POINTS.md document.
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: The Anthropic Python SDK is not installed. Please run: pip install anthropic>=0.9.0")
    sys.exit(1)

# Default test categories
TEST_CATEGORIES = [
    "tool-use",
    "reasoning",
    "multimodal",
    "system-prompt",
    "multi-turn",
    "knowledge",
    "api"
]

class Claude40Tester:
    """
    A testing tool for evaluating Claude 4.0 vulnerabilities based on identified pain points.
    """
    
    def __init__(self, api_key: str = None, output_dir: str = "./test_results"):
        """Initialize the tester."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.anthropic = Anthropic(api_key=self.api_key)
        self.results = []
        
        # Load test cases
        self.test_suite_path = Path(__file__).parent / "claude_4_0_red_team_test_suite.json"
        self.load_test_suite()
        
    def load_test_suite(self):
        """Load the test suite from JSON file."""
        try:
            with open(self.test_suite_path, 'r') as f:
                self.test_suite = json.load(f)
            print(f"Loaded {len(self.test_suite.get('test_cases', []))} test cases from {self.test_suite_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading test suite: {e}")
            self.test_suite = {"test_cases": []}
    
    def get_test_cases_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all test cases for a specific category."""
        all_tests = self.test_suite.get("test_cases", [])
        
        # Handle category mapping (e.g., "tool-use" -> "Tool Use")
        category_map = {
            "tool-use": "Tool Use",
            "reasoning": "Reasoning",
            "multimodal": "Multimodal",
            "system-prompt": "System Instructions",
            "multi-turn": "Multi-turn",
            "knowledge": "Knowledge",
            "api": "API"
        }
        
        search_category = category_map.get(category, category)
        
        # Find tests that have this category in their category list
        matching_tests = []
        for test in all_tests:
            if "category" in test and any(search_category.lower() in cat.lower() for cat in test["category"]):
                matching_tests.append(test)
                
        return matching_tests
    
    async def run_test(self, test_case: Dict[str, Any], model: str = "claude-4-sonnet-20240520") -> Dict[str, Any]:
        """Run a single test case and return the results."""
        test_id = test_case.get("id", "UNKNOWN")
        print(f"Running test {test_id}: {test_case.get('title', 'Untitled Test')}")
        
        result = {
            "id": test_id,
            "title": test_case.get("title", "Untitled Test"),
            "category": test_case.get("category", []),
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt": test_case.get("prompt", ""),
            "success_criteria": test_case.get("success_criteria", []),
            "expected_behavior": test_case.get("expected_behavior", ""),
            "vulnerable_behavior": test_case.get("vulnerable_behavior", ""),
        }
        
        # Handle single prompt vs prompt sequence
        if "prompt_sequence" in test_case:
            # Multi-turn conversation test
            messages = []
            responses = []
            
            for i, prompt in enumerate(test_case["prompt_sequence"]):
                print(f"  Turn {i+1}/{len(test_case['prompt_sequence'])}")
                messages.append({"role": "user", "content": prompt})
                
                try:
                    response = self.anthropic.messages.create(
                        model=model,
                        max_tokens=1024,
                        messages=messages
                    )
                    
                    response_text = response.content[0].text
                    responses.append(response_text)
                    messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    print(f"  Error: {e}")
                    result["error"] = str(e)
                    responses.append(f"[ERROR: {e}]")
                    break
            
            result["prompt"] = test_case["prompt_sequence"]
            result["responses"] = responses
            
        else:
            # Single prompt test
            prompt = test_case.get("prompt", "")
            try:
                response = self.anthropic.messages.create(
                    model=model,
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                response_text = response.content[0].text
                result["response"] = response_text
                
            except Exception as e:
                print(f"  Error: {e}")
                result["error"] = str(e)
                result["response"] = f"[ERROR: {e}]"
        
        # Store the result
        self.results.append(result)
        return result
    
    async def run_tests_by_category(self, category: str, model: str = "claude-4-sonnet-20240520") -> List[Dict[str, Any]]:
        """Run all tests for a specific category."""
        tests = self.get_test_cases_by_category(category)
        if not tests:
            print(f"No tests found for category: {category}")
            return []
        
        print(f"Running {len(tests)} tests for category: {category}")
        results = []
        
        for test in tests:
            result = await self.run_test(test, model)
            results.append(result)
            
            # Add a small delay to avoid rate limiting
            await asyncio.sleep(1)
        
        return results
    
    def save_results(self):
        """Save the test results to a JSON file."""
        if not self.results:
            print("No results to save.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"claude40_test_results_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results
            }, f, indent=2)
            
        print(f"Results saved to {output_file}")
    
    def generate_report(self):
        """Generate a human-readable report of the test results."""
        if not self.results:
            print("No results to report.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"claude40_test_report_{timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Claude 4.0 Vulnerability Test Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Group results by category
            categories = {}
            for result in self.results:
                for cat in result.get("category", ["Uncategorized"]):
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(result)
            
            # Write results by category
            for cat, results in categories.items():
                f.write(f"## {cat}\n\n")
                
                for result in results:
                    f.write(f"### {result.get('id', 'UNKNOWN')}: {result.get('title', 'Untitled Test')}\n\n")
                    
                    if "prompt_sequence" in result:
                        f.write("#### Multi-turn Test\n\n")
                        for i, (prompt, response) in enumerate(zip(result.get("prompt", []), result.get("responses", []))):
                            f.write(f"**Turn {i+1}**\n\n")
                            f.write(f"**User:** {prompt}\n\n")
                            f.write(f"**Claude:** {response}\n\n")
                    else:
                        f.write("#### Prompt\n\n")
                        f.write(f"{result.get('prompt', 'No prompt')}\n\n")
                        
                        f.write("#### Response\n\n")
                        f.write(f"{result.get('response', 'No response')}\n\n")
                    
                    f.write("#### Analysis\n\n")
                    f.write(f"**Expected Behavior:** {result.get('expected_behavior', 'Not specified')}\n\n")
                    f.write(f"**Vulnerable Behavior:** {result.get('vulnerable_behavior', 'Not specified')}\n\n")
                    f.write(f"**Success Criteria:**\n\n")
                    
                    for criterion in result.get("success_criteria", []):
                        f.write(f"- {criterion}\n")
                    
                    f.write("\n---\n\n")
            
        print(f"Report generated at {report_file}")

async def main():
    """Main function to run the test script."""
    parser = argparse.ArgumentParser(description="Claude 4.0 Pain Point Testing Script")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY environment variable)")
    parser.add_argument("--categories", nargs="+", choices=TEST_CATEGORIES, default=["tool-use"],
                      help="Categories of tests to run")
    parser.add_argument("--all", action="store_true", help="Run all test categories")
    parser.add_argument("--model", default="claude-4-sonnet-20240520",
                      help="Claude model to test")
    parser.add_argument("--output-dir", default="./test_results",
                      help="Directory to save test results")
    
    args = parser.parse_args()
    
    # Create tester
    tester = Claude40Tester(api_key=args.api_key, output_dir=args.output_dir)
    
    # Determine which categories to test
    categories = TEST_CATEGORIES if args.all else args.categories
    
    # Run tests for each category
    for category in categories:
        await tester.run_tests_by_category(category, args.model)
    
    # Save results and generate report
    tester.save_results()
    tester.generate_report()

if __name__ == "__main__":
    asyncio.run(main())
