#!/usr/bin/env python3
"""
Claude Safeguards Framework - Interactive Tour

This script provides an interactive tour of the Claude Safeguards Framework,
demonstrating both the research and safeguards capabilities.
"""
import os
import sys
import time
import subprocess
import argparse
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

class FrameworkTour:
    """
    Interactive tour of the Claude Safeguards Framework.
    """
    
    def __init__(self):
        """Initialize the tour"""
        self.base_dir = Path(__file__).parent.absolute()
        self.processes = {}
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a section header"""
        self.clear_screen()
        print(f"\n{Colors.HEADER}{Colors.BOLD}" + "=" * 60 + f"{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{title.center(60)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}" + "=" * 60 + f"{Colors.ENDC}\n")
    
    def wait_for_key(self, message="Press Enter to continue..."):
        """Wait for a key press"""
        input(f"\n{Colors.YELLOW}{message}{Colors.ENDC}")
    
    def run_command(self, cmd, shell=False):
        """Run a command and return its output"""
        try:
            if shell:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"{Colors.RED}Command failed: {stderr}{Colors.ENDC}")
                return False, stderr
            
            return True, stdout
        except Exception as e:
            print(f"{Colors.RED}Error running command: {e}{Colors.ENDC}")
            return False, str(e)
    
    def welcome(self):
        """Show welcome screen"""
        self.print_header("Welcome to the Claude Safeguards Framework Tour")
        
        print(f"{Colors.GREEN}This interactive tour will demonstrate the key capabilities of the framework:{Colors.ENDC}")
        print(f"  {Colors.BLUE}1. Project Structure and Organization{Colors.ENDC}")
        print(f"  {Colors.BLUE}2. Research Methodology and Vulnerability Taxonomy{Colors.ENDC}")
        print(f"  {Colors.BLUE}3. Safeguards Implementation{Colors.ENDC}")
        print(f"  {Colors.BLUE}4. Real-time Safety Monitoring{Colors.ENDC}")
        print(f"  {Colors.BLUE}5. Technical Refinements for Claude 3.7{Colors.ENDC}")
        
        self.wait_for_key()
    
    def show_project_structure(self):
        """Show project structure"""
        self.print_header("Project Structure and Organization")
        
        print(f"{Colors.GREEN}The framework is organized into research and implementation components:{Colors.ENDC}")
        
        # Show directory structure
        success, output = self.run_command(f"find {self.base_dir} -type d -not -path '*/\.*' | sort", shell=True)
        if success:
            dirs = output.strip().split("\n")
            for d in dirs:
                if d == str(self.base_dir):
                    continue
                
                # Display relative path
                rel_path = os.path.relpath(d, self.base_dir)
                
                # Indentation based on directory depth
                depth = rel_path.count(os.sep)
                indent = "  " * depth
                
                # Directory name only
                dir_name = os.path.basename(d)
                
                print(f"{indent}{Colors.BLUE}📁 {dir_name}/{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Each component serves a specific purpose:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• research/{Colors.ENDC} - Vulnerability research tools and methodology")
        print(f"  {Colors.BLUE}• core/{Colors.ENDC} - Core implementation of safeguards")
        print(f"  {Colors.BLUE}• tools/{Colors.ENDC} - Support tools and utilities")
        print(f"  {Colors.BLUE}• docs/{Colors.ENDC} - Comprehensive documentation")
        print(f"  {Colors.BLUE}• patterns/{Colors.ENDC} - Safety pattern definitions")
        print(f"  {Colors.BLUE}• config/{Colors.ENDC} - Configuration files")
        
        self.wait_for_key()
    
    def show_research_methodology(self):
        """Show research methodology"""
        self.print_header("Research Methodology and Vulnerability Taxonomy")
        
        print(f"{Colors.GREEN}The framework implements a systematic research methodology:{Colors.ENDC}")
        
        # Show methodology document
        methodology_path = self.base_dir / "docs" / "RESEARCH_METHODOLOGY.md"
        if methodology_path.exists():
            success, output = self.run_command(["head", "-n", "20", str(methodology_path)])
            if success:
                print(f"\n{Colors.BLUE}Excerpt from RESEARCH_METHODOLOGY.md:{Colors.ENDC}")
                print(f"{Colors.YELLOW}{output}{Colors.ENDC}")
        
        # Show taxonomy document
        taxonomy_path = self.base_dir / "docs" / "VULNERABILITY_TAXONOMY.md"
        if taxonomy_path.exists():
            success, output = self.run_command(["grep", "-A", "10", "Taxonomy Structure", str(taxonomy_path)])
            if success:
                print(f"\n{Colors.BLUE}Vulnerability Taxonomy Structure:{Colors.ENDC}")
                print(f"{Colors.YELLOW}{output}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Key Research Components:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• Multi-dimensional Testing{Colors.ENDC} - Testing across modes and models")
        print(f"  {Colors.BLUE}• Systematic Vulnerability Classification{Colors.ENDC} - Structured taxonomy")
        print(f"  {Colors.BLUE}• Quantitative Analysis{Colors.ENDC} - Statistical evaluation of results")
        print(f"  {Colors.BLUE}• Pattern Recognition{Colors.ENDC} - Identifying vulnerability patterns")
        
        self.wait_for_key()
    
    def show_safeguards_implementation(self):
        """Show safeguards implementation"""
        self.print_header("Safeguards Implementation")
        
        print(f"{Colors.GREEN}The framework implements real-time safeguards based on research findings:{Colors.ENDC}")
        
        # Show client implementation
        client_path = self.base_dir / "core" / "safeguards_client.py"
        if client_path.exists():
            success, output = self.run_command(["head", "-n", "20", str(client_path)])
            if success:
                print(f"\n{Colors.BLUE}Safeguards Client Implementation:{Colors.ENDC}")
                print(f"{Colors.YELLOW}{output}{Colors.ENDC}")
        
        # Show pattern file
        pattern_path = self.base_dir / "patterns" / "policy_patterns.json"
        if pattern_path.exists():
            success, output = self.run_command(["head", "-n", "20", str(pattern_path)])
            if success:
                print(f"\n{Colors.BLUE}Safety Pattern Definitions:{Colors.ENDC}")
                print(f"{Colors.YELLOW}{output}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Key Safeguards Components:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• Pattern-based Detection{Colors.ENDC} - Identifying policy violations")
        print(f"  {Colors.BLUE}• Pre-request Safety Checks{Colors.ENDC} - Preventing unsafe requests")
        print(f"  {Colors.BLUE}• Post-response Safety Verification{Colors.ENDC} - Ensuring safe responses")
        print(f"  {Colors.BLUE}• Child Safety Protections{Colors.ENDC} - Specialized safeguards for minors")
        
        self.wait_for_key()
    
    def show_real_time_monitoring(self):
        """Show real-time monitoring"""
        self.print_header("Real-time Safety Monitoring")
        
        print(f"{Colors.GREEN}The framework provides real-time monitoring of Claude API usage:{Colors.ENDC}")
        
        # Show monitor implementation
        monitor_path = self.base_dir / "core" / "safeguards_monitor.py"
        if monitor_path.exists():
            success, output = self.run_command(["head", "-n", "20", str(monitor_path)])
            if success:
                print(f"\n{Colors.BLUE}Real-time Monitoring Implementation:{Colors.ENDC}")
                print(f"{Colors.YELLOW}{output}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Monitoring Capabilities:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• WebSocket-based Streaming{Colors.ENDC} - Real-time analysis of conversations")
        print(f"  {Colors.BLUE}• Multi-channel Alerts{Colors.ENDC} - Console, log file, and webhook notifications")
        print(f"  {Colors.BLUE}• Configurable Thresholds{Colors.ENDC} - Adjustable sensitivity levels")
        print(f"  {Colors.BLUE}• Comprehensive Logging{Colors.ENDC} - Detailed audit trails")
        
        # Ask if user wants to start the monitor for demonstration
        print(f"\n{Colors.YELLOW}Would you like to start the monitor for demonstration? (y/n){Colors.ENDC}")
        choice = input().lower()
        if choice == 'y':
            print(f"{Colors.BLUE}Starting monitor...{Colors.ENDC}")
            
            try:
                process = subprocess.Popen(
                    [sys.executable, str(monitor_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.processes["monitor"] = process
                
                # Wait a moment to see if it starts
                time.sleep(2)
                if process.poll() is None:
                    print(f"{Colors.GREEN}Monitor started successfully. It will be stopped at the end of the tour.{Colors.ENDC}")
                else:
                    stdout, stderr = process.communicate()
                    print(f"{Colors.RED}Failed to start monitor: {stderr.decode('utf-8')}{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}Error starting monitor: {e}{Colors.ENDC}")
        
        self.wait_for_key()
    
    def show_technical_refinements(self):
        """Show technical refinements"""
        self.print_header("Technical Refinements for Claude 3.7")
        
        print(f"{Colors.GREEN}Based on research findings, we've developed technical refinement proposals:{Colors.ENDC}")
        
        # Show refinements document
        refinements_path = self.base_dir / "docs" / "TECHNICAL_REFINEMENTS.md"
        if refinements_path.exists():
            success, output = self.run_command(["grep", "-A", "15", "Technical Refinement Proposal", str(refinements_path)])
            if success:
                print(f"\n{Colors.BLUE}Example Technical Refinement Proposal:{Colors.ENDC}")
                print(f"{Colors.YELLOW}{output}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Key Technical Refinements:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• Instruction Processing Enhancements{Colors.ENDC} - Improved handling of complex instructions")
        print(f"  {Colors.BLUE}• Mode-Specific Safety Boundaries{Colors.ENDC} - Consistent safety across Quick and Depth modes")
        print(f"  {Colors.BLUE}• Context-Aware Safety Monitoring{Colors.ENDC} - Tracking safety across conversation turns")
        print(f"  {Colors.BLUE}• Enhanced Output Generation Controls{Colors.ENDC} - Safer handling of complex output formats")
        
        self.wait_for_key()
    
    def conclusion(self):
        """Show conclusion"""
        self.print_header("Tour Conclusion")
        
        print(f"{Colors.GREEN}Thank you for exploring the Claude Safeguards Framework!{Colors.ENDC}")
        print(f"\nThis framework demonstrates both:")
        print(f"  {Colors.BLUE}1. Deep technical understanding of Claude 3.7's architecture and capabilities{Colors.ENDC}")
        print(f"  {Colors.BLUE}2. Comprehensive approach to AI safety and user well-being{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Key Framework Strengths:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• Research-backed Implementation{Colors.ENDC} - Safety measures based on systematic research")
        print(f"  {Colors.BLUE}• Scalable Architecture{Colors.ENDC} - Designed for integration into production systems")
        print(f"  {Colors.BLUE}• Comprehensive Documentation{Colors.ENDC} - Detailed guides and technical documentation")
        print(f"  {Colors.BLUE}• Practical Refinement Proposals{Colors.ENDC} - Actionable improvements for Claude 3.7")
        
        print(f"\n{Colors.GREEN}To explore further:{Colors.ENDC}")
        print(f"  {Colors.BLUE}• Run the launcher:{Colors.ENDC} python launcher.py --all")
        print(f"  {Colors.BLUE}• Explore the documentation:{Colors.ENDC} docs/")
        print(f"  {Colors.BLUE}• Try the research tools:{Colors.ENDC} python research/index.py --list")
        
        # Stop any running processes
        for name, process in self.processes.items():
            if process and process.poll() is None:
                print(f"\n{Colors.YELLOW}Stopping {name}...{Colors.ENDC}")
                process.terminate()
                process.wait()
        
        self.wait_for_key("Press Enter to exit the tour...")
    
    def run_tour(self):
        """Run the complete tour"""
        try:
            self.welcome()
            self.show_project_structure()
            self.show_research_methodology()
            self.show_safeguards_implementation()
            self.show_real_time_monitoring()
            self.show_technical_refinements()
            self.conclusion()
        except KeyboardInterrupt:
            self.clear_screen()
            print(f"\n{Colors.YELLOW}Tour interrupted.{Colors.ENDC}")
            
            # Stop any running processes
            for name, process in self.processes.items():
                if process and process.poll() is None:
                    print(f"{Colors.YELLOW}Stopping {name}...{Colors.ENDC}")
                    process.terminate()
            
            print(f"\n{Colors.GREEN}Thank you for exploring the Claude Safeguards Framework!{Colors.ENDC}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Claude Safeguards Framework Interactive Tour")
    parser.add_argument("--quick", action="store_true", help="Run a shortened version of the tour")
    
    args = parser.parse_args()
    
    tour = FrameworkTour()
    tour.run_tour()

if __name__ == "__main__":
    main()
