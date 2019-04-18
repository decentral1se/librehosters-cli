"""Print utilities module."""

import typing

import click

from librehosters_cli.config import Config


def _success(message: typing.Text, config: Config) -> typing.Any:
    """Show validation sucess."""
    if config.colour:
        styled = click.style(message, fg='green', bold=True)
        return click.echo(styled)

    return click.echo(message)
