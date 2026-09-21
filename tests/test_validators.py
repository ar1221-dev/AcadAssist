import pytest
from app.services.validator import (
    DuplicateMaterialError,
    EmptyFileError,
    FileTooLargeError,
    InvalidSubjectError,
    MaterialValidator,
    UnsafeFilenameError,
    UnsupportedFileTypeError,
)
from app.models.material import Material, ProcessingStatus
from app.utils.security import compute_sha256, sanitize_filename


def test_validate_subject():
    assert MaterialValidator.validate_subject("Mathematics") == "Mathematics"
    assert MaterialValidator.validate_subject("  Data Structures  ") == "Data Structures"

    with pytest.raises(InvalidSubjectError):
        MaterialValidator.validate_subject("")

    with pytest.raises(InvalidSubjectError):
        MaterialValidator.validate_subject("   ")

    with pytest.raises(InvalidSubjectError):
        MaterialValidator.validate_subject(None)


def test_validate_filename_traversal():
    assert MaterialValidator.validate_filename("notes.pdf") == "notes.pdf"

    # Directory traversal attempts
    with pytest.raises(UnsafeFilenameError):
        MaterialValidator.validate_filename("../secret.pdf")

    with pytest.raises(UnsafeFilenameError):
        MaterialValidator.validate_filename("..\\boot.ini")

    with pytest.raises(UnsafeFilenameError):
        MaterialValidator.validate_filename("/etc/passwd.txt")

    with pytest.raises(UnsafeFilenameError):
        MaterialValidator.validate_filename("sub/file.pdf")

    with pytest.raises(UnsafeFilenameError):
        MaterialValidator.validate_filename("test\x00file.pdf")


def test_sanitize_filename():
    assert sanitize_filename("my notes.pdf") == "my_notes.pdf"
    assert sanitize_filename("../../../etc/shadow.txt") == "shadow.txt"
    assert sanitize_filename("..\\..\\windows\\system32.dll") == "system32.dll"
    assert sanitize_filename("clean_lecture_01.pptx") == "clean_lecture_01.pptx"


def test_validate_file_type():
    assert MaterialValidator.validate_file_type("lecture.pdf") == "pdf"
    assert MaterialValidator.validate_file_type("slides.pptx") == "pptx"
    assert MaterialValidator.validate_file_type("legacy.ppt") == "ppt"
    assert MaterialValidator.validate_file_type("document.docx") == "docx"
    assert MaterialValidator.validate_file_type("legacy.doc") == "doc"
    assert MaterialValidator.validate_file_type("notes.txt") == "txt"

    with pytest.raises(UnsupportedFileTypeError):
        MaterialValidator.validate_file_type("malware.exe")

    with pytest.raises(UnsupportedFileTypeError):
        MaterialValidator.validate_file_type("script.py")

    with pytest.raises(UnsupportedFileTypeError):
        MaterialValidator.validate_file_type("archive.zip")


def test_validate_file_content():
    # Valid content
    MaterialValidator.validate_file_content(b"Valid content")

    # Empty content
    with pytest.raises(EmptyFileError):
        MaterialValidator.validate_file_content(b"")

    # Content exceeding limit
    with pytest.raises(FileTooLargeError):
        huge_data = b"x" * (51 * 1024 * 1024)
        MaterialValidator.validate_file_content(huge_data)


def test_duplicate_check(db_session):
    data = b"Some identical content"
    chash = compute_sha256(data)

    m = Material(
        id="mat-123",
        title="Intro",
        original_filename="intro.txt",
        filename="intro.txt",
        file_type="txt",
        file_size=len(data),
        content_hash=chash,
        subject="Computer Science",
        storage_path="/tmp/fake",
        processing_status=ProcessingStatus.PROCESSED,
    )
    db_session.add(m)
    db_session.commit()

    # Same hash under different subject should succeed
    MaterialValidator.check_duplicate(db_session, content_hash=chash, subject="Mathematics")

    # Same hash under same subject must fail
    with pytest.raises(DuplicateMaterialError):
        MaterialValidator.check_duplicate(db_session, content_hash=chash, subject="Computer Science")
