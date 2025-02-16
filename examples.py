#!/usr/bin/env python3
"""
Example usage demonstrations for GitCommitAnalyzer
"""

import os
import subprocess
import sys

def run_example(cmd, description):
    """Run an example command and display the description."""
    print(f"\n{'='*60}")
    print(f"Example: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except Exception as e:
        print(f"Error running example: {e}")

def main():
    """Run all example commands."""
    script = "./git_analyzer.py"
    
    if not os.path.exists(script):
        print("git_analyzer.py not found in current directory!")
        sys.exit(1)
    
    examples = [
        (f"{script} --help", "Display help information"),
        (f"{script}", "Basic analysis of current repository"),
        (f"{script} -f", "Include frequency analysis"),
        (f"{script} -f -v", "Generate frequency analysis with charts"),
        (f"{script} -o json", "Output results in JSON format"),
        (f"{script} -f --export-csv", "Export data to CSV files"),
        (f"{script} -f -v -o html --report my_repo_report.html", 
         "Generate comprehensive HTML report with charts")
    ]
    
    print("GitCommitAnalyzer Usage Examples")
    print("="*40)
    print("This script demonstrates various ways to use GitCommitAnalyzer")
    
    for cmd, desc in examples:
        run_example(cmd, desc)
        input("\nPress Enter to continue to next example...")

if __name__ == '__main__':
    main()