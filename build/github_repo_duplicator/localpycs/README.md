# PyInstaller Local Python Cache

This directory contains cached Python bytecode files generated by PyInstaller during the build process.

## Contents:

- `.pyc` files: Compiled Python bytecode
- Other cached data used by PyInstaller

## Purpose:

These files are used by PyInstaller to:
- Speed up subsequent builds
- Store optimized bytecode
- Cache import analysis information

## Important Notes:

- This directory is automatically generated
- Contents should not be manually edited
- Files here are temporary build artifacts
- This directory should not be committed to version control

For more information on PyInstaller's caching mechanisms, refer to the [PyInstaller documentation](https://pyinstaller.org/en/stable/advanced-topics.html). 