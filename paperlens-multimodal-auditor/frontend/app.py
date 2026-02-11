"""
Streamlit Frontend for PaperLens
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="PaperLens",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { padding: 2rem; }
    .header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; }
    .subheader { font-size: 1.2rem; color: #666; }
    .success { color: #28a745; font-weight: bold; }
    .error { color: #dc3545; font-weight: bold; }
    .warning { color: #ff9800; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">🔍 PaperLens</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Multimodal Contradiction Detector</div>', unsafe_allow_html=True)
st.markdown("Detect hallucinations and inconsistencies in research papers using Gemini 3's multimodal reasoning.")

st.divider()

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **PaperLens** uses Gemini 3 to:
    1. Extract claims from paper text
    2. Cross-reference against figures & tables
    3. Detect contradictions automatically
    
    **Features:**
    - 3-phase reasoning pipeline
    - Multimodal (text + images)
    - Explainable results
    - JSON-structured reports
    """)
    
    st.divider()
    
    api_url = st.text_input(
        "Backend URL",
        value="http://127.0.0.1:8000",
        help="FastAPI backend endpoint"
    )
    
    st.divider()
    
    st.markdown("""
    **Gemini 3 Features Used:**
    - `thinking_level: high` for deep reasoning
    - `media_resolution: high` for charts
    - Structured outputs (JSON schema)
    - Multimodal input (text + images)
    """)

# Initialize session state for file uploads
if 'uploaded_file_data' not in st.session_state:
    st.session_state.uploaded_file_data = None
    st.session_state.uploaded_file_name = None

# Main section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Paper")
    
    st.markdown("""
    **Workaround for Codespaces:** Due to Streamlit upload issues in dev containers, 
    please upload your PDF to the `uploads` folder and enter the filename below.
    """)
    
    # Option 1: Direct file path input (workaround)
    use_file_path = st.checkbox("Use file path instead of uploader", value=True)
    
    if use_file_path:
        file_path = st.text_input(
            "PDF filename (in uploads folder)",
            value="AstroPhysics.pdf",
            help="Just the filename - we'll look in the uploads folder"
        )
        
        if file_path and st.button("Load File", type="primary"):
            import os
            full_path = f"/workspaces/gemini-hackathon/paperlens-multimodal-auditor/uploads/{file_path}"
            if os.path.exists(full_path):
                with open(full_path, 'rb') as f:
                    pdf_data = f.read()
                st.session_state.uploaded_file_data = pdf_data
                st.session_state.uploaded_file_name = os.path.basename(full_path)
                st.success(f"✅ Loaded {len(pdf_data)} bytes from {file_path}")
            else:
                st.error(f"❌ File not found: {full_path}")
                st.error(f"Please upload your PDF to the 'uploads' folder in the workspace")
    else:
        # Original uploader (may fail in Codespaces)
        st.warning("⚠️ File uploader may fail in Codespaces. Use file path option above.")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload a research paper in PDF format"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file_data = uploaded_file.read()
            st.session_state.uploaded_file_name = uploaded_file.name

with col2:
    st.subheader("📊 Status")
    status_placeholder = st.empty()

