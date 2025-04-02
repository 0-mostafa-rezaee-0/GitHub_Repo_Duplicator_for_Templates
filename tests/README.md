# Tests

This directory contains tests for the GitHub Repository Duplicator package.

## Test Files:

- `test_duplicator.py`: Unit tests for the core duplicator functionality
- `test_cli.py`: Tests for command-line interface behavior

## Running Tests

Run all tests with pytest:

```bash
# From project root
pytest

# With coverage report
pytest --cov=src
```

## Test Coverage

The tests focus on:
- Validating GitHub URLs and repository names
- Testing command execution functionality
- Ensuring proper repository handling
- Verifying correct CLI argument processing

When adding new features, please add corresponding tests to maintain code quality and prevent regressions. 