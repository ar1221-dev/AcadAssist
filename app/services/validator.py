from sqlalchemy.orm import Session

from app.config import settings
from app.models.material import Material
from app.utils.security import extract_extension


class MaterialValidationError(Exception):
    def __init__(self, message: str, error_code: str):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class UnsupportedFileTypeError(MaterialValidationError):
    def __init__(self, ext: str):
        super().__init__(
            f"File format '.{ext}' is unsupported. Allowed formats: {sorted(list(settings.ALLOWED_EXTENSIONS))}",
            error_code="UNSUPPORTED_FILE_TYPE",
        )


class FileTooLargeError(MaterialValidationError):
    def __init__(self, size: int, max_size: int):
        super().__init__(
            f"File size of {size} bytes exceeds maximum allowed limit of {max_size} bytes ({max_size // (1024 * 1024)}MB)",
            error_code="FILE_TOO_LARGE",
        )


class EmptyFileError(MaterialValidationError):
    def __init__(self):
        super().__init__("Uploaded file is empty (0 bytes).", error_code="EMPTY_FILE")


class UnsafeFilenameError(MaterialValidationError):
    def __init__(self, reason: str):
        super().__init__(f"Unsafe filename: {reason}", error_code="UNSAFE_FILENAME")


class InvalidSubjectError(MaterialValidationError):
    def __init__(self):
        super().__init__(
            "Subject is required and cannot be empty or whitespace only.",
            error_code="INVALID_SUBJECT",
        )


class DuplicateMaterialError(MaterialValidationError):
    def __init__(self, existing_id: str, title: str, subject: str):
        super().__init__(
            f"A document with identical content already exists under subject '{subject}' (ID: {existing_id}, Title: '{title}').",
            error_code="DUPLICATE_MATERIAL",
        )


class MaterialValidator:
    @staticmethod
    def validate_subject(subject: str | None) -> str:
        if not subject or not subject.strip():
            raise InvalidSubjectError()
        return subject.strip()

    @staticmethod
    def validate_filename(filename: str | None) -> str:
        if not filename or not filename.strip():
            raise UnsafeFilenameError("Filename cannot be empty")
        
        # Check for path traversal patterns
        if ".." in filename or "/" in filename or "\\" in filename:
            raise UnsafeFilenameError("Filename must not contain path traversal characters ('..', '/', '\\')")

        if "\x00" in filename:
            raise UnsafeFilenameError("Filename must not contain null bytes")

        return filename.strip()

    @staticmethod
    def validate_file_type(filename: str) -> str:
        ext = extract_extension(filename)
        if not ext or ext not in settings.ALLOWED_EXTENSIONS:
            raise UnsupportedFileTypeError(ext)
        return ext

    @staticmethod
    def validate_file_content(content: bytes) -> None:
        if len(content) == 0:
            raise EmptyFileError()
        if len(content) > settings.MAX_FILE_SIZE_BYTES:
            raise FileTooLargeError(len(content), settings.MAX_FILE_SIZE_BYTES)

    @staticmethod
    def check_duplicate(
        db: Session, content_hash: str, subject: str
    ) -> None:
        existing = (
            db.query(Material)
            .filter(Material.content_hash == content_hash, Material.subject == subject)
            .first()
        )
        if existing:
            raise DuplicateMaterialError(
                existing_id=existing.id,
                title=existing.title,
                subject=existing.subject,
            )
