from pathlib import Path
from app.services.processors import get_processor_for_extension


def test_samples():
    files = [
        "sample_data/trees.pdf",
        "sample_data/networks.pptx",
        "sample_data/normalization.docx",
        "sample_data/linear_algebra.txt",
        "sample_data/os_scheduling.ppt",
        "sample_data/software_eng.doc",
    ]
    for f in files:
        p = Path(f)
        ext = p.suffix.lstrip(".")
        proc = get_processor_for_extension(ext)
        res = proc.extract(p)
        print(f"=== {f} ({ext}) ===")
        print(f"Pages: {res.page_count}, Slides: {res.slide_count}, Total Chars: {res.total_chars}")
        print(f"Sections Count: {len(res.sections)}")
        if res.sections:
            snippet = res.sections[0]["content"][:80].replace("\n", " ")
            print(f"Snippet: {snippet}...")
        print()


if __name__ == "__main__":
    test_samples()
