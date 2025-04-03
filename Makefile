.PHONY: clean test build install generate-icon conda-setup

# Python executable
PYTHON = python3
PIP = pip3

# Variables
APP_NAME = github_repo_duplicator
MAIN_SCRIPT = scripts/run.py
VERSION = 1.2.0
SPEC_FILE = build/pyinstaller/github_repo_duplicator.spec
ICON_PATH = build/pyinstaller/icon.ico

# Default target
all: test build

# Run unit tests
test:
	$(PYTHON) -m pytest -v tests/

# Run tests with coverage
coverage:
	$(PYTHON) -m pytest --cov=src/github_repo_duplicator tests/

# Generate icon
generate-icon:
	@echo "Generating icon..."
	@if command -v pip &> /dev/null; then \
		if ! $(PIP) list | grep -F "Pillow" &> /dev/null; then \
			echo "Installing Pillow..."; \
			$(PIP) install Pillow; \
		fi; \
		mkdir -p build/pyinstaller; \
		$(PYTHON) -c "from src.github_repo_duplicator.create_icon import main; main()"; \
	else \
		echo "pip not available, cannot install Pillow."; \
		echo "Using ASCII icon instead."; \
		mkdir -p build/pyinstaller; \
		if [ ! -f "$(ICON_PATH)" ]; then \
			cp src/github_repo_duplicator/ascii_icon.txt $(ICON_PATH); \
		fi; \
	fi

# Build the executable using PyInstaller (with icon)
build: generate-icon
	$(PYTHON) -m PyInstaller --onefile --name $(APP_NAME) --icon=$(ICON_PATH) $(MAIN_SCRIPT)

# Build using spec file if it exists
build-with-spec: generate-icon
	@if [ -f "$(SPEC_FILE)" ]; then \
		$(PYTHON) -m PyInstaller $(SPEC_FILE); \
	else \
		echo "Spec file not found, using default build"; \
		$(MAKE) build; \
	fi

# Build without icon
build-no-icon:
	$(PYTHON) -m PyInstaller --onefile --name $(APP_NAME) $(MAIN_SCRIPT)

# Clean up build artifacts
clean:
	rm -rf build/pyinstaller/icon.ico dist/ __pycache__/ .pytest_cache/ .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name "*.egg-info" -type d -exec rm -rf {} +

# Install development dependencies
dev-setup:
	$(PIP) install -r requirements.txt

# Set up conda environment
conda-setup:
	bash scripts/setup_conda.sh

# Run the application directly
run:
	$(PYTHON) $(MAIN_SCRIPT)

# Install as a package
install:
	$(PIP) install -e .

# Uninstall the package
uninstall:
	$(PIP) uninstall -y github-repo-duplicator

# Run the bash install script
install-bash:
	bash scripts/install.sh

# Run the PowerShell install script (Windows)
install-powershell:
	powershell -ExecutionPolicy Bypass -File scripts/install.ps1

# Create a release package
release: clean test build
	mkdir -p release/$(APP_NAME)-$(VERSION)
	cp -r dist/$(APP_NAME)* release/$(APP_NAME)-$(VERSION)/
	cp README.md LICENSE release/$(APP_NAME)-$(VERSION)/
	cp scripts/install.sh scripts/install.ps1 scripts/install_standalone.sh release/$(APP_NAME)-$(VERSION)/
	cd release && zip -r $(APP_NAME)-$(VERSION).zip $(APP_NAME)-$(VERSION)
	@echo "Release package created at release/$(APP_NAME)-$(VERSION).zip"

# Help message
help:
	@echo "Available targets:"
	@echo "  all               - Run tests and build the executable"
	@echo "  test              - Run unit tests"
	@echo "  coverage          - Run tests with coverage report"
	@echo "  generate-icon     - Generate application icon"
	@echo "  build             - Build the executable using PyInstaller (with icon)"
	@echo "  build-with-spec   - Build using spec file if it exists"
	@echo "  build-no-icon     - Build the executable without icon"
	@echo "  clean             - Clean up build artifacts"
	@echo "  dev-setup         - Install development dependencies"
	@echo "  conda-setup       - Set up conda environment"
	@echo "  run               - Run the application directly"
	@echo "  install           - Install as a package"
	@echo "  uninstall         - Uninstall the package"
	@echo "  install-bash      - Run the bash install script"
	@echo "  install-powershell - Run the PowerShell install script (Windows)"
	@echo "  release           - Create a release package"
	@echo "  help              - Show this help message" 