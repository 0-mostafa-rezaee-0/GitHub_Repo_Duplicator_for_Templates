<div align="center">
    <img src="assets/logo.png" alt="GitHub Repo Duplicator" width="50%">
</div>

# GitHub Repo Duplicator

A tool that allows users to duplicate GitHub repositories with an interactive menu. This tool is designed for easily creating new projects from template repositories.

## Table of Contents 
<details>
  <summary><a href="#-quick-start"><i><b>1. Quick Start</b></i></a></summary>
  <div>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#prerequisites">1.1. Prerequisites</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#for-users">1.2. For Users</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#for-developers">1.3. For Developers</a><br>
  </div>
</details>
&nbsp;

<details>
  <summary><a href="#-features"><i><b>2. Features</b></i></a></summary>
</details>
&nbsp;

<details>
  <summary><a href="#-installation"><i><b>3. Installation</b></i></a></summary>
  <div>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#option-1-download-the-executable-recommended">3.1. Download the executable</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#option-2-install-as-a-python-package">3.2. Install as a Python package</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#option-3-run-from-source">3.3. Run from source</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#option-4-use-the-installation-scripts">3.4. Use the installation scripts</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#option-5-build-your-own-executable">3.5. Build your own executable</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#option-6-set-up-with-conda">3.6. Set up with Conda</a><br>
  </div>
</details>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-usage"><i><b>4. Usage</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-configuration"><i><b>5. Configuration</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-requirements"><i><b>6. Requirements</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-testing"><i><b>7. Testing</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-project-structure"><i><b>8. Project Structure</b></i></a>
</div>
&nbsp;

<details>
  <summary><a href="#-documentation"><i><b>9. Documentation</b></i></a></summary>
  <div>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#documentation-structure">9.1. Documentation Structure</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#documentation-benefits">9.2. Documentation Benefits</a><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#developer-documentation">9.3. Developer Documentation</a><br>
  </div>
</details>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-contributing"><i><b>10. Contributing</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-license"><i><b>11. License</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-changelog"><i><b>12. Changelog</b></i></a>
</div>
&nbsp;

<div>
  &nbsp;&nbsp;&nbsp;&nbsp;<a href="#-contact"><i><b>13. Contact</b></i></a>
</div>
&nbsp;

## ⚡ Quick Start

### Prerequisites

- **GitHub CLI**: This tool requires GitHub CLI (gh) for authentication and repository creation
  ```bash
  # Install on Ubuntu/Debian
  sudo apt install gh
  
  # Install on macOS
  brew install gh
  
  # Install on Windows
  # Download from: https://github.com/cli/cli/releases/latest
  ```
  
- **Authenticate with GitHub CLI**:
  ```bash
  gh auth login
  ```
  Follow the prompts to authenticate through your browser.

### For Users

#### Recommended: Install as a Python Package
```bash
# Clone the repository
git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git

# Change to the project directory
cd GitHub_Repo_Duplicator_for_Templates

# Install the package
pip install -e .

# Run from anywhere
github-repo-duplicator
```

#### Alternative: Run from Source
```bash
# Clone the repository
git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git

# Run the script
python3 GitHub_Repo_Duplicator_for_Templates/scripts/run.py
```

### For Developers
If you want to modify the list of template repositories, edit the `get_default_repositories` function in `src/github_repo_duplicator/duplicator.py`:

```python
def get_default_repositories() -> List[str]:
    return [
        "https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_FastAPI_and_Docker.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_PostgreSQL_Integration.git"
    ]
```

Replace these with your actual template repositories.

## 📋 Features

- Interactive menu to select template repositories
- Automatically creates a new GitHub repository
- Clones the new repository to your current directory
- Cross-platform support (Windows, macOS, Linux)
- Supports both Zsh and Bash shells
- Integration with GitHub CLI for enhanced functionality (if available)

## 🚀 Installation

### Option 1: Download the executable (Recommended)

1. Download the executable `github_repo_duplicator` (or `github_repo_duplicator.exe` on Windows) from the `dist` folder of this repository
2. Move the executable to a directory of your choice
3. Double-click to run, or execute from terminal

### Option 2: Install as a Python package

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```
2. Install the package:

   ```bash
   pip install -e .
   ```
3. Run the command:

   ```bash
   github-repo-duplicator
   ```

### Option 3: Run from source

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```
2. Make sure you have Python 3.6+ installed:

   ```bash
   python --version
   ```
3. Run the script:

   ```bash
   python scripts/run.py
   ```

### Option 4: Use the installation scripts

1. For Linux/macOS users:

   ```bash
   bash scripts/install.sh
   ```
2. For Windows users:

   ```powershell
   .\scripts\install.ps1
   ```

### Option 5: Build your own executable

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```
2. Use Make to build the executable:

   ```bash
   make build
   ```
3. Find the executable in the `dist` folder

### Option 6: Set up with Conda

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```
2. Set up a conda environment:

   ```bash
   make conda-setup
   conda activate duplicator
   ```
