# Developer Documentation

This document provides information for developers who want to contribute to the GitHub Repo Duplicator project.

## Project Structure

```
GitHub_Repo_Duplicator_for_Templates/
├── src/                         # Source code
│   └── github_repo_duplicator/  # Main package
│       ├── __init__.py          # Package initialization
│       ├── duplicator.py        # Core functionality
│       ├── create_icon.py       # Icon generation script
│       └── ascii_icon.txt       # ASCII art fallback icon
├── tests/                       # Test directory
│   ├── __init__.py              # Test package initialization
│   └── test_duplicator.py       # Unit tests
├── scripts/                     # Helper scripts
│   ├── github_repo_duplicator_cli.py # CLI entry point
│   ├── install.sh               # Linux/macOS installation script
│   ├── install.ps1              # Windows installation script
│   ├── setup_conda.sh           # Conda environment setup
│   └── run.py                   # Simple runner script
├── docs/                        # Documentation
│   ├── DEVELOPER.md             # Developer documentation (this file)
│   └── img/                     # Documentation images
├── environment/                 # Environment configuration
│   └── environment.yml          # Conda environment specification
├── build/                       # Build-related files
│   ├── MANIFEST.in              # Package manifest
│   └── pyinstaller/             # PyInstaller configuration
│       └── github_repo_duplicator.spec # PyInstaller spec file
├── setup.py                     # Package setup script
├── requirements.txt             # Development dependencies
├── Makefile                     # Development automation
├── README.md                    # User documentation
└── LICENSE                      # MIT License
```

## Implementation Details

### Core Functionality

The GitHub Repo Duplicator is designed with a modular architecture consisting of:

1. **Command Execution:** `execute_command()` function for running shell scripts
2. **Validation:** `validate_github_url()` and `validate_repo_name()` for input validation
3. **Main Workflow:** `main()` function handling the user interface and process flow

### Repository Duplication Methods

The tool uses two different methods for repository duplication:

1. **Git Commands Method:** Used when GitHub CLI is not available
   ```bash
   git clone --bare [ORIGINAL_REPO]
   cd [REPO_BASENAME].git
   git push --mirror https://github.com/[USERNAME]/[NEW_REPO].git
   cd ..
   rm -rf [REPO_BASENAME].git
   git clone https://github.com/[USERNAME]/[NEW_REPO].git
   ```

2. **GitHub CLI Method:** Used when GitHub CLI is available
   ```bash
   gh repo create [NEW_REPO] --public --confirm
   git clone [ORIGINAL_REPO] [TMP_DIR]
   cd [TMP_DIR]
   git remote remove origin
   git remote add origin https://github.com/[USERNAME]/[NEW_REPO].git
   git push -u origin main || git push -u origin master
   cd ..
   rm -rf [TMP_DIR]
   git clone https://github.com/[USERNAME]/[NEW_REPO].git
   ```

## Development Workflow

### Setting Up Development Environment

1. Clone the repository
   ```bash
   git clone https://github.com/USERNAME/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```

2. Install development dependencies
   ```bash
   make dev-setup
   ```

3. Alternatively, set up a conda environment
   ```bash
   make conda-setup
   conda activate duplicator
   ```

### Running Tests

Run the test suite:
```bash
make test
```

Run tests with coverage:
```bash
make coverage
```

### Building the Executable

Build the standalone executable:
```bash
make build
```

The executable will be available in the `dist/` directory.

## Code Style and Conventions

This project follows these code style guidelines:

1. **PEP 8** for Python code style
2. **Docstrings** in Google format for function documentation
3. **Type Hints** where appropriate for better code readability
4. **Error Handling** with proper logging

## Project Layout Principles

The project follows these organizational principles:

1. **Source code isolation**: All application code is in the `src/` directory
2. **Clear separation of concerns**: Different aspects of the application are in dedicated directories
3. **Minimal root directory**: Only essential project files like README and LICENSE in the root
4. **Consistent naming**: Files and directories are named for clarity and consistency

## Release Process

1. Update version in `setup.py` and `src/github_repo_duplicator/__init__.py`
2. Update CHANGELOG section in README.md
3. Build the executable with `make build`
4. Create a new release on GitHub with the executable attached
5. Add release notes documenting the changes

## Performance Considerations

- The tool is designed to work with repositories of any size
- For large repositories, the GitHub CLI method is recommended as it provides better progress information
- Test with large repositories to ensure performance is acceptable

## Security Considerations

- The tool requires GitHub authentication to be set up in advance
- All Git operations are performed using the user's credentials
- No passwords or tokens are stored by the application
- Temporary directories are cleaned up after use

## Additional Resources

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Git Documentation](https://git-scm.com/doc)
- [PyInstaller Documentation](https://pyinstaller.org/en/stable/) 