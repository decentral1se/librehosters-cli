"""Version test module."""


def test_version_generates():
    from librehosters_cli.__init__ import __version__

    assert __version__ != 'unknown'
