# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI-CLAUDE-REMINDER**: This is pylisticles - a flexible TUI-based list management application for personal use and learning TUI development. Uses Textual framework for TUI, stores data in markdown files with YAML frontmatter.

This is a Python project called "pylisticles" - a CLI application with Terminal User Interface (TUI) for creating, viewing, and managing various types of lists with custom fields and metadata. Built for personal use as a learning framework for TUI development.

### Key Concepts
- **Flexible Schema**: Each collection type can have different custom fields
- **TUI Interface**: Uses Textual framework for modern terminal UI
- **Markdown Storage**: Data stored as markdown files with YAML frontmatter for portability
- **Personal Tool**: Built for learning, not intended for collaboration or support

## Development Commands

### Running the application
```bash
python main.py
```

### Dependency management
- Install dependencies: `uv sync`
- Add new dependency: `uv add <package-name>`

### Code quality
- Format and lint code: `uv run ruff check --fix`
- Format code only: `uv run ruff format`
- Type check code: `uv run pyright`
- Run tests: `uv run pytest`
- Test coverage: `uv run coverage run -m pytest && uv run coverage report`
- Coverage HTML report: `uv run coverage html` (opens in `htmlcov/index.html`)
- Pre-commit hooks: `uv run pre-commit run --all-files`
- Install pre-commit hooks: `uv run pre-commit install`

**IMPORTANT**: All code must pass ruff, pyright, and pytest checks before committing. Pre-commit hooks will automatically run these checks. Coverage is tracked but not required to pass.

### Code Style Requirements
- Never use `any` type - all code must be explicitly typed
- Use Union types instead of Any for flexible typing
- Use Mapping instead of Dict for covariant parameter types

## Project Structure

```
pylisticles/
├── pylisticles/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── collection.py      # Collection, Field, Item data models
│   ├── ui/
│   │   └── __init__.py        # Textual UI components
│   ├── data/
│   │   └── __init__.py        # Markdown persistence layer
│   └── utils/
│       └── __init__.py        # Utility functions
├── tests/                     # Unit tests with pytest
│   ├── __init__.py
│   └── test_models.py         # Tests for data models
├── main.py                    # Entry point - runs PylisticlesApp
├── pyproject.toml            # Dependencies: textual, ruff, pyright, pytest
└── README.md                 # Project documentation
```

## Technical Decisions

### TUI Framework: Textual
- Modern, async-powered TUI library built on Rich
- 16.7M colors, mouse support, smooth animations
- Web-like component approach for building interfaces
- **IMPORTANT**: Only use CSS that is valid for Textual.

### Data Model
- **Collection**: name, type, fields, items, timestamps
- **Field**: name, type (text/number/date/boolean/select), required, options
- **Item**: id, data dict, timestamps
- Flexible schema allows different field types per collection

### Data Storage Format
Each collection stored as separate `.md` file:
```markdown
---
collection:
  name: "Guitar Practice"
  type: "music"
  created_at: "2024-01-15T10:30:00Z"
fields:
  - name: "song_name"
    type: "text"
    required: true
---

# Guitar Practice

| Song Name | Artist | Difficulty | Notes |
|-----------|--------|------------|-------|
| Wonderwall | Oasis | beginner | Working on transitions |
```

## Development Status & Next Steps

**AI-CLAUDE-REMINDER**: Phase 1 complete. Next phase: implement data persistence layer for markdown read/write operations, then basic TUI with collection navigation.

### Phase 1: Foundation & Research ✅ COMPLETED
1. ✅ Research TUI frameworks - Selected Textual
2. ✅ Design data model - Collection/Field/Item with flexible schema
3. ✅ Define markdown format - YAML frontmatter + markdown tables
4. ✅ Set up project structure - Created modules, added Textual dependency

### Phase 2: Core Implementation (IN PROGRESS)
5. 🔄 Implement data persistence - Markdown read/write operations
6. ⏳ Create basic TUI - Collection list and navigation with Textual
7. ⏳ Collection CRUD - Add, view, edit, delete collections
8. ⏳ Item CRUD - Manage individual items within collections

### Phase 3: Advanced Features (PLANNED)
9. ⏳ Custom fields - Allow defining different field types per collection
10. ⏳ Search & filtering - Find items across collections

## Key Information

- Python version requirement: >=3.12
- Uses uv for package management instead of pip
- Dependencies: textual>=3.3.0, ruff>=0.11.13
- Data directory: `~/pylisticles-data/` (markdown files)

## Coding Guidelines
- Never use the `any` type. All code should be explicitly typed.
- Code has to pass both ruff and pyright checks before it can be commited.
- Tests have to pass before any code can be commited.

## Test Writing Guidelines
- Feel free to add test skeletons, with a good set of use cases and clear naming but NEVER fill in the actual test. If, and only if, the name is too complicated, add a comment explaining the expected behaviour of the test. Inside the test, add a TODO comment.

## Commit Guidelines
- Perform a commit after implementing a logical feature or step from your plan. Use a commit message with a max length of 80 characters.
