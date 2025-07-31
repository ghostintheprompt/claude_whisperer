#!/usr/bin/env python3
"""
Claude Safeguards Analytics Dashboard

Visualizes and analyzes safeguards metrics, alert patterns, and vulnerability statistics
with an interactive web dashboard.
"""
from typing import Dict, List, Any, Optional
import os
import sys
import json
import logging
import datetime
import webbrowser
from pathlib import Path
from flask import Flask, render_template, jsonify, request

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("safeguards_analytics")

# Initialize Flask app
app = Flask(__name__, 
           template_folder=str(Path(__file__).parent.parent / "templates"),
           static_folder=str(Path(__file__).parent.parent / "static"))

class SafeguardsAnalytics:
    """
    Analyzes safeguards data and provides visualizations through an interactive dashboard.
    """
    
    def __init__(self, config_path=None, log_path="./safety_alerts.log", output_dir="./reports"):
        """
        Initialize the analytics dashboard.
        
        Args:
            config_path: Path to configuration file
            log_path: Path to log file
            output_dir: Directory for generated reports
        """
        self.log_path = log_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Get base directory
        self.base_dir = Path(__file__).parent.parent.absolute()
        
        # Set default config path if not provided
        if config_path is None:
            config_path = self.base_dir / "config" / "safeguards_config.json"
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Set up data paths
        self.logs_dir = self.base_dir / "logs"
        self.data_dir = self.base_dir / "data"
        
        # Check if template directory exists
        templates_dir = self.base_dir / "templates"
        if not templates_dir.exists():
            logger.warning(f"Templates directory not found at {templates_dir}, creating...")
            os.makedirs(templates_dir, exist_ok=True)
            
            # Create index.html template
            self._create_template_files()
        
        # Check if static directory exists
        static_dir = self.base_dir / "static"
        if not static_dir.exists():
            logger.warning(f"Static directory not found at {static_dir}, creating...")
            os.makedirs(static_dir, exist_ok=True)
            os.makedirs(static_dir / "js", exist_ok=True)
            os.makedirs(static_dir / "css", exist_ok=True)
            
            # Create static files
            self._create_static_files()
    
    def _load_config(self, config_path):
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            dict: Configuration object
        """
        try:
            if Path(config_path).exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    logger.info(f"Configuration loaded from {config_path}")
                    return config
            else:
                logger.warning(f"Configuration file not found at {config_path}")
                return self._default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self._default_config()
    
    def _default_config(self):
        """
        Create default configuration.
        
        Returns:
            dict: Default configuration
        """
        return {
            "analytics": {
                "port": 8766,
                "host": "localhost",
                "log_file": "safeguards.log",
                "alert_log": "alerts.log",
                "data_dir": "data"
            }
        }
    
    def load_alert_data(self):
        """Load alert data from the log file"""
        if not os.path.exists(self.log_path):
            logger.warning(f"No log file found at {self.log_path}")
            return []
        
        data = []
        with open(self.log_path, 'r') as f:
            for line in f:
                parts = line.strip().split(' - ', 2)
                if len(parts) == 3:
                    timestamp, session, issues_json = parts
                    try:
                        issues = json.loads(issues_json)
                        data.append({
                            "timestamp": timestamp,
                            "session": session,
                            "issues": issues
                        })
                    except json.JSONDecodeError:
                        continue
                        
        return data
    
    def generate_trend_report(self, days=7):
        """Generate trend report for alerts over time"""
        data = self.load_alert_data()
        if not data:
            logger.warning("No data available for analysis")
            return
        
        print(f"Generated trend report based on {len(data)} alerts")
    
    def generate_category_breakdown(self):
        """Generate breakdown of alerts by category"""
        data = self.load_alert_data()
        if not data:
            print("No data available for analysis")
            return
        
        # Extract categories from issues - placeholder implementation
        categories = {}
        
        print(f"Generated category breakdown with {len(categories)} categories")
    
    def generate_dashboard(self):
        """Generate a comprehensive dashboard with multiple visualizations"""
        print("Generating safeguards analytics dashboard...")
        self.generate_trend_report()
        self.generate_category_breakdown()
        
        # Create index.html
        index_path = os.path.join(self.output_dir, 'dashboard.html')
        with open(index_path, 'w') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Claude Safeguards Analytics Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .chart-container { margin-bottom: 30px; }
        h1 { color: #444; }
        h2 { color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Claude Safeguards Analytics Dashboard</h1>
        <p>Generated on ''' + datetime.now().isoformat() + '''</p>
        
        <div class="chart-container">
            <h2>Alert Trends</h2>
            <p>No data available for visualization</p>
        </div>
        
        <div class="chart-container">
            <h2>Alert Categories</h2>
            <p>No data available for visualization</p>
        </div>
    </div>
</body>
</html>''')
        
        print(f"Dashboard generated at {index_path}")
    
    def _create_template_files(self):
        """Create template files for the dashboard."""
        # Create the index.html template
        index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Safeguards Framework - Analytics Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Claude Safeguards Analytics</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" href="#overview">Overview</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#alerts">Alerts</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#patterns">Patterns</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#reports">Reports</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5 id="overview">Overview</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="card text-white bg-primary mb-3">
                                    <div class="card-header">Total Requests</div>
                                    <div class="card-body">
                                        <h5 class="card-title" id="total-requests">{{ stats.total_requests }}</h5>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card text-white bg-success mb-3">
                                    <div class="card-header">Safe Requests</div>
                                    <div class="card-body">
                                        <h5 class="card-title" id="safe-requests">{{ stats.safe_requests }}</h5>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card text-white bg-warning mb-3">
                                    <div class="card-header">Warnings</div>
                                    <div class="card-body">
                                        <h5 class="card-title" id="warnings">{{ stats.warnings }}</h5>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card text-white bg-danger mb-3">
                                    <div class="card-header">Blocked</div>
                                    <div class="card-body">
                                        <h5 class="card-title" id="blocked">{{ stats.blocked }}</h5>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row mt-4">
                            <div class="col-md-6">
                                <h5>Requests Over Time</h5>
                                <canvas id="requests-chart"></canvas>
                            </div>
                            <div class="col-md-6">
                                <h5>Alert Categories</h5>
                                <canvas id="categories-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5 id="alerts">Recent Alerts</h5>
                    </div>
                    <div class="card-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Timestamp</th>
                                    <th>Type</th>
                                    <th>Category</th>
                                    <th>Confidence</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="alerts-table">
                                {% for alert in alerts %}
                                <tr>
                                    <td>{{ alert.timestamp }}</td>
                                    <td>{{ alert.type }}</td>
                                    <td>{{ alert.category }}</td>
                                    <td>{{ alert.confidence }}</td>
                                    <td>{{ alert.action }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5 id="patterns">Pattern Effectiveness</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h5>Top Effective Patterns</h5>
                                <canvas id="effective-patterns-chart"></canvas>
                            </div>
                            <div class="col-md-6">
                                <h5>False Positive Rates</h5>
                                <canvas id="false-positives-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4 mb-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5 id="reports">Generate Reports</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Daily Summary</h5>
                                        <p class="card-text">Generate a daily summary report of safeguards activity.</p>
                                        <button class="btn btn-primary" id="daily-report-btn">Generate</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Pattern Analysis</h5>
                                        <p class="card-text">Analyze pattern effectiveness and suggest improvements.</p>
                                        <button class="btn btn-primary" id="pattern-report-btn">Generate</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">Vulnerability Report</h5>
                                        <p class="card-text">Generate a comprehensive vulnerability report.</p>
                                        <button class="btn btn-primary" id="vulnerability-report-btn">Generate</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
</body>
</html>
"""
        
        # Create the template directory if it doesn't exist
        templates_dir = self.base_dir / "templates"
        os.makedirs(templates_dir, exist_ok=True)
        
        # Write the template file
        with open(templates_dir / "index.html", "w") as f:
            f.write(index_html)
            
        logger.info(f"Created index.html template at {templates_dir / 'index.html'}")
    
    def _create_static_files(self):
        """Create static files for the dashboard."""
        # Create the CSS file
        css = """/* Dashboard CSS */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    border: none;
}

.card-header {
    background-color: #f1f3f5;
    border-bottom: none;
    font-weight: 600;
}

.table {
    margin-bottom: 0;
}

canvas {
    max-height: 300px;
}
"""
        
        # Create the JavaScript file
        js = """// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Fetch dashboard data
    fetchDashboardData();
    
    // Set up event listeners for report buttons
    document.getElementById('daily-report-btn').addEventListener('click', generateDailyReport);
    document.getElementById('pattern-report-btn').addEventListener('click', generatePatternReport);
    document.getElementById('vulnerability-report-btn').addEventListener('click', generateVulnerabilityReport);
    
    // Set up refresh interval (every 30 seconds)
    setInterval(fetchDashboardData, 30000);
});

function fetchDashboardData() {
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
        });
}

function updateDashboard(data) {
    // Update statistics
    document.getElementById('total-requests').textContent = data.stats.total_requests;
    document.getElementById('safe-requests').textContent = data.stats.safe_requests;
    document.getElementById('warnings').textContent = data.stats.warnings;
    document.getElementById('blocked').textContent = data.stats.blocked;
    
    // Update alerts table
    const alertsTable = document.getElementById('alerts-table');
    alertsTable.innerHTML = '';
    data.alerts.forEach(alert => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${alert.timestamp}</td>
            <td>${alert.type}</td>
            <td>${alert.category}</td>
            <td>${alert.confidence}</td>
            <td>${alert.action}</td>
        `;
        alertsTable.appendChild(row);
    });
    
    // Update charts
    updateRequestsChart(data.charts.requests_over_time);
    updateCategoriesChart(data.charts.alert_categories);
    updatePatternsChart(data.charts.effective_patterns);
    updateFalsePositivesChart(data.charts.false_positives);
}

let requestsChart = null;
function updateRequestsChart(data) {
    const ctx = document.getElementById('requests-chart').getContext('2d');
    
    if (requestsChart) {
        requestsChart.destroy();
    }
    
    requestsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Total',
                    data: data.total,
                    borderColor: 'rgba(13, 110, 253, 1)',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true
                },
                {
                    label: 'Blocked',
                    data: data.blocked,
                    borderColor: 'rgba(220, 53, 69, 1)',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

let categoriesChart = null;
function updateCategoriesChart(data) {
    const ctx = document.getElementById('categories-chart').getContext('2d');
    
    if (categoriesChart) {
        categoriesChart.destroy();
    }
    
    categoriesChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    'rgba(13, 110, 253, 0.7)',
                    'rgba(25, 135, 84, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(220, 53, 69, 0.7)',
                    'rgba(111, 66, 193, 0.7)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

let patternsChart = null;
function updatePatternsChart(data) {
    const ctx = document.getElementById('effective-patterns-chart').getContext('2d');
    
    if (patternsChart) {
        patternsChart.destroy();
    }
    
    patternsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Effectiveness (%)',
                data: data.values,
                backgroundColor: 'rgba(25, 135, 84, 0.7)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

let falsePositivesChart = null;
function updateFalsePositivesChart(data) {
    const ctx = document.getElementById('false-positives-chart').getContext('2d');
    
    if (falsePositivesChart) {
        falsePositivesChart.destroy();
    }
    
    falsePositivesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'False Positive Rate (%)',
                data: data.values,
                backgroundColor: 'rgba(220, 53, 69, 0.7)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function generateDailyReport() {
    fetch('/api/generate-report?type=daily')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Report generated successfully: ${data.filename}`);
            } else {
                alert(`Error generating report: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error generating report:', error);
            alert('Error generating report. Check the console for details.');
        });
}

function generatePatternReport() {
    fetch('/api/generate-report?type=pattern')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Report generated successfully: ${data.filename}`);
            } else {
                alert(`Error generating report: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error generating report:', error);
            alert('Error generating report. Check the console for details.');
        });
}

function generateVulnerabilityReport() {
    fetch('/api/generate-report?type=vulnerability')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Report generated successfully: ${data.filename}`);
            } else {
                alert(`Error generating report: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error generating report:', error);
            alert('Error generating report. Check the console for details.');
        });
}
"""
        
        # Create the static directories
        static_dir = self.base_dir / "static"
        css_dir = static_dir / "css"
        js_dir = static_dir / "js"
        
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        # Write the CSS file
        with open(css_dir / "dashboard.css", "w") as f:
            f.write(css)
            
        # Write the JavaScript file
        with open(js_dir / "dashboard.js", "w") as f:
            f.write(js)
            
        logger.info(f"Created dashboard.css at {css_dir / 'dashboard.css'}")
        logger.info(f"Created dashboard.js at {js_dir / 'dashboard.js'}")
    
    def generate_sample_data(self):
        """
        Generate sample data for demonstration purposes.
        
        Returns:
            dict: Sample dashboard data
        """
        # Current time
        now = datetime.now()
        
        # Sample alerts
        alerts = [
            {
                "timestamp": (now - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Policy Violation",
                "category": "Hacking",
                "confidence": "0.85",
                "action": "Blocked"
            },
            {
                "timestamp": (now - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Child Safety",
                "category": "Inappropriate",
                "confidence": "0.92",
                "action": "Blocked"
            },
            {
                "timestamp": (now - datetime.timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Content Moderation",
                "category": "Violence",
                "confidence": "0.75",
                "action": "Warning"
            },
            {
                "timestamp": (now - datetime.timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Policy Violation",
                "category": "Illegal Activity",
                "confidence": "0.88",
                "action": "Blocked"
            },
            {
                "timestamp": (now - datetime.timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Prompt Injection",
                "category": "System Prompt",
                "confidence": "0.78",
                "action": "Warning"
            }
        ]
        
        # Sample stats
        stats = {
            "total_requests": 1247,
            "safe_requests": 1192,
            "warnings": 32,
            "blocked": 23
        }
        
        # Sample chart data
        charts = {
            "requests_over_time": {
                "labels": [
                    (now - datetime.timedelta(hours=6)).strftime("%H:%M"),
                    (now - datetime.timedelta(hours=5)).strftime("%H:%M"),
                    (now - datetime.timedelta(hours=4)).strftime("%H:%M"),
                    (now - datetime.timedelta(hours=3)).strftime("%H:%M"),
                    (now - datetime.timedelta(hours=2)).strftime("%H:%M"),
                    (now - datetime.timedelta(hours=1)).strftime("%H:%M"),
                    now.strftime("%H:%M")
                ],
                "total": [178, 190, 203, 175, 182, 195, 124],
                "blocked": [3, 5, 4, 2, 3, 4, 2]
            },
            "alert_categories": {
                "labels": ["Policy Violation", "Child Safety", "Content Moderation", "Prompt Injection", "Data Leakage"],
                "values": [38, 12, 25, 18, 7]
            },
            "effective_patterns": {
                "labels": ["Child Abuse", "Hacking", "Illegal Activity", "System Prompt", "Personal Data"],
                "values": [98, 85, 92, 75, 88]
            },
            "false_positives": {
                "labels": ["Child Abuse", "Hacking", "Illegal Activity", "System Prompt", "Personal Data"],
                "values": [2, 12, 8, 18, 5]
            }
        }
        
        return {
            "alerts": alerts,
            "stats": stats,
            "charts": charts
        }
    
    def run_dashboard(self, host=None, port=None, debug=False):
        """
        Run the dashboard server.
        
        Args:
            host: Host to run on (default from config)
            port: Port to run on (default from config)
            debug: Whether to run in debug mode
        """
        if host is None:
            host = self.config.get("analytics", {}).get("host", "localhost")
            
        if port is None:
            port = self.config.get("analytics", {}).get("port", 8766)
        
        logger.info(f"Starting analytics dashboard on http://{host}:{port}")
        
        # Open browser automatically if configured
        if self.config.get("auto_open_browser", True):
            webbrowser.open(f"http://{host}:{port}")
        
        app.run(host=host, port=port, debug=debug)


# Initialize analytics
analytics = SafeguardsAnalytics()

@app.route('/')
def index():
    """Render the dashboard."""
    # Get sample data for now
    data = analytics.generate_sample_data()
    return render_template('index.html', stats=data["stats"], alerts=data["alerts"])

@app.route('/api/dashboard-data')
def api_dashboard_data():
    """API endpoint for dashboard data."""
    return jsonify(analytics.generate_sample_data())

@app.route('/api/generate-report')
def api_generate_report():
    """API endpoint for generating reports."""
    report_type = request.args.get('type', 'daily')
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{report_type}-report-{timestamp}.pdf"
    
    # In a real implementation, this would generate an actual report
    return jsonify({
        "success": True,
        "filename": filename,
        "download_url": f"/reports/{filename}"
    })

def main():
    """Main entry point."""
    # Support both old and new interfaces
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Safeguards Analytics Dashboard")
    parser.add_argument("--host", default=None, help="Host to run on")
    parser.add_argument("--port", type=int, default=None, help="Port to run on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--dashboard", action="store_true", help="Run the interactive dashboard")
    parser.add_argument("--report", action="store_true", help="Generate a static report")
    
    args = parser.parse_args()
    
    if args.dashboard:
        # Run the dashboard
        analytics.run_dashboard(host=args.host, port=args.port, debug=args.debug)
    else:
        # For backward compatibility, run the old dashboard 
        analytics.generate_dashboard()

if __name__ == "__main__":
    main()
