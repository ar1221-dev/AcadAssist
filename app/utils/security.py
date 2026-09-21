import hashlib
import re
from pathlib import Path


def compute_sha256(data: bytes) -> str:
    """Compute SHA-256 hex digest of binary content."""
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize an uploaded filename to prevent directory traversal,
    null byte injection, and invalid filesystem characters.
    """
    if not filename or not filename.strip():
        return "unnamed_document"

    # Strip directory components (both Unix and Windows slashes)
    clean_name = filename.replace("\\", "/").split("/")[-1]
    
    # Remove null bytes and path traversal patterns
    clean_name = clean_name.replace("\x00", "").replace("..", "")
    
    # Extract stem and extension
    p = Path(clean_name)
    stem = p.stem
    ext = p.suffix.lower()

    # Replace any non-alphanumeric, dash, underscore, space, or dot with underscore
    sanitized_stem = re.sub(r"[^\w\s\-.]", "_", stem).strip()
    sanitized_stem = re.sub(r"\s+", "_", sanitized_stem)

    if not sanitized_stem:
        sanitized_stem = "document"

    # Limit filename length
    if len(sanitized_stem) > 100:
        sanitized_stem = sanitized_stem[:100]

    return f"{sanitized_stem}{ext}"


def extract_extension(filename: str) -> str:
    """Extract normalized lowercase extension without leading dot."""
    p = Path(filename)
    suffix = p.suffix.lower()
    return suffix.lstrip(".")
