"""Pytest fixtures module."""

import pytest
from click.testing import CliRunner


@pytest.fixture(autouse=True)
def mock_config(mocker, mock_directory, mock_schema, requests_mock):
    """A mocked librehosters_cli.config.Config object.

    We `autouse` this fixture to ensure that even the tests that do not require
    interacting with a Config object still get it because this fixture
    currently encapsulates the suppression of all network requests.
    """
    from librehosters_cli.settings import SCHEMA_URL, DIRECTORY_URL

    requests_mock.get(SCHEMA_URL, json=mock_schema)
    requests_mock.get(DIRECTORY_URL, json=mock_directory)

    from librehosters_cli.config import Config

    return Config()


@pytest.fixture()
def runner():
    """Click command line test runner."""
    return CliRunner()


@pytest.fixture()
def mock_directory():
    """A mocked network directory listing."""
    return {
        'foo-bar': 'https://foo-bar.org/librehost.json',
        'bing-bong': 'http://bing-bong.org/librehost.json',
    }


@pytest.fixture()
def mock_schema():
    """A mocked standardised schema listing."""
    return {
        '@context': 'http://schema.org',
        '@type': 'Organization',
        'organizationType': 'Informal collective',
        'name': 'foobar.example',
        'tagLine': 'providing services for everyone',
        'homeUrl': 'https://foobar.example',
        'logo': 'https://foobar.example/logo.png',
        'description': 'libre service provider',
        'communicationLanguages': ['en', 'fr', 'nl'],
        'contactUrl': 'https://foobar.example/contact',
        'privacyPolicyUrl': 'https://foobar.example/policy/privacy',
        'termsOfServiceUrl': 'https://foobar.example/policy/tos',
        'isServiceProvider': True,
        'foundingDate': 'YYYY',
        'version': '0.0.1',
        'dateCreated': 'YYYY-MM-DDTHH:MM:54Z',
        'dateModified': '2018-11-10T22:32:54Z',
    }
