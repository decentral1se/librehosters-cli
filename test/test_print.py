"""Print utilities test module."""

import click
from tabulate import tabulate


def test_success_print_handles_colour_toggling(mocker):
    from librehosters_cli.print import _success

    mocker.spy(click, 'secho')

    _success('foo', colour=False)
    assert not click.secho.called

    _success('foo', colour=True)
    click.secho.assert_called_once_with('foo', bold=True, fg='green')


def test_to_table(mocker):
    from librehosters_cli.print import _to_table

    mocker.spy(click, 'echo')

    _to_table([['c1', 'c2']], ['h1', 'h2'], True)
    click.echo.assert_called_with('c1 c2')

    table, headers = [['c1', 'c2']], ['h1', 'h2']
    output = tabulate(table, headers=headers, tablefmt='grid')
    _to_table(table, headers, False)
    click.echo.assert_called_with(output)
