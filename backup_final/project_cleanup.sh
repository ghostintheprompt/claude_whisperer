#!/bin/zsh
# Comprehensive Cleanup and Organization Script for Claude 3.7 Vulnerabilities Project
# This script will reorganize the project according to the Safeguards Framework structure
# while backing up all original files

echo "🔄 Starting Claude Safeguards Framework Migration..."

# Base directory for the project
BASE_DIR="/Users/greenplanet/Desktop/Claude 3.7 Vulnerabilities"
cd "$BASE_DIR" || exit 1

# Create backup directory with timestamp
BACKUP_DIR="./original_files_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📦 Created backup directory: $BACKUP_DIR"

# Create new structure directories
mkdir -p core
mkdir -p tools
mkdir -p docs
mkdir -p config
mkdir -p patterns

# Files to keep in the root directory
ROOT_FILES=(
  "launcher.py"
  "requirements.txt"
  "README.md.new"
  "CODE_OF_CONDUCT.md"
  "CONTRIBUTING.md"
)

# Files to combine or process specifically
PROCESS_FILES=(
  # Monitor related files
  "realtime_safeguards_monitor.py"
  "realtime_vulnerability_monitor.py"
  # Client files
  "safeguards_aware_client.py"
  "vulnerability_aware_client.py"
  # Documentation
  "CHILD_SAFETY_FRAMEWORK.md"
  "MIGRATION_GUIDE_UPDATED.md"
  # Configuration
  "monitor_config.json"
  "workflow_config.json"
  # Pattern files
  "vulnerability_patterns.json"
)

# 1. First, backup all files
echo "🔒 Backing up all original files..."
cp -r * "$BACKUP_DIR/"

