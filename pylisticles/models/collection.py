"""Collection and related data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Mapping, Union
from uuid import uuid4


@dataclass
class Field:
    """Represents a field definition for a collection."""

    name: str
    type: str  # "text", "number", "date", "boolean", "select"
    required: bool = False
    options: List[str] = field(default_factory=list)


@dataclass
class Item:
    """Represents an item within a collection."""

    id: str = field(default_factory=lambda: str(uuid4()))
    data: Dict[str, Union[str, int, float, bool]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __init__(
        self, 
        data: Mapping[str, Union[str, int, float, bool]] | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """Initialize Item with proper type conversion."""
        self.id = id or str(uuid4())
        self.data = dict(data) if data else {}
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()


@dataclass
class Collection:
    """Represents a collection of items with custom fields."""

    name: str
    type: str
    fields: List[Field] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_item(self, data: Mapping[str, Union[str, int, float, bool]]) -> Item:
        """Add a new item to the collection."""
        item = Item(data=dict(data))
        self.items.append(item)
        self.updated_at = datetime.now()
        return item

    def get_field_names(self) -> List[str]:
        """Get list of field names for this collection."""
        return [field.name for field in self.fields]
