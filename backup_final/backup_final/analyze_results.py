#!/usr/bin/env python3
"""
Claude 3.7 Vulnerability Analysis Tool

This script analyzes the results of vulnerability tests and
provides statistical insights and visualizations.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Any, Optional
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


class VulnerabilityAnalyzer:
    """Analyzes results from vulnerability tests."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.results = []
        self.model_mode_results = {}
        self.category_stats = {}
        self.inconsistency_patterns = {}
    
    def load_results(self, filepath: str) -> None:
        """Load test results from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Handle both single test result and list of results
            if isinstance(data, list):
                self.results = data
            else:
                self.results = [data]
                
            print(f"Loaded {len(self.results)} test results from {filepath}")
        except Exception as e:
            print(f"Error loading results: {str(e)}")
    
    def analyze_mode_differences(self) -> Dict[str, Any]:
        """Analyze differences between Quick and Depth modes."""
        total_tests = len(self.results)
        mode_differences = []
        
        # Count mode-specific vulnerabilities
        quick_only = 0
        depth_only = 0
        both_modes = 0
        neither_mode = 0
        error_cases = 0
        
        for result in self.results:
            modes_data = result.get("modes", {})
            
            # Skip if we don't have both modes
            if "quick" not in modes_data or "depth" not in modes_data:
                continue
                
            # Skip if there were errors
            if "error" in modes_data.get("quick", {}) or "error" in modes_data.get("depth", {}):
                error_cases += 1
                continue
                
            quick_vulnerable = modes_data.get("quick", {}).get("is_vulnerable", False)
            depth_vulnerable = modes_data.get("depth", {}).get("is_vulnerable", False)
            
            if quick_vulnerable and depth_vulnerable:
                both_modes += 1
            elif quick_vulnerable:
                quick_only += 1
                mode_differences.append(result)
            elif depth_vulnerable:
                depth_only += 1
                mode_differences.append(result)
            else:
                neither_mode += 1
        
        valid_tests = total_tests - error_cases
        
        analysis = {
            "total_tests": total_tests,
            "valid_tests": valid_tests,
            "error_cases": error_cases,
            "quick_only_vulnerable": quick_only,
            "depth_only_vulnerable": depth_only,
            "both_modes_vulnerable": both_modes,
            "neither_mode_vulnerable": neither_mode,
            "inconsistency_rate": (quick_only + depth_only) / valid_tests if valid_tests > 0 else 0,
            "mode_differences": mode_differences
        }
        
        return analysis
    
    def analyze_by_category(self) -> Dict[str, Any]:
        """Analyze vulnerabilities by category."""
        categories = {}
        
        for result in self.results:
            # Extract categories from test case or result
            test_categories = []
            if "category" in result:
                test_categories = result["category"]
            elif "test_cases" in result:
                for test_case in result["test_cases"]:
                    if "category" in test_case:
                        test_categories.extend(test_case["category"])
            
            # Skip if no categories
            if not test_categories:
                continue
            
            # Process modes data
            modes_data = result.get("modes", {})
            
            for category in test_categories:
                if category not in categories:
                    categories[category] = {
                        "total": 0,
                        "quick_vulnerable": 0,
                        "depth_vulnerable": 0,
                        "both_vulnerable": 0,
                        "neither_vulnerable": 0,
                        "inconsistent": 0
                    }
                
                categories[category]["total"] += 1
                
                # Skip if we don't have both modes
                if "quick" not in modes_data or "depth" not in modes_data:
                    continue
                    
                # Skip if there were errors
                if "error" in modes_data.get("quick", {}) or "error" in modes_data.get("depth", {}):
                    continue
                    
                quick_vulnerable = modes_data.get("quick", {}).get("is_vulnerable", False)
                depth_vulnerable = modes_data.get("depth", {}).get("is_vulnerable", False)
                
                if quick_vulnerable and depth_vulnerable:
                    categories[category]["both_vulnerable"] += 1
                elif quick_vulnerable:
                    categories[category]["quick_vulnerable"] += 1
                    categories[category]["inconsistent"] += 1
                elif depth_vulnerable:
                    categories[category]["depth_vulnerable"] += 1
                    categories[category]["inconsistent"] += 1
                else:
                    categories[category]["neither_vulnerable"] += 1
        
        # Calculate percentages
        for category, stats in categories.items():
            total = stats["total"]
            if total > 0:
                stats["quick_vulnerable_pct"] = stats["quick_vulnerable"] / total * 100
                stats["depth_vulnerable_pct"] = stats["depth_vulnerable"] / total * 100
                stats["both_vulnerable_pct"] = stats["both_vulnerable"] / total * 100
                stats["neither_vulnerable_pct"] = stats["neither_vulnerable"] / total * 100
                stats["inconsistency_rate"] = stats["inconsistent"] / total * 100
        
        return categories
    
    def analyze_success_criteria(self) -> Dict[str, Any]:
        """Analyze which success criteria are most commonly met."""
        criteria_stats = {}
        criteria_by_mode = {"quick": {}, "depth": {}}
        
        for result in self.results:
            # Extract success criteria
            success_criteria = []
            if "success_criteria" in result:
                success_criteria = result["success_criteria"]
            
            # Skip if no criteria
            if not success_criteria:
                continue
            
            # Process modes data
            modes_data = result.get("modes", {})
            
            for criterion in success_criteria:
                if criterion not in criteria_stats:
                    criteria_stats[criterion] = {
                        "total": 0,
                        "quick_met": 0,
                        "depth_met": 0,
                        "both_met": 0,
                        "neither_met": 0
                    }
                
                criteria_stats[criterion]["total"] += 1
                
                # Check if criterion was met in each mode
                for mode in ["quick", "depth"]:
                    if mode not in modes_data or "error" in modes_data.get(mode, {}):
                        continue
                        
                    response = modes_data.get(mode, {}).get("response", "")
                    
                    # Simple check if criterion appears in response
                    if criterion.lower() in response.lower():
                        if mode == "quick":
                            criteria_stats[criterion]["quick_met"] += 1
                        else:
                            criteria_stats[criterion]["depth_met"] += 1
                        
                        # Count in mode-specific stats
                        if criterion not in criteria_by_mode[mode]:
                            criteria_by_mode[mode][criterion] = 0
                        criteria_by_mode[mode][criterion] += 1
            
            # Calculate both_met and neither_met
            for criterion, stats in criteria_stats.items():
                quick_met = criterion in criteria_by_mode["quick"]
                depth_met = criterion in criteria_by_mode["depth"]
                
                if quick_met and depth_met:
                    stats["both_met"] += 1
                elif not quick_met and not depth_met:
                    stats["neither_met"] += 1
        
        # Calculate percentages
        for criterion, stats in criteria_stats.items():
            total = stats["total"]
            if total > 0:
                stats["quick_met_pct"] = stats["quick_met"] / total * 100
                stats["depth_met_pct"] = stats["depth_met"] / total * 100
                stats["both_met_pct"] = stats["both_met"] / total * 100
                stats["neither_met_pct"] = stats["neither_met"] / total * 100
        
        return {"criteria_stats": criteria_stats, "criteria_by_mode": criteria_by_mode}
    
    def generate_visualizations(self, output_dir: str) -> None:
        """Generate visualizations of the analysis results."""
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Analyze mode differences
            mode_analysis = self.analyze_mode_differences()
            
            # Mode comparison pie chart
            plt.figure(figsize=(10, 7))
            labels = ['Both Modes Vulnerable', 'Quick Only Vulnerable', 'Depth Only Vulnerable', 'Neither Mode Vulnerable']
            sizes = [
                mode_analysis["both_modes_vulnerable"],
                mode_analysis["quick_only_vulnerable"],
                mode_analysis["depth_only_vulnerable"],
                mode_analysis["neither_mode_vulnerable"]
            ]
            colors = ['#ff6666', '#ffcc66', '#6666ff', '#66b266']
            
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True)
            plt.axis('equal')
            plt.title('Claude 3.7 Mode Vulnerability Comparison', fontsize=16)
            plt.tight_layout()
            
            plt.savefig(os.path.join(output_dir, 'mode_comparison_pie.png'))
            
            # Category analysis
            category_analysis = self.analyze_by_category()
            
            # Prepare data for category bar chart
            categories = list(category_analysis.keys())
            quick_only_values = [category_analysis[cat]["quick_vulnerable"] for cat in categories]
            depth_only_values = [category_analysis[cat]["depth_vulnerable"] for cat in categories]
            both_values = [category_analysis[cat]["both_vulnerable"] for cat in categories]
            
            plt.figure(figsize=(12, 8))
            width = 0.25
            x = range(len(categories))
            
            plt.bar([i - width for i in x], quick_only_values, width, label='Quick Only', color='#ffcc66')
            plt.bar(x, both_values, width, label='Both Modes', color='#ff6666')
            plt.bar([i + width for i in x], depth_only_values, width, label='Depth Only', color='#6666ff')
            
            plt.xlabel('Vulnerability Category', fontsize=12)
            plt.ylabel('Number of Vulnerabilities', fontsize=12)
            plt.title('Vulnerabilities by Category and Mode', fontsize=16)
            plt.xticks(x, categories, rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            
            plt.savefig(os.path.join(output_dir, 'category_comparison_bar.png'))
            
            # Success criteria analysis
            criteria_analysis = self.analyze_success_criteria()
            criteria_stats = criteria_analysis["criteria_stats"]
            
            # Top 10 criteria by mode difference
            criteria_diff = {}
            for criterion, stats in criteria_stats.items():
                criteria_diff[criterion] = abs(stats["depth_met"] - stats["quick_met"])
            
            top_criteria = sorted(criteria_diff.items(), key=lambda x: x[1], reverse=True)[:10]
            top_criteria_names = [c[0][:30] + "..." if len(c[0]) > 30 else c[0] for c, _ in top_criteria]
            
            plt.figure(figsize=(12, 8))
            
            # Data for each criterion
            data = []
            for criterion_name in top_criteria_names:
                full_name = next(c for c in criteria_stats.keys() if c.startswith(criterion_name.replace("...", "")))
                stats = criteria_stats[full_name]
                data.append({
                    'Criterion': criterion_name,
                    'Quick Mode': stats["quick_met"],
                    'Depth Mode': stats["depth_met"]
                })
            
            df = pd.DataFrame(data)
            
            # Prepare for grouped bar chart
            quick_values = df['Quick Mode'].values
            depth_values = df['Depth Mode'].values
            x = range(len(top_criteria_names))
            width = 0.35
            
            plt.bar([i - width/2 for i in x], quick_values, width, label='Quick Mode', color='#ffcc66')
            plt.bar([i + width/2 for i in x], depth_values, width, label='Depth Mode', color='#6666ff')
            
            plt.xlabel('Success Criterion', fontsize=12)
            plt.ylabel('Times Criterion Was Met', fontsize=12)
            plt.title('Top Success Criteria with Mode Differences', fontsize=16)
            plt.xticks(x, top_criteria_names, rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            
            plt.savefig(os.path.join(output_dir, 'criteria_mode_diff.png'))
            
            print(f"Visualizations saved to {output_dir}")
            
        except Exception as e:
            print(f"Error generating visualizations: {str(e)}")
    
    def generate_report(self, output_file: str) -> None:
        """Generate a comprehensive analysis report in markdown format."""
        try:
            # Run analyses
            mode_analysis = self.analyze_mode_differences()
            category_analysis = self.analyze_by_category()
            criteria_analysis = self.analyze_success_criteria()
            
            # Format timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate markdown report
            report = f"""# Claude 3.7 Vulnerability Analysis Report
            
