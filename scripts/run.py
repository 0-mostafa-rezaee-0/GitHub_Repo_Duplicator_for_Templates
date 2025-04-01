#!/usr/bin/env python3
"""
Simple runner script for GitHub Repo Duplicator.
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Run the main function
from src.github_repo_duplicator.duplicator import cli_entry_point

if __name__ == "__main__":
    cli_entry_point() 