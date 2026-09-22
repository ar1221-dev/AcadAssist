"""Test configuration and fixtures for AcadAssist unit tests."""

import pytest


@pytest.fixture(autouse=True)
def isolate_azure_environment(monkeypatch):
    """Isolate tests from live Azure cloud configuration and endpoints."""
    monkeypatch.setenv("FOUNDRY_PROJECT_ENDPOINT", "")
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "")
    monkeypatch.setenv("AZURE_STORAGE_ACCOUNT", "")
