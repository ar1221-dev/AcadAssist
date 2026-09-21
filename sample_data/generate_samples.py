import io
from pathlib import Path
import docx
from pptx import Presentation
from pptx.util import Inches, Pt
from pypdf import PdfWriter


def create_sample_pdf(dest: Path):
    """Generate a valid multi-page PDF with academic text using pypdf writer."""
    writer = PdfWriter()
    # Create blank pages and add annotations/text or write raw PDF stream
    # A standard minimal 2-page PDF file:
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R /Resources << /Font << /F1 7 0 R >> >> >>
endobj
4 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R /Resources << /Font << /F1 7 0 R >> >> >>
endobj
5 0 obj
<< /Length 83 >>
stream
BT
/F1 18 Tf
50 700 Td
(Data Structures: Binary Search Trees) Tj
/F1 12 Tf
0 -30 Td
(A BST is a node-based binary tree where left < root < right.) Tj
ET
endstream
endobj
6 0 obj
<< /Length 88 >>
stream
BT
/F1 18 Tf
50 700 Td
(BST Operations and Complexity) Tj
/F1 12 Tf
0 -30 Td
(Average search, insertion, and deletion complexity is O(log n).) Tj
ET
endstream
endobj
7 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 8
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000224 00000 n 
0000000333 00000 n 
0000000468 00000 n 
0000000608 00000 n 
trailer
<< /Size 8 /Root 1 0 R >>
startxref
687
%%EOF
"""
    dest.write_bytes(pdf_content)
    print(f"Created PDF at {dest}")


def create_sample_pptx(dest: Path):
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide1 = prs.slides.add_slide(slide_layout)
    slide1.shapes.title.text = "Computer Networks: OSI Model"
    slide1.placeholders[1].text = "Overview of 7 Layers from Physical to Application."

    slide_layout2 = prs.slide_layouts[1]  # Bullet layout
    slide2 = prs.slides.add_slide(slide_layout2)
    slide2.shapes.title.text = "Transport Layer Protocols"
    body2 = slide2.placeholders[1]
    body2.text = "TCP provides reliable, ordered stream delivery.\nUDP provides lightweight, connectionless datagram transport."

    prs.save(str(dest))
    print(f"Created PPTX at {dest}")


def create_sample_docx(dest: Path):
    doc = docx.Document()
    doc.add_heading("Database Management Systems: Normalization", level=0)
    
    p1 = doc.add_paragraph("Database normalization is the process of structuring a relational database.")
    p1.add_run(" The goal is to reduce data redundancy and improve data integrity.")

    doc.add_heading("First Normal Form (1NF)", level=1)
    doc.add_paragraph("Each column must contain atomic (indivisible) values, and each record must be unique.")

    doc.add_heading("Second Normal Form (2NF)", level=1)
    doc.add_paragraph("Must be in 1NF and all non-key attributes must be fully functionally dependent on the primary key.")

    # Add a summary table
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Normal Form"
    hdr_cells[1].text = "Key Requirement"
    row = table.add_row().cells
    row[0].text = "1NF"
    row[1].text = "Atomic attributes"
    row2 = table.add_row().cells
    row2[0].text = "2NF"
    row2[1].text = "No partial key dependencies"

    doc.save(str(dest))
    print(f"Created DOCX at {dest}")


def create_sample_txt(dest: Path):
    content = """=== Linear Algebra Lecture Notes ===
Subject: Mathematics
Course: MATH201

--- Section 1: Vector Spaces ---
A vector space over a field F is a set V together with two operations:
vector addition and scalar multiplication.

--- Section 2: Eigenvalues and Eigenvectors ---
Let A be an n-by-n matrix. A non-zero vector v is an eigenvector of A
if Av = lambda * v for some scalar lambda (the eigenvalue).
Characteristic equation: det(A - lambda * I) = 0.
"""
    dest.write_text(content, encoding="utf-8")
    print(f"Created TXT at {dest}")


def create_sample_ppt(dest: Path):
    """
    Create a legacy PPT binary file with valid OLE compound document structure
    or fallback text records.
    """
    # Create simple binary stream with PPT record structure
    # RT_TextCharsAtom = 4000 (0x0FA0), UTF-16LE
    # Struct: ver_inst(H), rec_type(H), rec_len(I), data
    text = "Operating Systems: Process Scheduling and Virtual Memory"
    utf16_bytes = text.encode("utf-16-le")
    rec_type = 4000
    ver_inst = 0
    rec_len = len(utf16_bytes)
    import struct
    header = struct.pack("<HHI", ver_inst, rec_type, rec_len)
    data = b"PowerPoint Document\x00\x00\x00" + header + utf16_bytes
    dest.write_bytes(data)
    print(f"Created legacy PPT at {dest}")


def create_sample_doc(dest: Path):
    """
    Create a legacy DOC binary file with valid binary stream containing Unicode text runs.
    """
    text = "Software Engineering: Agile Methodologies and CI/CD Pipelines"
    utf16_bytes = text.encode("utf-16-le")
    # FIB magic 0xA5EC followed by unicode text sequence
    import struct
    fib_magic = struct.pack("<H", 0xA5EC)
    padding = b"\x00" * 510
    data = fib_magic + padding + utf16_bytes
    dest.write_bytes(data)
    print(f"Created legacy DOC at {dest}")


def main():
    sample_dir = Path("sample_data")
    sample_dir.mkdir(parents=True, exist_ok=True)
    create_sample_pdf(sample_dir / "trees.pdf")
    create_sample_pptx(sample_dir / "networks.pptx")
    create_sample_docx(sample_dir / "normalization.docx")
    create_sample_txt(sample_dir / "linear_algebra.txt")
    create_sample_ppt(sample_dir / "os_scheduling.ppt")
    create_sample_doc(sample_dir / "software_eng.doc")


if __name__ == "__main__":
    main()
