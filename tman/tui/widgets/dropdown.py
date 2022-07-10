#  Copyright (c) 2021, Daniel Mouritzen.

"""Dropdown widget."""
from typing import Iterable

import rich.box
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import Reactive
from textual.widget import Widget


class DropdownSelectionChanged(Message, bubble=True):  # type: ignore
    """Emitted when the dropdown selection changes."""

    pass


class Dropdown(Widget):
    """Simple dropdown widget."""

    value: Reactive[str | None] = Reactive(None)
    _hovered: Reactive[str | None] = Reactive(None)
    _has_focus: Reactive[bool] = Reactive(False)
    _options: dict[str, Text]
    _debug: Reactive[str] = Reactive("")

    def __init__(
        self,
        *,
        name: str | None = None,
        title: str | None = None,
        value: str | None = None,
        options: list[str] | dict[str, str | Text | tuple[str, Style]],
    ) -> None:
        super().__init__(name)
        self.value = value
        self.title = title
        if not isinstance(options, dict):
            options = {x: x for x in options}
        self._options = {id: Text.assemble(label) for id, label in options.items()}
        self._option_ids = list(self._options.keys())
        # for id, label in self._options.items():
        #     label.apply_meta({"@click": f"click_option('{id}')", "option": id})

    def __rich_repr__(self) -> Iterable[tuple[str, str | None]]:
        yield "name", self.name
        yield "title", self.title
        yield "value", self.value

    @property
    def has_focus(self) -> bool:
        """Produces True if widget is focused."""
        return self._has_focus  # type: ignore

    def render(self) -> RenderableType:
        """Produce a Panel object containing placeholder text or value and cursor."""
        table = Table.grid(
            Column(ratio=1),
            Column(ratio=None),
            expand=True,
            pad_edge=False,
        )
        if self.has_focus:
            # text_parts = []
            # for id, label in self._options.items():
            #     label.style = "green on red" if id == self._hovered else "red on green"
            #     text_parts.extend([label, "\n"])
            # text = Text.assemble(*text_parts[:-1])
            first = True
            for id, label in self._options.items():
                label = label.copy()
                label.style = Style(
                    bgcolor="rgb(98,98,98)" if id == self._hovered else None,
                    meta={"@click": f"click_option('{id}')", "option": id},
                )
                table.add_row(
                    label,
                    "▼" if first else "",
                    # style=,
                )
                first = False
            height = len(self._options)
        else:
            table.add_row(self._options.get(self.value, ""), "◀")
            height = 1

        return Panel(
            table,
            title=self.title,
            title_align="left",
            height=height + 2,
            style=self.style or "",
            border_style=self.border_style or Style(color="blue"),
            box=rich.box.DOUBLE if self.has_focus else rich.box.SQUARE,
        )

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        """Store any key we are moving over."""
        self._hovered = event.style.meta.get("option")

    async def on_focus(self, event: events.Focus) -> None:
        """Handle focus event."""
        self._hovered = self.value or self._option_ids[0]
        self._has_focus = True

    async def on_click(self, event: events.Click) -> None:
        """Handle click event."""
        event.stop()
        self._hovered = event.style.meta.get("option")
        self._has_focus = True

    async def action_click_option(self, option_id: str) -> None:
        """Handle click event from option."""
        if self._has_focus:
            self.value = option_id
            self._has_focus = False
        else:
            self._hovered = option_id
            self._has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        """Handle unfocus event."""
        self._has_focus = False

    async def on_key(self, event: events.Key) -> None:
        """Handle key event."""
        if event.key in ["enter", " "]:
            if not self._has_focus:
                await self.on_focus(event)
            else:
                self.value = self._hovered
                self._has_focus = False
                await self._emit_on_change(event)
        if not self._hovered:
            return
        increment = 0
        if event.key == "up":
            increment = -1
        elif event.key == "down":
            increment = 1
        if increment:
            self._hovered = self._option_ids[
                (self._option_ids.index(self._hovered) + increment) % len(self._option_ids)
            ]

    async def _emit_on_change(self, event: events.Event) -> None:
        """Emit DropdownSelectionChanged event."""
        event.stop()
        await self.emit(DropdownSelectionChanged(self))
