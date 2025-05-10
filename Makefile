.PHONY: clean test install dev-install lint coverage docs

# Use Poetry for commands
POETRY := poetry

# Test command with verbose output
test:
	$(POETRY) run pytest -xvs ./easycmdline/tests

# Run tests with coverage
coverage:
	$(POETRY) run pytest --cov=easycmdline ./easycmdline/tests --cov-report=term --cov-report=html
	@echo "HTML coverage report generated in htmlcov/"

# Install package
install:
	$(POETRY) install

# Install development dependencies
dev-install:
	$(POETRY) install --with dev

# Lint code
lint:
	$(POETRY) run flake8 --max-line-length=120 easycmdline
	$(POETRY) run pylint --max-line-length=120 easycmdline

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
	$(POETRY) run python examples/myapp/mycli.py

# Type checking with mypy
typecheck:
	$(POETRY) run mypy easycmdline

# Show help
help:
	@echo "Available targets:"
	@echo "  test         Run tests"
	@echo "  coverage     Run tests with coverage report"
	@echo "  install      Install package"
	@echo "  dev-install  Install development dependencies"
	@echo "  lint         Lint code"
	@echo "  typecheck    Run mypy type checking"
	@echo "  clean        Clean build artifacts"
	@echo "  docs         Generate documentation" 
	@echo "  example      Run an example script"
