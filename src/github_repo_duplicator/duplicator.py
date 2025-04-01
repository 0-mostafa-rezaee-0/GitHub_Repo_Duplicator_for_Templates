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
import getpass
import json
import urllib.request
import urllib.error
import base64
from typing import List, Optional, Tuple

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


def get_saved_credentials() -> Tuple[str, str]:
    """
    Get saved GitHub credentials from the user's home directory.
    
    Returns:
        Tuple containing (username, token) if found, empty strings otherwise.
    """
    try:
        credentials_file = os.path.join(os.path.expanduser("~"), ".github_repo_duplicator")
        if os.path.exists(credentials_file):
            with open(credentials_file, "r") as f:
                lines = f.read().strip().split("\n")
                if len(lines) >= 2:
                    return lines[0], lines[1]
        return "", ""
    except Exception as e:
        logger.error(f"Error reading saved credentials: {str(e)}")
        return "", ""


def save_credentials(username: str, token: str) -> bool:
    """
    Save GitHub credentials to the user's home directory.
    
    Args:
        username: GitHub username.
        token: GitHub personal access token.
        
    Returns:
        True if credentials were saved successfully, False otherwise.
    """
    try:
        credentials_file = os.path.join(os.path.expanduser("~"), ".github_repo_duplicator")
        with open(credentials_file, "w") as f:
            f.write(f"{username}\n{token}")
        
        # Set permissions to user-only readable
        os.chmod(credentials_file, 0o600)
        return True
    except Exception as e:
        logger.error(f"Error saving credentials: {str(e)}")
        return False


def create_github_repository_api(repo_name: str) -> bool:
    """
    Create a new repository on GitHub using the GitHub API.
    
    Args:
        repo_name: The name of the new repository.
        
    Returns:
        True if the repository was created successfully, False otherwise.
    """
    try:
        # Check for saved credentials
        username, token = get_saved_credentials()
        
        if not (username and token):
            # Get GitHub username and personal access token
            print("\nTo create a new repository on GitHub, please enter your credentials:")
            username = input("GitHub username: ")
            print("\nA personal access token is required. You can create one at:")
            print("https://github.com/settings/tokens/new")
            print("Make sure to select the 'repo' scope.")
            token = getpass.getpass("GitHub personal access token: ")
            
            # Ask if the user wants to save credentials for future use
            save_creds = input("\nWould you like to save these credentials for future use? (y/n): ").strip().lower() == 'y'
            if save_creds:
                if save_credentials(username, token):
                    print("Credentials saved successfully.")
                else:
                    print("Failed to save credentials.")
        else:
            print(f"\nUsing saved credentials for GitHub user: {username}")
        
        # Create the request
        url = "https://api.github.com/user/repos"
        data = json.dumps({"name": repo_name, "private": False}).encode('utf-8')
        
        # Set up authentication
        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Repo-Duplicator"
        }
        
        # Create the request
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        # Send the request
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 201:
                print(f"\nRepository '{repo_name}' created successfully!")
                # Save the username for later use
                os.environ["GH_USERNAME"] = username
                return True
            else:
                logger.error(f"Failed to create repository. Status code: {response.getcode()}")
                print(f"\nFailed to create repository. Status code: {response.getcode()}")
                return False
                
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        logger.error(f"HTTP Error: {e.code} - {error_msg}")
        print(f"\nFailed to create repository: {json.loads(error_msg).get('message', str(e))}")
        # If credentials error, suggest trying again
        if e.code == 401:
            print("Authentication failed. Your token may be invalid or expired.")
            retry = input("Would you like to try again with new credentials? (y/n): ").strip().lower() == 'y'
            if retry:
                # Remove saved credentials
                save_credentials("", "")
                return create_github_repository_api(repo_name)
        return False
    except Exception as e:
        logger.error(f"Error creating repository: {str(e)}")
        print(f"\nAn error occurred while creating the repository: {str(e)}")
        return False


def check_gh_cli() -> bool:
    """
    Check if GitHub CLI is installed.
    
    Returns:
        True if GitHub CLI is available, False otherwise.
    """
    gh_available = shutil.which("gh") is not None
    if gh_available:
        logger.info("GitHub CLI is available")
    else:
        logger.info("GitHub CLI is not available, will use API instead")
    return gh_available


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
    
    # Create the repository on GitHub 
    created = False
    if gh_available:
        # Use GitHub CLI if available
        logger.info("Creating repository using GitHub CLI")
        create_repo_cmd = f"gh repo create {new_repo} --public --confirm"
        created = execute_command(create_repo_cmd, shell_cmd)
        if not created:
            logger.error("Failed to create repository with GitHub CLI")
            print("\nFailed to create repository. Trying with GitHub API instead.")
            created = create_github_repository_api(new_repo)
    else:
        # Use GitHub API directly
        logger.info("Creating repository using GitHub API")
        created = create_github_repository_api(new_repo)
    
    if not created:
        print("\nFailed to create repository. Please try again.")
        return False
        
    # Get the GitHub username
    if gh_available:
        # Get username from GitHub CLI
        result = subprocess.run(
            "gh api user | grep login | cut -d '\"' -f 4",
            shell=True,
            capture_output=True,
            text=True
        )
        username = result.stdout.strip()
    else:
        # Use the username provided during API authentication
        username = os.environ.get("GH_USERNAME", "")
        if not username:
            # Try to get username from git config
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
    # Check if GitHub CLI is installed (but don't require it)
    gh_available = check_gh_cli()
    
    # If GitHub CLI is available, check authentication
    if gh_available:
        is_authenticated = check_gh_auth()
        if not is_authenticated:
            print("\nWill use direct API authentication instead of GitHub CLI.")
            gh_available = False
        
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