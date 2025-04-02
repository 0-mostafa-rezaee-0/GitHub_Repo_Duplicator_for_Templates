# Utility Scripts

This directory contains utility scripts for running, installing, and managing the GitHub Repository Duplicator.

## Scripts:

- `run.py`: A simple Python runner script that executes the CLI interface
  - Usage: `python scripts/run.py`

- `github_repo_duplicator_cli.py`: Alternative entry point for the CLI
  - Usage: `python scripts/github_repo_duplicator_cli.py`

- `setup_conda.sh`: Sets up a Conda environment with all dependencies
  - Usage: `bash scripts/setup_conda.sh`

- `install.sh`: Installation script for Linux/macOS
  - Installs dependencies and makes the tool accessible system-wide
  - Usage: `bash scripts/install.sh`

- `install.ps1`: Installation script for Windows
  - PowerShell script that installs dependencies and the package
  - Usage: `powershell -ExecutionPolicy Bypass -File scripts/install.ps1`

These scripts are provided for convenience and should be run from the project root directory. They help with setting up development environments, installing the package, and running the tool directly without installation. 