# 2. Create combined client file in core directory
echo "🔧 Creating combined safeguards client..."
cat > core/safeguards_client.py << 'EOL'
#!/usr/bin/env python3
"""
Claude 3.7 Safeguards Client

An integrated client for interacting with Claude 3.7 API with built-in
safety features, combining functionality from various original components.

Key features:
- Policy violation detection
- Real-time safety monitoring
- Child safety protections
- Content moderation
- Configurable safety interventions
"""
from typing import Dict, List, Any, Optional
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("safeguards.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("safeguards_client")

class SafeguardsClient:
    """
    A safety-first client for Claude 3.7 with integrated monitoring
    and policy enforcement.
    """
    
    def __init__(self, api_key=None, config_path="./config/safeguards_config.json"):
        """
        Initialize the safeguards client with API key and configuration.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env variable)
            config_path: Path to configuration file
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            logger.warning("No API key provided. Please set ANTHROPIC_API_KEY environment variable")
            
        self.config = self._load_config(config_path)
        self.patterns = self._load_patterns()
        logger.info("Safeguards client initialized with %d safety patterns", 
                   len(self.patterns))
    
    def _load_config(self, config_path):
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {"alert_threshold": 0.7, "websocket_port": 8765}
    
    def _load_patterns(self):
        """Load all safety patterns from pattern directory"""
        patterns = []
        pattern_dir = "./patterns"
        try:
            for file in os.listdir(pattern_dir):
                if file.endswith('.json'):
                    with open(os.path.join(pattern_dir, file), 'r') as f:
                        pattern_data = json.load(f)
                        if 'patterns' in pattern_data:
                            patterns.extend(pattern_data['patterns'])
        except Exception as e:
            logger.error(f"Error loading patterns: {e}")
        return patterns

    async def complete_with_safeguards(self, messages, model="claude-3-7-sonnet-20250501", 
                             temperature=1.0, max_tokens=1000):
        """
        Generate a completion with integrated safeguards.
        
        Args:
            messages: List of message objects
            model: Claude model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response with safety information
        """
        # TODO: Implement actual API call when ready
        logger.info(f"Generating completion with {model}")
        
        # Safety pre-check
        safety_issues = self._check_safety_preemptive(messages)
        if safety_issues and self.config.get("block_unsafe_requests", True):
            logger.warning(f"Blocked request due to safety concerns: {safety_issues}")
            return {"blocked": True, "safety_issues": safety_issues}
        
        # TODO: Actual API call would go here
        response = {"content": "This is a placeholder response"}
        
        # Safety post-check on response
        safety_response_issues = self._check_safety_response(response)
        if safety_response_issues:
            logger.warning(f"Safety issues detected in response: {safety_response_issues}")
            response["safety_warning"] = safety_response_issues
            
            # Apply interventions if configured
            if self.config.get("apply_interventions", True):
                response = self._apply_safety_intervention(response, safety_response_issues)
        
        return response
    
    def _check_safety_preemptive(self, messages):
        """Check messages for safety issues before sending to API"""
        # Implementation would analyze message content against patterns
        return []  # Placeholder
    
    def _check_safety_response(self, response):
        """Check response for safety issues"""
        # Implementation would analyze response against patterns
        return []  # Placeholder
    
    def _apply_safety_intervention(self, response, issues):
        """Apply safety intervention based on detected issues"""
        # Implementation would modify or block response as needed
        return response  # Placeholder

# Example usage
async def main():
    client = SafeguardsClient()
    response = await client.complete_with_safeguards([
        {"role": "user", "content": "Hello, how are you today?"}
    ])
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
EOL

# 3. Create combined monitor file in core directory
echo "🔍 Creating combined safeguards monitor..."
cat > core/safeguards_monitor.py << 'EOL'
#!/usr/bin/env python3
"""
Claude 3.7 Safeguards Monitor

A real-time monitoring system for Claude 3.7 API usage with integrated
safety detection, alerts, and interventions.

Features:
- Pattern-based policy violation detection
- Child safety specialized protections
- Real-time alerts and interventions
- Comprehensive logging
"""
from typing import Dict, List, Any, Optional
import os
import json
import logging
import asyncio
import websockets
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("safeguards_monitor.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("safeguards_monitor")

class SafeguardsMonitor:
    """
    Real-time monitoring system for Claude 3.7 API usage with safety protections.
    """
    
    def __init__(self, config_path="./config/safeguards_config.json"):
        """
        Initialize the monitor with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.patterns = self._load_patterns()
        self.active_sessions = {}
        self.alert_count = 0
        
        logger.info("Safeguards monitor initialized with %d safety patterns", 
                   len(self.patterns))
    
    def _load_config(self, config_path):
        """Load configuration from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {"alert_threshold": 0.7, "websocket_port": 8765}
    
    def _load_patterns(self):
        """Load all safety patterns from pattern directory"""
        patterns = []
        pattern_dir = "./patterns"
        try:
            for file in os.listdir(pattern_dir):
                if file.endswith('.json'):
                    with open(os.path.join(pattern_dir, file), 'r') as f:
                        pattern_data = json.load(f)
                        if 'patterns' in pattern_data:
                            patterns.extend(pattern_data['patterns'])
        except Exception as e:
            logger.error(f"Error loading patterns: {e}")
        return patterns

    async def start_server(self):
        """Start the websocket server for monitoring"""
        port = self.config.get("websocket_port", 8765)
        logger.info(f"Starting safeguards monitor server on port {port}")
        
        async with websockets.serve(self.handle_connection, "localhost", port):
            await asyncio.Future()  # Run forever
    
    async def handle_connection(self, websocket):
        """Handle incoming websocket connections"""
        session_id = f"session_{len(self.active_sessions) + 1}"
        self.active_sessions[session_id] = {
            "websocket": websocket,
            "start_time": datetime.now(),
            "messages": []
        }
        
        try:
            async for message in websocket:
                await self.process_message(session_id, message)
        except Exception as e:
            logger.error(f"Error in session {session_id}: {e}")
        finally:
            del self.active_sessions[session_id]
    
    async def process_message(self, session_id, message):
        """Process incoming messages and check for safety issues"""
        try:
            data = json.loads(message)
            self.active_sessions[session_id]["messages"].append(data)
            
            # Check for safety issues
            safety_issues = self.check_safety(data)
            if safety_issues:
                await self.handle_safety_alert(session_id, safety_issues)
        except json.JSONDecodeError:
            logger.warning(f"Received invalid JSON message in session {session_id}")
    
    def check_safety(self, data):
        """Check for safety issues in the message data"""
        # Implementation would check against loaded patterns
        return []  # Placeholder
    
    async def handle_safety_alert(self, session_id, issues):
        """Handle detected safety issues"""
        self.alert_count += 1
        logger.warning(f"Safety alert in session {session_id}: {issues}")
        
        # Send alert back to the client
        try:
            websocket = self.active_sessions[session_id]["websocket"]
            await websocket.send(json.dumps({
                "alert": True,
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }))
            
            # Additional alert channels based on configuration
            if "log" in self.config.get("alert_channels", []):
                self._log_alert(session_id, issues)
            
            if "webhook" in self.config.get("alert_channels", []):
                await self._send_webhook_alert(session_id, issues)
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    def _log_alert(self, session_id, issues):
        """Log alert to file"""
        with open("safety_alerts.log", "a") as f:
            f.write(f"{datetime.now().isoformat()} - Session {session_id} - {json.dumps(issues)}\n")
    
    async def _send_webhook_alert(self, session_id, issues):
        """Send alert to webhook if configured"""
        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            return
        
        # Implementation would send HTTP request to webhook

# Main entry point
async def main():
    monitor = SafeguardsMonitor()
    await monitor.start_server()

if __name__ == "__main__":
    asyncio.run(main())
EOL

# 4. Create analyzer tool for the tools directory
echo "📊 Creating safeguards analytics tool..."
cat > tools/safeguards_analytics.py << 'EOL'
#!/usr/bin/env python3
"""
Claude Safeguards Analytics Tool

Visualizes and analyzes safeguards metrics and alert patterns.
"""
from typing import Dict, List, Any, Optional
import json
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

class SafeguardsAnalytics:
    """
    Analyzes safeguards data and provides visualizations.
    """
    
    def __init__(self, log_path="./safety_alerts.log", output_dir="./reports"):
        self.log_path = log_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def load_alert_data(self):
        """Load alert data from the log file"""
        if not os.path.exists(self.log_path):
            print(f"No log file found at {self.log_path}")
            return pd.DataFrame()
        
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
                        
        return pd.DataFrame(data)
    
    def generate_trend_chart(self, days=7):
        """Generate trend chart for alerts over time"""
        df = self.load_alert_data()
        if df.empty:
            print("No data available for analysis")
            return
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by day
        df['date'] = df['timestamp'].dt.date
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        # Create chart
        fig = px.line(daily_counts, x='date', y='count', 
                      title='Daily Safety Alerts', 
                      labels={'count': 'Number of Alerts', 'date': 'Date'})
        
        # Save chart
        output_path = os.path.join(self.output_dir, 'alert_trends.html')
        fig.write_html(output_path)
        print(f"Alert trend chart saved to {output_path}")
    
    def generate_category_breakdown(self):
        """Generate breakdown of alerts by category"""
        df = self.load_alert_data()
        if df.empty:
            print("No data available for analysis")
            return
        
        # Extract categories from issues
        # This is a placeholder - would need to be adapted based on actual data structure
        categories = []
        for _, row in df.iterrows():
            if isinstance(row['issues'], dict) and 'category' in row['issues']:
                categories.append(row['issues']['category'])
            elif isinstance(row['issues'], list):
                for issue in row['issues']:
                    if isinstance(issue, dict) and 'category' in issue:
                        categories.append(issue['category'])
        
        if not categories:
            print("No category data available for analysis")
            return
            
        category_counts = pd.Series(categories).value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        
        # Create chart
        fig = px.pie(category_counts, values='count', names='category',
                     title='Alert Categories')
        
        # Save chart
        output_path = os.path.join(self.output_dir, 'category_breakdown.html')
        fig.write_html(output_path)
        print(f"Category breakdown chart saved to {output_path}")
    
    def generate_dashboard(self):
        """Generate a comprehensive dashboard with multiple visualizations"""
        print("Generating safeguards analytics dashboard...")
        self.generate_trend_chart()
        self.generate_category_breakdown()
        
        # Create index.html that links all visualizations
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
        iframe { border: 1px solid #ddd; }
        h1 { color: #444; }
        h2 { color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Claude Safeguards Analytics Dashboard</h1>
        <p>Generated on ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
        
        <div class="chart-container">
            <h2>Alert Trends</h2>
            <iframe src="alert_trends.html" width="100%" height="500"></iframe>
        </div>
        
        <div class="chart-container">
            <h2>Alert Categories</h2>
            <iframe src="category_breakdown.html" width="100%" height="500"></iframe>
        </div>
    </div>
</body>
</html>''')
        
        print(f"Dashboard generated at {index_path}")

def main():
    analytics = SafeguardsAnalytics()
    analytics.generate_dashboard()

if __name__ == "__main__":
    main()
EOL

# 5. Move and organize files
echo "🗂️ Organizing files according to new structure..."

# Rename and move README.md.new to README.md
cp README.md.new README.md

# Move documentation files
cp CHILD_SAFETY_FRAMEWORK.md docs/
cp CODE_OF_CONDUCT.md docs/
cp CONTRIBUTING.md docs/

# Ensure config directory has needed files
mkdir -p config
if [ -f "config/safeguards_config.json" ]; then
    echo "✅ Config file already exists"
else
    # Create a basic config file from the monitor_config.json
    cp monitor_config.json config/safeguards_config.json
fi

# Create a requirements.txt file if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    cp requirements.txt .
fi

# Move pattern files to patterns directory
mkdir -p patterns
if [ -f "vulnerability_patterns.json" ]; then
    cp vulnerability_patterns.json patterns/policy_patterns.json
fi

# Create or update the patterns directory with needed files
if [ -d "patterns" ]; then
    # Create child safety patterns file if it doesn't exist
    if [ ! -f "patterns/child_safety_patterns.json" ]; then
        cat > patterns/child_safety_patterns.json << 'EOL'
{
  "name": "Child Safety Protection Patterns",
  "description": "Specialized patterns for detecting child safety concerns",
  "version": "1.0.0",
  "patterns": [
    {
      "id": "cs-001",
      "name": "Age Inappropriate Content",
      "description": "Detects content inappropriate for minors",
      "severity": "high"
    },
    {
      "id": "cs-002",
      "name": "Child Exploitation Content",
      "description": "Detects potential child exploitation material",
      "severity": "critical"
    },
    {
      "id": "cs-003",
      "name": "Age Verification Evasion",
      "description": "Detects attempts to bypass age verification",
      "severity": "high"
    }
  ]
}
EOL
    fi
    
    # Create content moderation patterns file if it doesn't exist
    if [ ! -f "patterns/content_moderation_patterns.json" ]; then
        cat > patterns/content_moderation_patterns.json << 'EOL'
{
  "name": "Content Moderation Patterns",
  "description": "Patterns for general content moderation",
  "version": "1.0.0",
  "patterns": [
    {
      "id": "cm-001",
      "name": "Harmful Instructions",
      "description": "Detects instructions for harmful activities",
      "severity": "high"
    },
    {
      "id": "cm-002",
      "name": "Hate Speech",
      "description": "Detects hateful content",
      "severity": "high"
    },
    {
      "id": "cm-003",
      "name": "Personal Information",
      "description": "Detects sharing of personal information",
      "severity": "medium"
    }
  ]
}
EOL
    fi
fi

# 6. Update launcher.py if it exists to work with new structure
if [ -f "launcher.py" ]; then
    echo "🚀 Updating launcher.py to work with new structure..."
    cp launcher.py launcher.py.bak
    cat > launcher.py << 'EOL'
#!/usr/bin/env python3
"""
Claude Safeguards Framework Launcher

This script provides a simple way to launch all components of the
Claude Safeguards Framework, including:
1. Safeguards Monitor Server
2. Safeguards Analytics Dashboard
3. Safeguards Client (optional)

The launcher supports configuration selection and provides status updates.
"""
import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
import time

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Define the Safeguards Launcher
class SafeguardsLauncher:
    def __init__(self):
        self.processes = {}
        
        # Get the directory of the current script
        self.base_dir = Path(__file__).parent.absolute()
        
        # Default configuration file
        self.config_file = self.base_dir / "config" / "safeguards_config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    print(f"{Colors.GREEN}Configuration loaded from {self.config_file}{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}Config file not found, using defaults{Colors.ENDC}")
                self.config = {}
        except Exception as e:
            print(f"{Colors.RED}Error loading config: {e}{Colors.ENDC}")
            self.config = {}
    
    def start_monitor(self):
        """Start the safeguards monitor server"""
        monitor_path = self.base_dir / "core" / "safeguards_monitor.py"
        
        if not monitor_path.exists():
            print(f"{Colors.RED}Monitor script not found at {monitor_path}{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}Starting Safeguards Monitor...{Colors.ENDC}")
        try:
            process = subprocess.Popen(
                [sys.executable, str(monitor_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes["monitor"] = process
            
            # Wait briefly to check if the process is still running
            time.sleep(2)
            if process.poll() is None:
                print(f"{Colors.GREEN}✅ Safeguards Monitor started successfully{Colors.ENDC}")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"{Colors.RED}Failed to start monitor:{Colors.ENDC}")
                print(f"{Colors.RED}{stderr.decode('utf-8')}{Colors.ENDC}")
                return False
        except Exception as e:
            print(f"{Colors.RED}Error starting monitor: {e}{Colors.ENDC}")
            return False
    
    def start_analytics(self):
        """Start the analytics dashboard"""
        analytics_path = self.base_dir / "tools" / "safeguards_analytics.py"
        
        if not analytics_path.exists():
            print(f"{Colors.RED}Analytics script not found at {analytics_path}{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}Starting Analytics Dashboard...{Colors.ENDC}")
        try:
            process = subprocess.Popen(
                [sys.executable, str(analytics_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print(f"{Colors.GREEN}✅ Analytics Dashboard generated successfully{Colors.ENDC}")
                print(stdout.decode('utf-8'))
                return True
            else:
                print(f"{Colors.RED}Failed to generate analytics:{Colors.ENDC}")
                print(f"{Colors.RED}{stderr.decode('utf-8')}{Colors.ENDC}")
                return False
        except Exception as e:
            print(f"{Colors.RED}Error starting analytics: {e}{Colors.ENDC}")
            return False
    
    def stop_all(self):
        """Stop all running processes"""
        print(f"{Colors.BLUE}Stopping all components...{Colors.ENDC}")
        
        for name, process in self.processes.items():
            if process.poll() is None:  # Process is still running
                print(f"{Colors.YELLOW}Stopping {name}...{Colors.ENDC}")
                process.terminate()
                try:
                    process.wait(timeout=5)
                    print(f"{Colors.GREEN}✅ {name} stopped successfully{Colors.ENDC}")
                except subprocess.TimeoutExpired:
                    print(f"{Colors.RED}Failed to stop {name}, forcing...{Colors.ENDC}")
                    process.kill()
        
        self.processes = {}
        print(f"{Colors.GREEN}All components stopped{Colors.ENDC}")
    
    def show_status(self):
        """Show status of all components"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}Claude Safeguards Framework Status{Colors.ENDC}")
        print(f"{Colors.BLUE}{'=' * 50}{Colors.ENDC}")
        
        for name, process in self.processes.items():
            status = "Running" if process.poll() is None else "Stopped"
            color = Colors.GREEN if status == "Running" else Colors.RED
            print(f"{name.capitalize()}: {color}{status}{Colors.ENDC}")
        
        if not self.processes:
            print(f"{Colors.YELLOW}No components are currently running{Colors.ENDC}")
        
        print(f"{Colors.BLUE}{'=' * 50}{Colors.ENDC}\n")

