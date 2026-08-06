#!/usr/bin/env python3
"""
Release script for Purepy package.

This script helps release the package to PyPI.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result

def check_requirements():
    """Check if required tools are installed."""
    required_tools = ['build', 'twine']
    
    for tool in required_tools:
        try:
            run_command(f"python -m {tool} --help")
        except:
            print(f"Error: {tool} is not installed. Install with: pip install {tool}")
            sys.exit(1)

def upload_to_pypi(test=False):
    """Upload package to PyPI or Test PyPI."""
    if test:
        print("Uploading to Test PyPI...")
        run_command("python -m twine upload --repository testpypi dist/*")
        print("\nPackage uploaded to Test PyPI!")
        print("Install with: pip install --index-url https://test.pypi.org/simple/ yonld-purepy")
    else:
        print("Uploading to PyPI...")
        confirmation = input("Are you sure you want to upload to PyPI? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Upload cancelled.")
            return
        
        run_command("python -m twine upload dist/*")
        print("\nPackage uploaded to PyPI!")
        print("Install with: pip install yonld-purepy")

def main():
    """Main release process."""
    parser = argparse.ArgumentParser(description="Release Purepy package")
    parser.add_argument("--test", action="store_true", 
                       help="Upload to Test PyPI instead of PyPI")
    parser.add_argument("--skip-build", action="store_true",
                       help="Skip building and use existing dist files")
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check requirements
    check_requirements()
    
    # Build if not skipping
    if not args.skip_build:
        print("Building package first...")
        run_command("python scripts/build.py")
    
    # Check if dist files exist
    if not os.path.exists("dist") or not os.listdir("dist"):
        print("Error: No distribution files found. Run build first.")
        sys.exit(1)
    
    # Upload
    upload_to_pypi(test=args.test)

if __name__ == "__main__":
    main()
