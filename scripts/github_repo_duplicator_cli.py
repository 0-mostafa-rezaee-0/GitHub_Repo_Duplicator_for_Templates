#!/usr/bin/env python3
"""
Command-line entry point for GitHub Repo Duplicator.
"""

import os
import sys

# Add parent directory to path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import and run the main function
from src.github_repo_duplicator.duplicator import cli_entry_point

if __name__ == "__main__":
    cli_entry_point() 