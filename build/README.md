# Build

This directory contains build artifacts and configuration files for the GitHub Repository Duplicator.

## Contents:

- `MANIFEST.in`: Defines files to include in the Python package distribution
- `pyinstaller/`: Configuration files for building standalone executables
- Build artifacts from previous builds (these are generally not committed to Git)

## Usage

This directory is primarily used by the build system and is referenced by:
- `setup.py` when building Python packages
- PyInstaller when creating standalone executables
- The GitHub Actions CI/CD workflow when building releases

### Building Packages

The files in this directory help with:
- Ensuring the correct files are included in the package
- Creating standalone executables
- Managing build configuration across environments

Note: Build artifacts in this directory (except configuration files) should typically be ignored by version control. 