"""Member registry exploration module."""

import textwrap
import typing

import click
from tabulate import tabulate

from librehosters_cli.config import (
    Config,
    librehosters_cli_choices,
    pass_config,
)
from librehosters_cli.network import _get_json
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
    """Explore the librehosters network registry.

    Please see https://librehosters-cli.readthedocs.io/ for examples.
    """
    _validate_option_use(librehoster, show)

    if show:
        headers = ['Librehoster', 'Hosted Schema']
        table = [[host, url] for host, url in config.directory.items()]
        click.echo(tabulate(table, headers=headers, tablefmt='grid'))

    if librehoster:
        hosted_schema = config.get_hosted_schema_url(librehoster)
        schema = _get_json(hosted_schema, config.timeout)

        table = []
        for key, value in schema.items():
            if not isinstance(value, list):
                table.append([key, textwrap.fill(str(value), width=50).strip()])
            else:
                table.append([key, ', '.join(value)])

        headers = ['Key', 'Value']
        click.echo(tabulate(table, headers=headers, tablefmt='grid'))