## Overview

* **Date**: {timestamp}
* **Total Tests**: {mode_analysis["total_tests"]}
* **Valid Tests**: {mode_analysis["valid_tests"]}
* **Error Cases**: {mode_analysis["error_cases"]}

## Mode Comparison Analysis

* **Both Modes Vulnerable**: {mode_analysis["both_modes_vulnerable"]} ({mode_analysis["both_modes_vulnerable"]/mode_analysis["valid_tests"]*100:.1f}%)
* **Quick Mode Only Vulnerable**: {mode_analysis["quick_only_vulnerable"]} ({mode_analysis["quick_only_vulnerable"]/mode_analysis["valid_tests"]*100:.1f}%)
* **Depth Mode Only Vulnerable**: {mode_analysis["depth_only_vulnerable"]} ({mode_analysis["depth_only_vulnerable"]/mode_analysis["valid_tests"]*100:.1f}%)
* **Neither Mode Vulnerable**: {mode_analysis["neither_mode_vulnerable"]} ({mode_analysis["neither_mode_vulnerable"]/mode_analysis["valid_tests"]*100:.1f}%)
* **Overall Inconsistency Rate**: {mode_analysis["inconsistency_rate"]*100:.1f}%

## Vulnerability Categories

| Category | Total Tests | Quick Only | Depth Only | Both | Neither | Inconsistency Rate |
|----------|-------------|------------|------------|------|---------|-------------------|
"""
            
            # Add category table rows
            for category, stats in category_analysis.items():
                report += f"| {category} | {stats['total']} | {stats['quick_vulnerable']} | {stats['depth_vulnerable']} | {stats['both_vulnerable']} | {stats['neither_vulnerable']} | {stats['inconsistency_rate']:.1f}% |\n"
            
            # Add success criteria analysis
            report += """
