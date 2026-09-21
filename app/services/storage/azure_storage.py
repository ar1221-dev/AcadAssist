"""Azure Blob Storage implementation of StorageService."""

import logging
import uuid
from pathlib import Path

from app.config import settings
from app.services.storage.base import StorageService
from app.services.storage.local_storage import LocalStorageService

logger = logging.getLogger(__name__)


class AzureStorageService(StorageService):
    """Azure Blob Storage service with production enforcement and dev fallback."""

    def __init__(
        self,
        connection_string: str | None = None,
        container_name: str | None = None,
    ):
        self.connection_string = connection_string or settings.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = container_name or settings.AZURE_STORAGE_CONTAINER
        self.fallback_storage: LocalStorageService | None = None

        if not self.connection_string:
            if settings.is_production():
                raise ValueError("AZURE_STORAGE_CONNECTION_STRING is mandatory in production environment.")
            logger.info("Azure Storage connection string not provided. Using local file storage for development/testing.")
            self.fallback_storage = LocalStorageService()
            self.blob_service_client = None
            self.container_client = None
        else:
            from azure.storage.blob import BlobServiceClient
            self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.container_client = self.blob_service_client.get_container_client(self.container_name)
            try:
                if not self.container_client.exists():
                    self.container_client.create_container()
            except Exception as e:
                logger.warning(f"Could not verify or create Azure Blob container '{self.container_name}': {e}")

    def save_file(self, file_bytes: bytes, filename: str, user_id: str) -> str:
        """Save file bytes to Azure Blob container (or local fallback)."""
        if self.fallback_storage:
            return self.fallback_storage.save_file(file_bytes, filename, user_id)

        blob_name = f"{user_id}/{uuid.uuid4().hex[:8]}_{Path(filename).name}"
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file_bytes, overwrite=True)
        return f"azure://{self.container_name}/{blob_name}"

    def get_file(self, storage_path: str) -> bytes:
        """Retrieve file bytes from Azure Blob container (or local fallback)."""
        if self.fallback_storage:
            return self.fallback_storage.get_file(storage_path)

        if not storage_path.startswith("azure://"):
            # If path is a local path created before or in test
            if Path(storage_path).exists():
                with open(storage_path, "rb") as f:
                    return f.read()
            raise ValueError(f"Invalid Azure storage path: {storage_path}")

        raw_path = storage_path.replace(f"azure://{self.container_name}/", "")
        blob_client = self.container_client.get_blob_client(raw_path)
        return blob_client.download_blob().readall()

    def delete_file(self, storage_path: str) -> bool:
        """Delete blob from Azure container (or local fallback)."""
        if self.fallback_storage:
            return self.fallback_storage.delete_file(storage_path)

        if not storage_path.startswith("azure://"):
            if Path(storage_path).exists():
                Path(storage_path).unlink()
                return True
            return False

        raw_path = storage_path.replace(f"azure://{self.container_name}/", "")
        blob_client = self.container_client.get_blob_client(raw_path)
        if blob_client.exists():
            blob_client.delete_blob()
            return True
        return False
