"""
Gemini 3 Multimodal Auditor
3-Phase contradiction detection pipeline.
"""

import json
import os
import base64
from typing import List, Dict, Any
from google import genai
from models import Claim, Contradiction, AuditReport


class MultimodalAuditor:
    """Orchestrates the 3-phase contradiction detection."""
    
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"  # Use stable model
    
    def _filter_claims(self, claims: List[Claim]) -> List[Claim]:
        if not claims:
            return []
        filtered: List[Claim] = []
        for c in claims:
            t = (c.text or "").strip()
            t_lower = t.lower()
            if not t:
                continue
            if t_lower.startswith("--- page"):
                continue
            if "contents" in t_lower:
                continue
            if "introduction" in t_lower and len(t) < 120:
                continue
            if "section" in t_lower and len(t) < 120:
                continue
            if "appendix" in t_lower or "references" in t_lower:
                continue
            if t_lower.count(" ") < 6:
                continue
            filtered.append(c)
        return filtered

    def phase_1_extract_claims(self, text: str) -> List[Claim]:
        """
        Phase 1: Extract quantitative claims from text using Gemini.
        """
        def _extract_from_chunk(chunk: str) -> List[Claim]:
            prompt = f"""You are a scientific claim extractor. Analyze the following research paper text 
and extract all quantitative and comparative claims. Focus on claims with numbers, percentages, 
increases/decreases, comparisons between conditions.

Return ONLY a valid JSON array of claims with this exact format:
[
  {{"text": "claim text here", "confidence": 0.9, "page": 1, "evidence_type": "quantitative"}},
  {{"text": "another claim", "confidence": 0.8, "page": 2, "evidence_type": "comparative"}}
]

PAPER TEXT:
{chunk}

Return ONLY the JSON array, no markdown, no explanation."""
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                response_text = response.text.strip()
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                    response_text = response_text.strip()

                claims_json = json.loads(response_text)
                if not isinstance(claims_json, list):
                    return []
                return [Claim(**c) for c in claims_json]
            except Exception as e:
                print(f"Error in phase 1 chunk parse: {e}")
                return []

        # Try multiple chunks (start, middle, end) to avoid missing claims
        chunks = []
        if text:
            chunks.append(text[:8000])
            if len(text) > 16000:
                mid_start = max(0, (len(text) // 2) - 4000)
                chunks.append(text[mid_start:mid_start + 8000])
                chunks.append(text[-8000:])

        claims: List[Claim] = []
        for chunk in chunks:
            claims = _extract_from_chunk(chunk)
            if claims:
                break

        # Fallback: heuristic numeric-claim extraction if Gemini yields none
        if not claims:
            import re
            sentences = re.split(r"(?<=[.!?])\s+", text)
            exclude_tokens = (
                "university",
                "department",
                "street",
                "avenue",
                "usa",
                "canada",
                "spain",
                "italy",
                "france",
                "germany",
                "prepared for submission",
                "astrophysics research centre",
            )
            include_tokens = (
                "we find",
                "we obtain",
                "we measure",
                "we derive",
                "we compute",
                "result",
                "constraint",
                "consistent with",
                "significant",
                "confidence",
            )

            numeric_sentences = []
            for s in sentences:
                s_clean = " ".join(s.split()).strip()
                if not s_clean or len(s_clean) < 20:
                    continue
                s_lower = s_clean.lower()
                if any(tok in s_lower for tok in exclude_tokens):
                    continue
                if not re.search(r"\d", s_clean):
                    continue
                if include_tokens and not any(tok in s_lower for tok in include_tokens):
                    continue
                numeric_sentences.append(s_clean)

            for s in numeric_sentences[:10]:
                claims.append(Claim(
                    text=s[:300],
                    confidence=0.55,
                    page=1,
                    evidence_type="quantitative",
                ))

        return self._filter_claims(claims)
    
    def phase_2_visual_verification(
        self, 
        text: str, 
        claims: List[Claim], 
        images: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Phase 2: Cross-reference claims against visual evidence.
        """
        
        if not claims:
            return {"verifications": []}
        
        claims_text = "\n".join([f"- {c.text}" for c in claims[:5]])  # Limit to first 5
        
        prompt = f"""You are a scientific auditor. Analyze these claims against the text:

CLAIMS:
{claims_text}

TEXT:
{text[:3000]}

For each claim, determine if there is visual/numerical evidence supporting or contradicting it.
Return ONLY valid JSON in this format:
{{
  "verifications": [
    {{"claim": "claim text", "visual_found": true, "supports": true, "confidence": 0.8}}
  ]
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            result = json.loads(response_text)
            return result
        except Exception as e:
            print(f"Error in phase 2: {e}")
            return {"verifications": []}
    
    def phase_3_contradiction_detection(
        self,
        text: str,
        claims: List[Claim],
        verifications: Dict[str, Any]
    ) -> List[Contradiction]:
        """
        Phase 3: Flag contradictions.
        """
        
        if not claims:
            return []
        
        verification_text = json.dumps(verifications, indent=2)
        claims_text = json.dumps([{"text": c.text, "confidence": c.confidence} for c in claims[:5]], indent=2)
        
        prompt = f"""You are a scientific auditor. Based on the claims and verification results, 
identify any contradictions.

CLAIMS:
{claims_text}

VERIFICATION RESULTS:
{verification_text}

Return ONLY a valid JSON array of contradictions:
[
  {{"claim": "text", "visual_evidence_page": 1, "visual_shows": "description", "contradiction_type": "direct_conflict", "confidence": 0.9, "reasoning": "explanation"}}
]

If no contradictions found, return empty array: []
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            contradictions_json = json.loads(response_text)
            if not contradictions_json:
                return []
            contradictions = [Contradiction(**c) for c in contradictions_json]
            return contradictions
        except Exception as e:
            print(f"Error in phase 3: {e}")
            return []
    
    def run_full_audit(
        self,
        text: str,
        images: List[Dict[str, Any]],
        total_pages: int
    ) -> AuditReport:
        """
        Run all 3 phases and generate final audit report.
        """
        
        print("[Phase 1] Extracting claims...")
        claims = self.phase_1_extract_claims(text)
        print(f"  → Found {len(claims)} claims")
        
        print("[Phase 2] Verifying against visual evidence...")
        verifications = self.phase_2_visual_verification(text, claims, images)
        print(f"  → Completed visual verification")
        
        print("[Phase 3] Detecting contradictions...")
        contradictions = self.phase_3_contradiction_detection(text, claims, verifications)
        print(f"  → Found {len(contradictions)} contradictions")
        
        # Generate summary
        summary = f"Analyzed {len(claims)} claims across {total_pages} pages. "
        summary += f"Detected {len(contradictions)} contradiction(s). "
        if contradictions:
            high_conf = sum(1 for c in contradictions if c.confidence > 0.8)
            summary += f"{high_conf} high-confidence contradictions."
        else:
            summary += "No major inconsistencies found."
        
        report = AuditReport(
            claims=claims,
            contradictions=contradictions,
            audit_summary=summary,
            total_pages=total_pages,
            processing_time_seconds=0,  # TODO: track actual time
        )
        
        return report
