#!/usr/bin/env zsh
# Script to organize research components into a more structured directory layout

# ANSI color codes for better output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "${BLUE}=== Claude Safeguards Framework - Research Organization ===${NC}"
echo "${YELLOW}This script will organize research components into a structured directory layout${NC}"

# Create the research directory structure
mkdir -p research/modes
mkdir -p research/models
mkdir -p research/taxonomy
mkdir -p research/tools
mkdir -p research/patterns
mkdir -p research/reports

echo "${GREEN}Created research directory structure${NC}"

# Move mode comparison files
echo "${BLUE}Organizing mode comparison components...${NC}"
mv mode_comparison_test_suite.json research/modes/
mv mode_comparison_tester.py research/modes/
mv mode_safeguards_comparison.py research/modes/
mv redteam_mode_analyzer.py research/modes/

# Move cross-model comparison files
echo "${BLUE}Organizing cross-model comparison components...${NC}"
mv cross_model_tester.py research/models/

# Move taxonomy and pattern files
echo "${BLUE}Organizing taxonomy and pattern analysis...${NC}"
cp vulnerability_taxonomy.md research/taxonomy/
cp pattern_analyzer.py research/tools/
cp vulnerability_patterns.json research/patterns/
cp advanced_vulnerability_test_suite.json research/patterns/
cp red_team_test_suite.json research/patterns/

# Move analysis tools
echo "${BLUE}Organizing analysis tools...${NC}"
cp analyze_results.py research/tools/
cp benchmark_vulnerability.py research/tools/
cp test_case_generator.py research/tools/

# Move report templates
echo "${BLUE}Organizing report templates...${NC}"
cp vulnerability-report-template.md research/reports/
cp sample-vulnerability-report.md research/reports/

# Create an index.py file in each directory to improve navigation
echo "${BLUE}Creating navigation helpers...${NC}"

cat > research/index.py << 'EOL'
#!/usr/bin/env python3
"""
Claude 3.7 Research Framework

This module provides an entry point to the research components of the
Claude Safeguards Framework, organizing vulnerability research tools
and methodologies.
"""

import os
import argparse
import importlib.util
import sys
from pathlib import Path

def list_components(directory):
    """List Python modules in a directory"""
    path = Path(directory)
    if not path.exists():
        print(f"Directory not found: {directory}")
        return []
    
    return [f.stem for f in path.glob("*.py") if f.stem != "index" and not f.stem.startswith("__")]

def show_header():
    """Display header information"""
    print("\n" + "=" * 60)
    print("Claude 3.7 Research Framework".center(60))
    print("=" * 60 + "\n")
    print("This framework provides tools for systematic vulnerability research")
    print("across multiple dimensions of Claude 3.7 behavior.\n")

def main():
    """Main entry point"""
    show_header()
    
    parser = argparse.ArgumentParser(description="Claude 3.7 Research Framework")
    parser.add_argument("--list", action="store_true", help="List available research components")
    parser.add_argument("--run", help="Run a specific research component")
    parser.add_argument("--mode", help="Specify mode comparison research")
    parser.add_argument("--model", help="Specify cross-model research")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent
    
    if args.list:
        print("Available Research Components:\n")
        
        print("Mode Comparison:")
        for comp in list_components(base_dir / "modes"):
            print(f"  - {comp}")
        
        print("\nModel Comparison:")
        for comp in list_components(base_dir / "models"):
            print(f"  - {comp}")
        
        print("\nAnalysis Tools:")
        for comp in list_components(base_dir / "tools"):
            print(f"  - {comp}")
        
    elif args.mode:
        mode_module = base_dir / "modes" / f"{args.mode}.py"
        if not mode_module.exists():
            print(f"Mode comparison module not found: {args.mode}")
            return
        
        print(f"Running mode comparison: {args.mode}")
        # Import and run the specified module
        spec = importlib.util.spec_from_file_location(args.mode, mode_module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()
        else:
            print("Module does not have a main() function")
    
    elif args.model:
        model_module = base_dir / "models" / f"{args.model}.py"
        if not model_module.exists():
            print(f"Model comparison module not found: {args.model}")
            return
        
        print(f"Running model comparison: {args.model}")
        # Import and run the specified module
        spec = importlib.util.spec_from_file_location(args.model, model_module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()
        else:
            print("Module does not have a main() function")
    
    elif args.run:
        run_path = None
        
        # Search for the module in all directories
        for subdir in ["modes", "models", "tools"]:
            candidate = base_dir / subdir / f"{args.run}.py"
            if candidate.exists():
                run_path = candidate
                break
        
        if not run_path:
            print(f"Research component not found: {args.run}")
            return
        
        print(f"Running research component: {args.run}")
        # Import and run the specified module
        spec = importlib.util.spec_from_file_location(args.run, run_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()
        else:
            print("Module does not have a main() function")
    
    else:
        print("No action specified. Use --list to see available components or --help for usage.")

if __name__ == "__main__":
    main()
EOL

# Make the script executable
chmod +x research/index.py

# Create a README for the research directory
cat > research/README.md << 'EOL'
# Claude 3.7 Vulnerability Research

This directory contains tools and methodologies for systematic research into Claude 3.7 vulnerabilities.

## Directory Structure

- **modes/** - Tools for comparing vulnerabilities across Claude 3.7 modes (Quick vs. Depth)
- **models/** - Tools for cross-model comparison (Claude 3.7 vs. other models)
- **taxonomy/** - Classification system for vulnerabilities
- **tools/** - Analysis utilities and research tools
- **patterns/** - Vulnerability patterns and test suites
- **reports/** - Report templates and example findings

## Getting Started

The `index.py` script provides a unified interface to the research tools:

```bash
# List available research components
python research/index.py --list

# Run mode comparison research
python research/index.py --mode mode_comparison_tester

# Run cross-model comparison
python research/index.py --model cross_model_tester

# Run any research component directly
python research/index.py --run test_case_generator
```

## Key Research Areas

1. **Mode Comparison** - Exploring differences between Quick and Depth modes
2. **Cross-Model Analysis** - Comparing Claude 3.7 with other models
3. **Vulnerability Patterns** - Identifying and classifying vulnerability patterns
4. **Safety Boundary Analysis** - Mapping and testing safety boundaries

## Integration with Safeguards Framework

The research components feed directly into the safeguards implementation:

1. Research identifies vulnerability patterns
2. Patterns are formalized in pattern files
3. Pattern files are integrated into the safeguards framework
4. Safeguards monitor and client implement protective measures

This research-to-implementation pipeline ensures that safety measures are based on empirical evidence and systematic testing.
EOL

echo "${GREEN}✅ Research components organization complete!${NC}"
echo "${YELLOW}The research framework is now available at ./research/${NC}"
echo "${BLUE}Run 'python research/index.py --list' to see available components${NC}"
