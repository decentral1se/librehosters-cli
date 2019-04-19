"""Command line configuration module."""

import typing

import click

from librehosters_cli.network import _get_json
from librehosters_cli.settings import DIRECTORY_URL, SCHEMA_URL, TIMEOUT


def normalise_librehoster_name(librehoster: typing.Text) -> typing.Text:
    """Normalise a single librehosters name.

    See `normalise_librehosters` docstring for further documentation.
    """
    return librehoster.lower().replace(' ', '-')


def normalise_librehosters_names() -> typing.List[typing.Text]:
    """Provide user friendly list of librehosters.

    This is necessary for the `--librehoster` command line option where the
    user is expected to supply the name of the librehoster. Since there are
    many variations within the naming, we aim here to normalize them.

    The convention shall be:

    * All lowercase naming
    * White space is replaced with hyphens.

    So, for example, 'LinuxPizza' becomes 'linuxpizza' and 'lain haus' becomes
    'lain-haus'.

    :raises click.UsageError
    :return A list of normalised librehoster names
    """
    normalised = []
    directory = _get_json(DIRECTORY_URL)
    for librehoster in directory.keys():
        normalised.append(normalise_librehoster_name(librehoster))
    return normalised


class Config:
    """The global configuration object."""

    def __init__(self):
        """The initial configuration.

        These settings are configured via the entrypoing context handling in
        librehosters_cli.__main__ as per the Click best practices
        documentation.
        """
        self.bare = False
        self.colour = True
        self.debug = False

        self.timeout = TIMEOUT

        self.directory_url = DIRECTORY_URL
        self.directory = self._get_directory_json()

        self.standard_schema_url = SCHEMA_URL
        self.standard_schema = self._get_standard_schema_json()

        self.target_schema = None
        self.target_schema_url = None

    def _get_schema_url(self, librehoster: typing.Text) -> typing.Text:
        """Retrieve the librehosters's hosted schema URL from the directory.

        :raises click.UsageError
        :return The hosted schema of a librehoster
        """
        try:
            return self.directory[librehoster]
        except KeyError:
            message = 'Could not lookup {}'.format(librehoster)
            raise click.UsageError(message)

    def _get_standard_schema_json(self) -> typing.Dict:
        """Get the current standardised schema.

        :raises click.UsageError
        :return A response object
        """
        return _get_json(self.standard_schema_url)

    def _get_directory_json(self) -> typing.Dict:
        """Get the current directory listing.

        :raises click.UsageError
        :return A response object
        """
        directory = _get_json(self.directory_url)
        normalised = {}
        for librehoster, hosted_schema in directory.items():
            normalised_name = normalise_librehoster_name(librehoster)
            normalised[normalised_name] = hosted_schema
        return normalised


pass_config = click.make_pass_decorator(Config, ensure=True)
librehosters_cli_choices = normalise_librehosters_names()
