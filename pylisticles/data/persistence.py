"""Markdown-based persistence layer for collections."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import yaml

from ..models.collection import Collection, Field, Item


class PersistenceError(Exception):
    """Base exception for persistence operations."""

    pass


class CollectionStorage:
    """Handles saving and loading collections to/from markdown files."""

    def __init__(self, data_dir: str | None = None) -> None:
        """Initialize storage with data directory."""
        if data_dir is None:
            data_dir = os.path.expanduser("~/pylisticles-data")

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, name: str) -> str:
        """Convert collection name to safe filename."""
        # Remove/replace unsafe characters
        safe_name = re.sub(r'[<>:"/\\|?*]', "_", name)
        # Remove leading/trailing whitespace and dots
        safe_name = safe_name.strip(". ")
        # Ensure not empty
        if not safe_name:
            safe_name = "unnamed_collection"
        return safe_name

    def _get_file_path(self, collection_name: str) -> Path:
        """Get file path for a collection."""
        filename = f"{self._sanitize_filename(collection_name)}.md"
        return self.data_dir / filename

    def _serialize_datetime(self, dt: datetime) -> str:
        """Convert datetime to ISO format string."""
        return dt.isoformat()

    def _deserialize_datetime(self, dt_str: str) -> datetime:
        """Convert ISO format string to datetime."""
        return datetime.fromisoformat(dt_str)

    def _collection_to_yaml_data(
        self, collection: Collection
    ) -> Dict[str, Union[Dict[str, str], List[Dict[str, Union[str, bool, List[str]]]]]]:
        """Convert Collection to YAML-serializable data."""
        return {
            "collection": {
                "name": collection.name,
                "type": collection.type,
                "created_at": self._serialize_datetime(collection.created_at),
                "updated_at": self._serialize_datetime(collection.updated_at),
            },
            "fields": [
                {
                    "name": field.name,
                    "type": field.type,
                    "required": field.required,
                    "options": field.options,
                }
                for field in collection.fields
            ],
        }

    def _items_to_markdown_table(self, collection: Collection) -> str:
        """Convert collection items to markdown table."""
        if not collection.items:
            return ""

        field_names = collection.get_field_names()
        if not field_names:
            return ""

        # Create table header
        header = "| " + " | ".join(field_names) + " |"
        separator = "| " + " | ".join("---" for _ in field_names) + " |"

        # Create table rows
        rows = []
        for item in collection.items:
            row_data = []
            for field_name in field_names:
                value = item.data.get(field_name, "")
                # Convert value to string for table display
                if isinstance(value, bool):
                    row_data.append("✓" if value else "✗")
                elif isinstance(value, (int, float)):
                    row_data.append(str(value))
                elif isinstance(value, str):
                    # Escape pipe characters in strings
                    row_data.append(value.replace("|", "\\|"))
                else:
                    row_data.append(str(value))

            row = "| " + " | ".join(row_data) + " |"
            rows.append(row)

        return "\n".join([header, separator] + rows)

    def _markdown_table_to_items(
        self, markdown_content: str, fields: List[Field]
    ) -> List[Item]:
        """Parse markdown table back to items."""
        if not markdown_content.strip():
            return []

        lines = markdown_content.strip().split("\n")
        if len(lines) < 3:  # Need header, separator, and at least one row
            return []

        # Parse field names from header
        header_line = lines[0].strip()
        if not header_line.startswith("|") or not header_line.endswith("|"):
            return []

        field_names = [name.strip() for name in header_line[1:-1].split("|")]

        # Create field type mapping
        field_types = {field.name: field.type for field in fields}

        # Parse data rows (skip header and separator)
        items = []
        for line in lines[2:]:
            line = line.strip()
            if not line.startswith("|") or not line.endswith("|"):
                continue

            values = [val.strip() for val in line[1:-1].split("|")]
            if len(values) != len(field_names):
                continue

            # Convert values based on field types
            item_data: Dict[str, Union[str, int, float, bool]] = {}
            for field_name, value in zip(field_names, values):
                if not value:  # Empty value
                    continue

                field_type = field_types.get(field_name, "text")

                try:
                    if field_type == "boolean":
                        item_data[field_name] = value == "✓"
                    elif field_type == "number":
                        # Try int first, then float
                        if "." in value:
                            item_data[field_name] = float(value)
                        else:
                            item_data[field_name] = int(value)
                    else:  # text, date, select
                        # Unescape pipe characters
                        item_data[field_name] = value.replace("\\|", "|")
                except ValueError:
                    # If conversion fails, store as string
                    item_data[field_name] = value.replace("\\|", "|")

            if item_data:  # Only add if we have data
                items.append(Item(data=item_data))

        return items

    def save_collection(self, collection: Collection) -> None:
        """Save collection to markdown file."""
        try:
            file_path = self._get_file_path(collection.name)

            # Create YAML frontmatter
            yaml_data = self._collection_to_yaml_data(collection)
            yaml_content = yaml.dump(
                yaml_data, default_flow_style=False, sort_keys=False
            )

            # Create markdown content
            markdown_table = self._items_to_markdown_table(collection)

            # Combine into full file content
            content = f"---\n{yaml_content}---\n\n# {collection.name}\n\n"
            if markdown_table:
                content += markdown_table + "\n"

            # Write to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        except Exception as e:
            raise PersistenceError(
                f"Failed to save collection '{collection.name}': {e}"
            ) from e

    def load_collection(self, collection_name: str) -> Collection:
        """Load collection from markdown file."""
        try:
            file_path = self._get_file_path(collection_name)

            if not file_path.exists():
                raise PersistenceError(f"Collection '{collection_name}' not found")

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split frontmatter and content
            if not content.startswith("---\n"):
                raise PersistenceError(
                    f"Invalid file format for '{collection_name}': missing YAML frontmatter"
                )

            parts = content[4:].split("\n---\n", 1)
            if len(parts) != 2:
                raise PersistenceError(
                    f"Invalid file format for '{collection_name}': malformed frontmatter"
                )

            yaml_content, markdown_content = parts

            # Parse YAML frontmatter
            yaml_data = yaml.safe_load(yaml_content)
            if not isinstance(yaml_data, dict):
                raise PersistenceError(f"Invalid YAML data in '{collection_name}'")

            collection_data = yaml_data.get("collection", {})
            fields_data = yaml_data.get("fields", [])

            # Create Field objects
            fields = [
                Field(
                    name=field_data["name"],
                    type=field_data["type"],
                    required=field_data.get("required", False),
                    options=field_data.get("options", []),
                )
                for field_data in fields_data
            ]

            # Parse items from markdown table
            # Find the table in markdown content (after the header)
            lines = markdown_content.strip().split("\n")
            table_start = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("|") and "|" in line.strip()[1:]:
                    table_start = i
                    break

            table_content = ""
            if table_start >= 0:
                table_lines = []
                for line in lines[table_start:]:
                    if line.strip().startswith("|"):
                        table_lines.append(line)
                    elif line.strip() == "":
                        continue  # Skip empty lines within table
                    else:
                        break  # End of table
                table_content = "\n".join(table_lines)

            items = self._markdown_table_to_items(table_content, fields)

            # Create Collection object
            collection = Collection(
                name=collection_data["name"],
                type=collection_data["type"],
                fields=fields,
                items=items,
                created_at=self._deserialize_datetime(collection_data["created_at"]),
                updated_at=self._deserialize_datetime(collection_data["updated_at"]),
            )

            return collection

        except PersistenceError:
            raise
        except Exception as e:
            raise PersistenceError(
                f"Failed to load collection '{collection_name}': {e}"
            ) from e

    def list_collections(self) -> List[str]:
        """List all available collection names."""
        try:
            collections = []
            for file_path in self.data_dir.glob("*.md"):
                # Extract collection name from filename
                collection_name = file_path.stem
                collections.append(collection_name)
            return sorted(collections)
        except Exception as e:
            raise PersistenceError(f"Failed to list collections: {e}") from e

    def delete_collection(self, collection_name: str) -> None:
        """Delete a collection file."""
        try:
            file_path = self._get_file_path(collection_name)
            if not file_path.exists():
                raise PersistenceError(f"Collection '{collection_name}' not found")

            file_path.unlink()
        except PersistenceError:
            raise
        except Exception as e:
            raise PersistenceError(
                f"Failed to delete collection '{collection_name}': {e}"
            ) from e

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists."""
        file_path = self._get_file_path(collection_name)
        return file_path.exists()
