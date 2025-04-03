#!/bin/bash
# Installation script for GitHub Repo Duplicator

# Color codes for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}    GitHub Repo Duplicator Installation       ${NC}"
echo -e "${GREEN}==============================================${NC}"

# Check for Python
echo -e "\n${YELLOW}Checking for Python...${NC}"
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}Python 3 found!${NC}"
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    python_version=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1)
    if [ "$python_version" -ge 3 ]; then
        echo -e "${GREEN}Python 3 found!${NC}"
        PYTHON_CMD="python"
    else
        echo -e "${RED}Error: Python 3 is required but Python $python_version was found.${NC}"
        echo -e "${YELLOW}Please install Python 3 and try again.${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: Python 3 is required but not found.${NC}"
    echo -e "${YELLOW}Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check for Git
echo -e "\n${YELLOW}Checking for Git...${NC}"
if command -v git &>/dev/null; then
    echo -e "${GREEN}Git found!${NC}"
else
    echo -e "${RED}Error: Git is required but not found.${NC}"
    echo -e "${YELLOW}Please install Git and try again.${NC}"
    exit 1
fi

# Check if user is authenticated with GitHub
echo -e "\n${YELLOW}Checking GitHub authentication...${NC}"
if git config user.name &>/dev/null && git config user.email &>/dev/null; then
    echo -e "${GREEN}GitHub user configuration found:${NC}"
    echo -e "Username: $(git config user.name)"
    echo -e "Email: $(git config user.email)"
else
    echo -e "${RED}Error: GitHub user configuration not found.${NC}"
    echo -e "${YELLOW}Please configure Git with your GitHub credentials:${NC}"
    echo -e "git config --global user.name \"Your Name\""
    echo -e "git config --global user.email \"your.email@example.com\""
    exit 1
fi

# Installation method selection
echo -e "\n${YELLOW}How would you like to install GitHub Repo Duplicator?${NC}"
echo -e "1) Install as a Python package"
echo -e "2) Build an executable"
echo -e "3) Run directly from source (no installation)"

read -p "Select an option [1-3]: " install_option

case $install_option in
    1)
        echo -e "\n${YELLOW}Installing as a Python package...${NC}"
        $PYTHON_CMD -m pip install -e .
        
        if [ $? -eq 0 ]; then
            echo -e "\n${GREEN}Installation successful!${NC}"
            echo -e "You can now run the tool with the command: ${YELLOW}github-repo-duplicator${NC}"
        else
            echo -e "\n${RED}Installation failed.${NC}"
            exit 1
        fi
        ;;
    2)
        echo -e "\n${YELLOW}Building executable...${NC}"
        
        # Check for PyInstaller
        $PYTHON_CMD -m pip show pyinstaller &>/dev/null
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}PyInstaller not found. Installing...${NC}"
            $PYTHON_CMD -m pip install pyinstaller
        fi
        
        # Build the executable
        $PYTHON_CMD -m PyInstaller --onefile --name github_repo_duplicator duplicate_repo.py
        
        if [ $? -eq 0 ]; then
            echo -e "\n${GREEN}Build successful!${NC}"
            echo -e "The executable is available at: ${YELLOW}$(pwd)/dist/github_repo_duplicator${NC}"
            
            # Offer to add to PATH on Linux/macOS
            if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
                read -p "Do you want to add the executable to your PATH? (y/n) " add_to_path
                if [[ $add_to_path == "y" || $add_to_path == "Y" ]]; then
                    mkdir -p "$HOME/.local/bin"
                    cp dist/github_repo_duplicator "$HOME/.local/bin/"
                    
                    # Check if ~/.local/bin is in PATH
                    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
                        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
                        echo -e "${YELLOW}Added $HOME/.local/bin to PATH in .bashrc${NC}"
                        echo -e "${YELLOW}Please restart your terminal or run 'source ~/.bashrc'${NC}"
                    fi
                    
                    echo -e "${GREEN}Executable added to PATH at $HOME/.local/bin/github_repo_duplicator${NC}"
                fi
            fi
        else
            echo -e "\n${RED}Build failed.${NC}"
            exit 1
        fi
        ;;
    3)
        echo -e "\n${YELLOW}Running from source...${NC}"
        echo -e "${GREEN}No installation required.${NC}"
        echo -e "You can run the tool with: ${YELLOW}$PYTHON_CMD duplicate_repo.py${NC}"
        
        # Offer to create a shell alias
        if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
            read -p "Do you want to create a shell alias? (y/n) " create_alias
            if [[ $create_alias == "y" || $create_alias == "Y" ]]; then
                SHELL_FILE="$HOME/.bashrc"
                if [[ "$SHELL" == *"zsh"* ]]; then
                    SHELL_FILE="$HOME/.zshrc"
                fi
                
                ALIAS_CMD="alias github-repo-duplicator='$PYTHON_CMD $(pwd)/duplicate_repo.py'"
                echo "$ALIAS_CMD" >> "$SHELL_FILE"
                
                echo -e "${GREEN}Alias added to $SHELL_FILE${NC}"
                echo -e "${YELLOW}Please restart your terminal or run 'source $SHELL_FILE'${NC}"
            fi
        fi
        ;;
    *)
        echo -e "\n${RED}Invalid option. Exiting.${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}==============================================${NC}"
echo -e "${GREEN}  GitHub Repo Duplicator Setup Complete!      ${NC}"
echo -e "${GREEN}==============================================${NC}" 