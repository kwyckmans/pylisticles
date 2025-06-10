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

## Screenshots

### Collection List View
![Collection List](screenshots/collection-list.png)
*Main view showing available collections with item counts. Navigate using arrow keys and press Enter to view details.*

### Collection Details View
![Collection Details](screenshots/collection-details.png)
*Detailed view of a collection showing all items in a table format with custom fields.*

The application uses the gruvbox theme providing excellent contrast and readability in terminal environments. Keyboard shortcuts are clearly visible in the footer with proper color contrast.

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

# Try the persistence layer demo
python demo_persistence.py
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

### Persistence Layer Demo

Run `python demo_persistence.py` to see the persistence layer in action. This creates a sample "Guitar Practice" collection and demonstrates saving/loading functionality.

Example output:
```
🚀 Pylisticles Persistence Layer Demo
========================================

📝 Creating a 'Guitar Practice' collection...
   Collection: Guitar Practice
   Fields: ['song_name', 'artist', 'difficulty', 'practiced_today', 'rating']
   Items: 3

💾 Saving collection to markdown file...
   Saved to: /home/user/pylisticles-data/Guitar Practice.md

📄 Generated markdown file contents:
----------------------------------------
---
collection:
  name: Guitar Practice
  type: music
  created_at: '2024-01-15T10:30:00.123456'
  updated_at: '2024-01-15T10:30:00.123456'
fields:
- name: song_name
  type: text
  required: true
  options: []
- name: artist
  type: text
  required: false
  options: []
- name: difficulty
  type: select
  required: false
  options:
  - beginner
  - intermediate
  - advanced
---

# Guitar Practice

| song_name | artist | difficulty | practiced_today | rating |
| --- | --- | --- | --- | --- |
| Wonderwall | Oasis | beginner | ✓ | 4 |
| Stairway to Heaven | Led Zeppelin | advanced | ✗ | 5 |
| Blackbird | The Beatles | intermediate | ✓ | 4 |
----------------------------------------

🎵 Loaded practice items:
   1. Wonderwall by Oasis (beginner) - Practiced: ✓ - Rating: 4/5
   2. Stairway to Heaven by Led Zeppelin (advanced) - Practiced: ✗ - Rating: 5/5
   3. Blackbird by The Beatles (intermediate) - Practiced: ✓ - Rating: 4/5

✅ Demo complete! Collection saved to /home/user/pylisticles-data/Guitar Practice.md
```

The demo creates a collection in `~/pylisticles-data/` that you can inspect and edit directly.

## Status

=� This project is in early development. The basic structure is in place and core features are being implemented.

## Learning Goals

This project serves as a framework for learning TUI development in Python while building personalized productivity tools.

## Contributing

This is a personal project not intended for collaboration. Feel free to fork it for your own use, but I won't be accepting contributions or providing support.
