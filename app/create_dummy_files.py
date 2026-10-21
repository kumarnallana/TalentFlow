# create_multipage_pdf.py
import io


def generate_multipage_pdf(filename="sample_multipage_resume.pdf"):
    buf = io.BytesIO()
    offsets = {}

    def write_object(num: int, content: bytes):
        offsets[num] = buf.tell()
        buf.write(f"{num} 0 obj\n".encode("ascii"))
        buf.write(content)
        buf.write(b"\nendobj\n")

    buf.write(b"%PDF-1.4\n")

    # Page 1 Text Stream
    stream_page_1 = (
        b"BT\n/F1 12 Tf\n"
        b"50 720 Td (Sarah Connor - Lead Python Engineer) Tj\n"
        b"0 -24 Td (Email: sarah.connor@example.com | Phone: +1-555-0144) Tj\n"
        b"0 -36 Td (PAGE 1: CORE SKILLS & HIGHLIGHTS) Tj\n"
        b"0 -24 Td (Primary Skills: Python, FastAPI, Docker, Microservices, AsyncIO) Tj\n"
        b"0 -36 Td (PROFESSIONAL EXPERIENCE) Tj\n"
        b"0 -24 Td (Lead Backend Engineer - TechCorp Systems [2022 - Present]) Tj\n"
        b"0 -20 Td (- Architected high-throughput asynchronous APIs using FastAPI and Uvicorn.) Tj\n"
        b"0 -20 Td (- Containerized scalable backend microservices using Docker.) Tj\n"
        b"0 -20 Td (- Optimized I/O operations and background task queueing routines.) Tj\n"
        b"ET"
    )

    # Page 2 Text Stream
    stream_page_2 = (
        b"BT\n/F1 12 Tf\n"
        b"50 720 Td (PAGE 2: DATABASE ARCHITECTURE & EDUCATION) Tj\n"
        b"0 -36 Td (EXTENDED TECHNICAL STACK) Tj\n"
        b"0 -24 Td (Database Systems: PostgreSQL, Redis, SQLAlchemy, SQL) Tj\n"
        b"0 -24 Td (DevOps & Tools: Kubernetes, Git, Linux, CI/CD) Tj\n"
        b"0 -36 Td (EDUCATION) Tj\n"
        b"0 -24 Td (Bachelor of Technology in Computer Science) Tj\n"
        b"0 -20 Td (- Coursework: Distributed Systems, Database Management, Data Structures.) Tj\n"
        b"0 -36 Td (PROJECT HIGHLIGHTS) Tj\n"
        b"0 -24 Td (- Implemented high-concurrency document processing engines in Python.) Tj\n"
        b"ET"
    )

    # 1: Catalog
    write_object(1, b"<< /Type /Catalog /Pages 2 0 R >>")

    # 2: Pages Parent
    write_object(2, b"<< /Type /Pages /Kids [3 0 R 6 0 R] /Count 2 >>")

    # 3: Page 1 Object
    write_object(
        3, b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")

    # 4: Standard Helvetica Font
    write_object(4, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    # 5: Page 1 Stream
    write_object(5, f"<< /Length {len(stream_page_1)} >>\nstream\n".encode(
        "ascii") + stream_page_1 + b"\nendstream")

    # 6: Page 2 Object
    write_object(
        6, b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 7 0 R >>")

    # 7: Page 2 Stream
    write_object(7, f"<< /Length {len(stream_page_2)} >>\nstream\n".encode(
        "ascii") + stream_page_2 + b"\nendstream")

    # Cross-reference Table (Xref)
    startxref = buf.tell()
    buf.write(b"xref\n0 8\n0000000000 65535 f \n")
    for i in range(1, 8):
        buf.write(f"{offsets[i]:010d} 00000 n \n".encode("ascii"))

    # Trailer
    buf.write(
        f"trailer\n<< /Size 8 /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF".encode("ascii"))

    with open(filename, "wb") as f:
        f.write(buf.getvalue())

    print(f"Successfully created: {filename} (2 Pages)")


if __name__ == "__main__":
    generate_multipage_pdf()
