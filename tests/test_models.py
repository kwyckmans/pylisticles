"""Tests for pylisticles data models."""

from datetime import datetime


from pylisticles.models.collection import Collection, Field, Item


class TestField:
    """Test cases for Field model."""

    def test_field_creation(self) -> None:
        """Test basic field creation."""
        field = Field(name="test_field", type="text")
        assert field.name == "test_field"
        assert field.type == "text"
        assert field.required is False
        assert field.options == []

    def test_field_with_options(self) -> None:
        """Test field creation with options."""
        field = Field(
            name="difficulty",
            type="select",
            required=True,
            options=["easy", "medium", "hard"],
        )
        assert field.name == "difficulty"
        assert field.type == "select"
        assert field.required is True
        assert field.options == ["easy", "medium", "hard"]


class TestItem:
    """Test cases for Item model."""

    def test_item_creation(self) -> None:
        """Test basic item creation."""
        data = {"title": "Test Song", "artist": "Test Artist"}
        item = Item(data=data)

        assert item.data == data
        assert isinstance(item.id, str)
        assert len(item.id) > 0
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_item_with_different_data_types(self) -> None:
        """Test item with various data types."""
        data = {
            "title": "Test Song",
            "rating": 5,
            "price": 9.99,
            "is_favorite": True,
        }
        item = Item(data=data)
        assert item.data == data


class TestCollection:
    """Test cases for Collection model."""

    def test_collection_creation(self) -> None:
        """Test basic collection creation."""
        collection = Collection(name="Test Collection", type="music")

        assert collection.name == "Test Collection"
        assert collection.type == "music"
        assert collection.fields == []
        assert collection.items == []
        assert isinstance(collection.created_at, datetime)
        assert isinstance(collection.updated_at, datetime)

    def test_collection_with_fields(self) -> None:
        """Test collection creation with fields."""
        fields = [
            Field(name="title", type="text", required=True),
            Field(name="rating", type="number"),
        ]
        collection = Collection(name="Music Collection", type="music", fields=fields)

        assert collection.fields == fields
        assert collection.get_field_names() == ["title", "rating"]

    def test_add_item(self) -> None:
        """Test adding items to collection."""
        collection = Collection(name="Test Collection", type="music")
        data = {"title": "Test Song", "artist": "Test Artist"}

        initial_updated = collection.updated_at
        item = collection.add_item(data)

        assert len(collection.items) == 1
        assert collection.items[0] == item
        assert item.data == data
        assert collection.updated_at > initial_updated

    def test_get_field_names_empty(self) -> None:
        """Test getting field names from empty collection."""
        collection = Collection(name="Empty Collection", type="test")
        assert collection.get_field_names() == []
