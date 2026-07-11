from unittest.mock import patch, MagicMock
from devops_toolkit.services.dns_service import check_domains


@patch("devops_toolkit.services.dns_service.ssl.create_default_context")
@patch("devops_toolkit.services.dns_service.socket.create_connection")
def test_check_domains_valid(mock_socket, mock_ssl_context):
    """Testuje poprawne parsowanie daty certyfikatu dla sprawdzanej domeny."""

    mock_context_instance = MagicMock()
    mock_sslsock = MagicMock()

    mock_sslsock.getpeercert.return_value = {"notAfter": "Dec 31 23:59:59 2040 GMT"}

    mock_context_instance.wrap_socket.return_value.__enter__.return_value = mock_sslsock
    mock_ssl_context.return_value = mock_context_instance

    has_errors, results = check_domains(["dummy-domain.com"], 14)

    assert has_errors is False


@patch("devops_toolkit.services.dns_service.socket.create_connection")
def test_check_domains_connection_error(mock_socket):
    """Testuje obsługę błędu połączenia (np. strona nie istnieje)."""
    mock_socket.side_effect = Exception("Connection Refused")

    has_errors, results = check_domains(["nonexistent-domain.internal"], 14)

    assert has_errors is True
