#  Copyright (c) 2021, Daniel Mouritzen.

"""Main CLI entry point."""

import click


@click.group()
def cli() -> None:
    """Welcome to the TMan CLI!"""  # noqa: D400
    pass


@cli.command()
def gui() -> None:
    """Start the TMan GUI."""
    from tman.gui import run

    run()


@cli.command()
def tui() -> None:
    """Start the TMan TUI."""
    from tman.tui import run

    run()
