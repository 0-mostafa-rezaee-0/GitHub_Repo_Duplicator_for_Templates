# GitHub Workflows

This directory contains GitHub Actions workflows for automated testing, building, and releasing.

## Workflows:

- `python-tests.yml`: Runs automatic tests on push and pull requests
  - Tests across multiple Python versions (3.7-3.10)
  - Runs linting with flake8
  - Checks code formatting with black and isort

- `release.yml`: Handles package releases when version tags are pushed
  - Triggered on tags starting with 'v' (e.g., v1.1.0)
  - Builds Python packages (.whl and .tar.gz)
  - Creates GitHub releases with generated assets
  - Optionally publishes to PyPI when configured

## Usage

The workflows run automatically on specified events. To trigger a release:

```bash
# Update version in src/github_repo_duplicator/__init__.py
# Update CHANGELOG.md
git tag v1.1.0
git push origin v1.1.0
```

For PyPI publishing, set the following secrets in the repository settings:
- `PYPI_USERNAME`
- `PYPI_PASSWORD`

And set the repository variable `PUBLISH_TO_PYPI` to 'true'. 