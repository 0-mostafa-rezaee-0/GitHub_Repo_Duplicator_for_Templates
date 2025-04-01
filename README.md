# GitHub Repo Duplicator

A tool that allows users to duplicate GitHub repositories with an interactive menu. This tool is designed for easily creating new projects from template repositories.

## ⚡ Quick Start

### For Users
Simply download the `github_repo_duplicator` executable from the `dist` folder of this repository to the directory where you want to clone a template. Then double-click on it or run it from the terminal. The tool will guide you through the process.

> **Note:** Once releases are published, you'll be able to download the executable directly from the Releases section.

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
│   ├── DEVELOPER.md             # Developer documentation
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

If you have any questions, feel free to open an issue or contact the maintainer directly.

---

Made with ❤️ by Mostafa Rezaee
