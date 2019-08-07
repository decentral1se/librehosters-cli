"""Schema command test module."""

import json

import click
import pytest


def test_validate_schema_version_missing(mock_config, mock_schema):
    from librehosters_cli.commands.schema import _validate_schema_version

    schema_version = mock_schema['version']
    bad_schema = mock_schema.copy()

    mock_config.target_schema = bad_schema
    mock_config.target_schema_url = 'https://foo.org/librehost.json'

    with pytest.raises(click.UsageError) as exception:
        del mock_config.standard_schema['version']
        _validate_schema_version(mock_config)

    assert 'Unable to retrieve version' in str(exception.value)
    assert mock_config.standard_schema_url in str(exception.value)

    with pytest.raises(click.UsageError) as exception:
        mock_config.standard_schema['version'] = schema_version
        del mock_config.target_schema['version']
        _validate_schema_version(mock_config)

    assert 'Unable to retrieve version' in str(exception.value)
    assert 'https://foo.org/librehost.json' in str(exception.value)


def test_validate_schema_version_mismatch(mock_schema, mock_config):
    from librehosters_cli.commands.schema import _validate_schema_version

    bad_schema = mock_schema.copy()
    bad_schema['version'] = '9.9.9'

    with pytest.raises(click.UsageError) as exception:
        mock_config.target_schema = bad_schema
        _validate_schema_version(mock_config)

    assert 'Schema version mismatch' in str(exception.value)
    assert '0.0.1 != 9.9.9'


def test_validate_schema_version_match(mock_schema, mock_config):
    from librehosters_cli.commands.schema import _validate_schema_version

    mock_config.target_schema = mock_schema
    assert _validate_schema_version(mock_config) is None


def test_validate_schema_keys_match(mock_schema, mock_config):
    from librehosters_cli.commands.schema import _validate_schema_keys

    mock_config.target_schema = mock_schema
    assert _validate_schema_keys(mock_config) is None


def test_validate_schema_keys_unknown(mock_schema, mock_config):
    from librehosters_cli.commands.schema import _validate_schema_keys

    mock_config.target_schema = mock_schema.copy()
    mock_config.target_schema_url = 'foo.json'
    mock_config.target_schema['unknownkey'] = 666

    with pytest.raises(click.UsageError) as exception:
        assert _validate_schema_keys(mock_config)

    assert 'Unknown schema key(s):' in str(exception.value)
    assert '"unknownkey" in foo.json' in str(exception.value)


def test_validate_schema_keys_missing(mock_schema, mock_config):
    from librehosters_cli.commands.schema import _validate_schema_keys

    bad_schema = mock_schema.copy()
    mock_config.standard_schema['missingkey'] = 666

    with pytest.raises(click.UsageError) as exception:
        mock_config.target_schema = bad_schema
        assert _validate_schema_keys(mock_config) is None

    assert 'Missing schema key(s):' in str(exception.value)
    assert '"missingkey" in {}'.format(mock_config.standard_schema_url) in str(
        exception.value
    )


def test_validate_schema_calls_sub_validators(mock_schema, mock_config):
    from librehosters_cli.commands.schema import _validate_schema

    mock_config.target_schema = mock_schema.copy()
    mock_config.target_schema_url = 'foo.json'
    assert _validate_schema(mock_config) is None


def test_load_local_schema(runner, mock_schema):
    from librehosters_cli.commands.schema import _load_local_schema

    with runner.isolated_filesystem():
        with open('foo.json', 'w') as f:
            f.write(json.dumps(mock_schema))
        assert _load_local_schema('foo.json') == mock_schema


def test_load_local_schema_missing_file():
    from librehosters_cli.commands.schema import _load_local_schema

    with pytest.raises(click.UsageError) as exception:
        _load_local_schema('doesnt-exist')

    assert 'Unable to open' in str(exception.value)


def test_validate_local_schema_file(runner, mock_schema):
    from librehosters_cli.commands.schema import schema

    with runner.isolated_filesystem():
        with open('foo.json', 'w') as f:
            f.write(json.dumps(mock_schema))
        result = runner.invoke(schema, ['--schema', 'foo.json'])

    assert result.exit_code == 0
    assert 'validated successfully' in result.output
    assert 'foo.json' in result.output


def test_validate_librehoster_hosted_schema(
    runner, mock_schema, mock_directory, requests_mock
):
    from librehosters_cli.commands.schema import schema

    requests_mock.get(mock_directory['foo-bar'], json=mock_schema)

    result = runner.invoke(schema, ['--librehoster', 'foo-bar'])

    assert result.exit_code == 0
    assert 'validated successfully' in result.output
    assert mock_directory['foo-bar'] in result.output


def test_show_schema(runner, mock_schema):
    from librehosters_cli.commands.schema import schema

    result = runner.invoke(schema, ['--show'])

    assert result.exit_code == 0
    assert json.loads(result.output) == mock_schema


def test_validate_url_schema(runner, mock_schema, requests_mock):
    from librehosters_cli.commands.schema import schema

    target_schema_url = 'https://foo.org/librehost.json'

    requests_mock.get(target_schema_url, json=mock_schema)

    result = runner.invoke(schema, ['--url', target_schema_url])

    assert result.exit_code == 0
    assert 'validated successfully' in result.output
    assert target_schema_url in result.output


def test_validate_all_network_schemas(
    runner, mock_schema, mock_directory, requests_mock
):
    from librehosters_cli.commands.schema import schema

    for target_schema_url in mock_directory.values():
        requests_mock.get(target_schema_url, json=mock_schema)

    result = runner.invoke(schema, ['--validate-all'])

    for target_schema_url in mock_directory.values():
        assert result.exit_code == 0
        assert 'validated successfully' in result.output
        assert target_schema_url in result.output
