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
