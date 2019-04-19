"""Print utilities module."""

import typing

import click


def _success(message: typing.Text, colour: bool) -> typing.Any:
    """Show a sucessful message."""
    if colour:
        return click.secho(message, fg='green', bold=True)
    return click.echo(message)
