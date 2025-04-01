#!/bin/bash
# Script to set up a conda environment for GitHub Repo Duplicator

# Color codes for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}    Setting up conda environment for         ${NC}"
echo -e "${GREEN}      GitHub Repo Duplicator                 ${NC}"
echo -e "${GREEN}==============================================${NC}"

# Check for conda
if ! command -v conda &> /dev/null; then
    echo -e "${RED}Error: conda is not installed or not in PATH${NC}"
    echo -e "${YELLOW}Please install Miniconda or Anaconda:${NC}"
    echo -e "https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html"
    exit 1
fi

# Environment file
ENV_FILE="environment/environment.yml"

# Check if the environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}Error: Environment file not found at $ENV_FILE${NC}"
    exit 1
fi

# Create or update the environment
if conda env list | grep -q "^duplicator "; then
    echo -e "${YELLOW}Environment 'duplicator' already exists. Updating...${NC}"
    conda env update -f "$ENV_FILE"
else
    echo -e "${YELLOW}Creating new environment 'duplicator'...${NC}"
    conda env create -f "$ENV_FILE"
fi

# Check if the environment was created/updated successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Conda environment setup completed successfully!${NC}"
    echo -e "${YELLOW}To activate the environment, run:${NC}"
    echo -e "  conda activate duplicator"
    echo -e "${YELLOW}To install the package in development mode, run:${NC}"
    echo -e "  pip install -e ."
    echo -e "${YELLOW}To run the tests, run:${NC}"
    echo -e "  make test"
else
    echo -e "${RED}Failed to set up conda environment.${NC}"
    exit 1
fi 