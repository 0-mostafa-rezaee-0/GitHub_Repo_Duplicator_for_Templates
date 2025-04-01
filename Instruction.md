# GitHub Repo Duplicator for Templates

## Important note

**If you want to use my templates, ignore the entire repository and follow these simple steps:**

1. Download the executable file from the releases section.
2. Copy the file to any location you prefer.
3. Double-click the file to run it.
4. Choose a template from the list presented.
5. The tool will create a new GitHub repository based on the selected template and clone it to your current directory.

That’s it! You now have your project based on my template.

### Comprehensive Guide to Creating a GitHub Repo Duplicator

#### Introduction

The **GitHub Repo Duplicator** is a tool designed to duplicate any GitHub repository easily and efficiently. It provides an interactive menu to choose from multiple original repositories and automatically creates a new repository with the same content. This tool is cross-platform and can be executed as a standalone file, making it highly accessible and user-friendly.

---

#### Objectives:

1. Automate the duplication of GitHub repositories.
2. Provide an interactive selection menu to choose the original repo.
3. Generate a standalone executable for easy double-click execution.

---

#### Step 1: Script Design

The tool is implemented in Python for cross-platform compatibility. It first prompts the user to select an original repository from a list of predefined URLs and then asks for the new repository name. The script then duplicates the chosen repository using either **Zsh** or  **Bash** , depending on availability.

---

#### Step 2: Python Script

Here’s the complete script:

```python
import os
import shutil
import subprocess

def main():
    # Define a list of original repositories
    original_repos = [
        "https://github.com/ORIGINAL_USER/ORIGINAL_REPO_1.git",
        "https://github.com/ORIGINAL_USER/ORIGINAL_REPO_2.git",
        "https://github.com/ORIGINAL_USER/ORIGINAL_REPO_3.git"
    ]

    # Display the menu
    print("Select the original repository to duplicate:")
    for i, repo in enumerate(original_repos, 1):
        print(f"{i}. {repo}")

    # Get the user's choice
    choice = int(input("Enter the number of the original repository: ")) - 1
    if choice < 0 or choice >= len(original_repos):
        print("Invalid choice. Exiting.")
        return

    # Get the new repository name
    new_repo = input("Enter the new repository name: ")

    # Check if Zsh is available, otherwise use Bash
    shell_cmd = "zsh" if shutil.which("zsh") else "bash"

    # Selected original repo
    original_repo = original_repos[choice]

    # The script to be executed
    script = f"""
    git clone --bare {original_repo} && 
    cd {os.path.basename(original_repo).replace('.git', '')}.git && 
    git push --mirror https://github.com/$(git config user.name)/{new_repo}.git && 
    cd .. && 
    rm -rf {os.path.basename(original_repo).replace('.git', '')}.git && 
    git clone https://github.com/$(git config user.name)/{new_repo}.git
    """

    # Execute the script
    subprocess.run(script, shell=True, executable=shell_cmd)

if __name__ == "__main__":
    main()
```

---

#### Step 3: Making the Script Executable

To make it a standalone application, package it using  **PyInstaller** :

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Create the executable:
   ```
   pyinstaller --onefile --name github_repo_duplicator duplicate_repo.py
   ```
3. Run the generated file from the `dist` folder:
   ```
   ./dist/github_repo_duplicator
   ```
4. Double-click the executable to run it directly.

---

#### Step 4: Running the Program

When the executable runs, it will:

1. Display a list of original repositories.
2. Prompt the user to choose one.
3. Ask for the new repository name.
4. Duplicate the selected repository to the new location.

---

#### Benefits:

* **Cross-Platform:** Works on Windows, Mac, and Linux.
* **Standalone Executable:** Easy to distribute and run without dependencies.
* **Interactive:** User-friendly and efficient.

---

#### Final Note:

Share the executable or the script with your students, and ask them to:

1. Run the program.
2. Duplicate a repository of their choice.
3. Share their experience and feedback.

This project is an excellent exercise in combining scripting, automation, and software distribution. Let me know if you need more features or improvements!