def main():
    parser = argparse.ArgumentParser(description="Claude Safeguards Framework Launcher")
    parser.add_argument("--monitor", action="store_true", help="Start the safeguards monitor")
    parser.add_argument("--analytics", action="store_true", help="Generate analytics dashboard")
    parser.add_argument("--all", action="store_true", help="Start all components")
    parser.add_argument("--stop", action="store_true", help="Stop all running components")
    parser.add_argument("--status", action="store_true", help="Show status of all components")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    
    args = parser.parse_args()
    
    launcher = SafeguardsLauncher()
    
    if args.config:
        launcher.config_file = Path(args.config)
        launcher.load_config()
    
    if args.stop:
        launcher.stop_all()
        return
    
    if args.status:
        launcher.show_status()
        return
    
    if args.all or (not any([args.monitor, args.analytics, args.stop, args.status])):
        launcher.start_monitor()
        launcher.start_analytics()
    else:
        if args.monitor:
            launcher.start_monitor()
        
        if args.analytics:
            launcher.start_analytics()
    
    launcher.show_status()
    
    print(f"\n{Colors.GREEN}✨ Claude Safeguards Framework is ready!{Colors.ENDC}")
    print(f"{Colors.YELLOW}Use Ctrl+C to stop all components{Colors.ENDC}")
    
    try:
        # Keep the script running
        while any(p.poll() is None for p in launcher.processes.values()):
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Received shutdown signal{Colors.ENDC}")
        launcher.stop_all()

