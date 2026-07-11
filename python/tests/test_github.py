import pytest
from unittest.mock import patch, MagicMock
from devops_toolkit.services.github_service import audit_target

@patch("devops_toolkit.services.github_service.requests.get")
def test_audit_target_passes(mock_get):
    """Test dla wariantu, gdzie repozytorium spełnia zasady polityki."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "DobreRepo", "description": "Jest opis", "has_issues": True, "archived": False}
    ]
    mock_response.links = {}
    mock_get.return_value = mock_response

    has_errors, results = audit_target("test_user", "dummy_token", False)
    
    assert has_errors is False
    assert len(results) >= 0

@patch("devops_toolkit.services.github_service.requests.get")
def test_audit_target_fails(mock_get):
    """Test dla wariantu, gdzie repozytorium łamie zasady (brak opisu i issues)."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "ZleRepo", "description": None, "has_issues": False, "archived": False}
    ]
    mock_response.links = {}
    mock_get.return_value = mock_response

    has_errors, results = audit_target("test_user", "dummy_token", False)
    
    assert has_errors is True