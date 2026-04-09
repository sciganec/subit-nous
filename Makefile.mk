# Makefile for SUBIT-NOUS

.PHONY: help install install-dev test lint format clean build publish docker-build docker-up docker-down hooks-install hooks-uninstall

# Default target
help:
	@echo "Available commands:"
	@echo "  make install         - Install package with core dependencies"
	@echo "  make install-dev     - Install with dev dependencies"
	@echo "  make test            - Run tests"
	@echo "  make lint            - Run linters (flake8, mypy)"
	@echo "  make format          - Format code with black and isort"
	@echo "  make clean           - Remove build artifacts"
	@echo "  make build           - Build distribution packages"
	@echo "  make publish         - Upload to PyPI (requires credentials)"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-up       - Start Docker Compose services"
	@echo "  make docker-down     - Stop Docker Compose services"
	@echo "  make hooks-install   - Install Git hooks in current repo"
	@echo "  make hooks-uninstall - Remove Git hooks"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

test:
	pytest tests/ -v --cov=src/subit_nous

lint:
	flake8 src/subit_nous tests
	mypy src/subit_nous

format:
	black src/subit_nous tests
	isort src/subit_nous tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

docker-build:
	docker build -t subit-nous .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

hooks-install:
	nous hooks install .

hooks-uninstall:
	nous hooks uninstall .