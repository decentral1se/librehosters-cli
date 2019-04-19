"""Print utilities test module."""

import click


def test_success_print_handles_colour_toggling(mocker):
    from librehosters_cli.print import _success

    mocker.spy(click, 'secho')

    _success('foo', colour=False)
    assert not click.secho.called

    _success('foo', colour=True)
    click.secho.assert_called_once_with('foo', bold=True, fg='green')
