from __future__ import annotations

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")

import os
import asyncio
from functools import partial

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown

from utils import tree_schema

class NoteSearchApp(App):
    """Searches ab dictionary API as-you-type."""

    CSS_PATH = "dictionary.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_word(message.value)
        else:
            # Clear the results
            self.query_one("#results", Markdown).update("")

    @work(exclusive=True)
    async def lookup_word(self, search_pattern: str) -> None:
        """Looks up a word."""

        vault_path = '~/Documents/personalvault-1/'
        if '~' in vault_path:
            vault_path = os.path.expanduser(vault_path)

        # Use partial to pass arguments to tree_schema
        async_tree_schema = partial(tree_schema, vault_path, search_pattern)

        # Call tree_schema asynchronously using asyncio.to_thread()
        search_results = await asyncio.to_thread(async_tree_schema)

        #search_results = tree_schema(vault_path, search_pattern)

        if search_pattern == self.query_one(Input).value:
            markdown = self.make_word_markdown(search_results)
            self.query_one("#results", Markdown).update(markdown)

    def make_word_markdown(self, results: object) -> str:
        """Convert the results in to markdown."""
        lines = []

        for row in results:
            lines.append(f"- {row['title']}")
        if False:
            if isinstance(results, dict):
                lines.append(f"# {results['title']}")
                lines.append(results["message"])
            elif isinstance(results, list):
                for result in results:
                    lines.append(f"# {result['word']}")
                    lines.append("")
                    for meaning in result.get("meanings", []):
                        lines.append(f"_{meaning['partOfSpeech']}_")
                        lines.append("")
                        for definition in meaning.get("definitions", []):
                            lines.append(f" - {definition['definition']}")
                        lines.append("---")

        return "\n".join(lines)


if __name__ == "__main__":
    app = NoteSearchApp()
    app.run()