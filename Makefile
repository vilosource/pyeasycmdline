.PHONY: clean test install dev-install lint coverage docs

# Default Python command
PYTHON := python
PIP := pip

# Test command with verbose output
test:
	pytest -xvs ./easycmdline/tests

# Run tests with coverage
coverage:
	pytest --cov=easycmdline ./easycmdline/tests --cov-report=term --cov-report=html
	@echo "HTML coverage report generated in htmlcov/"

# Install package
install:
	$(PIP) install -e .

# Install development dependencies
dev-install:
	$(PIP) install -e ".[dev]"
	$(PIP) install pytest pytest-mock pytest-cov

# Lint code
lint:
	flake8 easycmdline
	pylint easycmdline

# Clean Python and build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

# Generate documentation (placeholder - customize as needed)
docs:
	@echo "Documentation generation not yet configured."
	@echo "Consider using Sphinx or mkdocs for documentation."

# Run an example (modify path as needed)
example:
	$(PYTHON) examples/myapp/mycli.py

# Show help
help:
	@echo "Available targets:"
	@echo "  test         Run tests"
	@echo "  coverage     Run tests with coverage report"
	@echo "  install      Install package"
	@echo "  dev-install  Install development dependencies"
	@echo "  lint         Lint code"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Generate documentation"
	@echo "  example      Run an example script"
