#!/usr/bin/env python3
"""
Setup script for GitHub Repo Duplicator.
"""

import os
import re
from setuptools import setup, find_packages

# Read the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version from __init__.py
with open("src/github_repo_duplicator/__init__.py", encoding="utf-8") as f:
    version = re.search(r'__version__ = ["\']([^"\']+)["\']', f.read()).group(1)

setup(
    name="github-repo-duplicator",
    version=version,
    author="Mostafa Rezaee",
    author_email="0.mostafa.rezaee.0@gmail.com",
    description="A tool to duplicate GitHub repositories with an interactive menu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0-mostafa-rezaee-0/GitHub_Repo_Duplicator_for_Templates",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "github-repo-duplicator=github_repo_duplicator.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 