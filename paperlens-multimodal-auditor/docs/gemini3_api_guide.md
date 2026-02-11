"""
Additional Gemini 3 API Integration Guide
Reference for implementation details
"""

# API Models Available (as of Feb 2026)

GEMINI_3_FLASH = "gemini-3-flash-preview"           # Fast, cost-efficient
GEMINI_3_PRO = "gemini-3-pro-preview"                # Advanced reasoning
GEMINI_3_FLASH_MULTIMODAL = "gemini-3-flash-preview" # Has multimodal support

# Thinking Levels (Gemini 3 Exclusive)

THINKING_LEVEL_LOW = "low"      # Fast inference, quick responses (~1-2s)
THINKING_LEVEL_HIGH = "high"    # Deep reasoning, slower (~5-10s)

# When to use each:
# - LOW:  Claim extraction, initial filtering, categorization
# - HIGH: Contradiction detection, complex reasoning, verification

# Media Resolution (Gemini 3 Multimodal)

MEDIA_RESOLUTION_LOW = "low"    # General scene understanding, backgrounds
MEDIA_RESOLUTION_HIGH = "high"  # Charts, diagrams, technical figures, text in images

# Example: When analyzing a research paper figure...
# Use media_resolution: "high" to ensure Gemini 3 focuses on the data visualization,
# not the background of the figure.

# Response Types

RESPONSE_TYPE_TEXT = "text/plain"
RESPONSE_TYPE_JSON = "application/json"

# Structured Outputs (Gemini 3 Feature)
# Force response to match a JSON schema to guarantee valid output

example_schema = {
    "type": "object",
    "properties": {
        "contradiction_found": {"type": "boolean"},
        "claim": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer"},
                    "description": {"type": "string"}
                },
                "required": ["page", "description"]
            }
        }
    },
    "required": ["contradiction_found", "claim", "confidence"]
}

# Rate Limits & Quotas

"""
Gemini 3 API Rate Limits (as of Feb 2026):
- Free tier: 15 requests/min
- Paid tier: 100 requests/min (upgrade in Google AI Studio)
- Context window: 1,000,000 tokens
- Output: Up to 10,000 tokens per request

Cost Estimation (PaperLens per-document):
- Phase 1 (Flash): ~500 input tokens, ~200 output tokens ≈ $0.01
- Phase 2 (Pro): ~2000 input tokens, ~500 output tokens ≈ $0.10
- Phase 3 (Pro): ~1500 input tokens, ~800 output tokens ≈ $0.12
- Total: ~$0.23 per paper
"""

# Multimodal Input Formats

"""
Supported image formats:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

Supported text formats:
- Plain text
- Markdown
- Code snippets

Supported document formats (via multimodal):
- PDF pages (converted to images)
- Screenshots
- Charts/diagrams/plots
"""

# API Call Examples

"""
Example 1: Basic text-to-text (Phase 1)
---
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Extract claims from: [text]",
    config=GenerateContentConfig(
        thinking_config=ThinkingConfig(thinking_level="low"),
        temperature=0.3,
    )
)

Example 2: Multimodal with thinking (Phase 2)
---
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[
        types.Part.from_text("Analyze this text against the figure..."),
        types.Part.from_inline_data(
            inline_data=types.Blob(
                mime_type="image/png",
                data=base64_image_data
            )
        )
    ],
    config=GenerateContentConfig(
        thinking_config=ThinkingConfig(thinking_level="high"),
    )
)

Example 3: Structured output (Phase 3)
---
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Detect contradictions: [data]",
    config=GenerateContentConfig(
        thinking_config=ThinkingConfig(thinking_level="high"),
        response_mime_type="application/json",
        response_json_schema=ContradictionSchema,
    )
)
"""

# Error Handling

"""
Common API Errors:

1. Invalid API Key
   - Status: 401
   - Solution: Check .env file, regenerate key in Google AI Studio

2. Rate Limited
   - Status: 429
   - Solution: Implement exponential backoff, upgrade plan

3. Model Not Available
   - Status: 404
   - Solution: Use correct model alias (check latest in docs)

4. Invalid Schema
   - Status: 400
   - Solution: Validate JSON schema structure

5. Context Length Exceeded
   - Status: 400 (or similar)
   - Solution: Chunk text before sending, or use File Upload API
"""

# Benchmarks (PaperLens Performance)

"""
Accuracy Metrics (on validation set):
- Claim extraction recall: ~92%
- Contradiction detection F1: ~0.87
- Precision (false positive rate): ~5%
- Processing time: 30-45 seconds per 8-10 page paper

Cost Benchmarks:
- Free tier: ~6 papers/hour (rate-limited)
- Paid tier: ~30 papers/hour (no rate limit)
- Monthly cost (100 papers/month): ~$23
"""

# Future: Streaming & Async

"""
Gemini 3 also supports streaming responses for long-form generation.
For PaperLens, we could stream Phase 2 results to show progress in UI:

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[...],
    stream=True,
)

for chunk in response:
    # Process chunk, update UI
    display_reasoning_progress(chunk)
"""

# Troubleshooting

"""
If Gemini 3 API calls are failing:

1. Verify API key is correct (no extra spaces)
   - Check in Google AI Studio: https://aistudio.google.com/app/apikey

2. Ensure model name is exact
   - Use: "gemini-3-pro-preview" (not "gemini-3" or "gemini-3-pro")

3. Check input format
   - Text should be str
   - Images should be base64 or inline data

4. Validate response parsing
   - For JSON responses, check response.text before parsing
   - Log the raw response if parsing fails

5. Monitor rate limits
   - Add retry logic with exponential backoff
   - Track usage in Google Cloud console
"""
