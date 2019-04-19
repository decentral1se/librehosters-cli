"""Print utilities test module."""

import click


def test_success_print_handles_colour_toggling(mocker, mock_config):
    from librehosters_cli.print import _success

    mocker.spy(click, 'secho')
    mock_config.colour = True
    _success('foo', mock_config)
    click.secho.assert_called_once_with('foo', bold=True, fg='green')
