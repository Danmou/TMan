#  Copyright (c) 2021, Daniel Mouritzen.

"""Main CLI entry point."""

import click


@click.command()
def main() -> None:
    """Welcome to the TaskManager CLI!"""  # noqa: D400
    click.echo("TaskManager")
    click.echo("=" * len("TaskManager"))
    click.echo("Skeleton project created by Cookiecutter PyPackage")
