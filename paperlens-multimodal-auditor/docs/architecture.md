# Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│           PAPERLENS SYSTEM ARCHITECTURE                  │
└─────────────────────────────────────────────────────────┘

USER
  ↓
[Streamlit Frontend]
  ├─ File upload
  ├─ Progress tracking
  └─ Results visualization
  
  ↓ POST /api/audit
  
[FastAPI Backend]
  ├─ Route handler
  ├─ Request validation
  └─ Error handling
  
  ↓
[Ingestion Pipeline]
  ├─ PDF parsing (PyMuPDF)
  ├─ Text extraction
  └─ Image extraction (high-res)
  
  ↓
[Multimodal Auditor]
  │
  ├─→ [Phase 1: Claim Extraction]
  │   ├─ Model: Gemini 3 Flash
  │   ├─ thinking_level: low
  │   └─ Output: JSON claims array
  │
  ├─→ [Phase 2: Visual Verification]
  │   ├─ Model: Gemini 3 Pro
  │   ├─ thinking_level: high
  │   ├─ Input: Text + high-res images
  │   ├─ media_resolution: high
  │   └─ Output: Verification results
  │
  └─→ [Phase 3: Contradiction Detection]
      ├─ Model: Gemini 3 Pro
      ├─ thinking_level: high
      ├─ Input: Claims + Verifications
      ├─ response_mime_type: application/json
      └─ Output: Structured audit report
  
  ↓
[AuditReport]
  ├─ claims: List[Claim]
  ├─ contradictions: List[Contradiction]
  └─ audit_summary: str
  
  ↓
[Response to Frontend]
  └─ Display results + download JSON
```

---

## Key Components

### 1. Frontend (Streamlit)
- **Purpose:** User-facing interface for PDF upload and results visualization
- **Features:**
  - Drag-and-drop PDF upload
  - Real-time progress tracking
  - Interactive claims & contradictions view
  - JSON export/download
- **Tech Stack:** Streamlit, Requests, Pillow

### 2. Backend (FastAPI)
- **Purpose:** RESTful API for processing and orchestration
- **Endpoints:**
  - `GET /health` — Health check
  - `POST /api/audit` — Upload PDF and run audit
- **Tech Stack:** FastAPI, Uvicorn, Pydantic

### 3. Ingestion Pipeline
- **Purpose:** Extract text and images from PDFs
- **Process:**
  - Parse PDF using PyMuPDF
  - Extract all text per page
  - Extract all images in high resolution
  - Chunk text for processing
- **Output:** Dictionary with text data + list of images with base64 encoding

### 4. Multimodal Auditor (Core)
Three-phase pipeline leveraging Gemini 3:

#### Phase 1: Claim Extraction
```
Input:  Full paper text
Model:  Gemini 3 Flash (fast, cost-efficient)
Config: thinking_level: "low"
Output: JSON array of claims with confidence scores
```

**Why Gemini 3 Flash?**
- Fast inference for initial analysis
- Lower cost (appropriate for filtering step)
- Sufficient reasoning for claim detection

#### Phase 2: Visual Verification
```
Input:  Text chunks + extracted page images
Model:  Gemini 3 Pro (advanced reasoning)
Config: 
  - thinking_level: "high"
  - media_resolution: "high" (for charts/diagrams)
Output: Verification JSON mapping claims to visual evidence
```

**Why `media_resolution: high`?**
- Charts, tables, and diagrams need high detail
- Gemini 3's multimodal stack processes images in-context
- Single transformer processes text + images simultaneously

#### Phase 3: Contradiction Detection
```
Input:  Claims + verification results
Model:  Gemini 3 Pro (structured reasoning)
Config:
  - thinking_level: "high"
  - response_mime_type: "application/json"
  - response_json_schema: ContradictionAudit
Output: Structured JSON with contradictions flagged
```

**Why Structured Outputs?**
- Guarantees JSON validity
- Enforces schema compliance
- Reduces parsing errors
- Judges see Gemini 3 API best practices

---

## Data Models (Pydantic)

### Claim
```python
{
  "text": str,           # The extracted claim
  "confidence": float,   # 0-1 confidence score
  "page": int,           # Estimated page number
  "evidence_type": str   # "quantitative", "qualitative", "comparative"
}
```

### Contradiction
```python
{
  "claim": str,                    # Original claim
  "visual_evidence_page": int,     # Page with contradicting figure
  "visual_shows": str,             # Description of figure content
  "contradiction_type": str,       # "direct_conflict" / "partial_contradiction" / "unsupported"
  "confidence": float,             # 0-1 confidence
  "reasoning": str (optional)      # Explanation of contradiction
}
```

### AuditReport
```python
{
  "claims": List[Claim],           # All extracted claims
  "contradictions": List[Contradiction],  # Detected contradictions
  "audit_summary": str,            # Human-readable summary
  "total_pages": int,              # PDF page count
  "processing_time_seconds": float # End-to-end execution time
}
```

---

## Gemini 3 API Usage

### Key Parameters

| Parameter | Value | Why |
|-----------|-------|-----|
| `model` | `gemini-3-pro-preview` | Latest Gemini 3 reasoning model |
| `thinking_level` | `"low"` (Phase 1), `"high"` (Phase 2-3) | Trade-off speed vs. reasoning depth |
| `media_resolution` | `"high"` (figures), `"low"` (optional) | Optimize for multimodal understanding |
| `response_mime_type` | `"application/json"` (Phase 3) | Enforce structured output |
| `response_json_schema` | ContradictionAudit schema | Validate output structure |
| `temperature` | 0.2-0.3 | Low temperature for deterministic reasoning |

### Token Efficiency

**Context Window:** Gemini 3 Pro supports 1M input tokens
- Full paper text + images can be ingested in single request if under limit
- Falls back to chunking if necessary

**Cost Optimization:**
- Phase 1: Use Flash for initial filtering (lower cost)
- Phase 2-3: Use Pro for complex reasoning (higher accuracy > cost)

---

## Error Handling

| Error | Handling |
|-------|----------|
| Invalid PDF | Return 400 with message |
| No text extracted | Return warning in summary |
| API rate limit | Retry with exponential backoff |
| JSON parsing failure | Return error, log response |
| Empty claims/contradictions | Return empty arrays + summary |

---

## Performance Characteristics

**Typical Processing Time:**
- Phase 1 (Claim Extraction): 5-10s
- Phase 2 (Visual Verification): 15-20s
- Phase 3 (Contradiction Detection): 10-15s
- **Total:** 30-45s for average research paper

**Scalability Considerations:**
- Each PDF is processed independently
- Can queue requests for batch processing
- Image extraction is compute-intensive; consider caching

---

## Security & Privacy

- PDFs uploaded to backend are processed but not stored
- Gemini 3 API calls are over HTTPS
- User should use `.env` for API key (never hardcode)
- No data retention on backend (process & discard)

---

## Future Enhancements

1. **Caching:** Store embeddings to skip Phase 1 for repeated papers
2. **Batch Processing:** Queue multiple PDFs
3. **Fine-tuned Models:** Domain-specific claim detection
4. **Multi-language Support:** Translate before analysis
5. **Figure Captioning:** Auto-generate descriptions of figures
6. **Citation Retrieval:** Link contradictions to source citations
7. **Confidence Calibration:** Learn from user feedback to refine scores
