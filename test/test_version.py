"""Version test module."""


def test_version_fails_gracefully(mocker):
    target = 'pkg_resources.get_distribution'
    with mocker.patch(target, side_effect=Exception()):
        from librehosters_cli.__init__ import __version__

        assert __version__ == 'unknown'


def test_version_generates_successfully(runner):
    from librehosters_cli.__main__ import main

    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert 'unknown' not in result.output
