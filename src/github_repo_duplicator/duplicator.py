#!/usr/bin/env python3
"""
GitHub Repo Duplicator

A tool that allows users to duplicate GitHub repositories with an interactive menu.
It creates a new repository with the same content as the selected template repository.
"""

import logging
import os
import platform
import re
import shutil
import subprocess
import sys
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ANSI color codes for terminal output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def print_success(message: str) -> None:
    """Print a success message in green color."""
    print(f"{Colors.GREEN}{message}{Colors.END}")


def print_error(message: str) -> None:
    """Print an error message in red color."""
    print(f"{Colors.RED}{Colors.BOLD}Error: {message}{Colors.END}")


def print_warning(message: str) -> None:
    """Print a warning message in yellow color."""
    print(f"{Colors.YELLOW}Warning: {message}{Colors.END}")


def print_info(message: str) -> None:
    """Print an info message in blue color."""
    print(f"{Colors.BLUE}{message}{Colors.END}")


def print_header(message: str) -> None:
    """Print a header message in purple and bold."""
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.END}")


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
            text=True,
        )
        logger.info(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")

        # Extract more specific error messages for common failures
        if "permission denied" in e.stderr.lower():
            print_error("Permission denied. Please check your file permissions.")
        elif "not found" in e.stderr.lower():
            print_error("Command or file not found. Please check your environment.")
        elif "could not read from remote repository" in e.stderr.lower():
            print_error(
                "Could not access the remote repository. Please check your authentication and connectivity."
            )
        elif "fatal: remote origin already exists" in e.stderr.lower():
            print_error(
                "Remote 'origin' already exists. Previous operation may have partially succeeded."
            )
        else:
            print_error(f"Command execution failed: {e.stderr.strip()}")

        return False
    except Exception as e:
        logger.exception("An unexpected error occurred")
        print_error(f"An unexpected error occurred: {str(e)}")
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
    return bool(re.match(r"^[a-zA-Z0-9_.-]+$", name))


def get_git_username() -> str:
    """
    Get the user's git username from git config.

    Returns:
        The git username if available, or empty string if not.
    """
    try:
        result = subprocess.run(
            "git config user.name", shell=True, capture_output=True, text=True
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
            text=True,
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
            print(
                "Please download the installer from: https://github.com/cli/cli/releases/latest"
            )
            print("Run the installer (.msi file) and restart this tool.")
            return False

        elif system == "Darwin":  # macOS
            # Try to install using brew
            print("Installing with Homebrew...")
            result = subprocess.run(
                "which brew && brew install gh || echo 'Homebrew not installed'",
                shell=True,
                capture_output=True,
                text=True,
            )
            if "not installed" in result.stdout or result.returncode != 0:
                print(
                    "Homebrew not found. Please install Homebrew from https://brew.sh/"
                )
                print("Then run: brew install gh")
                return False

        elif system == "Linux":
            # Try to detect and use the appropriate package manager
            if os.path.exists("/etc/debian_version") or os.path.exists(
                "/etc/ubuntu_version"
            ):
                print("Installing with apt...")
                subprocess.run(
                    "sudo apt-get update && sudo apt-get install -y gh", shell=True
                )
            elif os.path.exists("/etc/fedora-release"):
                print("Installing with dnf...")
                subprocess.run("sudo dnf install -y gh", shell=True)
            elif os.path.exists("/etc/arch-release"):
                print("Installing with pacman...")
                subprocess.run("sudo pacman -S --noconfirm github-cli", shell=True)
            else:
                print(
                    "Could not automatically install GitHub CLI for your Linux distribution."
                )
                print(
                    "Please visit: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
                )
                return False

        # Check if installation was successful
        gh_available = shutil.which("gh") is not None
        if gh_available:
            print_success("GitHub CLI installed successfully!")

            # Run GitHub authentication
            print(
                "\nNow setting up GitHub authentication. This will open a browser window."
            )
            subprocess.run("gh auth login -w", shell=True)

            # Verify authentication
            auth_result = subprocess.run(
                "gh auth status", shell=True, capture_output=True, text=True
            )
            if auth_result.returncode == 0:
                print_success("GitHub CLI authentication successful!")
                return True
            else:
                print_error(
                    "GitHub CLI authentication failed. Please run 'gh auth login' manually."
                )
                return False
        else:
            print_error("Failed to install GitHub CLI. Please install it manually.")
            return False

    except Exception as e:
        logger.error(f"Error during GitHub CLI installation: {str(e)}")
        print(f"An error occurred while installing GitHub CLI: {str(e)}")
        return False


def check_github_cli_installed() -> bool:
    """Check if GitHub CLI is installed."""
    return shutil.which("gh") is not None


def check_github_authenticated() -> bool:
    """Check if the user is authenticated with GitHub CLI."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, check=False
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error checking GitHub CLI authentication: {str(e)}")
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
    repo_basename = os.path.basename(original_repo).replace(".git", "")

    print("\nInitiating repository duplication...")
    print(f"Source: {original_repo}")
    print(f"Destination: {new_repo}")

    # Create the repository on GitHub using GitHub CLI
    logger.info("Creating repository using GitHub CLI")
    create_repo_cmd = f"gh repo create {new_repo} --public --confirm"
    created = execute_command(create_repo_cmd, shell_cmd)

    if not created:
        logger.error("Failed to create repository with GitHub CLI")
        print(
            "\nFailed to create repository. Please check GitHub CLI is properly authenticated."
        )
        print("Run 'gh auth login' and try again.")
        return False

    # Get username from GitHub CLI
    result = subprocess.run(
        "gh api user | grep login | cut -d '\"' -f 4",
        shell=True,
        capture_output=True,
        text=True,
    )
    username = result.stdout.strip()
    if not username:
        username = get_git_username()
        if not username:
            logger.error("Could not determine GitHub username")
            print(
                "\nCould not determine your GitHub username. Please check your git configuration."
            )
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
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_PostgreSQL_Integration.git",
    ]


def main(
    template_url: Optional[str] = None,
    new_repo_name: Optional[str] = None,
    skip_confirmations: bool = False,
) -> None:
    """
    Main function to run the GitHub Repo Duplicator.

    Args:
        template_url: Optional pre-selected template URL to skip selection
        new_repo_name: Optional pre-defined new repository name to skip prompt
        skip_confirmations: Whether to skip confirmation prompts
    """
    print_header("\nGitHub Repository Duplicator for Templates")

    # Check for GitHub CLI and authenticate if needed
    if not check_github_cli_installed():
        if not check_gh_cli():
            print_error("GitHub CLI is required but could not be installed")
            print_info("Please install GitHub CLI manually: https://cli.github.com/")
            sys.exit(1)

    if not check_github_authenticated():
        print_warning("You are not authenticated with GitHub CLI")
        print_info("Please authenticate with GitHub")
        subprocess.run("gh auth login -w", shell=True)

        # Verify authentication was successful
        if not check_github_authenticated():
            print_error("GitHub authentication failed")
            sys.exit(1)

    # Get available repository templates
    templates = get_default_repositories()

    # Let user select a template if not provided
    if not template_url:
        print_info("\nAvailable template repositories:")
        for i, repo in enumerate(templates, 1):
            print(f"{i}. {repo}")

        while True:
            try:
                choice = input(
                    "\nSelect a template repository (1-{}): ".format(len(templates))
                )
                index = int(choice) - 1
                if 0 <= index < len(templates):
                    template_url = templates[index]
                    break
                else:
                    print_warning(
                        f"Invalid selection. Please enter a number between 1 and {len(templates)}"
                    )
            except ValueError:
                print_warning("Please enter a valid number")

    # Get new repository name if not provided
    if not new_repo_name:
        while True:
            new_repo_name = input("\nEnter a name for your new repository: ").strip()
            if validate_repo_name(new_repo_name):
                break
            else:
                print_warning(
                    "Invalid repository name. Use only letters, numbers, hyphens, underscores, and periods"
                )

    # Show summary and confirm
    if not skip_confirmations:
        print("\nRepository Duplication Details:")
        print_info(f"Template repository: {template_url}")
        print_info(f"New repository name: {new_repo_name}")

        confirmation = input("\nContinue with these settings? (y/n): ").lower()
        if confirmation != "y":
            print_warning("Operation cancelled by user")
            sys.exit(0)

    # Determine which shell to use
    shell_cmd = "/bin/bash"
    if platform.system() == "Windows":
        shell_cmd = "cmd.exe"

    # Create temp directory for cloning
    temp_dir = f"{new_repo_name}_temp"
    if os.path.exists(temp_dir):
        print_warning(f"Directory {temp_dir} already exists. Removing it...")
        shutil.rmtree(temp_dir)

    try:
        # Clone the template repository
        print_info(f"\nCloning template repository: {template_url}")
        if not execute_command(f"git clone {template_url} {temp_dir}", shell_cmd):
            print_error("Failed to clone the template repository")
            sys.exit(1)

        # Create a new repository on GitHub
        print_info(f"\nCreating new repository: {new_repo_name}")
        if not execute_command(
            f"gh repo create {new_repo_name} --private --confirm", shell_cmd
        ):
            print_error("Failed to create the new repository")
            sys.exit(1)

        # Set up the new repository and push
        print_info("\nSetting up the new repository")
        commands = [
            f"cd {temp_dir}",
            "git remote remove origin",
            f"git remote add origin $(gh repo view {new_repo_name} --json sshUrl -q .sshUrl)",
            "git push -u origin main || git push -u origin master",
        ]

        if not execute_command(" && ".join(commands), shell_cmd):
            print_error("Failed to push to the new repository")
            sys.exit(1)

        # Clean up
        print_info("\nCleaning up temporary files")
        shutil.rmtree(temp_dir)

        # Show success message
        repo_url = subprocess.check_output(
            f"gh repo view {new_repo_name} --json url -q .url", shell=True, text=True
        ).strip()

        print_success(f"\n✅ Repository successfully duplicated!")
        print_info(f"New repository: {repo_url}")
        print_info(f"You can clone it with: git clone {repo_url}.git")

    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        sys.exit(1)

    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        logger.exception("Detailed error information:")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        sys.exit(1)


def cli_entry_point():
    """Entry point for the command-line script."""
    main()


def clone_repository(
    repo_url: str, destination: str, shell_cmd: str = "/bin/bash"
) -> bool:
    """
    Clone a repository to a destination directory.

    Args:
        repo_url: The URL of the repository to clone.
        destination: The directory to clone into.
        shell_cmd: The shell to use for command execution.

    Returns:
        True if the cloning was successful, False otherwise.
    """
    logger.info(f"Cloning repository: {repo_url} to {destination}")
    print_info(f"Cloning repository: {repo_url}")

    if os.path.exists(destination):
        print_warning(f"Directory {destination} already exists. Removing it...")
        shutil.rmtree(destination)

    cmd = f"git clone {repo_url} {destination}"
    return execute_command(cmd, shell_cmd)


def create_new_repository(
    repo_name: str,
    description: str = "",
    private: bool = True,
    shell_cmd: str = "/bin/bash",
) -> bool:
    """
    Create a new GitHub repository.

    Args:
        repo_name: The name for the new repository.
        description: Optional description for the repository.
        private: Whether the repository should be private.
        shell_cmd: The shell to use for command execution.

    Returns:
        True if the repository creation was successful, False otherwise.
    """
    logger.info(f"Creating new repository: {repo_name}")
    print_info(f"Creating new repository: {repo_name}")

    visibility = "--private" if private else "--public"
    desc_option = f'--description "{description}"' if description else ""
    cmd = f"gh repo create {repo_name} {visibility} {desc_option} --confirm"

    return execute_command(cmd, shell_cmd)


def push_to_new_repository(
    local_dir: str, repo_name: str, shell_cmd: str = "/bin/bash"
) -> bool:
    """
    Push local content to a new GitHub repository.

    Args:
        local_dir: The directory containing the local content.
        repo_name: The name of the target repository.
        shell_cmd: The shell to use for command execution.

    Returns:
        True if the push was successful, False otherwise.
    """
    logger.info(f"Pushing to new repository: {repo_name}")
    print_info(f"Pushing to new repository: {repo_name}")

    try:
        # Get the repo URL from GitHub CLI
        result = subprocess.run(
            f"gh repo view {repo_name} --json sshUrl -q .sshUrl",
            shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        repo_url = result.stdout.strip()

        # Set up git commands
        commands = [
            f"cd {local_dir}",
            "git remote remove origin",
            f"git remote add origin {repo_url}",
            "git push -u origin main || git push -u origin master",
        ]

        return execute_command(" && ".join(commands), shell_cmd)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting repository URL: {e}")
        print_error(f"Failed to get repository URL: {e.stderr.strip()}")
        return False
    except Exception as e:
        logger.exception("Error during push operation")
        print_error(f"Error during push operation: {str(e)}")
        return False


if __name__ == "__main__":
    cli_entry_point()
