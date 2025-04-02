# PyInstaller Configuration

This directory contains configuration files and resources for building standalone executables using PyInstaller.

## Contents:

- `.spec` files: PyInstaller specification files that define how to build the executable
- Hook scripts for properly including dependencies
- Resource files needed during the build process

## Usage

PyInstaller uses these files when building the standalone executable:

```bash
# Run from project root
pyinstaller build/pyinstaller/github_repo_duplicator.spec
```

## Configuration Details

The PyInstaller build process:
1. Analyzes the Python code to find dependencies
2. Bundles all necessary modules and libraries
3. Creates a self-contained executable for distribution

When customizing the build:
- Modify the `.spec` file to adjust build parameters
- Add hook scripts for handling special dependencies
- Configure resource handling for application assets

Refer to the [PyInstaller documentation](https://pyinstaller.org/en/stable/) for more details. 