"""Schema command module."""

import json
import typing
from json.decoder import JSONDecodeError

import click
from requests.exceptions import RequestException

from librehosters_cli.config import (
    Config,
    librehosters_cli_choices,
    pass_config,
)
from librehosters_cli.network import _get_json
from librehosters_cli.print import _success
from librehosters_cli.validate import _validate_option_use


def _validate_schema_version(config: Config) -> typing.Any:
    """Validated a schema version.

    :raises click.UsageError
    """
    try:
        standard_schema_version = config.standard_schema['version']
    except KeyError:
        message = 'Unable to retrieve version from {}'
        raise click.UsageError(message.format(config.standard_schema_url))

    try:
        retrieved_schema_version = config.target_schema['version']
    except KeyError:
        message = 'Unable to retrieve version from {}'
        raise click.UsageError(message.format(config.target_schema_url))

    if standard_schema_version != retrieved_schema_version:
        message = 'Schema version mismatch: {} != {}'.format(
            standard_schema_version, retrieved_schema_version
        )
        raise click.UsageError(message)


def _validate_schema_keys(config: Config) -> typing.Any:
    """Validate schema keys.

    :raises click.UsageError
    """

    missing_diff = set(config.target_schema) - set(config.standard_schema)
    if missing_diff:
        message = 'Unknown schema key(s): "{}" in {}'.format(
            ', '.join(missing_diff), config.target_schema_url
        )
        raise click.UsageError(message)

    unknown_diff = set(config.standard_schema) - set(config.target_schema)
    if unknown_diff:
        message = 'Missing schema key(s): "{}" in {}'.format(
            ', '.join(unknown_diff), config.standard_schema_url
        )
        raise click.UsageError(message)


def _validate_schema(config: Config) -> typing.Any:
    """Validate a schema against the latest standardised schema."""
    _validate_schema_version(config)
    _validate_schema_keys(config)
    message = '{} validated successfully!'.format(config.target_schema_url)
    return _success(message, config.colour)


def _load_local_schema(schema: typing.Text) -> typing.Dict:
    """Load a local schema JSON file.

    :raises click.UsageError
    :return A local schema JSON
    """
    try:
        with open(schema, 'r') as handle:
            try:
                return json.loads(handle.read())
            except json.decoder.JSONDecodeError:
                message = 'Unable to decode {} as JSON'.format(schema)
                raise click.UsageError(message)
    except FileNotFoundError:
        message = 'Unable to open {}'.format(schema)
        raise click.UsageError(message)


@click.command()
@click.option(
    '-s',
    '--schema',
    metavar='SCHEMA-JSON-FILE',
    help='A local schema JSON file path',
    type=click.Path(exists=True),
)
@click.option(
    '-lh',
    '--librehoster',
    metavar='LIBREHOSTER',
    help='A librehoster network member',
    type=click.Choice(librehosters_cli_choices),
)
@click.option('-u', '--url', metavar='URL', help='A hosted schema URL')
@click.option(
    '-S',
    '--show',
    'show_schema',
    flag_value='show',
    help='Show the latest standardised schema',
)
@click.option(
    '-va',
    '--validate-all',
    flag_value='validate_all',
    help='Validate all network member schemas',
)
@pass_config
def schema(
    config: Config,
    schema: typing.Text,
    librehoster: typing.Text,
    url: typing.Text,
    show_schema: bool,
    validate_all: bool,
) -> typing.Any:
    """Compare schema against the latest standardised schema."""
    _validate_option_use(schema, librehoster, url, show_schema, validate_all)

    if schema:
        config.target_schema = _load_local_schema(schema)
        config.target_schema_url = schema
        _validate_schema(config)

    if librehoster:
        config.target_schema_url = config._get_schema_url(librehoster)
        config.target_schema = _get_json(config.target_schema_url)
        _validate_schema(config)

    if show_schema:
        try:
            return click.echo(json.dumps(config.standard_schema, indent=2))
        except TypeError:
            message = 'Unable to show {}'.format(config.standard_schema)
            raise click.UsageError(message)

    if url:
        try:
            config.target_schema_url = url
            config.target_schema = _get_json(config.target_schema_url)
            _validate_schema(config)
        except (RequestException, JSONDecodeError):
            message = 'Unable to retrieve {}'.format(config.target_schema_url)
            raise click.UsageError(message)

    if validate_all:
        for librehoster, target_schema_url in config.directory.items():
            config.target_schema_url = target_schema_url
            config.target_schema = _get_json(target_schema_url)
            try:
                _validate_schema(config)
            except click.UsageError as exception:
                click.echo(str(exception))
