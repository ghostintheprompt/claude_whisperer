# 🔄 Claude Safeguards Framework Migration Guide

This document outlines how to transition from the current extensive collection of vulnerability detection files to the new streamlined safeguards framework structure.

## New Structure

```
Claude-Safeguards-Framework/
├── README.md                     # Modern, concise project introduction
├── launcher.py                   # Easy startup for all components
├── requirements.txt              # All dependencies in one file
├── core/                         # Core functionality
│   ├── safeguards_client.py      # Main client for interacting with Claude
│   └── safeguards_monitor.py     # Real-time safety monitoring system
├── tools/                        # Utility tools
│   └── safeguards_analytics.py   # Analytics dashboard for visualization
├── docs/                         # Documentation
│   ├── GETTING_STARTED.md        # Quick start guide
│   └── CHILD_SAFETY_FRAMEWORK.md # Child safety specialized protections
├── config/                       # Configuration files
│   └── safeguards_config.json    # Central configuration for all components
└── patterns/                     # Safety patterns
    ├── child_safety_patterns.json # Child safety specialized patterns
    ├── policy_patterns.json       # General policy enforcement patterns
    └── content_moderation_patterns.json # Content moderation patterns
```

## Migration Steps

Follow these steps to migrate from the current repository to the new Claude Safeguards Framework:

### 1. Create the New Structure

```bash
# Create main directories
mkdir -p Claude-Safeguards-Framework/core
mkdir -p Claude-Safeguards-Framework/tools
mkdir -p Claude-Safeguards-Framework/docs
mkdir -p Claude-Safeguards-Framework/config
mkdir -p Claude-Safeguards-Framework/patterns

# Make directory structure accessible
chmod -R 755 Claude-Safeguards-Framework
```

### 2. Copy and Transform Core Files

```bash
# Copy and rename updated files
cp 'Claude 3.7 Vulnerabilities/safeguards_aware_client.py' 'Claude-Safeguards-Framework/core/safeguards_client.py'
cp 'Claude 3.7 Vulnerabilities/realtime_safeguards_monitor.py' 'Claude-Safeguards-Framework/core/safeguards_monitor.py'

# Copy launcher
cp 'Claude 3.7 Vulnerabilities/launcher.py' 'Claude-Safeguards-Framework/launcher.py'

# Make core scripts executable
chmod +x 'Claude-Safeguards-Framework/core/safeguards_client.py'
chmod +x 'Claude-Safeguards-Framework/core/safeguards_monitor.py'
chmod +x 'Claude-Safeguards-Framework/launcher.py'
```

### 3. Copy and Update Documentation

```bash
# Copy key documentation
cp 'Claude 3.7 Vulnerabilities/CHILD_SAFETY_FRAMEWORK.md' 'Claude-Safeguards-Framework/docs/'

# Create new README
cp 'Claude 3.7 Vulnerabilities/README.md' 'Claude-Safeguards-Framework/README.md'
```

### 4. Create Configuration Files

```bash
# Create config files from templates
cat > 'Claude-Safeguards-Framework/config/safeguards_config.json' << 'EOL'
{
  "alert_threshold": 0.7,
  "max_conversation_history": 20,
  "report_interval_minutes": 15,
  "websocket_port": 8765,
  "alert_channels": ["console", "log", "webhook"],
  "webhook_url": "",
  "safeguards_pattern_paths": [
    "patterns/child_safety_patterns.json",
    "patterns/policy_patterns.json",
    "patterns/content_moderation_patterns.json"
  ]
}
EOL

# Create pattern files
cat > 'Claude-Safeguards-Framework/patterns/child_safety_patterns.json' << 'EOL'
[
  {
    "id": "child-safety-001",
    "title": "Child Safety: Inappropriate Content",
    "description": "Detects content inappropriate for minors",
    "pattern": "(?i)(explicit material|adult content|not appropriate for children)",
    "severity": "high",
    "tags": ["child_safety", "content"],
    "recommended_action": "block"
  },
  {
    "id": "child-safety-002",
    "title": "Child Safety: Personal Information",
    "description": "Detects attempts to collect personal information from minors",
    "pattern": "(?i)(where do you live|how old are you|what's your (address|phone|email))",
    "severity": "high",
    "tags": ["child_safety", "privacy"],
    "recommended_action": "block"
  }
]
EOL
```

### 5. Create Requirements File

```bash
# Create requirements file
cat > 'Claude-Safeguards-Framework/requirements.txt' << 'EOL'
# Core dependencies
anthropic>=0.8.0
websockets>=11.0.3
pandas>=2.0.0

# Visualization dependencies
plotly>=5.18.0
dash>=2.14.0

# Testing dependencies
pytest>=7.4.0
pytest-asyncio>=0.21.1

# Documentation
sphinx>=7.2.6
sphinx-rtd-theme>=1.3.0
EOL
```

### 6. Create Analytics Tool

