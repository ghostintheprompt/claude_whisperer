#!/usr/bin/env python3
"""
Vulnerability Visualization Dashboard for Claude 3.7 Research

This script generates an interactive HTML dashboard visualizing vulnerability
test results across different models, modes, and vulnerability categories.
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
import numpy as np
import base64
from io import BytesIO

# HTML template for the dashboard
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude 3.7 Vulnerability Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .card {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .card h2 {
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .chart-container {
            width: 100%;
            text-align: center;
            margin-bottom: 30px;
        }
        .chart-image {
            max-width: 100%;
            height: auto;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        .data-table th, .data-table td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .data-table th {
            background-color: #f2f2f2;
        }
        .data-table tr:hover {
            background-color: #f5f5f5;
        }
        .vulnerability-high {
            background-color: #ffdddd;
        }
        .vulnerability-medium {
            background-color: #ffffcc;
        }
        .vulnerability-low {
            background-color: #e6ffe6;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            padding: 20px;
            color: #666;
            font-size: 0.8em;
        }
        .tabs {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
            border-radius: 5px 5px 0 0;
        }
        .tab-button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
        }
        .tab-button:hover {
            background-color: #ddd;
        }
        .tab-button.active {
            background-color: #2c3e50;
            color: white;
        }
        .tab-content {
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 5px 5px;
            animation: fadeEffect 1s;
        }
        @keyframes fadeEffect {
            from {opacity: 0;}
            to {opacity: 1;}
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Claude 3.7 Vulnerability Dashboard</h1>
        <p>Generated: {generation_time}</p>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>Executive Summary</h2>
            <p>This dashboard provides visualizations and analysis of vulnerability testing results for Claude 3.7 across different modes and vulnerability categories.</p>
            <p><strong>Total Tests Run:</strong> {total_tests}</p>
            <p><strong>Models Tested:</strong> {models_tested}</p>
            <p><strong>Most Vulnerable Category:</strong> {most_vulnerable_category}</p>
            <p><strong>Mode Comparison Summary:</strong> {mode_comparison_summary}</p>
        </div>

        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'overview')">Overview</button>
            <button class="tab-button" onclick="openTab(event, 'categories')">Categories</button>
            <button class="tab-button" onclick="openTab(event, 'modes')">Mode Comparison</button>
            <button class="tab-button" onclick="openTab(event, 'details')">Detailed Results</button>
        </div>

        <div id="overview" class="tab-content" style="display: block;">
            <div class="card">
                <h2>Vulnerability Overview</h2>
                <div class="chart-container">
                    <img class="chart-image" src="data:image/png;base64,{overview_chart}" alt="Vulnerability Overview Chart">
                </div>
                <p>{overview_insights}</p>
            </div>
        </div>

        <div id="categories" class="tab-content">
            <div class="card">
                <h2>Vulnerability by Category</h2>
                <div class="chart-container">
                    <img class="chart-image" src="data:image/png;base64,{category_chart}" alt="Vulnerability by Category Chart">
                </div>
                <table class="data-table">
                    <tr>
                        <th>Category</th>
                        <th>Test Count</th>
                        <th>High</th>
                        <th>Medium</th>
                        <th>Low</th>
                        <th>None</th>
                        <th>Success Rate</th>
                    </tr>
                    {category_table_rows}
                </table>
            </div>
        </div>

        <div id="modes" class="tab-content">
            <div class="card">
                <h2>Mode Comparison (Quick vs Depth)</h2>
                <div class="chart-container">
                    <img class="chart-image" src="data:image/png;base64,{mode_chart}" alt="Mode Comparison Chart">
                </div>
                <p>{mode_insights}</p>
                <h3>Tests with Mode Differences</h3>
                <table class="data-table">
                    <tr>
                        <th>Test ID</th>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Quick Mode</th>
                        <th>Depth Mode</th>
                        <th>Difference</th>
                    </tr>
                    {mode_table_rows}
                </table>
            </div>
        </div>

        <div id="details" class="tab-content">
            <div class="card">
                <h2>Detailed Test Results</h2>
                <table class="data-table">
                    <tr>
                        <th>Test ID</th>
                        <th>Model</th>
                        <th>Category</th>
                        <th>Vulnerability Level</th>
                        <th>Success %</th>
                    </tr>
                    {detail_table_rows}
                </table>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Claude 3.7 Vulnerability Research Dashboard | Advanced Research Team | Last Updated: {generation_time}</p>
    </div>

    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tab-button");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
    </script>
</body>
</html>
"""

