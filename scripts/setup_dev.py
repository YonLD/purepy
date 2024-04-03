#!/usr/bin/env python3
"""
Development environment setup script for Purepy.

This script sets up the development environment with all necessary dependencies.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        sys.exit(1)
    return result

def create_virtual_env():
    """Create a virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("Virtual environment already exists.")
        return
    
    print("Creating virtual environment...")
    venv.create("venv", with_pip=True)

def install_dependencies():
    """Install development dependencies."""
    print("Installing development dependencies...")
    
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Upgrade pip
    run_command(f"{python_path} -m pip install --upgrade pip")
    
    # Install build tools
    run_command(f"{pip_path} install build twine")
    
    # Install development dependencies
    run_command(f"{pip_path} install pytest pytest-cov black flake8 mypy")
    
    # Install package in development mode
    run_command(f"{pip_path} install -e .")

def main():
    """Main setup process."""
    print("Setting up Purepy development environment...")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Create virtual environment
    create_virtual_env()
    
    # Install dependencies
    install_dependencies()
    
    print("\nDevelopment environment setup completed!")
    print("\nTo activate the environment:")
    if os.name == 'nt':  # Windows
        print("  venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("  source venv/bin/activate")
    
    print("\nTo run tests:")
    print("  pytest")
    
    print("\nTo build package:")
    print("  python scripts/build.py")

if __name__ == "__main__":
    main()
