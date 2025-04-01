#!/usr/bin/env python3
"""
GitHub Repo Duplicator

A tool that allows users to duplicate GitHub repositories with an interactive menu.
It creates a new repository with the same content as the selected template repository.
"""

import os
import shutil
import subprocess
import sys
import logging
import re
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def execute_command(command: str, shell_cmd: str) -> bool:
    """
    Execute a shell command with the specified shell.
    
    Args:
        command: The command to execute.
        shell_cmd: The shell to use (bash or zsh).
        
    Returns:
        True if the command was successful, False otherwise.
    """
    try:
        logger.info(f"Executing command with {shell_cmd}")
        result = subprocess.run(
            command,
            shell=True,
            executable=shell_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.info(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False


def validate_github_url(url: str) -> bool:
    """
    Validate if a URL is a proper GitHub repository URL.
    
    Args:
        url: The URL to validate.
        
    Returns:
        True if the URL is valid, False otherwise.
    """
    return url.startswith("https://github.com/") and url.endswith(".git")


def validate_repo_name(name: str) -> bool:
    """
    Validate if a repository name is valid.
    
    Args:
        name: The repository name to validate.
        
    Returns:
        True if the name is valid, False otherwise.
    """
    # Repository names should not contain spaces or special characters
    return bool(re.match(r'^[a-zA-Z0-9_.-]+$', name))


def duplicate_repository(original_repo: str, new_repo: str, shell_cmd: str,
                         gh_available: bool = False) -> bool:
    """
    Duplicate a GitHub repository.
    
    Args:
        original_repo: The URL of the original repository.
        new_repo: The name of the new repository.
        shell_cmd: The shell to use for command execution.
        gh_available: Whether GitHub CLI is available.
    
    Returns:
        True if the duplication was successful, False otherwise.
    """
    # Extract repository basename without .git
    repo_basename = os.path.basename(original_repo).replace('.git', '')
    
    print("\nInitiating repository duplication...")
    print(f"Source: {original_repo}")
    print(f"Destination: {new_repo}")
    
    if not gh_available:
        logger.info("Using git commands for repository duplication")
        # Script to duplicate the repository using git commands
        script = f"""
        git clone --bare {original_repo} && 
        cd {repo_basename}.git && 
        git push --mirror https://github.com/$(git config user.name)/{new_repo}.git && 
        cd .. && 
        rm -rf {repo_basename}.git && 
        git clone https://github.com/$(git config user.name)/{new_repo}.git
        """
    else:
        logger.info("Using GitHub CLI for repository duplication")
        # Create a temporary directory for cloning
        tmp_dir = f"tmp_{repo_basename}"
        
        # Script to duplicate using GitHub CLI
        script = f"""
        # Create new repository
        gh repo create {new_repo} --public --confirm &&
        # Clone original repository to temporary directory
        git clone {original_repo} {tmp_dir} &&
        cd {tmp_dir} &&
        # Remove original remote
        git remote remove origin &&
        # Add new repository as remote
        git remote add origin https://github.com/$(git config user.name)/{new_repo}.git &&
        # Push all content to new repository
        git push -u origin main || git push -u origin master &&
        # Clean up
        cd .. &&
        rm -rf {tmp_dir} &&
        # Clone the new repository
        git clone https://github.com/$(git config user.name)/{new_repo}.git
        """

    # Execute the script
    return execute_command(script, shell_cmd)


def get_default_repositories() -> List[str]:
    """
    Get the default list of template repositories.
    
    Returns:
        A list of repository URLs.
    """
    return [
        "https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_FastAPI_and_Docker.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_PostgreSQL_Integration.git"
    ]


def main():
    """
    Main function to run the GitHub Repo Duplicator.
    
    This function displays a menu of template repositories,
    gets user input for selection and new repo name,
    and then duplicates the selected repository.
    """
    # Get the list of original repositories (templates)
    original_repos = get_default_repositories()

    # Display header
    print("\n" + "=" * 50)
    print("GitHub Repo Duplicator for Templates".center(50))
    print("=" * 50 + "\n")

    # Display the menu
    print("Select the template repository to duplicate:")
    for i, repo in enumerate(original_repos, 1):
        print(f"{i}. {repo}")

    # Get the user's choice
    try:
        choice = int(input("\nEnter the number of the template repository: ")) - 1
        if choice < 0 or choice >= len(original_repos):
            logger.error("Invalid choice selected")
            print("Invalid choice. Exiting.")
            return
    except ValueError:
        logger.error("Invalid input for repository selection")
        print("Invalid input. Please enter a number. Exiting.")
        return

    # Get the new repository name
    new_repo = input("Enter the new repository name: ")
    if not validate_repo_name(new_repo):
        logger.error(f"Invalid repository name: {new_repo}")
        print("Invalid repository name. Repository names should only contain letters, numbers, underscores, dots, and hyphens.")
        return

    # Check if GitHub CLI (gh) is available
    gh_available = shutil.which("gh") is not None
    
    # Check if Zsh is available, otherwise use Bash
    shell_cmd = shutil.which("zsh") or shutil.which("bash")
    if not shell_cmd:
        logger.error("Neither zsh nor bash is available")
        print("Error: Neither zsh nor bash is available on your system. Exiting.")
        return

    # Selected original repo
    original_repo = original_repos[choice]
    
    # Duplicate the repository
    success = duplicate_repository(
        original_repo,
        new_repo,
        shell_cmd,
        gh_available
    )
    
    if success:
        print("\n" + "=" * 50)
        print("Repository Duplication Completed Successfully!".center(50))
        print(f"Your new repository '{new_repo}' is ready to use.".center(50))
        print("=" * 50 + "\n")
    else:
        print("\nError: Repository duplication failed. Please check the logs for details.")


def cli_entry_point():
    """Entry point for the command-line interface."""
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
        sys.exit(1)
    except Exception as e:
        logger.exception("An unexpected error occurred")
        print(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli_entry_point() 