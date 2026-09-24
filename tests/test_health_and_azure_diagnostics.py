"""Unit tests for /api/health and /api/health/azure diagnostics.

Covers:
1. Azure not configured
2. Azure configured
3. Successful Azure connectivity
4. Authentication failure
5. Azure unavailable / network error
6. No secrets exposed in response
7. Health endpoint schema and subsystem readiness
8. Existing functionality remains intact
"""

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from azure.core.exceptions import ClientAuthenticationError, ServiceRequestError

from app.main import app
from app.api.routes.health import (
    check_azure_blob_storage,
    check_azure_search,
    check_microsoft_foundry,
)

client = TestClient(app)


def test_api_health_endpoint():
    """Verify GET /api/health returns healthy status and subsystems."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert data["service"] == "AcadAssist API"
    assert "subsystems" in data
    assert data["subsystems"]["knowledge_rag"] == "operational"
    assert data["subsystems"]["assessment"] == "operational"
    assert data["subsystems"]["study_intelligence"] == "operational"
    assert "database" in data


def test_root_health_endpoint():
    """Verify GET /health backwards-compatible route."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert data["service"] == "AcadAssist API"


def test_azure_diagnostics_not_configured():
    """Verify /api/health/azure when Azure services are not configured."""
    with patch("app.api.routes.health.check_azure_blob_storage", return_value={"status": "not_configured", "message": "Azure Blob Storage not configured."}), \
         patch("app.api.routes.health.check_azure_search", return_value={"status": "not_configured", "message": "Azure AI Search not configured."}), \
         patch("app.api.routes.health.check_microsoft_foundry", return_value={"status": "not_configured", "message": "Microsoft Foundry not configured."}):
        response = client.get("/api/health/azure")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "not_configured"
        assert "services" in data
        assert data["services"]["azure_blob_storage"]["status"] == "not_configured"
        assert data["services"]["azure_ai_search"]["status"] == "not_configured"
        assert data["services"]["microsoft_foundry"]["status"] == "not_configured"


def test_azure_diagnostics_successful_connectivity():
    """Verify /api/health/azure when all Azure services connect successfully."""
    with patch("app.api.routes.health.check_azure_blob_storage", return_value={"status": "connected", "message": "Azure Blob Storage connected."}), \
         patch("app.api.routes.health.check_azure_search", return_value={"status": "connected", "message": "Azure AI Search connected."}), \
         patch("app.api.routes.health.check_microsoft_foundry", return_value={"status": "connected", "message": "Microsoft Foundry connected."}):
        response = client.get("/api/health/azure")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "connected"
        assert data["services"]["azure_blob_storage"]["status"] == "connected"
        assert data["services"]["azure_ai_search"]["status"] == "connected"
        assert data["services"]["microsoft_foundry"]["status"] == "connected"


def test_azure_diagnostics_authentication_failure():
    """Verify /api/health/azure handles authentication failure gracefully."""
    with patch("app.api.routes.health.check_azure_blob_storage", return_value={"status": "authentication_failed", "message": "Azure Blob Storage authentication failed. Check credentials."}), \
         patch("app.api.routes.health.check_azure_search", return_value={"status": "not_configured", "message": "not configured"}), \
         patch("app.api.routes.health.check_microsoft_foundry", return_value={"status": "not_configured", "message": "not configured"}):
        response = client.get("/api/health/azure")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "authentication_failed"
        assert data["services"]["azure_blob_storage"]["status"] == "authentication_failed"


def test_azure_diagnostics_unreachable():
    """Verify /api/health/azure handles network/service unreachability."""
    with patch("app.api.routes.health.check_azure_blob_storage", return_value={"status": "not_configured", "message": "not configured"}), \
         patch("app.api.routes.health.check_azure_search", return_value={"status": "unreachable", "message": "Azure AI Search service is unreachable."}), \
         patch("app.api.routes.health.check_microsoft_foundry", return_value={"status": "not_configured", "message": "not configured"}):
        response = client.get("/api/health/azure")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unreachable"
        assert data["services"]["azure_ai_search"]["status"] == "unreachable"


def test_azure_diagnostics_zero_secrets_exposed():
    """Verify no secret tokens, keys, passwords, or connection strings appear in health output."""
    raw_secret_key = "SECRET_SUPER_KEY_9999_NEVER_EXPOSE"
    mock_blob = MagicMock()
    mock_blob.get_container_client.return_value.exists.side_effect = RuntimeError(f"Error with key {raw_secret_key}")

    mock_search = MagicMock()
    mock_search.get_index_client.return_value.list_index_names.side_effect = RuntimeError(f"Search failed {raw_secret_key}")

    mock_foundry = MagicMock()
    mock_foundry.is_configured = True
    mock_foundry.get_openai_client.return_value.models.list.side_effect = RuntimeError(f"Foundry failed {raw_secret_key}")

    with patch("app.api.routes.health.settings") as mock_settings, \
         patch("app.azure.storage.AzureStorageClient", return_value=mock_blob), \
         patch("app.azure.search.AzureSearchManager", return_value=mock_search), \
         patch("app.azure.foundry.FoundryProjectManager", return_value=mock_foundry):
        mock_settings.AZURE_STORAGE_ACCOUNT = "secret_acct"
        mock_settings.AZURE_STORAGE_CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName=secret_acct;AccountKey={raw_secret_key};EndpointSuffix=core.windows.net"
        mock_settings.AZURE_SEARCH_ENDPOINT = "https://secret.search.windows.net"
        mock_settings.AZURE_SEARCH_KEY = raw_secret_key
        mock_settings.AZURE_OPENAI_API_KEY = raw_secret_key
        mock_settings.JWT_SECRET_KEY = raw_secret_key

        response = client.get("/api/health/azure")
        body_text = response.text
        assert raw_secret_key not in body_text
        assert "DefaultEndpointsProtocol" not in body_text
        assert "AccountKey" not in body_text


def test_blob_storage_checker_auth_failure_handling():
    """Verify check_azure_blob_storage properly maps ClientAuthenticationError."""
    mock_blob_client = MagicMock()
    mock_container = MagicMock()
    mock_container.exists.side_effect = ClientAuthenticationError("Invalid token")
    mock_blob_client.get_container_client.return_value = mock_container

    with patch("app.api.routes.health.settings") as mock_settings, \
         patch("app.azure.storage.AzureStorageClient", return_value=mock_blob_client):
        mock_settings.AZURE_STORAGE_ACCOUNT = "test_acct"
        result = check_azure_blob_storage()
        assert result["status"] == "authentication_failed"
        assert "Invalid token" not in result["message"]


def test_azure_search_checker_unreachable_handling():
    """Verify check_azure_search properly maps ServiceRequestError."""
    mock_search_mgr = MagicMock()
    mock_idx_client = MagicMock()
    mock_idx_client.list_index_names.side_effect = ServiceRequestError("DNS resolution failed")
    mock_search_mgr.get_index_client.return_value = mock_idx_client

    with patch("app.api.routes.health.settings") as mock_settings, \
         patch("app.azure.search.AzureSearchManager", return_value=mock_search_mgr):
        mock_settings.AZURE_SEARCH_ENDPOINT = "https://test.search.windows.net"
        result = check_azure_search()
        assert result["status"] == "unreachable"
