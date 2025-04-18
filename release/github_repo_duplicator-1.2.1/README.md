<div align="center">
    <img src="assets/logo.png" alt="GitHub Repo Duplicator" width="50%">
</div>

# GitHub Repo Duplicator

A tool that allows users to duplicate GitHub repositories with an interactive menu. This tool is designed for easily creating new projects from template repositories.

## Table of Contents

<details>
  <summary><a href="#1-quick-start"><i><b>1. Quick Start</b></i></a></summary>
  <div>
              <a href="#11-prerequisites">1.1. Prerequisites</a><br>
              <a href="#12-for-users">1.2. For Users</a><br>
              <a href="#13-for-developers">1.3. For Developers</a><br>
  </div>
</details>

<div>
      <a href="#2-features"><i><b>2. Features</b></i></a>
</div>

<details>
  <summary><a href="#3-installation"><i><b>3. Installation</b></i></a></summary>
  <div>
              <a href="#31-download-the-executable-recommended-for-all-users">3.1. Download the executable</a><br>
              <a href="#32-install-as-a-python-package">3.2. Install as a Python package</a><br>
              <a href="#33-run-from-source">3.3. Run from source</a><br>
              <a href="#34-use-the-installation-scripts">3.4. Use the installation scripts</a><br>
              <a href="#35-build-your-own-executable">3.5. Build your own executable</a><br>
              <a href="#36-set-up-with-conda">3.6. Set up with Conda</a><br>
  </div>
</details>

<div>
      <a href="#4-usage"><i><b>4. Usage</b></i></a>
</div>

<div>
      <a href="#5-configuration"><i><b>5. Configuration</b></i></a>
</div>

<div>
      <a href="#6-requirements"><i><b>6. Requirements</b></i></a>
</div>

<div>
      <a href="#7-testing"><i><b>7. Testing</b></i></a>
</div>

<div>
      <a href="#8-project-structure"><i><b>8. Project Structure</b></i></a>
</div>

<details>
  <summary><a href="#9-documentation"><i><b>9. Documentation</b></i></a></summary>
  <div>
              <a href="#91-documentation-structure">9.1. Documentation Structure</a><br>
              <a href="#92-documentation-benefits">9.2. Documentation Benefits</a><br>
              <a href="#93-developer-documentation">9.3. Developer Documentation</a><br>
  </div>
</details>

<div>
      <a href="#10-contributing"><i><b>10. Contributing</b></i></a>
</div>

<div>
      <a href="#11-license"><i><b>11. License</b></i></a>
</div>

<div>
      <a href="#12-changelog"><i><b>12. Changelog</b></i></a>
</div>

<div>
      <a href="#13-contact"><i><b>13. Contact</b></i></a>
</div>

## 1. Quick Start

### 1.1. Prerequisites

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

### 1.2. For Users

#### 1.2.1. Standalone Executable (Recommended, No Python Required)

This is the easiest way to use the tool - no Python or conda environment needed!

1. Download the latest release:

   - 📥 **[Download Executable (Linux/macOS/WSL)](https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates/releases/latest/download/github_repo_duplicator)** (5.8 MB)
     - For Linux/macOS: Use directly
     - For Windows: Use WSL (Windows Subsystem for Linux) to run the Linux executable. No native Windows executable will be provided.
2. **Move the downloaded executable to the directory where you want to duplicate the template repository**

   ```bash
   # For Linux/macOS - Example: if you want to create a new project in ~/projects/
   mv ~/Downloads/github_repo_duplicator ~/projects/
   cd ~/projects/

   # For Windows WSL users - Example: accessing files from Windows Downloads folder
   # (Assuming your project folder is in your WSL home directory)
   cp /mnt/c/Users/YourUsername/Downloads/github_repo_duplicator ~/projects/
   cd ~/projects/
   ```
3. Run the executable:
   
   **For Linux/macOS:**
   ```bash
   chmod +x github_repo_duplicator
   ./github_repo_duplicator
   ```
   
   **For Windows (WSL required):**
   ```bash
   # Inside your WSL terminal
   chmod +x github_repo_duplicator
   ./github_repo_duplicator
   ```
   
   > **Note for Windows users:** WSL is required to run this tool on Windows. If you don't have WSL set up yet, see [Microsoft's WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install)
   
   **Optional:** Install the executable globally to run from anywhere:
   ```bash
   chmod +x install_standalone.sh
   ./install_standalone.sh
   ```
   This script will help you install the executable in your PATH. So, you can run it from anywhere.

4. For Windows users (WSL required):

   ```bash
   # Inside your WSL terminal
   chmod +x github_repo_duplicator
   ./github_repo_duplicator
   ```

   > **Note for Windows users:** WSL is required to run this tool on Windows. If you don't have WSL set up yet, see [Microsoft's WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install)
   

#### 1.2.2. Install as a Python package (Alternative Method)

```bash
# Clone the repository
git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git

# Change to the project directory
cd GitHub_Repo_Duplicator_for_Templates

# Set up and activate conda environment
conda env create -f environment/environment.yml
conda activate duplicator

# Install the package
pip install -e .

# To use the tool:
# 1. Navigate to the directory where you want to duplicate the template
# 2. Run the command (only works while conda environment is activated)
cd /path/to/your/target/directory
github-repo-duplicator

# When you're done using the tool, deactivate the conda environment
conda deactivate
```

