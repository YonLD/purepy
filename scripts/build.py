#!/usr/bin/env python3
"""
Build script for Purepy package.

This script helps build and prepare the package for distribution.
"""

import os
import sys
import subprocess
import shutil
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

def clean_build():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    
    # Directories to clean
    dirs_to_clean = ['build', 'dist', 'pure.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")
    
    # Find and remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"Removed {pycache_path}")

def run_tests():
    """Run the test suite."""
    print("Running tests...")
    run_command("python -m pytest tests/ -v")

def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")

def check_package():
    """Check the built package."""
    print("Checking package...")
    run_command("python -m twine check dist/*")

def main():
    """Main build process."""
    print("Starting Purepy build process...")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Clean previous builds
    clean_build()
    
    # Run tests
    run_tests()
    
    # Build package
    build_package()
    
    # Check package
    check_package()
    
    print("\nBuild completed successfully!")
    print("To upload to PyPI:")
    print("  Test PyPI: python -m twine upload --repository testpypi dist/*")
    print("  PyPI: python -m twine upload dist/*")

if __name__ == "__main__":
    main()
