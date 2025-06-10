"""Main Textual application for pylisticles."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive, Reactive
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    ListView,
    ListItem,
    Static,
)

from ..data.persistence import CollectionStorage, PersistenceError
from ..models.collection import Collection


class CollectionListView(Container):
    """Widget for displaying list of collections."""

    def __init__(self) -> None:
        super().__init__()
        self.storage = CollectionStorage()
        self.collections: list[str] = []

    def compose(self) -> ComposeResult:
        """Compose the collection list view."""
        yield Static("Collections", classes="section-title")
        yield ListView(id="collection-list")

    def on_mount(self) -> None:
        """Load collections when mounted."""
        self.refresh_collections()

    def refresh_collections(self) -> None:
        """Refresh the list of collections."""
        try:
            self.collections = self.storage.list_collections()
            list_view = self.query_one("#collection-list", ListView)
            list_view.clear()

            if not self.collections:
                list_view.append(
                    ListItem(Static("No collections found"), disabled=True)
                )
            else:
                for collection_name in self.collections:
                    try:
                        # Load collection to get item count
                        collection = self.storage.load_collection(collection_name)
                        item_count = len(collection.items)
                        label = f"{collection_name} ({item_count} items)"
                    except PersistenceError:
                        label = f"{collection_name} (error loading)"

                    list_view.append(ListItem(Static(label), name=collection_name))
        except PersistenceError as e:
            list_view = self.query_one("#collection-list", ListView)
            list_view.clear()
            list_view.append(ListItem(Static(f"Error: {e}"), disabled=True))


class CollectionDetailView(Container):
    """Widget for displaying collection details and items."""

    def __init__(self) -> None:
        super().__init__()
        self.storage = CollectionStorage()
        self.current_collection: Collection | None = None

    def compose(self) -> ComposeResult:
        """Compose the collection detail view."""
        yield Static("Collection Details", classes="section-title", id="detail-title")
        yield Static("", id="collection-info")
        yield DataTable(id="items-table")

    def show_collection(self, collection_name: str) -> None:
        """Display details for a specific collection."""
        try:
            self.current_collection = self.storage.load_collection(collection_name)
            self._update_display()
        except PersistenceError as e:
            self._show_error(f"Error loading collection: {e}")

    def _update_display(self) -> None:
        """Update the display with current collection data."""
        if not self.current_collection:
            return

        # Update title and info
        title = self.query_one("#detail-title", Static)
        title.update(f"Collection: {self.current_collection.name}")

        info = self.query_one("#collection-info", Static)
        info_text = (
            f"Type: {self.current_collection.type} | "
            f"Items: {len(self.current_collection.items)} | "
            f"Created: {self.current_collection.created_at.strftime('%Y-%m-%d')}"
        )
        info.update(info_text)

        # Update data table
        table = self.query_one("#items-table", DataTable)
        table.clear(columns=True)

        if not self.current_collection.fields:
            table.add_column("No fields defined")
            table.add_row("This collection has no fields defined")
            return

        # Add columns for each field
        field_names = self.current_collection.get_field_names()
        for field_name in field_names:
            table.add_column(field_name)

        # Add rows for each item
        if not self.current_collection.items:
            table.add_row(
                *["No items" if i == 0 else "" for i in range(len(field_names))]
            )
        else:
            for item in self.current_collection.items:
                row_data = []
                for field_name in field_names:
                    value = item.data.get(field_name, "")
                    if isinstance(value, bool):
                        row_data.append("✓" if value else "✗")
                    else:
                        row_data.append(str(value))
                table.add_row(*row_data)

    def _show_error(self, error_message: str) -> None:
        """Display an error message."""
        title = self.query_one("#detail-title", Static)
        title.update("Error")

        info = self.query_one("#collection-info", Static)
        info.update(error_message)

        table = self.query_one("#items-table", DataTable)
        table.clear()
        table.add_column("Error")
        table.add_row(error_message)


class PylisticlesApp(App[None]):
    """Main application class for pylisticles TUI."""

    theme: Reactive[str] = reactive("gruvbox")

    CSS = """
    .section-title {
        background: $primary;
        color: $text;
        padding: 0 1;
        margin-bottom: 1;
        text-align: center;
        text-style: bold;
    }

    #collection-list {
        height: 1fr;
        border: solid $primary;
    }

    #items-table {
        height: 1fr;
        border: solid $primary;
    }

    #collection-info {
        padding: 1;
        background: $surface;
        color: $text;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("escape", "back", "Back"),
    ]

    current_view: reactive[str] = reactive("list")

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield Header()

        with Container(id="main-container"):
            self.collection_list = CollectionListView()
            self.collection_detail = CollectionDetailView()

            yield self.collection_list
            yield self.collection_detail

        yield Footer()

    def on_mount(self) -> None:
        """Handle app startup."""
        self.title = "Pylisticles"
        self.sub_title = "Personal List Management"
        self._update_view()

    def watch_current_view(self, _old_view: str, _new_view: str) -> None:
        """React to view changes."""
        self._update_view()

    def _update_view(self) -> None:
        """Update the display based on current view."""
        if self.current_view == "list":
            self.collection_list.display = True
            self.collection_detail.display = False
            self.sub_title = "Personal List Management"
        elif self.current_view == "detail":
            self.collection_list.display = False
            self.collection_detail.display = True
            collection_name = getattr(
                self.collection_detail.current_collection, "name", "Collection"
            )
            self.sub_title = f"Viewing: {collection_name}"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle collection selection."""
        if event.list_view.id == "collection-list" and event.item.name:
            self.collection_detail.show_collection(event.item.name)
            self.current_view = "detail"

    def action_refresh(self) -> None:
        """Refresh the current view."""
        if self.current_view == "list":
            self.collection_list.refresh_collections()
        elif (
            self.current_view == "detail" and self.collection_detail.current_collection
        ):
            self.collection_detail.show_collection(
                self.collection_detail.current_collection.name
            )

    async def action_back(self) -> None:
        """Go back to the collection list."""
        if self.current_view == "detail":
            self.current_view = "list"
