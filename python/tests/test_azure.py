from devops_toolkit.services.azure_service import get_azure_costs

def test_get_azure_costs_dry_run():
    result = get_azure_costs("dummy_sub", is_dry_run=True)
    assert "SYMULACJA" in result
    assert "120.50 USD" in result

def test_get_azure_costs_mock_env(monkeypatch):
    monkeypatch.setenv("USE_MOCK_DATA", "true")
    result = get_azure_costs("dummy_sub", is_dry_run=False)
    assert "SYMULACJA" in result