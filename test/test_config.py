"""Config test module."""

import click
import pytest


def test_normalise_librehoster_name():
    from librehosters_cli.config import normalise_librehoster_name

    assert normalise_librehoster_name('lain haus') == 'lain-haus'


def test_normalise_librehoster_names():
    from librehosters_cli.config import normalise_librehosters_names

    assert normalise_librehosters_names() == ['foo-bar', 'bing-bong']


def test_get_hosted_schema_url(mock_config, mock_directory):
    assert mock_config._get_schema_url('foo-bar') == mock_directory['foo-bar']

    with pytest.raises(click.UsageError) as exception:
        mock_config._get_schema_url('not-here')
    assert 'Could not lookup' in str(exception)


def test_retrieve_schema(mock_config, mock_schema):
    assert mock_config._get_standard_schema_json() == mock_schema


def test_retrieve_directory(mock_config, mock_directory):
    assert mock_config._get_directory_json() == mock_directory
