"""Azure and Microsoft Foundry Integration Module."""

from app.azure.credentials import get_azure_credential
from app.azure.storage import AzureStorageClient
from app.azure.search import (
    AzureSearchManager,
    build_acadassist_index_schema,
    INDEX_NAME,
    VECTOR_DIMENSIONS,
)
from app.azure.foundry import FoundryProjectManager
from app.azure.agent import AcadAssistAgentService, ACADASSIST_SYSTEM_INSTRUCTIONS
from app.azure.tools import get_agent_tools, FOUNDRY_TOOL_DEFINITIONS
from app.azure.adapters import ToolDispatcher

__all__ = [
    "ACADASSIST_SYSTEM_INSTRUCTIONS",
    "AcadAssistAgentService",
    "AzureSearchManager",
    "AzureStorageClient",
    "FOUNDRY_TOOL_DEFINITIONS",
    "FoundryProjectManager",
    "INDEX_NAME",
    "ToolDispatcher",
    "VECTOR_DIMENSIONS",
    "build_acadassist_index_schema",
    "get_agent_tools",
    "get_azure_credential",
]