3. Run the application:

   ```bash
   python scripts/run.py
   ```

## 📝 Usage

1. Run the executable or script
2. Select a template repository from the list
3. Enter a name for your new repository
4. Wait for the process to complete
5. Your new repository will be cloned to the current directory

## ⚙️ Configuration

To customize the list of template repositories, edit the `get_default_repositories` function in the `src/github_repo_duplicator/duplicator.py` file:

```python
def get_default_repositories() -> List[str]:
    return [
        "https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_FastAPI_and_Docker.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_PostgreSQL_Integration.git"
    ]
```

## 📋 Requirements

- Python 3.6 or higher (if running from source)
- Git installed and configured on your system
- GitHub account with proper authentication set up
- Either Bash or Zsh shell available
- GitHub CLI (optional, provides enhanced functionality)

## 🧪 Testing

Ensure everything is working by running:

```bash
make test
```

## 📁 Project Structure

```
+----.github                        <-- GitHub configuration files
|
|    README.md                      <-- GitHub configuration documentation
|
|    +----ISSUE_TEMPLATE            <-- GitHub issue templates
|         README.md                 <-- Issue templates documentation
|
|    +----workflows                 <-- GitHub Actions workflows
|         README.md                 <-- Workflows documentation
|         python-tests.yml          <-- Test automation
|         release.yml               <-- Release automation
|
+----assets                         <-- Project assets (images, styles)
|    README.md                      <-- Assets documentation
|    logo.png                       <-- Project logo
|
+----docs                           <-- Documentation files
|    README.md                      <-- Documentation overview
|    DEVELOPER.md                   <-- Developer documentation
|
|    +----.github                   <-- Documentation GitHub templates
|         README.md                 <-- Doc GitHub templates info
|
|    +----img                       <-- Documentation images
|         README.md                 <-- Image guidelines
|
+----environment                    <-- Environment configuration
|    README.md                      <-- Environment documentation
|    environment.yml                <-- Conda environment specification
|
+----scripts                        <-- Utility scripts
|    README.md                      <-- Scripts documentation
|    run.py                         <-- Simple runner script
|    github_repo_duplicator_cli.py  <-- CLI entry point
|    install.sh                     <-- Linux/macOS installation script
|    install.ps1                    <-- Windows installation script
|    setup_conda.sh                 <-- Conda environment setup
|
+----src                            <-- Source code
|    README.md                      <-- Source code documentation
|
|    +----github_repo_duplicator    <-- Main package
|         README.md                 <-- Package documentation
|         __init__.py               <-- Package initialization
|         cli.py                    <-- Command-line interface
|         duplicator.py             <-- Core functionality
|         create_icon.py            <-- Icon generation script
|         ascii_icon.txt            <-- ASCII art fallback icon
|
+----tests                          <-- Test directory
|    README.md                      <-- Testing documentation
|    __init__.py                    <-- Test package initialization
|    test_duplicator.py             <-- Unit tests
|
|    .gitignore                     <-- Specifies files to ignore in Git
|    CHANGELOG.md                   <-- Version history
|    LICENSE                        <-- License information
|    Makefile                       <-- Development automation
|    MANIFEST.in                    <-- Package manifest
|    pyproject.toml                 <-- Project configuration (PEP 518)
|    README.md                      <-- This file
|    requirements.txt               <-- Development dependencies
|    setup.py                       <-- Package setup script
```

## 📚 Documentation

This project follows a comprehensive documentation approach with README files in every directory. This makes it easy for new contributors to understand the purpose and contents of each part of the project.

### Documentation Structure

- **Root README**: This file - provides an overview of the entire project
- **Directory READMEs**: Each directory contains its own README.md explaining:
  - Purpose of the directory
  - Contents and their functions
  - Usage instructions if applicable
  - Special notes about the directory

### Documentation Benefits

- **Easy Navigation**: Quickly understand any part of the project
- **Self-Contained Context**: Each directory explains itself without needing to read the entire project docs
- **Improved Onboarding**: New contributors can easily understand the codebase organization
- **Maintainability**: Better organization leads to more maintainable code

### Developer Documentation

For detailed information on developing and contributing to this project, see:

- [DEVELOPER.md](docs/DEVELOPER.md): Comprehensive development guide
- [CHANGELOG.md](CHANGELOG.md): Version history and changes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For more detailed information for developers, see [DEVELOPER.md](docs/DEVELOPER.md).

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Changelog

- **v1.0.0** - Initial release
  - Base functionality for repository duplication
  - Support for Zsh and Bash shells
  - GitHub CLI integration

## 📞 Contact

If you have any questions or suggestions, feel free to reach out to [Mostafa Rezaee](https://www.linkedin.com/in/mostafa-rezaee/) at Linkedin. You can also open an issue on the project repository.