```bash
# Create analytics dashboard script
mkdir -p 'Claude-Safeguards-Framework/tools'
cat > 'Claude-Safeguards-Framework/tools/safeguards_analytics.py' << 'EOL'
#!/usr/bin/env python3
"""
Claude Safeguards Analytics Dashboard

A web-based dashboard for visualizing safeguards data, policy violations,
and safety metrics from the Claude Safeguards Framework.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
import json
import argparse
import os
import sys

# Initialize the Dash app
app = dash.Dash(__name__, title="Claude Safeguards Analytics")

# Create layout
app.layout = html.Div([
    html.H1("Claude Safeguards Analytics Dashboard"),
    html.Div([
        html.H2("Policy Violation Summary"),
        dcc.Graph(id="violation-summary")
    ]),
    html.Div([
        html.H2("Child Safety Metrics"),
        dcc.Graph(id="child-safety-metrics")
    ]),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # Update every 10 seconds
        n_intervals=0
    )
])

# Callback to update violation summary graph
@app.callback(
    Output('violation-summary', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_violation_graph(n):
    # This would normally load data from the monitoring system
    # For now, we'll generate mock data
    data = {
        "categories": ["Content", "Privacy", "Child Safety", "Harmful Instructions", "Misinformation"],
        "counts": [14, 7, 18, 5, 9]
    }
    
    fig = px.bar(
        x=data["categories"],
        y=data["counts"],
        labels={"x": "Violation Category", "y": "Count"},
        title="Policy Violations by Category"
    )
    
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Violation Category",
        yaxis_title="Count",
    )
    
    return fig

# Callback to update child safety metrics
@app.callback(
    Output('child-safety-metrics', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_child_safety_graph(n):
    # Mock time-series data for child safety metrics
    dates = pd.date_range(start="2023-01-01", end="2023-01-10", freq="D")
    detection_counts = [3, 5, 2, 8, 6, 4, 7, 9, 5, 4]
    blocked_counts = [2, 3, 1, 5, 4, 2, 5, 7, 3, 2]
    
    df = pd.DataFrame({
        "date": dates,
        "detections": detection_counts,
        "blocked": blocked_counts
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["detections"],
        mode='lines+markers',
        name='Detections'
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["blocked"],
        mode='lines+markers',
        name='Blocked Responses'
    ))
    
    fig.update_layout(
        title="Child Safety Detections Over Time",
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Count",
    )
    
    return fig

def main():
    parser = argparse.ArgumentParser(description="Claude Safeguards Analytics Dashboard")
    parser.add_argument("--port", type=int, default=8766, help="Port to run the dashboard on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    args = parser.parse_args()
    
    print(f"Starting Safeguards Analytics Dashboard on port {args.port}")
    app.run_server(debug=args.debug, port=args.port, host="0.0.0.0")

if __name__ == "__main__":
    main()
EOL

# Make the script executable
chmod +x 'Claude-Safeguards-Framework/tools/safeguards_analytics.py'
```

### 7. Update Getting Started Guide

```bash
# Create getting started guide
cat > 'Claude-Safeguards-Framework/docs/GETTING_STARTED.md' << 'EOL'
# Getting Started with Claude Safeguards Framework

This guide will help you set up and start using the Claude Safeguards Framework.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An Anthropic API key for Claude access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Claude-Safeguards-Framework.git
   cd Claude-Safeguards-Framework
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Quick Start

The easiest way to start all components is using the launcher script:

```bash
./launcher.py
```

This will start:
- The safeguards monitor server
- The analytics dashboard (opens in your browser)

## Starting an Interactive Session

To start an interactive session with Claude that includes safeguards monitoring:

```bash
./launcher.py --client
```

## Configuration

All configuration is centralized in the `config/safeguards_config.json` file.
Key settings:

- `alert_threshold`: Minimum confidence for policy violation alerts (0.0-1.0)
- `max_conversation_history`: Number of conversation turns to keep in memory
- `websocket_port`: Port for the safeguards monitor WebSocket server
- `safeguards_pattern_paths`: Paths to pattern files for different safeguards

## Advanced Usage

### Using the Safeguards Client in Your Code

```python
from core.safeguards_client import SafeguardsAwareClient

async def main():
    client = SafeguardsAwareClient(api_key="your_api_key")
    await client.connect_to_monitor()
    
    response = await client.get_completion("Hello, Claude!")
    print(response)
    
    await client.close_monitor_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
EOL
```

## Components Not Migrated

The following components from the original repository are not included in the new framework:

1. Advanced testing scripts (cross_model_tester.py, benchmark_vulnerability.py, etc.)
2. Vulnerability taxonomies and categorizations
3. Mode comparison testers
4. Test case generators
5. Detailed vulnerability documentation

## Next Steps

After migrating to the new framework, consider:

1. Updating pattern files with additional safeguards patterns
2. Creating custom analytics visualizations
3. Extending the child safety framework
4. Integrating the framework with your existing applications