# Process uploaded file
if st.session_state.uploaded_file_data is not None:
    st.divider()
    
    # Show file info
    st.write(f"**File:** {st.session_state.uploaded_file_name}")
    st.write(f"**Size:** {len(st.session_state.uploaded_file_data) / 1024:.1f} KB")
    
    # Debug: Show backend URL
    st.caption(f"Backend: {api_url}")
    
    if len(st.session_state.uploaded_file_data) > 200 * 1024 * 1024:
        st.warning("File is larger than 200MB and may fail to upload. Try a smaller PDF.")
    
    # Process button
    if st.button("🚀 Run Audit", use_container_width=True, type="primary"):
        status_placeholder.info("⏳ Processing... this may take 30-60 seconds")
        
        try:
            # Send to backend using direct Python request (bypasses Streamlit's Axios client)
            st.write("📡 Reading file...")
            pdf_bytes = st.session_state.uploaded_file_data
            st.write(f"✅ File read: {len(pdf_bytes)} bytes")
            
            st.write("📡 Sending to backend...")
            files = {"file": (st.session_state.uploaded_file_name, pdf_bytes, "application/pdf")}
            response = requests.post(
                f"{api_url}/api/audit",
                files=files,
                timeout=120,
                headers={"User-Agent": "PaperLens/1.0"}
            )
            st.write(f"✅ Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if result["status"] == "success":
                    status_placeholder.success("✅ Audit Complete")
                    
                    audit = result["audit_report"]
                    
                    # Summary section
                    st.subheader("📋 Audit Summary")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Claims", len(audit["claims"]))
                    with col2:
                        st.metric("Contradictions Found", len(audit["contradictions"]))
                    with col3:
                        st.metric("Processing Time", f"{audit['processing_time_seconds']:.1f}s")
                    
                    st.info(audit["audit_summary"])
                    
                    st.divider()
                    
                    # Claims section
                    if audit["claims"]:
                        st.subheader("💡 Extracted Claims")
                        
                        for i, claim in enumerate(audit["claims"], 1):
                            with st.expander(f"Claim {i} - {claim['text'][:60]}..."):
                                st.write(f"**Text:** {claim['text']}")
                                st.write(f"**Confidence:** {claim['confidence']:.1%}")
                                st.write(f"**Type:** {claim['evidence_type']}")
                                st.write(f"**Page:** {claim['page']}")
                    
                    st.divider()
                    
                    # Contradictions section
                    if audit["contradictions"]:
                        st.subheader("⚠️ Detected Contradictions")
                        
                        for i, contradiction in enumerate(audit["contradictions"], 1):
                            with st.expander(
                                f"Contradiction {i} - {contradiction['contradiction_type'].replace('_', ' ').title()}",
                                expanded=True
                            ):
                                st.write(f"**Claim:** {contradiction['claim']}")
                                st.write(f"**Page with Visual Evidence:** {contradiction['visual_evidence_page']}")
                                st.write(f"**Visual Shows:** {contradiction['visual_shows']}")
                                st.write(f"**Confidence:** {contradiction['confidence']:.1%}")
                                
                                if contradiction.get("reasoning"):
                                    st.write(f"**Reasoning:** {contradiction['reasoning']}")
                    else:
                        st.success("✅ No contradictions detected! Paper is consistent.")
                    
                    st.divider()
                    
                    # Raw JSON export
                    st.subheader("📥 Raw Report (JSON)")
                    st.json(audit)
                    
                    # Download button
                    st.download_button(
                        "Download Report",
                        json.dumps(audit, indent=2),
                        file_name=f"paperlens_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                else:
                    status_placeholder.error("❌ Audit Failed")
                    st.error(f"Error: {result.get('error_details', 'Unknown error')}")
            
            else:
                status_placeholder.error("❌ Server Error")
                error_text = response.text.strip() or "(no response body)"
                st.error(f"Status code: {response.status_code}")
                st.code(error_text)
        
        except requests.exceptions.ConnectionError as e:
            status_placeholder.error(f"❌ Cannot connect to backend")
            st.error(f"Make sure the backend is running at {api_url}")
            st.error(f"Connection error details: {str(e)}")
        except requests.exceptions.RequestException as e:
            status_placeholder.error(f"❌ Request Error")
            st.error(f"Request failed: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
        except Exception as e:
            status_placeholder.error(f"❌ Error: {str(e)}")
            st.error(f"Unexpected error: {e}")
            st.error(f"Error type: {type(e).__name__}")

else:
    st.info("👆 Upload a PDF to get started")
    
    # Example usage
    st.divider()
    st.subheader("📚 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Phase 1: Claim Extraction**
        - Gemini 3 Flash (`thinking_level: low`)
        - Extract quantitative claims
        - Fast + cost-efficient
        """)
    
    with col2:
        st.markdown("""
        **Phase 2: Visual Verification**
        - Gemini 3 Pro (`thinking_level: high`)
        - Cross-reference with figures
        - High-res image analysis
        """)
    
    with col3:
        st.markdown("""
        **Phase 3: Contradiction Detection**
        - Gemini 3 Pro (structured outputs)
        - Flag inconsistencies
        - Confidence scoring
        """)
