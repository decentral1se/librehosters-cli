"""Command line interface entrypoint module."""

import click

from librehosters_cli.commands.schema import schema
from librehosters_cli.commands.whois import whois
from librehosters_cli.config import Config

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '--usage'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.option(
    '--bare/--no-bare',
    help='Use a machine friendly output format',
    default=False,
    show_default=True,
)
@click.option(
    '--colour/--no-colour',
    help='Use ANSI colours',
    default=True,
    show_default=True,
)
@click.pass_context
def main(context, bare, debug, colour) -> None:
    """
    \b
     _ _ _              _               _                           _ _
    | (_) |            | |             | |                         | (_)
    | |_| |__  _ __ ___| |__   ___  ___| |_ ___ _ __ ___ ______ ___| |_
    | | | '_ \| '__/ _ \ '_ \ / _ \/ __| __/ _ \ '__/ __|______/ __| | |
    | | | |_) | | |  __/ | | | (_) \__ \ ||  __/ |  \__ \     | (__| | |
    |_|_|_.__/|_|  \___|_| |_|\___/|___/\__\___|_|  |___/      \___|_|_|

                         https://libreho.st/

    """  # noqa
    context.ensure_object(Config)
    context.obj.bare = bare
    context.obj.debug = debug
    context.obj.colour = colour


main.add_command(schema)
main.add_command(whois)
