#!/usr/bin/env python3
"""Demonstration of the persistence layer functionality."""

from pylisticles.data import CollectionStorage
from pylisticles.models.collection import Collection, Field


def main() -> None:
    """Demonstrate persistence layer features."""
    print("🚀 Pylisticles Persistence Layer Demo")
    print("=" * 40)
    
    # Initialize storage (will use ~/pylisticles-data by default) 
    storage = CollectionStorage()
    
    # Create a sample collection
    print("\n📝 Creating a 'Guitar Practice' collection...")
    collection = Collection(name="Guitar Practice", type="music")
    
    # Add fields
    collection.fields = [
        Field(name="song_name", type="text", required=True),
        Field(name="artist", type="text", required=False),
        Field(name="difficulty", type="select", options=["beginner", "intermediate", "advanced"]),
        Field(name="practiced_today", type="boolean", required=False),
        Field(name="rating", type="number", required=False),
    ]
    
    # Add some sample items
    collection.add_item({
        "song_name": "Wonderwall", 
        "artist": "Oasis",
        "difficulty": "beginner",
        "practiced_today": True,
        "rating": 4
    })
    
    collection.add_item({
        "song_name": "Stairway to Heaven",
        "artist": "Led Zeppelin", 
        "difficulty": "advanced",
        "practiced_today": False,
        "rating": 5
    })
    
    collection.add_item({
        "song_name": "Blackbird",
        "artist": "The Beatles",
        "difficulty": "intermediate", 
        "practiced_today": True,
        "rating": 4
    })
    
    print(f"   Collection: {collection.name}")
    print(f"   Fields: {[f.name for f in collection.fields]}")
    print(f"   Items: {len(collection.items)}")
    
    # Save to file
    print("\n💾 Saving collection to markdown file...")
    storage.save_collection(collection)
    file_path = storage._get_file_path(collection.name)
    print(f"   Saved to: {file_path}")
    
    # Show file contents
    print("\n📄 Generated markdown file contents:")
    print("-" * 40)
    with open(file_path, 'r') as f:
        print(f.read())
    print("-" * 40)
    
    # Load it back
    print("\n📖 Loading collection from file...")
    loaded_collection = storage.load_collection("Guitar Practice")
    print(f"   Loaded: {loaded_collection.name}")
    print(f"   Fields: {[f.name for f in loaded_collection.fields]}")
    print(f"   Items: {len(loaded_collection.items)}")
    
    # Show loaded items
    print("\n🎵 Loaded practice items:")
    for i, item in enumerate(loaded_collection.items, 1):
        song = item.data.get("song_name", "Unknown")
        artist = item.data.get("artist", "Unknown Artist")
        difficulty = item.data.get("difficulty", "unknown")
        practiced = "✓" if item.data.get("practiced_today") else "✗"
        rating = item.data.get("rating", "N/A")
        print(f"   {i}. {song} by {artist} ({difficulty}) - Practiced: {practiced} - Rating: {rating}/5")
    
    # List all collections
    print(f"\n📚 All collections: {storage.list_collections()}")
    
    print(f"\n✅ Demo complete! Collection saved to {file_path}")
    print("You can edit the markdown file directly and reload it.")


if __name__ == "__main__":
    main()