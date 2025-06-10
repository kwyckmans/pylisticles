"""Tests for persistence layer."""

import tempfile
from pathlib import Path

import pytest

from pylisticles.data import CollectionStorage, PersistenceError
from pylisticles.models.collection import Collection, Field


class TestCollectionStorage:
    """Test CollectionStorage functionality."""

    def test_save_and_load_empty_collection(self):
        """Test saving and loading an empty collection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            # Create empty collection
            collection = Collection(name="Test Collection", type="test")
            collection.fields = [
                Field(name="title", type="text", required=True),
                Field(name="completed", type="boolean", required=False),
            ]

            # Save and load
            storage.save_collection(collection)
            loaded = storage.load_collection("Test Collection")

            assert loaded.name == collection.name
            assert loaded.type == collection.type
            assert len(loaded.fields) == 2
            assert loaded.fields[0].name == "title"
            assert loaded.fields[0].type == "text"
            assert loaded.fields[0].required is True
            assert loaded.fields[1].name == "completed"
            assert loaded.fields[1].type == "boolean"
            assert loaded.fields[1].required is False
            assert len(loaded.items) == 0

    def test_save_and_load_collection_with_items(self):
        """Test saving and loading a collection with items."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            # Create collection with items
            collection = Collection(name="Tasks", type="todo")
            collection.fields = [
                Field(name="task", type="text", required=True),
                Field(name="priority", type="number", required=False),
                Field(name="done", type="boolean", required=False),
            ]

            # Add items
            collection.add_item({"task": "Buy groceries", "priority": 1, "done": False})
            collection.add_item({"task": "Walk dog", "priority": 2, "done": True})

            # Save and load
            storage.save_collection(collection)
            loaded = storage.load_collection("Tasks")

            assert loaded.name == "Tasks"
            assert len(loaded.items) == 2

            # Check first item
            item1 = loaded.items[0]
            assert item1.data["task"] == "Buy groceries"
            assert item1.data["priority"] == 1
            assert item1.data["done"] is False

            # Check second item
            item2 = loaded.items[1]
            assert item2.data["task"] == "Walk dog"
            assert item2.data["priority"] == 2
            assert item2.data["done"] is True

    def test_list_collections(self):
        """Test listing collections."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            # Initially empty
            assert storage.list_collections() == []

            # Create and save collections
            coll1 = Collection(name="Collection 1", type="test")
            coll2 = Collection(name="Collection 2", type="test")

            storage.save_collection(coll1)
            storage.save_collection(coll2)

            # Should list both
            collections = storage.list_collections()
            assert set(collections) == {"Collection 1", "Collection 2"}

    def test_delete_collection(self):
        """Test deleting a collection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            # Create and save collection
            collection = Collection(name="To Delete", type="test")
            storage.save_collection(collection)

            assert storage.collection_exists("To Delete")

            # Delete it
            storage.delete_collection("To Delete")

            assert not storage.collection_exists("To Delete")
            assert "To Delete" not in storage.list_collections()

    def test_collection_exists(self):
        """Test checking if collection exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            assert not storage.collection_exists("Nonexistent")

            # Create collection
            collection = Collection(name="Exists", type="test")
            storage.save_collection(collection)

            assert storage.collection_exists("Exists")

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            # Test with problematic characters
            collection = Collection(name="Test/Collection<>:|?*", type="test")
            storage.save_collection(collection)

            # Should be able to load it back
            loaded = storage.load_collection("Test/Collection<>:|?*")
            assert loaded.name == "Test/Collection<>:|?*"

    def test_load_nonexistent_collection(self):
        """Test loading nonexistent collection raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            with pytest.raises(PersistenceError, match="not found"):
                storage.load_collection("Nonexistent")

    def test_delete_nonexistent_collection(self):
        """Test deleting nonexistent collection raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            with pytest.raises(PersistenceError, match="not found"):
                storage.delete_collection("Nonexistent")

    def test_data_directory_creation(self):
        """Test that data directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "nested" / "data"

            # Directory doesn't exist yet
            assert not nested_dir.exists()

            # Creating storage should create directory
            CollectionStorage(str(nested_dir))
            assert nested_dir.exists()
            assert nested_dir.is_dir()

    def test_field_types_roundtrip(self):
        """Test that different field types are preserved through save/load."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CollectionStorage(temp_dir)

            collection = Collection(name="Types Test", type="test")
            collection.fields = [
                Field(name="text_field", type="text"),
                Field(name="number_field", type="number"),
                Field(name="bool_field", type="boolean"),
                Field(name="select_field", type="select", options=["A", "B", "C"]),
            ]

            # Add item with different types
            collection.add_item(
                {
                    "text_field": "Hello World",
                    "number_field": 42,
                    "bool_field": True,
                    "select_field": "A",
                }
            )

            storage.save_collection(collection)
            loaded = storage.load_collection("Types Test")

            # Check field definitions
            field_map = {f.name: f for f in loaded.fields}
            assert field_map["select_field"].options == ["A", "B", "C"]

            # Check item data types
            item = loaded.items[0]
            assert item.data["text_field"] == "Hello World"
            assert item.data["number_field"] == 42
            assert item.data["bool_field"] is True
            assert item.data["select_field"] == "A"
