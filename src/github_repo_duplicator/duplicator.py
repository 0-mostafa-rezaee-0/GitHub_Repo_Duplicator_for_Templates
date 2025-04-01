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
import platform
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


def get_git_username() -> str:
    """
    Get the user's git username from git config.
    
    Returns:
        The git username if available, or empty string if not.
    """
    try:
        result = subprocess.run(
            "git config user.name",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return ""
    except Exception:
        return ""


def check_ssh_github() -> bool:
    """
    Check if SSH key is set up for GitHub.
    
    Returns:
        True if SSH is properly set up, False otherwise.
    """
    try:
        # Try a test connection to GitHub
        result = subprocess.run(
            "ssh -o BatchMode=yes -o ConnectTimeout=5 -T git@github.com 2>&1",
            shell=True,
            capture_output=True,
            text=True
        )
        # GitHub returns error code 1 when authentication succeeds but shell access is denied
        # This is normal and expected
        if "successfully authenticated" in result.stdout:
            return True
        
        return False
    except Exception:
        return False


def check_gh_cli() -> bool:
    """
    Check if GitHub CLI is installed, and attempt to install it if not.
    
    Returns:
        True if GitHub CLI is available or was successfully installed, False otherwise.
    """
    gh_available = shutil.which("gh") is not None
    if gh_available:
        logger.info("GitHub CLI is available")
        return True
        
    system = platform.system()
    print("\nGitHub CLI is not installed. Attempting to install it automatically...")
    
    try:
        if system == "Windows":
            print("Automatic installation on Windows is not supported.")
            print("Please download the installer from: https://github.com/cli/cli/releases/latest")
            print("Run the installer (.msi file) and restart this tool.")
            return False
            
        elif system == "Darwin":  # macOS
            # Try to install using brew
            print("Installing with Homebrew...")
            result = subprocess.run(
                "which brew && brew install gh || echo 'Homebrew not installed'",
                shell=True,
                capture_output=True,
                text=True
            )
            if "not installed" in result.stdout or result.returncode != 0:
                print("Homebrew not found. Please install Homebrew from https://brew.sh/")
                print("Then run: brew install gh")
                return False
                
        elif system == "Linux":
            # Try to detect and use the appropriate package manager
            if os.path.exists("/etc/debian_version") or os.path.exists("/etc/ubuntu_version"):
                print("Installing with apt...")
                subprocess.run(
                    "sudo apt-get update && sudo apt-get install -y gh",
                    shell=True
                )
            elif os.path.exists("/etc/fedora-release"):
                print("Installing with dnf...")
                subprocess.run(
                    "sudo dnf install -y gh",
                    shell=True
                )
            elif os.path.exists("/etc/arch-release"):
                print("Installing with pacman...")
                subprocess.run(
                    "sudo pacman -S --noconfirm github-cli",
                    shell=True
                )
            else:
                print("Could not automatically install GitHub CLI for your Linux distribution.")
                print("Please visit: https://github.com/cli/cli/blob/trunk/docs/install_linux.md")
                return False
        
        # Check if installation was successful
        gh_available = shutil.which("gh") is not None
        if gh_available:
            print("GitHub CLI installed successfully!")
            
            # Run GitHub authentication
            print("\nNow setting up GitHub authentication. This will open a browser window.")
            subprocess.run(
                "gh auth login -w",
                shell=True
            )
            
            # Verify authentication
            auth_result = subprocess.run(
                "gh auth status",
                shell=True,
                capture_output=True,
                text=True
            )
            if auth_result.returncode == 0:
                print("GitHub CLI authentication successful!")
                return True
            else:
                print("GitHub CLI authentication failed. Please run 'gh auth login' manually.")
                return False
        else:
            print("Failed to install GitHub CLI. Please install it manually.")
            return False
            
    except Exception as e:
        logger.error(f"Error during GitHub CLI installation: {str(e)}")
        print(f"An error occurred while installing GitHub CLI: {str(e)}")
        return False


def check_gh_auth() -> bool:
    """
    Check if the user is authenticated with GitHub CLI.
    
    Returns:
        True if the user is authenticated, False otherwise.
    """
    try:
        # Try to get the authenticated user
        result = subprocess.run(
            "gh auth status",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("User is authenticated with GitHub CLI")
            return True
        else:
            print("\nYou need to authenticate with GitHub CLI.")
            print("Please run: gh auth login")
            print("Then run this tool again.")
            logger.error("User is not authenticated with GitHub CLI")
            return False
    except Exception as e:
        logger.error(f"Error checking GitHub authentication: {str(e)}")
        print(f"\nFailed to check GitHub authentication: {str(e)}")
        return False


def duplicate_repository(original_repo: str, new_repo: str, shell_cmd: str) -> bool:
    """
    Duplicate a GitHub repository.
    
    Args:
        original_repo: The URL of the original repository.
        new_repo: The name of the new repository.
        shell_cmd: The shell to use for command execution.
    
    Returns:
        True if the duplication was successful, False otherwise.
    """
    # Extract repository basename without .git
    repo_basename = os.path.basename(original_repo).replace('.git', '')
    
    print("\nInitiating repository duplication...")
    print(f"Source: {original_repo}")
    print(f"Destination: {new_repo}")
    
    # Create the repository on GitHub using GitHub CLI
    logger.info("Creating repository using GitHub CLI")
    create_repo_cmd = f"gh repo create {new_repo} --public --confirm"
    created = execute_command(create_repo_cmd, shell_cmd)
    
    if not created:
        logger.error("Failed to create repository with GitHub CLI")
        print("\nFailed to create repository. Please check GitHub CLI is properly authenticated.")
        print("Run 'gh auth login' and try again.")
        return False
    
    # Get username from GitHub CLI
    result = subprocess.run(
        "gh api user | grep login | cut -d '\"' -f 4",
        shell=True,
        capture_output=True,
        text=True
    )
    username = result.stdout.strip()
    if not username:
        username = get_git_username()
        if not username:
            logger.error("Could not determine GitHub username")
            print("\nCould not determine your GitHub username. Please check your git configuration.")
            return False
    
    # Create a temporary directory for cloning
    tmp_dir = f"tmp_{repo_basename}"
    
    # Check if SSH key exists and is set up with GitHub
    ssh_available = check_ssh_github()
    
    # Use SSH URLs if SSH keys are set up, otherwise use HTTPS
    if ssh_available:
        print("\nUsing SSH authentication for Git operations.")
        remote_url = f"git@github.com:{username}/{new_repo}.git"
        clone_url = remote_url
    else:
        print("\nUsing HTTPS for Git operations (SSH key not detected).")
        remote_url = f"https://github.com/{username}/{new_repo}.git"
        clone_url = remote_url
    
    # Script to duplicate the repository
    script = f"""
    # Clone original repository to temporary directory
    git clone {original_repo} {tmp_dir} &&
    cd {tmp_dir} &&
    # Remove original remote
    git remote remove origin &&
    # Add new repository as remote
    git remote add origin {remote_url} &&
    # Push all content to new repository
    git push -u origin main || git push -u origin master || git push -u origin $(git branch --show-current) &&
    # Clean up
    cd .. &&
    rm -rf {tmp_dir} &&
    # Clone the new repository
    git clone {clone_url}
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
    # Make sure GitHub CLI is installed and authenticated
    gh_available = check_gh_cli()
    if not gh_available:
        print("\nGitHub CLI is required for this tool to work.")
        print("Please install GitHub CLI and run the tool again.")
        sys.exit(1)
    
    # Make sure the user is authenticated
    is_authenticated = check_gh_auth()
    if not is_authenticated:
        print("\nPlease authenticate with GitHub CLI by running 'gh auth login'")
        print("Then run this tool again.")
        sys.exit(1)
        
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
        shell_cmd
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