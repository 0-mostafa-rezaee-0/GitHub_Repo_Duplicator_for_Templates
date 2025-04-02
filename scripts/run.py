#!/usr/bin/env python3
"""
Entry point script for the GitHub Repo Duplicator.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.github_repo_duplicator.cli import main

if __name__ == "__main__":
    main() 