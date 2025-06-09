# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project called "pylisticles" that uses uv for dependency management. The project is in early development with a simple main.py entry point.

## Development Commands

### Running the application
```bash
python main.py
```

### Dependency management
- Install dependencies: `uv sync`
- Add new dependency: `uv add <package-name>`

### Code quality
- Format and lint code: `ruff check --fix`
- Format code only: `ruff format`

## Project Structure

- `main.py` - Main entry point with a simple hello world function
- `pyproject.toml` - Project configuration and dependencies
- Dependencies managed via uv with ruff included for code formatting/linting

## Key Information

- Python version requirement: >=3.12
- Uses uv for package management instead of pip
- Ruff is configured for code quality checks