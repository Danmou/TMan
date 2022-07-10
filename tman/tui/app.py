#  Copyright (c) 2021, Daniel Mouritzen.

"""Top-level TUI application."""
from typing import Any

import rich.box
from rich.panel import Panel
from textual.app import App
from textual.message import Message
from textual.reactive import Reactive
from textual.widgets import Footer, Header, Static
from textual_inputs import IntegerInput, TextInput

from tman.tui.widgets import Dropdown


class TManTUI(App):
    """Top-level TUI application."""

    current_index: Reactive[int] = Reactive(-1)

    def __init__(self, **kwargs: Any) -> None:
        """TODO."""
        super().__init__(**kwargs)
        self.tab_index = ["username", "choice", "age"]
        self.header = Header(tall=False, style="white on rgb(98,98,98)", symbol="🗂️")
        self.footer = Footer(style="white on rgb(98,98,98)")
        self.username = TextInput(
            name="username",
            placeholder="enter your username...",
            title="Username",
        )
        self.choice = Dropdown(
            name="choice",
            title="Choose something",
            options=["Option_1", "Option_2"],
        )
        self.age = IntegerInput(
            name="age",
            placeholder="enter your age...",
            title="Age",
        )
        self.output = Static(renderable=Panel("", title="Report", border_style="blue", box=rich.box.SQUARE))

    async def on_load(self) -> None:
        """TODO."""
        await self.bind("q", "quit", "Quit")
        await self.bind("enter", "submit", "Submit")
        await self.bind("escape", "reset_focus", show=False)
        await self.bind("ctrl+i", "next_tab_index", show=False)  # Tab character
        await self.bind("shift+tab", "previous_tab_index", show=False)

    async def on_mount(self) -> None:
        """TODO."""
        await self.view.dock(self.header, edge="top")
        await self.view.dock(self.footer, edge="bottom")
        await self.view.dock(self.output, edge="left", size=40)
        await self.view.dock(self.username, self.choice, self.age, edge="top")

    async def action_next_tab_index(self) -> None:
        """Changes the focus to the next form field."""
        if self.current_index < len(self.tab_index) - 1:
            self.current_index += 1
            await getattr(self, self.tab_index[self.current_index]).focus()

    async def action_previous_tab_index(self) -> None:
        """Changes the focus to the previous form field."""
        self.log(f"PREVIOUS {self.current_index}")
        if self.current_index > 0:
            self.current_index -= 1
            await getattr(self, self.tab_index[self.current_index]).focus()

    async def action_submit(self) -> None:
        """TODO."""
        await self.output.update(Panel("", title="Report", border_style="blue", box=rich.box.SQUARE))

    async def action_reset_focus(self) -> None:
        """TODO."""
        self.current_index = -1
        await self.header.focus()

    async def message_input_on_change(self, message: Message) -> None:
        """TODO."""
        self.log(f"Input: {message.sender.name} changed")

    async def message_input_on_focus(self, message: Message) -> None:
        """TODO."""
        self.current_index = self.tab_index.index(message.sender.name)
