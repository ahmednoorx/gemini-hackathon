"""
FastAPI Backend for PaperLens
Multimodal Contradiction Detector
"""

import os
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from ingestion import extract_text_and_images
from gemini_auditor import MultimodalAuditor
from models import UploadResponse
import traceback


# Load environment variables
load_dotenv()

app = FastAPI(
    title="PaperLens",
    description="Multimodal Contradiction Detector using Gemini 3",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"\n🌐 {request.method} {request.url.path} | Client: {request.client.host}")
    response = await call_next(request)
    print(f"   ✅ Response: {response.status_code}")
    return response

# Initialize auditor
try:
    auditor = MultimodalAuditor()
    print("✅ Gemini 3 Auditor initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize auditor: {e}")
    auditor = None


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PaperLens",
        "gemini_ready": auditor is not None
    }


@app.post("/api/audit")
async def upload_and_audit(file: UploadFile = File(...)):
    """
    Upload a PDF and run the full contradiction detection pipeline.
    
    Returns:
        UploadResponse with audit report or error details
    """
    
    print(f"\n{'='*70}")
    print(f"📨 INCOMING REQUEST TO /api/audit")
    print(f"{'='*70}")
    
    if auditor is None:
        raise HTTPException(
            status_code=500,
            detail="Gemini 3 API not initialized. Check GOOGLE_API_KEY."
        )
    
    try:
        start_time = time.time()
        
        # Read PDF bytes
        pdf_bytes = await file.read()
        print(
            f"📄 Processing PDF: {file.filename} ({len(pdf_bytes)} bytes, "
            f"content_type={file.content_type})"
        )
        
        # Basic PDF validation (extension OR PDF header)
        is_pdf_extension = file.filename.lower().endswith(".pdf") if file.filename else False
        has_pdf_header = pdf_bytes[:4] == b"%PDF"
        is_pdf_mime = (file.content_type or "").lower() == "application/pdf"
        print(
            f"🔎 PDF validation: extension={is_pdf_extension}, header={has_pdf_header}, "
            f"mime={is_pdf_mime}"
        )
        print(f"🔎 PDF header bytes: {pdf_bytes[:8]!r}")
        
        if not (is_pdf_extension or has_pdf_header or is_pdf_mime):
            print(f"❌ PDF validation FAILED")
            raise HTTPException(
                status_code=400,
                detail=(
                    "File rejected: not a valid PDF. Please upload a .pdf file "
                    "or ensure the file starts with %PDF."
                )
            )
        
        if len(pdf_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty. Please upload a valid PDF."
            )
        
        # Phase 0: Ingest PDF
        print("[Ingestion] Extracting text and images...")
        text_data, images = extract_text_and_images(pdf_bytes)
        total_pages = text_data["pages"]
        full_text = text_data["text"]
        print(f"  → Extracted {len(full_text)} characters, {len(images)} images")
        
        # Run audit pipeline
        audit_report = auditor.run_full_audit(full_text, images, total_pages)
        audit_report.processing_time_seconds = time.time() - start_time
        
        return UploadResponse(
            status="success",
            message=f"Audit completed in {audit_report.processing_time_seconds:.1f}s",
            audit_report=audit_report
        )
    
    except HTTPException as e:
        print(f"❌ HTTP error during audit: {e.detail}")
        raise
    except Exception as e:
        print(f"❌ Error during audit: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Audit failed: {e}"
        )


@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "name": "PaperLens",
        "description": "Multimodal Contradiction Detector using Gemini 3",
        "endpoints": {
            "GET /health": "Health check",
            "POST /api/audit": "Upload PDF and run contradiction detection"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