## Success Criteria Analysis

| Criterion | Total Tests | Quick Mode Met | Depth Mode Met | Difference |
|-----------|-------------|----------------|----------------|------------|
"""
            
            # Sort criteria by difference between modes
            criteria_stats = criteria_analysis["criteria_stats"]
            sorted_criteria = sorted(
                criteria_stats.items(),
                key=lambda x: abs(x[1]["quick_met"] - x[1]["depth_met"]),
                reverse=True
            )
            
            # Add top 10 criteria with largest differences
            for criterion, stats in sorted_criteria[:10]:
                diff = abs(stats["quick_met"] - stats["depth_met"])
                report += f"| {criterion} | {stats['total']} | {stats['quick_met']} ({stats['quick_met_pct']:.1f}%) | {stats['depth_met']} ({stats['depth_met_pct']:.1f}%) | {diff} |\n"
            
            # Add mode inconsistency examples
            if mode_analysis["mode_differences"]:
                report += """
## Mode Inconsistency Examples

The following test cases showed different results between Quick and Depth modes:

"""
                # Add top 5 examples
                for i, example in enumerate(mode_analysis["mode_differences"][:5]):
                    test_id = example.get("id", f"Test {i+1}")
                    report += f"### {test_id}: {example.get('title', 'Untitled')}\n\n"
                    report += f"**Prompt**: {example.get('prompt', 'No prompt available')[:200]}...\n\n"
                    
                    quick_result = "Vulnerable" if example.get("modes", {}).get("quick", {}).get("is_vulnerable", False) else "Safe"
                    depth_result = "Vulnerable" if example.get("modes", {}).get("depth", {}).get("is_vulnerable", False) else "Safe"
                    
                    report += f"**Quick Mode**: {quick_result}\n\n"
                    report += f"**Depth Mode**: {depth_result}\n\n"
                    report += "---\n\n"
            
            # Write report to file
            with open(output_file, 'w') as f:
                f.write(report)
            
            print(f"Analysis report saved to {output_file}")
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Analyze Claude 3.7 vulnerability test results")
    parser.add_argument("results_file", help="JSON file containing test results")
    parser.add_argument("--report", default="analysis_report.md", help="Output file for analysis report")
    parser.add_argument("--viz", default="./viz", help="Directory for visualization outputs")
    
    args = parser.parse_args()
    
    analyzer = VulnerabilityAnalyzer()
    analyzer.load_results(args.results_file)
    analyzer.generate_report(args.report)
    analyzer.generate_visualizations(args.viz)


if __name__ == "__main__":
    main()
