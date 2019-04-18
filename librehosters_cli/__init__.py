"""Librehosters-cli module."""

try:
    import pkg_resources
except ImportError:
    pass


try:
    __version__ = pkg_resources.get_distribution('librehosters-cli').version
except Exception:
    __version__ = 'unknown'
