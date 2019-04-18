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


def _validate_schema_version(
    standard_schema: typing.Dict,
    retrieved_schema: typing.Dict,
    config: Config,
    schema_id: typing.Text,
) -> typing.Any:
    """Validated a schema version.

    :raises click.ClickException
    """
    try:
        standard_schema_version = standard_schema['version']
    except KeyError:
        message = 'Unable to retrieve version from {}'.format(config.schema_url)
        raise click.UsageError(message)

    try:
        retrieved_schema_version = retrieved_schema['version']
    except KeyError:
        message = 'Unable to retrieve version from {}'.format(schema_id)
        raise click.UsageError(message)

    if standard_schema_version != retrieved_schema_version:
        message = '{} has version {} and {} schema has version {}'.format(
            config.schema_url,
            standard_schema_version,
            schema_id,
            retrieved_schema_version,
        )
        raise click.UsageError(message)


def _validate_schema_keys(
    standard_schema: typing.Dict,
    retrieved_schema: typing.Dict,
    config: Config,
    schema_id: typing.Text,
) -> typing.Any:
    """Validate schema keys.

    :raises click.ClickException
    """
    standard_keys = config.schema.keys()
    retrieved_keys = retrieved_schema.keys()
    key_difference = set(retrieved_keys).difference(set(standard_keys))
    if key_difference:
        message = (
            'Schema key mistmatch.\n'
            'Found keys "{}" in {} that are not present in {}'
        ).format(', '.join(key_difference), schema_id, config.schema_url)
        raise click.UsageError(message)


def _validate_schema(
    standard_schema: typing.Dict,
    retrieved_schema: typing.Dict,
    config: Config,
    schema_id: typing.Text,
) -> typing.Any:
    """Validate a schema."""
    schema_args = [config.schema, retrieved_schema, config, schema_id]
    _validate_schema_version(*schema_args)
    _validate_schema_keys(*schema_args)
    message = '{} validated successfully!'.format(schema_id)
    return _success(message, config)


def _load_local_schema(schema_path: typing.Text) -> typing.Dict:
    """Load a local schema JSON file.

    :raises click.ClickException
    :return A local schema JSON
    """
    with open(schema_path, 'r') as handle:
        try:
            return json.loads(handle.read())
        except json.decoder.JSONDecodeError:
            message = 'Unable to decode {} as JSON'.format(schema_path)
            raise click.ClickException(message)


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
@click.option(
    '-u',
    '--url',
    metavar='URL',
    help='A domain (include HTTP/S scheme) that exposes /librehost.json',
)
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
    """Compare schema against the latest standardised schema.

    Please see https://librehosters-cli.readthedocs.io/ for examples.
    """
    _validate_option_use(schema, librehoster, url, show_schema, validate_all)

    if schema:
        retrieved = _load_local_schema(schema)
        _validate_schema(config.schema, retrieved, config, schema)

    if librehoster:
        schema_url = config.get_hosted_schema_url(librehoster)
        retrieved = _get_json(schema_url, config.timeout)
        _validate_schema(config.schema, retrieved, config, schema_url)

    if show_schema:
        try:
            return click.echo(json.dumps(config.schema, indent=2))
        except TypeError:
            message = 'Unable to print {}'.format(config.schema)
            raise click.ClickException(message)

    if url:
        try:
            schema_url = '{}/librehost.json'.format(url)
            retrieved = _get_json(schema_url, config.timeout)
            _validate_schema(config.schema, retrieved, config, url)
        except (RequestException, JSONDecodeError):
            message = 'Unable to retrieve {}'.format(url)
            raise click.ClickException(message)

    if validate_all:
        for librehoster, schema_url in config.directory.items():
            retrieved = _get_json(schema_url, config.timeout)
            try:
                _validate_schema(config.schema, retrieved, config, schema_url)
            except click.ClickException as exception:
                click.echo(str(exception))