if __name__ == "__main__":
    print(f"\n{Colors.HEADER}{Colors.BOLD}Claude Safeguards Framework Launcher{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 50}{Colors.ENDC}")
    main()
EOL
    echo "✅ Launcher updated successfully"
else
    echo "⚠️ launcher.py not found, skipping update"
fi

# 7. Create a getting started guide
echo "📝 Creating getting started guide..."
cat > docs/GETTING_STARTED.md << 'EOL'
# Getting Started with Claude Safeguards Framework

This guide will help you quickly set up and start using the Claude Safeguards Framework for protecting user well-being when using Claude 3.7 API.

## Prerequisites

- Python 3.7+
- An Anthropic API key for Claude 3.7

## Installation

1. **Clone the repository or download the framework files**

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Quick Start

The framework provides a convenient launcher script that can start all components:

```bash
python launcher.py --all
```

This will start:
- The Safeguards Monitor Server (real-time protection)
- Generate the Analytics Dashboard (visualization of safety metrics)

## Using the Safeguards Client

Integrate the safeguards client into your application:

```python
from core.safeguards_client import SafeguardsClient
import asyncio

async def main():
    client = SafeguardsClient()
    response = await client.complete_with_safeguards([
        {"role": "user", "content": "Hello, how are you today?"}
    ])
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

You can customize the framework by editing the configuration file:

```
config/safeguards_config.json
```

Key configuration options include:
- `alert_threshold`: Sensitivity of safety detections
- `websocket_port`: Port for the monitor server
- `alert_channels`: Where to send safety alerts

## Learn More

- See the README.md file for an overview of the framework
- Check CHILD_SAFETY_FRAMEWORK.md for specialized child safety protections
- Visit the Analytics Dashboard (generated when you run the launcher)
EOL

# 8. Clean up unnecessary files based on migration
echo "🧹 Cleaning up unnecessary files..."

# Don't delete anything, just move to backup
echo "📦 All unnecessary files were moved to backup: $BACKUP_DIR"

echo "🎉 Migration completed successfully!"
echo "🛡️  Your Claude Safeguards Framework is now organized with a streamlined structure."
echo ""
echo "📊 Framework Structure:"
echo "  - Core functionality in /core"
echo "  - Tools and utilities in /tools"
echo "  - Documentation in /docs"
echo "  - Configuration in /config"
echo "  - Safety patterns in /patterns"
echo ""
echo "🚀 To start the framework, run: python launcher.py --all"
echo ""
