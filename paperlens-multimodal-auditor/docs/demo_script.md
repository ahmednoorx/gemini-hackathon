# 3-Minute Demo Video Script

## Target: Judges watching on Devpost

**Goal:** Show that PaperLens is NOT just a wrapper around Gemini 3, but a **novel tool** that uses Gemini 3's unique multimodal capabilities in a way that solves a real problem.

---

## Shot-by-Shot Breakdown

### [0:00–0:15] Title Card (15 seconds)

**Visual:** Clean title slide with PaperLens logo/text

**Script:**
> "This is **PaperLens** — a multimodal contradiction detector powered by Google Gemini 3.
> We detect when research papers' text claims contradict their own figures.
> Let's see it in action."

**Why:** Sets context. "Contradiction detection" is immediately different from "yet another AI chatbot."

---

### [0:15–0:35] Problem Statement (20 seconds)

**Visual:** Show a research paper PDF on screen, highlight text and figure side-by-side

**Script:**
> "Here's a real problem: Scientists write papers with text claims and figures.
> Sometimes they contradict each other — like a paper saying 'Growth increased by 15%' while the graph shows a 5% decrease.
> Manual checking takes hours. We automate it with Gemini 3's multimodal reasoning."

**Why:** Judges understand the value. Real, concrete problem.

---

### [0:35–1:30] Live Demo (55 seconds)

**Visual:** Streamlit app on screen. User uploads a PDF.

**Script (as you interact):**

> **[0:35–0:45]** "Here's our Streamlit interface. I'm uploading a test research paper in PDF format."
> 
> *[Show file upload, click "Run Audit" button]*
> 
> **[0:45–1:00]** "The backend is now running our three-phase pipeline:
> - Phase 1: Extract claims using Gemini 3 Flash (fast, cost-efficient)
> - Phase 2: Verify claims against figures using Gemini 3 Pro with high thinking levels
> - Phase 3: Detect contradictions with structured JSON output"
> 
> *[Wait for results to appear on screen ~15 seconds]*
> 
> **[1:00–1:20]** "Here are the results. We found 12 claims and **2 contradictions**.
> Look at this one: 'Results showed 40% improvement' — but Figure 3 clearly shows only a 15% improvement.
> See the confidence score? 0.88 — Gemini 3 is confident there's a contradiction."
> 
> *[Click on the contradiction, show the details]*
> 
> **[1:20–1:30]** "You can see the exact claim, the page number, what the figure shows, and Gemini 3's reasoning. All exportable as JSON."

**Why:** Live demo sells the credibility. Judges see it works in real-time.

---

### [1:30–2:10] Technical Deep Dive (40 seconds)

**Visual:** Show architecture diagram or code snippet (can be slide or screen recording)

**Script:**
> "Here's what makes this Gemini 3-specific:
> 
> **First:** We use `media_resolution: high` when passing figures to Gemini 3.
> This tells Gemini 3 to focus on chart details, not just background.
> 
> **Second:** We use `thinking_level: high` for contradiction detection.
> This makes Gemini 3 reason deeply about text-image consistency.
> 
> **Third:** We enforce structured JSON output using Gemini 3's response schema feature.
> This guarantees every contradiction report is machine-readable and validated.
> 
> These are Gemini 3-exclusive features. Older models can't do this."

**Visual suggestion:**
```python
# Show brief code snippet
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[text_part, image_part],
    config=GenerateContentConfig(
        thinking_config=ThinkingConfig(thinking_level="high"),
        response_mime_type="application/json",
        response_json_schema=ContradictionAudit.model_json_schema(),
    )
)
```

**Why:** Shows judges you understand Gemini 3's capabilities. Not just "we used an LLM."

---

### [2:10–2:50] Impact & Use Cases (40 seconds)

**Visual:** Slide show or text overlay with bullet points

**Script:**
> "Who benefits from PaperLens?
> 
> **Researchers** use it to catch inconsistencies before submission.
> 
> **Publishers** use it to flag suspicious papers during peer review.
> 
> **Students** use it to verify claims in papers they're reading.
> 
> **This solves a real problem in science:** Misinformation detection at scale.
> 
> The code is open-source, the API is fast (30–45 seconds per paper), and the cost is minimal (~$0.50 per analysis)."

**Why:** Demonstrates impact (not just a tech demo) and scalability.

---

### [2:50–3:00] Call-to-Action (10 seconds)

**Visual:** Show GitHub repo link, live demo link, or closing slide

**Script:**
> "Check out the code on GitHub, try the live demo, and let us know what contradictions you find!
> Thanks for watching."

**Visual:** End with PaperLens logo or credits.

---

## Recording Tips

1. **Screen Resolution:** 1920x1080 minimum (judges watch on various screens)
2. **Microphone:** Clear audio, no background noise
3. **Pacing:** Speak clearly, not too fast (judges might pause to take notes)
4. **Lighting:** If showing your face, good lighting
5. **File Size:** Compress to ~100–300 MB for smooth YouTube upload
6. **Subtitle/Captions:** Optional but helps accessibility

---

## Video Production Checklist

- [ ] Have Streamlit app running and tested before recording
- [ ] Have a test PDF with clear contradictions ready
- [ ] Record on a clean desktop (hide personal files)
- [ ] Have code snippet or architecture diagram visible
- [ ] Test audio (no echo, no background noise)
- [ ] Record in full screen (no distracting tabs)
- [ ] Do a dry run first; don't go live on first take
- [ ] Upload to YouTube as "Unlisted" (then link in Devpost)

---

## Script Notes

- **Use the pause:** After showing results, pause 2 seconds so judges can read the JSON output
- **Point to details:** Use mouse cursor to highlight specific numbers/fields (0.88 confidence, Figure 3, etc.)
- **Admit limitations:** If you have time, mention one future improvement ("We're working on multi-paper cross-reference detection")
- **Enthusiasm matters:** Show excitement about the tech. Judges feed off energy.

---

## Common Mistakes to Avoid

❌ Too much jargon (judges may not be ML experts)  
❌ Rushing through the demo  
❌ Showing code for more than 15 seconds (viewers tune out)  
❌ Not explaining why this is Gemini 3-specific  
❌ Going over 3 minutes (judges may not watch beyond)  

---

## Example Timings (for your reference)

| Segment | Duration | Cumulative |
|---------|----------|-----------|
| Title | 15s | 0:15 |
| Problem | 20s | 0:35 |
| Demo Part 1 | 35s | 1:10 |
| Demo Part 2 (waiting) | 20s | 1:30 |
| Tech Deep Dive | 40s | 2:10 |
| Impact | 40s | 2:50 |
| CTA | 10s | 3:00 |

---

## Final Checklist Before Upload

- [ ] Total video length: ~3:00 (under 3:30 max)
- [ ] Audio is clear and synced
- [ ] No sensitive info visible (API keys, passwords)
- [ ] Subtitles added (if possible)
- [ ] Formatted as MP4 or MOV
- [ ] Uploaded to YouTube
- [ ] Link copied to clipboard for Devpost form

---

Good luck! 🎬
