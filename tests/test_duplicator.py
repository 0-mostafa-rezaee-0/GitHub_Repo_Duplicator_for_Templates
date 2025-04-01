#!/usr/bin/env python3
"""
Tests for the GitHub Repo Duplicator.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.github_repo_duplicator import duplicator


class TestDuplicator(unittest.TestCase):
    """Test cases for the GitHub Repo Duplicator functions."""

    def test_validate_github_url(self):
        """Test the validate_github_url function with various inputs."""
        # Valid GitHub URLs
        self.assertTrue(duplicator.validate_github_url("https://github.com/user/repo.git"))
        self.assertTrue(duplicator.validate_github_url("https://github.com/user/repo-name.git"))
        
        # Invalid GitHub URLs
        self.assertFalse(duplicator.validate_github_url("https://gitlab.com/user/repo.git"))
        self.assertFalse(duplicator.validate_github_url("https://github.com/user/repo"))
        self.assertFalse(duplicator.validate_github_url("http://github.com/user/repo.git"))
        self.assertFalse(duplicator.validate_github_url(""))
        self.assertFalse(duplicator.validate_github_url("not a url"))

    def test_validate_repo_name(self):
        """Test the validate_repo_name function with various inputs."""
        # Valid repository names
        self.assertTrue(duplicator.validate_repo_name("repo"))
        self.assertTrue(duplicator.validate_repo_name("repo-name"))
        self.assertTrue(duplicator.validate_repo_name("repo_name"))
        self.assertTrue(duplicator.validate_repo_name("repo.name"))
        self.assertTrue(duplicator.validate_repo_name("repo123"))
        
        # Invalid repository names
        self.assertFalse(duplicator.validate_repo_name("repo name"))  # Contains space
        self.assertFalse(duplicator.validate_repo_name("repo/name"))  # Contains slash
        self.assertFalse(duplicator.validate_repo_name("repo:name"))  # Contains colon
        self.assertFalse(duplicator.validate_repo_name(""))  # Empty string

    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        """Test the execute_command function with a successful command."""
        # Setup the mock
        mock_process = MagicMock()
        mock_process.stdout = "Command output"
        mock_run.return_value = mock_process
        
        # Call the function
        result = duplicator.execute_command("echo 'test'", "/bin/bash")
        
        # Assert
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_execute_command_failure(self, mock_run):
        """Test the execute_command function with a failed command."""
        # Setup the mock to raise an exception
        # Create a mock CalledProcessError with compatible arguments for different Python versions
        error = duplicator.subprocess.CalledProcessError(1, "test command")
        error.stderr = "Error message"
        mock_run.side_effect = error
        
        # Call the function
        result = duplicator.execute_command("false", "/bin/bash")
        
        # Assert
        self.assertFalse(result)
        mock_run.assert_called_once()

    def test_get_default_repositories(self):
        """Test the get_default_repositories function."""
        repos = duplicator.get_default_repositories()
        
        # Verify it returns a list of strings
        self.assertIsInstance(repos, list)
        self.assertTrue(all(isinstance(repo, str) for repo in repos))
        
        # Verify each string is a valid GitHub URL
        self.assertTrue(all(duplicator.validate_github_url(repo) for repo in repos))


if __name__ == '__main__':
    unittest.main() 