#### 1.2.3. Alternative: Run from Source

```bash
# Clone the repository
git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git

# Navigate to the directory where you want to duplicate the template
cd /path/to/your/target/directory

# Run the script
python3 /path/to/GitHub_Repo_Duplicator_for_Templates/scripts/run.py
```

### 1.3. For Developers

If you want to modify the list of template repositories, edit the `get_default_repositories` function in `src/github_repo_duplicator/duplicator.py`:

```python
def get_default_repositories() -> List[str]:
    return [
        "https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git",
        "https://github.com/0-mostafa-rezaee-0/Docker_for_Data_Science_Projects.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_FastAPI_and_Docker.git",
        "https://github.com/0-mostafa-rezaee-0/ML_API_with_PostgreSQL_Integration.git"
    ]
```

### 1.4. Available Templates

1. **GitHub Repo Duplicator for Templates**: This template itself - allows you to create your own template duplicator.

2. **Docker for Data Science Projects**: A Docker-based alternative to Conda/venv for data science projects.
   - Uses Docker for reproducible development environments
   - Includes Dockerfile and docker-compose.yml configuration
   - Pre-configured directory structure (data, notebooks, scripts, figures)
   - Perfect for teams that prefer containerization over traditional virtual environments

3. **ML API with FastAPI and Docker**: Create machine learning APIs with FastAPI framework.

4. **ML API with PostgreSQL Integration**: Build ML APIs with database integration.

You can add your own template repositories to the list or modify the existing ones.

## 2. Features

- Interactive menu to select template repositories:
  - **GitHub Repo Duplicator**: This template itself - for creating more template duplicators
  - **Docker for Data Science Projects**: A Docker-based alternative to Conda/venv for data science workflows
  - **ML API with FastAPI and Docker**: Template for creating ML APIs with FastAPI
  - **ML API with PostgreSQL Integration**: Template for ML APIs with database integration
- Automatically creates a new GitHub repository
- Clones the new repository to your current directory
- Cross-platform support (Windows, macOS, Linux)
- Supports both Zsh and Bash shells
- Integration with GitHub CLI for enhanced functionality (if available)

## 3. Installation

### 3.1. Download the executable (Recommended for All Users)

1. Download the latest release:

   - 📥 **[Download Executable (Linux/macOS/WSL)](https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates/releases/latest/download/github_repo_duplicator)** (5.8 MB)
     - For Linux/macOS: Use directly
     - For Windows: Use WSL (Windows Subsystem for Linux) to run the Linux executable. No native Windows executable will be provided.
2. **Move the downloaded executable to the directory where you want to duplicate the template repository**

   ```bash
   # For Linux/macOS - Example: if you want to create a new project in ~/projects/my-new-project
   mv ~/Downloads/github_repo_duplicator ~/projects/my-new-project/
   cd ~/projects/my-new-project/

   # For Windows WSL users - Example: accessing files from Windows Downloads folder
   # (Assuming your project folder is in your WSL home directory)
   cp /mnt/c/Users/YourUsername/Downloads/github_repo_duplicator ~/my-new-project/
   cd ~/my-new-project/
   ```
3. Run the executable:
   
   **For Linux/macOS:**
   ```bash
   chmod +x github_repo_duplicator
   ./github_repo_duplicator
   ```
   
   **For Windows (WSL required):**
   ```bash
   # Inside your WSL terminal
   chmod +x github_repo_duplicator
   ./github_repo_duplicator
   ```
   
   > **Note for Windows users:** WSL is required to run this tool on Windows. If you don't have WSL set up yet, see [Microsoft's WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install)
   
   **Optional:** Install the executable globally to run from anywhere:
   ```bash
   chmod +x install_standalone.sh
   ./install_standalone.sh
   ```
   This script will help you install the executable in your PATH. So, you can run it from anywhere.

### 3.2. Install as a Python package (Alternative Method)

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```
2. Set up and activate a conda environment (recommended):

   ```bash
   conda env create -f environment/environment.yml
   conda activate duplicator
   ```
3. Install the package:

   ```bash
   pip install -e .
   ```
4. Navigate to the directory where you want to duplicate the template:

   ```bash
   cd /path/to/your/target/directory
   ```
5. Run the command (only works while conda environment is activated):

   ```bash
   github-repo-duplicator
   ```
6. When you're done using the tool, deactivate the conda environment:

   ```bash
   conda deactivate
   ```

### 3.3. Run from source

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   ```
2. Make sure you have Python 3.6+ installed:

   ```bash
   python --version
   ```
3. Navigate to the directory where you want to duplicate the template:

   ```bash
   cd /path/to/your/target/directory
   ```
4. Run the script:

   ```bash
   python /path/to/GitHub_Repo_Duplicator_for_Templates/scripts/run.py
   ```

### 3.4. Use the installation scripts

1. For Linux/macOS users:

   ```bash
   bash scripts/install.sh
   ```
2. For Windows users:

   ```powershell
   .\scripts\install.ps1
   ```

### 3.5. Build your own executable

1. Clone this repository:

   ```bash
   git clone https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates.git
   cd GitHub_Repo_Duplicator_for_Templates
   ```
2. Use Make to build the executable:

   ```bash
   make build
   ```
3. Find the executable in the `
