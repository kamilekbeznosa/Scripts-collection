from unittest.mock import patch, MagicMock
from devops_toolkit.services.k8s_service import check_cluster_health


@patch("devops_toolkit.services.k8s_service.client.CoreV1Api")
@patch("devops_toolkit.services.k8s_service.config.load_kube_config")
def test_check_cluster_health_ok(mock_config, mock_api_client):
    mock_api_instance = MagicMock()
    mock_pod = MagicMock()
    mock_pod.status.phase = "Running"
    mock_pod.status.container_statuses = []

    mock_api_instance.list_namespaced_pod.return_value = MagicMock(items=[mock_pod])
    mock_api_client.return_value = mock_api_instance

    has_critical = check_cluster_health("default")
    assert has_critical is False


@patch("devops_toolkit.services.k8s_service.client.CoreV1Api")
@patch("devops_toolkit.services.k8s_service.config.load_kube_config")
def test_check_cluster_health_crashloop(mock_config, mock_api_client):
    mock_api_instance = MagicMock()
    mock_pod = MagicMock()
    mock_pod.status.phase = "Running"

    mock_container = MagicMock()
    mock_container.state.waiting.reason = "CrashLoopBackOff"
    mock_pod.status.container_statuses = [mock_container]

    mock_api_instance.list_namespaced_pod.return_value = MagicMock(items=[mock_pod])
    mock_api_client.return_value = mock_api_instance

    has_critical = check_cluster_health("default")
    assert has_critical is True
