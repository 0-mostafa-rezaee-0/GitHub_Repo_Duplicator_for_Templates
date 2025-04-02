"""
GitHub Repo Duplicator - A tool for duplicating GitHub repositories.

This package provides a simple way to create a new GitHub repository
based on an existing template repository.
"""

__version__ = '1.1.0'
__author__ = 'Mostafa Rezaee'
__license__ = 'MIT'

from .duplicator import main as duplicator_main
from .cli import main as cli_main

__all__ = ['duplicator_main', 'cli_main'] 