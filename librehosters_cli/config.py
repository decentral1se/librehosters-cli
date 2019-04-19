"""Command line configuration module."""

import typing

import click

from librehosters_cli.network import _get_json

SCHEMA_URL = 'https://lab.libreho.st/librehosters/librehost-api/raw/master/librehost.json'  # noqa
DIRECTORY_URL = 'https://libreho.st/directory.json'
TIMEOUT = 0.8


def normalise_librehoster_name(librehoster: typing.Text) -> typing.Text:
    """Normalise a single librehosters name.

    See `normalise_librehosters` docstring for further documentation.
    """
    return librehoster.lower().replace(' ', '-')


def normalise_librehosters() -> typing.List[typing.Text]:
    """Provide user friendly list of librehosters.

    This is necessary for the `--librehoster` command line option where the
    user is expected to supply the name of the librehoster. Since there are
    many variations within the naming, we aim here to normalize them.

    The convention shall be:

    * All lowercase naming
    * White space is replaced with hyphens.

    So, for example, 'LinuxPizza' becomes 'linuxpizza' and 'lain haus' becomes
    'lain-haus'.

    :raises click.ClickException
    :return A list of normalised librehoster names
    """
    normalised = []
    directory = _get_json(DIRECTORY_URL, TIMEOUT)
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
        self.directory_url = DIRECTORY_URL
        self.schema_url = SCHEMA_URL
        self.timeout = TIMEOUT

        self.directory = self._retrieve_directory()
        self.schema = self._retrieve_schema()

    def get_hosted_schema_url(self, librehoster: typing.Text) -> typing.Text:
        """Retrieve the librehosters's hosted schema URL.

        :raises click.ClickException
        :return The hosted schema of a librehoster
        """
        try:
            return self.directory[librehoster]
        except KeyError:
            message = 'Could not lookup {}'.format(librehoster)
            raise click.ClickException(message)

    def _retrieve_schema(self) -> typing.Dict:
        """Get the current standardised schema.

        :raises click.ClickException
        :return A response object
        """
        return _get_json(self.schema_url, self.timeout)

    def _retrieve_directory(self) -> typing.Dict:
        """Get the current directory listing.

        :raises click.ClickException
        :return A response object
        """
        directory = _get_json(self.directory_url, self.timeout)
        normalised = {}
        for librehoster, hosted_schema in directory.items():
            normalised_name = normalise_librehoster_name(librehoster)
            normalised[normalised_name] = hosted_schema
        return normalised


pass_config = click.make_pass_decorator(Config, ensure=True)
librehosters_cli_choices = normalise_librehosters()
