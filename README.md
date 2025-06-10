# Pylisticles



A flexible CLI application with a Terminal User Interface (TUI) for creating, viewing, and managing various types of lists with custom fields and metadata.

**Personal Project Notice**: This is a personal tool built for my own use as I learn TUI development and create personalized software. While others are free to use it, I do not intend to maintain it for general use, collaborate on features, or provide support.

## Overview

Pylisticles allows you to organize different types of collections - whether it's songs you want to learn on guitar, books you've read, movies to watch, or any other categorized items. Each list type can have its own custom fields and metadata, giving you complete flexibility in how you structure your data.

## Features

- **Flexible Schema**: Each list type can have different fields/columns tailored to its purpose
- **TUI Interface**: Clean, keyboard-driven terminal interface for easy navigation and editing
- **Markdown Storage**: All data is stored in markdown files, making it portable and readable in other applications
- **Multiple Collection Types**: Support for various list types (music practice, reading list, movies, etc.)
- **Custom Metadata**: Add any fields you need for each collection type

## Example Use Cases

- **Music Practice**: Track songs learned/practicing with fields like instrument, difficulty, date practiced, notes
- **Reading List**: Manage books with author, genre, rating, reading status, notes
- **Movie Watchlist**: Organize movies with director, year, genre, watched status, rating
- **Custom Lists**: Create any type of list with the fields that matter to you

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd pylisticles

# Install dependencies
uv sync

# Run the application
python main.py
```

## Requirements

- Python e3.12
- uv (for dependency management)

## Development

### Setup
```bash
uv sync
```

### Code Quality
```bash
# Format and lint
ruff check --fix

# Format only
ruff format
```

## Data Storage

Collections are stored as markdown files in a structured format, making them:
- Human-readable
- Portable across different applications
- Easy to backup and version control
- Editable in any text editor or markdown viewer

## Status

=� This project is in early development. The basic structure is in place and core features are being implemented.

## Learning Goals

This project serves as a framework for learning TUI development in Python while building personalized productivity tools.

## Contributing

This is a personal project not intended for collaboration. Feel free to fork it for your own use, but I won't be accepting contributions or providing support.
