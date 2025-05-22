#!/usr/bin/env python3
"""
Claude Safeguards Framework & Research Platform

This unified launcher provides access to both the safeguards implementation
and research components through a single interface.

Components:
1. Safeguards Monitor - Real-time safety monitoring
2. Safeguards Client - Safe interaction with Claude API
3. Analytics Dashboard - Visualization of safety metrics
4. Research Platform - Tools for vulnerability research
"""
import os
import sys
import argparse
import subprocess
import time
import json
import webbrowser
from pathlib import Path

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class UnifiedLauncher:
    """
    Unified launcher for both safeguards and research components.
    """
    
    def __init__(self):
        """Initialize the launcher"""
        self.processes = {}
        
        # Set base directory
        self.base_dir = Path(__file__).parent.absolute()
        
        # Define paths
        self.config_dir = self.base_dir / "config"
        self.monitor_path = self.base_dir / "core" / "safeguards_monitor.py"
        self.analytics_path = self.base_dir / "tools" / "safeguards_analytics.py"
        self.research_path = self.base_dir / "research" / "index.py"
        
        # Configuration paths
        self.config_path = self.config_dir / "safeguards_config.json"
        self.launcher_config_path = self.config_dir / "launcher_config.json"
        
        # Load configuration
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from files"""
        config = {
            "monitor_port": 8765,
            "analytics_port": 8766,
            "auto_open_browser": True,
            "enable_research": True
        }
        
        # Try to load launcher config
        if self.launcher_config_path.exists():
            try:
                with open(self.launcher_config_path, 'r') as f:
                    launcher_config = json.load(f)
                    config.update(launcher_config)
                    print(f"{Colors.GREEN}Launcher config loaded{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.YELLOW}Error loading launcher config: {e}{Colors.ENDC}")
        
        # Try to load safeguards config
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    safeguards_config = json.load(f)
                    # Extract relevant config for launcher
                    if "websocket_port" in safeguards_config:
                        config["monitor_port"] = safeguards_config["websocket_port"]
                    print(f"{Colors.GREEN}Safeguards config loaded{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.YELLOW}Error loading safeguards config: {e}{Colors.ENDC}")
        
        return config
    
    def print_banner(self):
        """Display a banner with ASCII art"""
        banner = f"""
{Colors.BLUE}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  {Colors.BOLD}CLAUDE SAFEGUARDS & RESEARCH PLATFORM{Colors.ENDC}{Colors.BLUE}              ║
║                                                          ║
║  {Colors.GREEN}Combined safety enforcement and vulnerability research{Colors.BLUE}  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(banner)
    
    def start_monitor(self):
        """Start the safeguards monitor"""
        if not self.monitor_path.exists():
            print(f"{Colors.RED}Monitor not found at {self.monitor_path}{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}Starting Safeguards Monitor...{Colors.ENDC}")
        
        try:
            # Check if file is executable, make it executable if needed
            if not os.access(self.monitor_path, os.X_OK):
                os.chmod(self.monitor_path, 0o755)
            
            process = subprocess.Popen(
                [sys.executable, str(self.monitor_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["monitor"] = process
            
            # Check if process started successfully
            time.sleep(1)
            if process.poll() is None:
                print(f"{Colors.GREEN}✅ Safeguards Monitor started successfully{Colors.ENDC}")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"{Colors.RED}Failed to start monitor: {stderr}{Colors.ENDC}")
                return False
        except Exception as e:
            print(f"{Colors.RED}Error starting monitor: {e}{Colors.ENDC}")
            return False
    
    def start_analytics(self):
        """Start the analytics dashboard"""
        if not self.analytics_path.exists():
            print(f"{Colors.RED}Analytics dashboard not found at {self.analytics_path}{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}Starting Analytics Dashboard...{Colors.ENDC}")
        
        try:
            process = subprocess.Popen(
                [sys.executable, str(self.analytics_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print(f"{Colors.GREEN}✅ Analytics Dashboard generated successfully{Colors.ENDC}")
                
                # Try to open dashboard in browser
                dashboard_path = self.base_dir / "reports" / "dashboard.html"
                if dashboard_path.exists() and self.config.get("auto_open_browser", True):
                    print(f"{Colors.BLUE}Opening dashboard in browser...{Colors.ENDC}")
                    webbrowser.open(str(dashboard_path))
                
                return True
            else:
                print(f"{Colors.RED}Failed to generate analytics: {stderr}{Colors.ENDC}")
                return False
        except Exception as e:
            print(f"{Colors.RED}Error starting analytics: {e}{Colors.ENDC}")
            return False
    
    def run_research_component(self, component=None, research_args=None):
        """Run a research component"""
        if not self.research_path.exists():
            print(f"{Colors.RED}Research platform not found at {self.research_path}{Colors.ENDC}")
            return False
        
        if not self.config.get("enable_research", True):
            print(f"{Colors.YELLOW}Research platform is disabled in configuration{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}Running Research Platform...{Colors.ENDC}")
        
        try:
            cmd = [sys.executable, str(self.research_path)]
            
            if component:
                cmd.append("--run")
                cmd.append(component)
            elif research_args:
                cmd.extend(research_args)
            else:
                cmd.append("--list")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print(stdout)
                print(f"{Colors.GREEN}✅ Research component completed successfully{Colors.ENDC}")
                return True
            else:
                print(f"{Colors.RED}Error in research component: {stderr}{Colors.ENDC}")
                return False
        except Exception as e:
            print(f"{Colors.RED}Error running research component: {e}{Colors.ENDC}")
            return False
    
    def start_interactive_client(self, model=None):
        """Start an interactive client session"""
        client_path = self.base_dir / "core" / "safeguards_client.py"
        
        if not client_path.exists():
            print(f"{Colors.RED}Client not found at {client_path}{Colors.ENDC}")
            return False
        
        print(f"{Colors.BLUE}Starting Safeguards Client...{Colors.ENDC}")
        
        try:
            # Build command with model if specified
            cmd = [sys.executable, str(client_path)]
            if model:
                cmd.append("--model")
                cmd.append(model)
            
            print(f"{Colors.GREEN}Starting interactive session with Claude{Colors.ENDC}")
            process = subprocess.Popen(cmd)
            self.processes["client"] = process
            
            return True
        except Exception as e:
            print(f"{Colors.RED}Error starting client: {e}{Colors.ENDC}")
            return False
    
    def show_status(self):
        """Show status of all running components"""
        print(f"\n{Colors.HEADER}Component Status{Colors.ENDC}")
        print(f"{Colors.BLUE}{'=' * 50}{Colors.ENDC}")
        
        components = {
            "monitor": {"path": self.monitor_path, "name": "Safeguards Monitor"},
            "client": {"name": "Safeguards Client"},
            "research": {"path": self.research_path, "name": "Research Platform"}
        }
        
        for key, details in components.items():
            # Check if component is in running processes
            if key in self.processes:
                process = self.processes[key]
                if process and process.poll() is None:
                    print(f"{details['name']}: {Colors.GREEN}Running{Colors.ENDC}")
                else:
                    print(f"{details['name']}: {Colors.RED}Stopped{Colors.ENDC}")
            else:
                # Check if component exists
                path = details.get("path")
                if path and path.exists():
                    print(f"{details['name']}: {Colors.YELLOW}Available (not running){Colors.ENDC}")
                else:
                    print(f"{details['name']}: {Colors.RED}Not Available{Colors.ENDC}")
        
        # Check for dashboard
        dashboard_path = self.base_dir / "reports" / "dashboard.html"
        if dashboard_path.exists():
            modified_time = dashboard_path.stat().st_mtime
            modified_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified_time))
            print(f"Analytics Dashboard: {Colors.GREEN}Available (last updated: {modified_str}){Colors.ENDC}")
        else:
            print(f"Analytics Dashboard: {Colors.YELLOW}Not Generated{Colors.ENDC}")
        
        print(f"{Colors.BLUE}{'=' * 50}{Colors.ENDC}\n")
    
    def stop_all(self):
        """Stop all running processes"""
        print(f"{Colors.YELLOW}Stopping all components...{Colors.ENDC}")
        
        for name, process in self.processes.items():
            if process and process.poll() is None:
                print(f"{Colors.YELLOW}Stopping {name}...{Colors.ENDC}")
                process.terminate()
                try:
                    process.wait(timeout=5)
                    print(f"{Colors.GREEN}✅ {name} stopped{Colors.ENDC}")
                except subprocess.TimeoutExpired:
                    print(f"{Colors.RED}Forcing termination of {name}...{Colors.ENDC}")
                    process.kill()
        
        self.processes = {}
        print(f"{Colors.GREEN}All components stopped{Colors.ENDC}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Claude Safeguards Framework & Research Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Launch all safeguards components:
    python launcher.py --all
  
  Run specific research component:
    python launcher.py --research mode_comparison_tester
  
  Start interactive client session:
    python launcher.py --client --model claude-3-7-sonnet
        """
    )
    
    # Safeguards components
    safeguards_group = parser.add_argument_group("Safeguards Components")
    safeguards_group.add_argument("--all", action="store_true", help="Start all safeguards components")
    safeguards_group.add_argument("--monitor", action="store_true", help="Start the safeguards monitor")
    safeguards_group.add_argument("--analytics", action="store_true", help="Generate analytics dashboard")
    safeguards_group.add_argument("--client", action="store_true", help="Start interactive client session")
    safeguards_group.add_argument("--model", help="Model to use with client (default: claude-3-7-sonnet)")
    
    # Research components
    research_group = parser.add_argument_group("Research Components")
    research_group.add_argument("--research", help="Run a specific research component")
    research_group.add_argument("--mode", help="Run mode comparison research")
    research_group.add_argument("--model-compare", dest="model_compare", help="Run cross-model comparison")
    research_group.add_argument("--list-research", action="store_true", help="List available research components")
    
    # Control options
    control_group = parser.add_argument_group("Control Options")
    control_group.add_argument("--stop", action="store_true", help="Stop all running components")
    control_group.add_argument("--status", action="store_true", help="Show status of components")
    
    args = parser.parse_args()
    
    launcher = UnifiedLauncher()
    launcher.print_banner()
    
    try:
        # Handle control options first
        if args.stop:
            launcher.stop_all()
            return
        
        if args.status:
            launcher.show_status()
            return
        
        # Handle safeguards components
        safeguards_started = False
        
        if args.all or args.monitor:
            safeguards_started = launcher.start_monitor()
        
        if args.all or args.analytics:
            launcher.start_analytics()
        
        if args.client:
            launcher.start_interactive_client(args.model)
        
        # Handle research components
        if args.research:
            launcher.run_research_component(args.research)
        elif args.mode:
            launcher.run_research_component(None, ["--mode", args.mode])
        elif args.model_compare:
            launcher.run_research_component(None, ["--model", args.model_compare])
        elif args.list_research:
            launcher.run_research_component()
        
        # If no specific actions were requested, show help and status
        if not any([args.all, args.monitor, args.analytics, args.client, 
                   args.research, args.mode, args.model_compare, args.list_research,
                   args.stop, args.status]):
            print(f"{Colors.YELLOW}No actions specified. Use --help to see available options.{Colors.ENDC}")
            launcher.show_status()
            return
        
        # Show final status
        launcher.show_status()
        
        # Keep running if monitor is active
        monitor_process = launcher.processes.get("monitor")
        if monitor_process and monitor_process.poll() is None:
            print(f"{Colors.GREEN}Monitor is running. Press Ctrl+C to stop all components.{Colors.ENDC}")
            try:
                while monitor_process.poll() is None:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Received interrupt signal{Colors.ENDC}")
                launcher.stop_all()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Received interrupt signal{Colors.ENDC}")
        launcher.stop_all()
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")
        launcher.stop_all()

if __name__ == "__main__":
    main()
