# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.5] - 2025-04-04

### Added
- Improved explanations about GitHub CLI security and benefits
- Added confidence-building information about authentication methods
- Enhanced documentation about credential storage safety

### Changed
- More descriptive messaging around secure authentication options
- Better explanations of GitHub's recommended authentication practices

## [1.2.4] - 2025-04-04

### Fixed
- Prioritized GitHub CLI for repository cloning to address authentication issues
- Improved detection of GitHub CLI availability
- Enhanced fallback mechanisms when cloning fails

### Changed
- Simplified user guidance for authentication problems
- More accurate messages about GitHub authentication requirements

## [1.2.3] - 2025-04-04

### Added
- Option to store GitHub credentials for HTTPS users
- Helpful tips for avoiding authentication prompts in the future

### Improved
- Enhanced error handling for repository cloning
- Better user guidance for authentication issues

## [1.2.2] - 2025-04-04

### Fixed
- Improved repository cloning to handle both SSH and HTTPS authentication methods
- Added fallback to GitHub CLI for cloning when available to avoid authentication prompts

## [1.2.1] - 2025-04-04

### Added
- Automatic repository cloning after duplication

### Fixed
- Included Python shared library in the executable to prevent loading errors

## [1.2.0] - 2025-04-03

### Added
- New template: Docker for Data Science Projects
- Enhanced template descriptions in README
- New "Available Templates" section with detailed information
- Automatic repository cloning after duplication

### Changed
- Updated documentation with clearer installation instructions
- Improved template selection descriptions

## [1.1.0] - 2025-04-01

### Added
- GitHub CLI integration for better authentication flow
- Automatic GitHub CLI installation on supported platforms
- SSH key detection and support for Git operations
- CHANGELOG.md for tracking version history
- Improved error handling and user feedback

### Changed
- Updated README with clearer installation instructions
- Improved terminal output with color and formatting
- Simplified user experience, eliminating need for manual token management
- Reorganized code structure for better maintainability

### Removed
- API-based authentication that required manual token input
- Dependency on custom token storage

## [1.0.0] - 2025-03-28

### Added
- Initial release
- Template repository selection
- Interactive CLI
- Support for both Zsh and Bash shells
- Cross-platform compatibility
- Repository duplication functionality
