"""
PDF Ingestion Module
Extracts text and high-resolution images from PDFs.
"""

import fitz  # PyMuPDF
import io
from typing import Tuple, List
from PIL import Image
import base64


def extract_text_and_images(pdf_bytes: bytes) -> Tuple[dict, List[dict]]:
    """
    Extract text and images from a PDF file.
    
    Args:
        pdf_bytes: Binary PDF data
        
    Returns:
        Tuple of:
        - text_data: {"text": str, "pages": int}
        - images: List of {"page": int, "image_b64": str, "image_pil": PIL.Image}
    """
    
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    if pdf_document.is_encrypted:
        # Try to authenticate with empty password (some PDFs use it)
        if not pdf_document.authenticate(""):
            pdf_document.close()
            raise ValueError(
                "PDF is password-protected or encrypted. Please upload an unencrypted PDF."
            )
    total_pages = len(pdf_document)
    
    # Extract all text
    full_text = ""
    for page_num in range(total_pages):
        page = pdf_document[page_num]
        full_text += f"\n--- PAGE {page_num + 1} ---\n"
        full_text += page.get_text()
    
    # Extract images (high resolution)
    extracted_images = []
    for page_num in range(total_pages):
        page = pdf_document[page_num]
        
        # Get all images on this page
        image_list = page.get_images(full=True)
        
        for img_index, img_ref in enumerate(image_list):
            xref = img_ref[0]
            pix = fitz.Pixmap(pdf_document, xref)
            
            # Convert to RGB if needed
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                timg = pix
            else:
                timg = fitz.Pixmap(fitz.csRGB, pix)
            
            # Convert to PIL Image
            img_data = timg.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            
            # Encode to base64
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_b64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
            
            extracted_images.append({
                "page": page_num + 1,
                "image_index": img_index,
                "image_b64": img_b64,
                "image_pil": img,
                "mime_type": "image/png"
            })
    
    pdf_document.close()
    
    text_data = {
        "text": full_text,
        "pages": total_pages
    }
    
    return text_data, extracted_images


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split extracted text into chunks with overlap.
    
    Args:
        text: Full text from PDF
        chunk_size: Characters per chunk
        overlap: Overlapping characters between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks
