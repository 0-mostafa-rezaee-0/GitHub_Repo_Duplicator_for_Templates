# Environment Configuration

This directory contains environment configuration files for setting up development environments for the GitHub Repository Duplicator.

## Files:

- `environment.yml`: Conda environment specification file
  - Defines dependencies needed for development
  - Used by `setup_conda.sh` script

## Usage

### With Conda

Create and activate the environment:

```bash
# Create the environment
conda env create -f environment/environment.yml

# Activate the environment
conda activate github-repo-duplicator
```

### Manual Setup

If not using Conda, you can still reference this file to understand the required dependencies for the project. 