"""Main Textual application for pylisticles."""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class PylisticlesApp(App[None]):
    """Main application class for pylisticles TUI."""

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        # Placeholder - will be implemented in Phase 2
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        """Handle app startup."""
        self.title = "Pylisticles"
        self.sub_title = "Personal List Management"