class VulnerabilityDashboard:
    """Generates an interactive HTML dashboard for vulnerability visualization."""
    
    def __init__(self):
        """Initialize the dashboard generator."""
        self.results = []
        self.test_info = {}
        
    def load_results(self, results_file: str) -> None:
        """Load vulnerability test results from a JSON file."""
        try:
            with open(results_file, 'r') as f:
                self.results = json.load(f)
                
            if not isinstance(self.results, list):
                if "results" in self.results:
                    self.results = self.results["results"]
                else:
                    self.results = [self.results]
                    
            print(f"Loaded {len(self.results)} test results from {results_file}")
        except Exception as e:
            print(f"Error loading results: {str(e)}")
            
    def load_test_info(self, test_suite_files: List[str]) -> None:
        """Load test case metadata from test suite files."""
        for file_path in test_suite_files:
            try:
                with open(file_path, 'r') as f:
                    suite = json.load(f)
                
                test_cases = suite.get("test_cases", [])
                if not test_cases and isinstance(suite, list):
                    test_cases = suite
                
                for test in test_cases:
                    test_id = test.get("vulnerability_id", test.get("id", ""))
                    if test_id:
                        self.test_info[test_id] = {
                            "title": test.get("title", "Unknown"),
                            "category": test.get("category", ["Unknown"]),
                            "severity": test.get("severity", "Unknown")
                        }
                        
                print(f"Loaded {len(test_cases)} test cases from {file_path}")
            except Exception as e:
                print(f"Error loading test suite {file_path}: {str(e)}")
    
    def get_test_metadata(self, test_id: str) -> Dict[str, Any]:
        """Get metadata for a specific test ID."""
        return self.test_info.get(test_id, {"title": "Unknown", "category": ["Unknown"], "severity": "Unknown"})
    
    def create_vulnerability_overview_chart(self) -> str:
        """Create a chart showing overall vulnerability levels."""
        plt.figure(figsize=(10, 6))
        
        vulnerability_counts = {"High": 0, "Medium": 0, "Low": 0, "None": 0}
        
        for result in self.results:
            if "success_criteria" in result:
                level = result["success_criteria"].get("vulnerability_level", "None")
                if level in vulnerability_counts:
                    vulnerability_counts[level] += 1
        
        # Create pie chart
        labels = vulnerability_counts.keys()
        sizes = vulnerability_counts.values()
        colors = ['#ff6666', '#ffcc66', '#99cc99', '#66b3ff']
        explode = (0.1, 0, 0, 0)  # explode the 1st slice (High)
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Overall Vulnerability Distribution')
        
        # Convert plot to base64 string
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return img_str
    
    def create_category_chart(self) -> str:
        """Create a chart showing vulnerability by category."""
        # Group results by category
        category_data = {}
        
        for result in self.results:
            test_id = result.get("test_id", "unknown")
            metadata = self.get_test_metadata(test_id)
            
            for category in metadata["category"]:
                if category not in category_data:
                    category_data[category] = {"High": 0, "Medium": 0, "Low": 0, "None": 0, "total": 0}
                
                if "success_criteria" in result:
                    level = result["success_criteria"].get("vulnerability_level", "None")
                    if level in category_data[category]:
                        category_data[category][level] += 1
                    category_data[category]["total"] += 1
        
        # Prepare data for stacked bar chart
        categories = list(category_data.keys())
        high_values = [category_data[cat]["High"] for cat in categories]
        medium_values = [category_data[cat]["Medium"] for cat in categories]
        low_values = [category_data[cat]["Low"] for cat in categories]
        none_values = [category_data[cat]["None"] for cat in categories]
        
        # Sort categories by vulnerability (high + medium)
        sorted_indices = np.argsort([(h + m) for h, m in zip(high_values, medium_values)])[::-1]
        categories = [categories[i] for i in sorted_indices]
        high_values = [high_values[i] for i in sorted_indices]
        medium_values = [medium_values[i] for i in sorted_indices]
        low_values = [low_values[i] for i in sorted_indices]
        none_values = [none_values[i] for i in sorted_indices]
        
        # Create stacked bar chart
        plt.figure(figsize=(12, 8))
        width = 0.8
        
        plt.bar(categories, high_values, width, label='High', color='#ff6666')
        plt.bar(categories, medium_values, width, bottom=high_values, label='Medium', color='#ffcc66')
        plt.bar(categories, low_values, width, bottom=[i+j for i,j in zip(high_values, medium_values)],
                label='Low', color='#99cc99')
        plt.bar(categories, none_values, width, 
                bottom=[i+j+k for i,j,k in zip(high_values, medium_values, low_values)],
                label='None', color='#66b3ff')
        
        plt.xlabel('Vulnerability Category')
        plt.ylabel('Number of Tests')
        plt.title('Vulnerability Distribution by Category')
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Convert plot to base64 string
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return img_str
    
    def create_mode_comparison_chart(self) -> str:
        """Create a chart comparing Quick vs Depth modes."""
        # Group results by mode
        quick_data = {"High": 0, "Medium": 0, "Low": 0, "None": 0}
        depth_data = {"High": 0, "Medium": 0, "Low": 0, "None": 0}
        
        for result in self.results:
            if "success_criteria" in result:
                level = result["success_criteria"].get("vulnerability_level", "None")
                model = result.get("model", "")
                
                if "quick" in model.lower():
                    if level in quick_data:
                        quick_data[level] += 1
                elif "depth" in model.lower():
                    if level in depth_data:
                        depth_data[level] += 1
        
        # Set up grouped bar chart
        plt.figure(figsize=(10, 6))
        x = np.arange(4)  # 4 vulnerability levels
        width = 0.35
        
        levels = ["High", "Medium", "Low", "None"]
        quick_values = [quick_data[level] for level in levels]
        depth_values = [depth_data[level] for level in levels]
        
        plt.bar(x - width/2, quick_values, width, label='Quick Mode', color='#5DA5DA')
        plt.bar(x + width/2, depth_values, width, label='Depth Mode', color='#F15854')
        
        plt.xlabel('Vulnerability Level')
        plt.ylabel('Number of Tests')
        plt.title('Vulnerability Comparison: Quick vs Depth Mode')
        plt.xticks(x, levels)
        plt.legend()
        plt.tight_layout()
        
        # Convert plot to base64 string
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return img_str
    
    def generate_category_table_rows(self) -> str:
        """Generate HTML table rows for category data."""
        # Group results by category
        category_data = {}
        
        for result in self.results:
            test_id = result.get("test_id", "unknown")
            metadata = self.get_test_metadata(test_id)
            
            for category in metadata["category"]:
                if category not in category_data:
                    category_data[category] = {
                        "High": 0, "Medium": 0, "Low": 0, "None": 0, 
                        "total": 0, "success_total": 0
                    }
                
                if "success_criteria" in result:
                    level = result["success_criteria"].get("vulnerability_level", "None")
                    if level in category_data[category]:
                        category_data[category][level] += 1
                    
                    success_pct = result["success_criteria"].get("success_percentage", 0)
                    category_data[category]["success_total"] += success_pct
                    
                    category_data[category]["total"] += 1
        
        # Sort categories by vulnerability (high + medium)
        sorted_categories = sorted(
            category_data.keys(),
            key=lambda cat: category_data[cat]["High"] + category_data[cat]["Medium"],
            reverse=True
        )
        
        # Generate table rows
        rows = []
        for category in sorted_categories:
            data = category_data[category]
            if data["total"] > 0:
                success_rate = data["success_total"] / data["total"]
            else:
                success_rate = 0
                
            row = f"""<tr>
                <td>{category}</td>
                <td>{data["total"]}</td>
                <td class="vulnerability-high">{data["High"]}</td>
                <td class="vulnerability-medium">{data["Medium"]}</td>
                <td class="vulnerability-low">{data["Low"]}</td>
                <td>{data["None"]}</td>
                <td>{success_rate:.1f}%</td>
            </tr>"""
            rows.append(row)
        
        return "\n".join(rows)
    
    def generate_mode_table_rows(self) -> str:
        """Generate HTML table rows for mode comparison data."""
        # Find tests that have results for both quick and depth modes
        test_pairs = {}
        
        for result in self.results:
            if "success_criteria" in result:
                test_id = result.get("test_id", "unknown")
                model = result.get("model", "")
                
                if test_id not in test_pairs:
                    test_pairs[test_id] = {}
                    
                if "quick" in model.lower():
                    test_pairs[test_id]["quick"] = result
                elif "depth" in model.lower():
                    test_pairs[test_id]["depth"] = result
        
        # Generate rows for tests that show differences
        rows = []
        for test_id, pair in test_pairs.items():
            if "quick" in pair and "depth" in pair:
                quick_level = pair["quick"]["success_criteria"].get("vulnerability_level", "None")
                depth_level = pair["depth"]["success_criteria"].get("vulnerability_level", "None")
                
                # Check if there's a difference in vulnerability level
                if quick_level != depth_level:
                    metadata = self.get_test_metadata(test_id)
                    categories = ", ".join(metadata["category"])
                    
                    if {"None": 0, "Low": 1, "Medium": 2, "High": 3}[depth_level] > \
                       {"None": 0, "Low": 1, "Medium": 2, "High": 3}[quick_level]:
                        difference = "More vulnerable in Depth mode"
                    else:
                        difference = "More vulnerable in Quick mode"
                    
                    row = f"""<tr>
                        <td>{test_id}</td>
                        <td>{metadata["title"]}</td>
                        <td>{categories}</td>
                        <td class="vulnerability-{quick_level.lower()}">{quick_level}</td>
                        <td class="vulnerability-{depth_level.lower()}">{depth_level}</td>
                        <td>{difference}</td>
                    </tr>"""
                    rows.append(row)
        
        return "\n".join(rows)
    
    def generate_detail_table_rows(self) -> str:
        """Generate HTML table rows for detailed results."""
        rows = []
        
        # Sort results by vulnerability level
        sorted_results = sorted(
            self.results,
            key=lambda r: {"None": 0, "Low": 1, "Medium": 2, "High": 3}[
                r.get("success_criteria", {}).get("vulnerability_level", "None")
            ],
            reverse=True
        )
        
        for result in sorted_results:
            if "success_criteria" in result:
                test_id = result.get("test_id", "unknown")
                model = result.get("model", "unknown")
                level = result["success_criteria"].get("vulnerability_level", "None")
                success_pct = result["success_criteria"].get("success_percentage", 0)
                
                metadata = self.get_test_metadata(test_id)
                categories = ", ".join(metadata["category"])
                
                row = f"""<tr>
                    <td>{test_id}</td>
                    <td>{model}</td>
                    <td>{categories}</td>
                    <td class="vulnerability-{level.lower()}">{level}</td>
                    <td>{success_pct:.1f}%</td>
                </tr>"""
                rows.append(row)
        
        return "\n".join(rows)
    
    def generate_insights(self) -> Dict[str, str]:
        """Generate insights from the test results."""
        insights = {}
        
        # Overview insights
        vulnerability_counts = {"High": 0, "Medium": 0, "Low": 0, "None": 0}
        
        for result in self.results:
            if "success_criteria" in result:
                level = result["success_criteria"].get("vulnerability_level", "None")
                if level in vulnerability_counts:
                    vulnerability_counts[level] += 1
        
        total_vulnerable = vulnerability_counts["High"] + vulnerability_counts["Medium"]
        total_tests = sum(vulnerability_counts.values())
        
        if total_tests > 0:
            vulnerability_rate = (total_vulnerable / total_tests) * 100
            insights["overview"] = f"Overall, {vulnerability_rate:.1f}% of tests resulted in Medium or High vulnerability levels. " \
                                f"This indicates areas where safety mechanisms could be strengthened, particularly for " \
                                f"High vulnerability cases which account for {(vulnerability_counts['High'] / total_tests) * 100:.1f}% of all tests."
        else:
            insights["overview"] = "No vulnerability data available."
        
        # Mode comparison insights
        quick_data = {"High": 0, "Medium": 0, "Low": 0, "None": 0, "total": 0}
        depth_data = {"High": 0, "Medium": 0, "Low": 0, "None": 0, "total": 0}
        
        for result in self.results:
            if "success_criteria" in result:
                level = result["success_criteria"].get("vulnerability_level", "None")
                model = result.get("model", "")
                
                if "quick" in model.lower():
                    if level in quick_data:
                        quick_data[level] += 1
                    quick_data["total"] += 1
                elif "depth" in model.lower():
                    if level in depth_data:
                        depth_data[level] += 1
                    depth_data["total"] += 1
        
        if quick_data["total"] > 0 and depth_data["total"] > 0:
            quick_vulnerable = quick_data["High"] + quick_data["Medium"]
            depth_vulnerable = depth_data["High"] + depth_data["Medium"]
            
            quick_rate = (quick_vulnerable / quick_data["total"]) * 100
            depth_rate = (depth_vulnerable / depth_data["total"]) * 100
            
            if depth_rate > quick_rate:
                insights["mode"] = f"Depth mode shows a higher vulnerability rate ({depth_rate:.1f}%) compared to " \
                                f"Quick mode ({quick_rate:.1f}%). This suggests that Depth mode's more comprehensive reasoning " \
                                f"capabilities may lead to increased vulnerability to certain testing techniques, " \
                                f"particularly those involving knowledge boundaries and reasoning chains."
            else:
                insights["mode"] = f"Quick mode shows a higher vulnerability rate ({quick_rate:.1f}%) compared to " \
                                f"Depth mode ({depth_rate:.1f}%). This suggests that Quick mode's more streamlined processing " \
                                f"might be more susceptible to certain vulnerability patterns, potentially due to " \
                                f"reduced context analysis or safety checking."
                                
            # Mode comparison summary
            if abs(depth_rate - quick_rate) > 20:
                comparison = f"Significant difference between modes: {abs(depth_rate - quick_rate):.1f}% difference in vulnerability rates"
            elif abs(depth_rate - quick_rate) > 10:
                comparison = f"Notable difference between modes: {abs(depth_rate - quick_rate):.1f}% difference in vulnerability rates"
            else:
                comparison = f"Similar vulnerability rates between modes: {abs(depth_rate - quick_rate):.1f}% difference"
                
            insights["mode_summary"] = comparison
        else:
            insights["mode"] = "Insufficient data for mode comparison."
            insights["mode_summary"] = "Insufficient data for mode comparison"
        
        # Find most vulnerable category
        category_vulnerability = {}
        
        for result in self.results:
            test_id = result.get("test_id", "unknown")
            metadata = self.get_test_metadata(test_id)
            
            if "success_criteria" in result:
                level = result["success_criteria"].get("vulnerability_level", "None")
                level_score = {"None": 0, "Low": 1, "Medium": 2, "High": 3}[level]
                
                for category in metadata["category"]:
                    if category not in category_vulnerability:
                        category_vulnerability[category] = {"score": 0, "count": 0}
                    
                    category_vulnerability[category]["score"] += level_score
                    category_vulnerability[category]["count"] += 1
        
        if category_vulnerability:
            # Calculate average vulnerability score per category
            for category in category_vulnerability:
                if category_vulnerability[category]["count"] > 0:
                    category_vulnerability[category]["avg"] = category_vulnerability[category]["score"] / category_vulnerability[category]["count"]
                else:
                    category_vulnerability[category]["avg"] = 0
            
            # Find most vulnerable category
            most_vulnerable = max(category_vulnerability.items(), key=lambda x: x[1]["avg"])
            insights["most_vulnerable"] = most_vulnerable[0]
        else:
            insights["most_vulnerable"] = "Unknown"
        
        return insights
    
    def generate_dashboard(self, output_file: str = "vulnerability_dashboard.html") -> None:
        """Generate the complete dashboard HTML file."""
        print("Generating vulnerability dashboard...")
        
        # Generate components
        overview_chart = self.create_vulnerability_overview_chart()
        category_chart = self.create_category_chart()
        mode_chart = self.create_mode_comparison_chart()
        
        category_table_rows = self.generate_category_table_rows()
        mode_table_rows = self.generate_mode_table_rows()
        detail_table_rows = self.generate_detail_table_rows()
        
        insights = self.generate_insights()
        
        # Get models tested
        models = set()
        for result in self.results:
            model = result.get("model", "")
            if model:
                models.add(model)
        models_str = ", ".join(models) if models else "Unknown"
        
        # Fill the HTML template
        html = HTML_TEMPLATE.format(
            generation_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_tests=len(self.results),
            models_tested=models_str,
            most_vulnerable_category=insights.get("most_vulnerable", "Unknown"),
            mode_comparison_summary=insights.get("mode_summary", "N/A"),
            overview_chart=overview_chart,
            category_chart=category_chart,
            mode_chart=mode_chart,
            category_table_rows=category_table_rows,
            mode_table_rows=mode_table_rows,
            detail_table_rows=detail_table_rows,
            overview_insights=insights.get("overview", "No insights available."),
            mode_insights=insights.get("mode", "No mode comparison insights available.")
        )
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(html)
            
        print(f"Dashboard generated and saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate Vulnerability Visualization Dashboard")
    
    parser.add_argument("results_file", help="JSON file containing vulnerability test results")
    parser.add_argument("--output", default="vulnerability_dashboard.html", help="Output HTML file")
    parser.add_argument("--test-suites", nargs="+", 
                      default=["mode_comparison_test_suite.json", "advanced_vulnerability_test_suite.json"],
                      help="Test suite files for metadata")
    
    args = parser.parse_args()
    
    dashboard = VulnerabilityDashboard()
    dashboard.load_results(args.results_file)
    dashboard.load_test_info(args.test_suites)
    dashboard.generate_dashboard(args.output)


if __name__ == "__main__":
    main()
