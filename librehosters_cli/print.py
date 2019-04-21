"""Print utilities module."""

import typing

import click
from tabulate import tabulate


def _success(message: typing.Text, colour: bool) -> typing.Any:
    """Show a sucessful message."""
    if colour:
        return click.secho(message, fg='green', bold=True)
    return click.echo(message)


def _to_table(
    table: typing.List, headers: typing.List, bare: bool
) -> typing.Any:
    """Print table output."""
    if bare:
        rows = [map(str, row) for row in table]
        return click.echo('\n'.join(' '.join(row) for row in rows))
    return click.echo(tabulate(table, headers=headers, tablefmt='grid'))
