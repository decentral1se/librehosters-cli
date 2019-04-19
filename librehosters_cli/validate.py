"""Command line options validation module."""

import typing

import click


def _validate_option_use(*cli_args) -> typing.Any:
    """Validate user specified options can work.

    As of current implementation, all options must be used in isolation from
    each other. This validation makes sure that the user is warned about this
    constraint.

    :raises click.UsageError
    """
    if len(list(filter(None, cli_args))) > 1:
        message = 'Cannot use these options together'
        raise click.UsageError(message)
