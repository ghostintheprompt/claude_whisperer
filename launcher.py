#!/usr/bin/env python3
"""
Claude 4.0 Safeguards Framework & Research Platform

This unified launcher provides access to both the safeguards implementation
and research components through a single interface.

Components:
1. Safeguards Monitor - Real-time safety monitoring
2. Safeguards Client - Safe interaction with Claude API
3. Analytics Dashboard - Visualization of safety metrics
4. Research Platform - Tools for vulnerability research
"""
import argparse
import os
import sys
from pathlib import Path

class UnifiedLauncher:
    """Unified launcher for Claude 4.0 Safeguards Framework & Research Platform"""
    
    def __init__(self):
        """Initialize the launcher"""
        self.base_dir = Path(__file__).parent.absolute()
    
    def launch_monitor(self):
        """Launch the safeguards monitor"""
        print("Launching Claude 4.0 Safeguards Monitor...")
        monitor_path = self.base_dir / "core" / "vulnerability_monitor.py"
        if monitor_path.exists():
            os.system(f"python {monitor_path} --server")
        else:
            print(f"Error: Monitor not found at {monitor_path}")
    
    def launch_client(self):
        """Launch the safeguards client"""
        print("Launching Claude 4.0 Safeguards Client...")
        client_path = self.base_dir / "core" / "safeguards_client.py"
        if client_path.exists():
            os.system(f"python {client_path}")
        else:
            print(f"Error: Client not found at {client_path}")
    
    def launch_dashboard(self):
        """Launch the analytics dashboard"""
        print("Launching Claude 4.0 Analytics Dashboard...")
        dashboard_path = self.base_dir / "tools" / "generate_dashboard.py"
        if dashboard_path.exists():
            os.system(f"python {dashboard_path}")
        else:
            print(f"Error: Dashboard not found at {dashboard_path}")
    
    def run_tests(self, category=None):
        """Run vulnerability tests"""
        print(f"Running Claude 4.0 Vulnerability Tests for category: {category or 'all'}")
        test_path = self.base_dir / "tests" / "test_claude40_pain_points.py"
        if test_path.exists():
            cmd = f"python {test_path}"
            if category:
                cmd += f" --category {category}"
            os.system(cmd)
        else:
            print(f"Error: Tests not found at {test_path}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Claude 4.0 Safeguards Framework & Research Platform")
    parser.add_argument("--monitor", action="store_true", help="Launch the safeguards monitor")
    parser.add_argument("--client", action="store_true", help="Launch the safeguards client")
    parser.add_argument("--dashboard", action="store_true", help="Launch the analytics dashboard")
    parser.add_argument("--test", action="store_true", help="Run vulnerability tests")
    parser.add_argument("--category", type=str, help="Test category (tool-use, reasoning, etc.)")
    
    args = parser.parse_args()
    launcher = UnifiedLauncher()
    
    if args.monitor:
        launcher.launch_monitor()
    elif args.client:
        launcher.launch_client()
    elif args.dashboard:
        launcher.launch_dashboard()
    elif args.test:
        launcher.run_tests(args.category)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
