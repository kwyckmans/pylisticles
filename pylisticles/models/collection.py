"""Collection and related data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
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
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Collection:
    """Represents a collection of items with custom fields."""
    name: str
    type: str
    fields: List[Field] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_item(self, data: Dict[str, Any]) -> Item:
        """Add a new item to the collection."""
        item = Item(data=data)
        self.items.append(item)
        self.updated_at = datetime.now()
        return item
    
    def get_field_names(self) -> List[str]:
        """Get list of field names for this collection."""
        return [field.name for field in self.fields]