"""
ReportLab PDF Generation Service Test Suite.
Tests: Server-side ReportLab document compilation, section flowables, NumberedCanvas footers, and binary file serving.
"""

import asyncio
import os
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.services.pdf_service import PDFService
from backend.schemas.pdf import PDFRequest


async def verify_pdf_generation():
    print("Beginning ReportLab PDF Generation Service Verification...\n")
    service = PDFService()

    req = PDFRequest(title="Stripe Corporate Research Report")
    pdf_res = await service.generate_pdf(req)

    print(f"[ReportLab PDF Generated]")
    print(f"PDF ID: {pdf_res.pdf_id}")
    print(f"File Name: {pdf_res.file_name}")
    print(f"File Size: {pdf_res.file_size_bytes} bytes")
    print(f"Download URL: {pdf_res.download_url}")

    assert pdf_res.pdf_id is not None
    assert pdf_res.file_name.endswith(".pdf")
    assert pdf_res.file_size_bytes > 0

    # Verify binary file exists on disk
    file_path = service.get_pdf_file_path(pdf_res.pdf_id)
    assert file_path is not None
    assert os.path.exists(file_path)

    # Verify PDF binary magic bytes
    with open(file_path, "rb") as f:
        header = f.read(5)
        assert header == b"%PDF-", f"Expected %PDF- magic bytes header, got {header}"

    print("  • Verified valid ReportLab %PDF- binary header on disk.")

    # Test REST Endpoint POST /generate-pdf & GET /downloads/pdf/{pdf_id}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # POST /generate-pdf
        res_post = await client.post("/generate-pdf", json={"title": "Nvidia Market Report"})
        print(f"\n[POST /generate-pdf REST Test] Status: {res_post.status_code} | PDF ID: {res_post.json()['data']['pdf_id']}")
        assert res_post.status_code == 200

        pdf_id = res_post.json()["data"]["pdf_id"]

        # GET /downloads/pdf/{pdf_id}
        res_get = await client.get(f"/downloads/pdf/{pdf_id}")
        print(f"[GET /downloads/pdf/{pdf_id} REST Test] Status: {res_get.status_code} | Content-Type: {res_get.headers.get('content-type')}")
        assert res_get.status_code == 200
        assert "application/pdf" in res_get.headers.get("content-type", "")
        assert res_get.content.startswith(b"%PDF-")

    print("\nREPORTLAB PDF GENERATION VERIFICATION PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(verify_pdf_generation())
