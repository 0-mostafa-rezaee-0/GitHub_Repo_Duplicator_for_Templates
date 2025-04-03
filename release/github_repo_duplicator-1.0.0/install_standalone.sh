#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if the executable exists in the current directory
if [ ! -f "github_repo_duplicator" ]; then
    echo -e "${RED}Error: github_repo_duplicator executable not found in the current directory.${NC}"
    echo -e "${YELLOW}Please make sure you're running this script from the directory containing the executable.${NC}"
    exit 1
fi

# Make the executable... executable
chmod +x github_repo_duplicator

# Ask user where to install
echo -e "${YELLOW}Where would you like to install github_repo_duplicator?${NC}"
echo "1) /usr/local/bin (system-wide, requires sudo)"
echo "2) ~/.local/bin (user only)"
echo "3) Custom location"

read -p "Select an option [1-3]: " install_option

case $install_option in
    1)
        sudo cp github_repo_duplicator /usr/local/bin/
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Installation successful!${NC}"
            echo -e "You can now run the tool with the command: ${YELLOW}github_repo_duplicator${NC}"
        else
            echo -e "${RED}Installation failed.${NC}"
            exit 1
        fi
        ;;
    2)
        mkdir -p "$HOME/.local/bin"
        cp github_repo_duplicator "$HOME/.local/bin/"
        
        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo -e "${YELLOW}Adding ~/.local/bin to your PATH...${NC}"
            
            # Determine shell and add to appropriate config file
            if [ -n "$ZSH_VERSION" ]; then
                # Zsh
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
                echo -e "${YELLOW}Added to ~/.zshrc. Please run: source ~/.zshrc${NC}"
            elif [ -n "$BASH_VERSION" ]; then
                # Bash
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
                echo -e "${YELLOW}Added to ~/.bashrc. Please run: source ~/.bashrc${NC}"
            else
                # Unknown shell, add to both
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
                echo -e "${YELLOW}Added to ~/.bashrc and ~/.zshrc. Please restart your terminal or source the appropriate file.${NC}"
            fi
        fi
        
        echo -e "${GREEN}Installation successful!${NC}"
        echo -e "You can now run the tool with the command: ${YELLOW}github_repo_duplicator${NC}"
        ;;
    3)
        read -p "Enter the directory to install to: " custom_dir
        
        # Create directory if it doesn't exist
        if [ ! -d "$custom_dir" ]; then
            mkdir -p "$custom_dir"
        fi
        
        cp github_repo_duplicator "$custom_dir/"
        
        echo -e "${GREEN}Installation successful!${NC}"
        echo -e "The tool has been installed to ${YELLOW}$custom_dir/github_repo_duplicator${NC}"
        echo -e "${YELLOW}Make sure this directory is in your PATH to run it directly.${NC}"
        ;;
    *)
        echo -e "${RED}Invalid option.${NC}"
        exit 1
        ;;
esac 