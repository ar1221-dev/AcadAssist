"""AcadAssist Configuration System.

Uses Pydantic Settings to load and validate application and Azure infrastructure configuration.
Follows 12-factor configuration principles with Entra ID / DefaultAzureCredential defaults.
"""

from typing import Optional
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application and Azure service settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Microsoft Foundry / Azure AI Projects
    foundry_project_endpoint: Optional[str] = Field(
        default=None,
        description="Azure AI Foundry project endpoint or connection string",
    )
    foundry_project: str = Field(
        default="acadassist-foundry",
        description="Azure AI Foundry project resource name",
    )
    foundry_model_deployment: str = Field(
        default="gpt-4o",
        description="Model deployment name in Azure Foundry for Agent reasoning",
    )
    foundry_embedding_deployment: str = Field(
        default="text-embedding-3-small",
        description="Embedding model deployment name in Azure Foundry",
    )
    foundry_agent_name: str = Field(
        default="AcadAssist",
        description="Display name for the single AcadAssist Agent",
    )

    # Azure AI Search
    azure_search_endpoint: Optional[str] = Field(
        default=None,
        description="Azure AI Search service endpoint URL",
    )
    azure_search_index: str = Field(
        default="acadassist-index",
        description="Target index name in Azure AI Search",
    )

    # Azure Blob Storage
    azure_storage_account: Optional[str] = Field(
        default=None,
        description="Azure Storage Account name hosting study materials",
    )
    azure_storage_container: str = Field(
        default="study-materials",
        description="Blob container name for uploaded academic source files",
    )

    # Application Settings
    database_url: Optional[str] = Field(
        default=None,
        description="Database connection string",
    )
    environment: str = Field(
        default="development",
        description="Deployment environment (development, staging, production)",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )

    @computed_field
    @property
    def is_development(self) -> bool:
        """Check if environment is development."""
        return self.environment.lower() in ("development", "dev", "test", "testing")

    @computed_field
    @property
    def azure_storage_endpoint(self) -> Optional[str]:
        """Construct blob storage service endpoint URL from account name."""
        if not self.azure_storage_account:
            return None
        if self.azure_storage_account.startswith("http"):
            return self.azure_storage_account
        return f"https://{self.azure_storage_account}.blob.core.windows.net"

    @computed_field
    @property
    def is_foundry_configured(self) -> bool:
        """Check if Foundry connection details are provided."""
        return bool(self.foundry_project_endpoint)

    @computed_field
    @property
    def is_search_configured(self) -> bool:
        """Check if Azure Search connection details are provided."""
        return bool(self.azure_search_endpoint)

    @computed_field
    @property
    def is_storage_configured(self) -> bool:
        """Check if Azure Storage connection details are provided."""
        return bool(self.azure_storage_account)


def get_settings() -> Settings:
    """Return a cached or fresh Settings instance."""
    return Settings()
