"""Whois command test module."""


def test_whois_show(runner, mock_directory):
    from librehosters_cli.commands.whois import whois

    result = runner.invoke(whois, ['--show'])

    assert result.exit_code == 0

    assert 'Librehoster' in result.output
    assert 'Hosted Schema' in result.output

    for mock_librehoster in mock_directory:
        assert mock_librehoster in result.output


def test_whois_librehosters_show(
    runner, mock_directory, requests_mock, mock_schema
):
    from librehosters_cli.commands.whois import whois

    requests_mock.get(mock_directory['foo-bar'], json=mock_schema)

    result = runner.invoke(whois, ['--librehoster', 'foo-bar'])

    assert result.exit_code == 0

    assert 'Key' in result.output
    assert 'Value' in result.output

    for key in mock_schema:
        assert key in result.output
