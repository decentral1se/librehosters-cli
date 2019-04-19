"""Main entrypoint test module."""


def test_multiple_help_options(runner):
    from librehosters_cli.__main__ import main

    assert runner.invoke(main, ['--usage']).exit_code == 0
    assert runner.invoke(main, ['--help']).exit_code == 0
    assert runner.invoke(main, ['-h']).exit_code == 0
