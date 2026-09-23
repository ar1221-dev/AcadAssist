"""Microsoft Foundry Project Integration Layer.

Uses Azure AI Projects SDK 2.x (`azure-ai-projects`) and `DefaultAzureCredential`.
Reads model and embedding deployments from typed configuration.
"""

import logging
from typing import Optional
from azure.core.credentials import TokenCredential
from azure.ai.projects import AIProjectClient
import openai

from config.settings import get_settings
from app.azure.credentials import get_azure_credential

logger = logging.getLogger(__name__)


class FoundryProjectManager:
    """Manager for Microsoft Foundry Project connection and client lifecycle."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        credential: Optional[TokenCredential] = None,
        model_deployment: Optional[str] = None,
        embedding_deployment: Optional[str] = None,
    ):
        settings = get_settings()
        self.endpoint = endpoint or settings.foundry_project_endpoint
        self.credential = credential or get_azure_credential()
        self.model_deployment = model_deployment or settings.foundry_model_deployment
        self.embedding_deployment = embedding_deployment or settings.foundry_embedding_deployment
        self._project_client: Optional[AIProjectClient] = None
        self._openai_client: Optional[openai.OpenAI] = None

    @property
    def is_configured(self) -> bool:
        """Check if Foundry project endpoint is provided."""
        return bool(self.endpoint)

    def get_project_client(self) -> AIProjectClient:
        """Get or initialize AIProjectClient using Entra ID credentials."""
        if self._project_client is None:
            if not self.endpoint:
                raise ValueError(
                    "Foundry Project endpoint is not configured. Set FOUNDRY_PROJECT_ENDPOINT in .env."
                )
            logger.info("Connecting to Microsoft Foundry project at %s", self.endpoint)
            self._project_client = AIProjectClient(
                endpoint=self.endpoint,
                credential=self.credential,
            )
        return self._project_client

    def get_openai_client(self) -> openai.OpenAI:
        """Get the authenticated OpenAI client configured for this Foundry project."""
        if self._openai_client is None:
            project_client = self.get_project_client()
            self._openai_client = project_client.get_openai_client()
        return self._openai_client


__all__ = ["FoundryProjectManager"]
