"""
GitHub Repo Duplicator - A tool for duplicating GitHub repositories.

This package provides a simple way to create a new GitHub repository
based on an existing template repository.
"""

__version__ = "1.2.5"
__author__ = "Mostafa Rezaee"
__license__ = "MIT"

from .cli import main as cli_main
from .duplicator import main as duplicator_main

__all__ = ["duplicator_main", "cli_main"]
