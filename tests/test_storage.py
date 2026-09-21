from pathlib import Path
from app.services.storage import StorageService


def test_storage_service(tmp_path: Path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    storage = StorageService(raw_base_dir=raw_dir, processed_base_dir=processed_dir)

    mat_id = "test-mat-001"
    filename = "lecture1.pdf"
    content = b"PDF mock content binary"

    # 1. Save raw
    raw_path = storage.save_raw_file(mat_id, filename, content)
    assert raw_path.exists()
    assert raw_path.read_bytes() == content
    assert storage.get_raw_file_path(mat_id, filename) == raw_path

    # 2. Save processed
    processed_text = "Normalized content ready for RAG"
    proc_path = storage.save_processed_content(mat_id, processed_text)
    assert proc_path.exists()
    assert storage.read_processed_content(mat_id) == processed_text

    # 3. Delete material storage
    storage.delete_material_storage(mat_id)
    assert not (raw_dir / mat_id).exists()
    assert not (processed_dir / mat_id).exists()
    assert storage.read_processed_content(mat_id) is None
