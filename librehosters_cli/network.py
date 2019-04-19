"""Network requests module."""

import typing
from json.decoder import JSONDecodeError

import click
import requests
from requests.exceptions import RequestException

from librehosters_cli.settings import TIMEOUT


def _get_json(url: typing.Text, timeout: float = TIMEOUT) -> typing.Dict:
    """Retrieve JSON payload with the HTTP GET method.

    :raises click.UsageError
    :return A JSON response
    """
    try:
        return requests.get(url, timeout=timeout).json()
    except (RequestException, JSONDecodeError):
        message = 'Unable to retrieve {}'.format(url)
        raise click.UsageError(message)
