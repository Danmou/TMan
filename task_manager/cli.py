"""Console script for task_manager."""

import click


@click.command()
def main() -> None:
    """Main entrypoint."""
    click.echo("TaskManager")
    click.echo("=" * len("TaskManager"))
    click.echo("Skeleton project created by Cookiecutter PyPackage")


if __name__ == "__main__":
    main()  # pragma: no cover
