#!/usr/bin/env python3
"""
Command-line interface for GitHub Repo Duplicator.
"""

import argparse
import logging
import os
import sys
from typing import List, Optional

from . import __version__
from .duplicator import (
    check_github_cli_installed,
    check_github_authenticated,
    get_default_repositories,
    clone_repository,
    create_new_repository,
    push_to_new_repository,
    main as duplicator_main,
    print_header,
    print_info,
    print_success,
    print_error,
    print_warning,
    Colors
)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="GitHub Repository Duplicator for Templates",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "-v", 
        "--verbose", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "-l", 
        "--list-templates", 
        action="store_true", 
        help="List available template repositories and exit"
    )
    
    parser.add_argument(
        "-t", 
        "--template", 
        type=str,
        help="Template repository URL to use (skips template selection)"
    )
    
    parser.add_argument(
        "-n", 
        "--name", 
        type=str,
        help="Name for the new repository (skips name prompt)"
    )
    
    parser.add_argument(
        "-y", 
        "--yes", 
        action="store_true", 
        help="Skip all confirmation prompts"
    )
    
    parser.add_argument(
        "--check", 
        action="store_true", 
        help="Check GitHub CLI installation and authentication"
    )

    return parser.parse_args()


def list_templates_and_exit() -> None:
    """Display available template repositories and exit."""
    print_header("Available Template Repositories:")
    for i, repo in enumerate(get_default_repositories(), 1):
        print_info(f"{i}. {repo}")
    sys.exit(0)


def check_environment_and_exit() -> None:
    """Check GitHub CLI installation and authentication status and exit."""
    print_header("Environment Check")
    
    if check_github_cli_installed():
        print_success("✓ GitHub CLI is installed")
    else:
        print_error("✗ GitHub CLI is not installed")
        print_info("Please install GitHub CLI: https://cli.github.com/")
        sys.exit(1)
        
    if check_github_authenticated():
        print_success("✓ GitHub CLI is authenticated")
    else:
        print_error("✗ GitHub CLI is not authenticated")
        print_info("Please run 'gh auth login' to authenticate")
        sys.exit(1)
        
    print_success("Environment is ready for GitHub Repo Duplicator")
    sys.exit(0)


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    setup_logging(args.verbose)
    
    if args.check:
        check_environment_and_exit()
        
    if args.list_templates:
        list_templates_and_exit()
    
    # Run the main program with CLI arguments
    try:
        duplicator_main(
            template_url=args.template,
            new_repo_name=args.name,
            skip_confirmations=args.yes
        )
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        if args.verbose:
            logging.exception("Detailed error information:")
        sys.exit(1)


if __name__ == "__main__":
    main() 