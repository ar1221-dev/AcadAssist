from pathlib import Path
from app.config import settings


class StorageService:
    def __init__(
        self,
        raw_base_dir: Path | None = None,
        processed_base_dir: Path | None = None,
    ):
        self.raw_base_dir = raw_base_dir or settings.STORAGE_RAW_DIR
        self.processed_base_dir = processed_base_dir or settings.STORAGE_PROCESSED_DIR

        # Ensure base storage directories exist
        self.raw_base_dir.mkdir(parents=True, exist_ok=True)
        self.processed_base_dir.mkdir(parents=True, exist_ok=True)

    def save_raw_file(self, material_id: str, filename: str, content: bytes) -> Path:
        """
        Store the raw uploaded document in storage/raw/<material_id>/<filename>.
        Returns the absolute Path.
        """
        material_dir = self.raw_base_dir / material_id
        material_dir.mkdir(parents=True, exist_ok=True)

        destination = material_dir / filename
        destination.write_bytes(content)
        return destination

    def save_processed_content(self, material_id: str, content: str) -> Path:
        """
        Store normalized processed text in storage/processed/<material_id>/content.txt.
        Returns the absolute Path.
        """
        material_dir = self.processed_base_dir / material_id
        material_dir.mkdir(parents=True, exist_ok=True)

        destination = material_dir / "content.txt"
        destination.write_text(content, encoding="utf-8")
        return destination

    def get_raw_file_path(self, material_id: str, filename: str) -> Path:
        return self.raw_base_dir / material_id / filename

    def get_processed_content_path(self, material_id: str) -> Path:
        return self.processed_base_dir / material_id / "content.txt"

    def read_processed_content(self, material_id: str) -> str | None:
        path = self.get_processed_content_path(material_id)
        if path.is_file():
            return path.read_text(encoding="utf-8")
        return None

    def delete_material_storage(self, material_id: str) -> None:
        """
        Delete both raw and processed artifacts for the specified material ID.
        """
        # Delete raw folder
        raw_dir = self.raw_base_dir / material_id
        if raw_dir.is_dir():
            for child in raw_dir.iterdir():
                if child.is_file():
                    child.unlink()
            raw_dir.rmdir()

        # Delete processed folder
        processed_dir = self.processed_base_dir / material_id
        if processed_dir.is_dir():
            for child in processed_dir.iterdir():
                if child.is_file():
                    child.unlink()
            processed_dir.rmdir()


# Default singleton instance
storage_service = StorageService()
