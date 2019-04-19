"""Command line validation test module."""


def test_libreh_doesnt_accept_multiple_options(runner):
    from librehosters_cli.commands.schema import schema
    from librehosters_cli.commands.whois import whois

    options = ('--show', '--librehoster', 'foo-bar')

    for command in (schema, whois):
        result = runner.invoke(command, options)
        assert result.exit_code == 2
        assert 'Cannot use these options together' in result.output
