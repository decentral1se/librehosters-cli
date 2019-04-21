"""Member registry exploration module."""

import textwrap
import typing

import click

from librehosters_cli.config import (
    Config,
    librehosters_cli_choices,
    pass_config,
)
from librehosters_cli.network import _get_json
from librehosters_cli.print import _to_table
from librehosters_cli.validate import _validate_option_use


@click.command()
@click.option(
    '-lh',
    '--librehoster',
    metavar='LIBREHOSTER',
    help='A librehoster network member',
    type=click.Choice(librehosters_cli_choices),
)
@click.option(
    '-S',
    '--show',
    'show',
    flag_value='show',
    help='Show all members of the network',
)
@pass_config
def whois(
    config: Config, librehoster: typing.Text, show: typing.Text
) -> typing.Any:
    """Explore the librehosters network registry."""
    _validate_option_use(librehoster, show)

    if show:
        headers = ['Librehoster', 'Hosted Schema']
        table = [[host, url] for host, url in config.directory.items()]
        _to_table(table, headers, config.bare)

    if librehoster:
        schema = _get_json(config._get_schema_url(librehoster))

        headers = ['Key', 'Value']
        table = []
        for key, value in schema.items():
            if not isinstance(value, list):
                if not config.bare:
                    value = textwrap.fill(str(value), width=50).strip()
                table.append([key, value])
            else:
                table.append([key, ', '.join(value)])

        _to_table(table, headers, config.bare)
