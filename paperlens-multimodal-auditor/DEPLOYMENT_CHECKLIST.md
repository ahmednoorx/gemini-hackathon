# ✅ PaperLens Deployment Checklist

Use this before sharing your project with anyone.

---

## 🔐 Security & Configuration

- [ ] Check `.env` is in `.gitignore`
  ```bash
  echo "backend/.env" >> .gitignore
  ```

- [ ] Remove any hardcoded API keys
  ```bash
  grep -r "AIzaSy" --include="*.py"  # Should be empty
  ```

- [ ] CORS is configured (already done)
  ```bash
  # Check: .streamlit/config.toml has enableCORS = false
  ```

---

## 🧪 Testing

- [ ] Run health check
  ```bash
  bash health-check.sh
  # Should show all ✅
  ```

- [ ] Backend starts successfully
  ```bash
  cd backend && python main.py
  # Expected: ✅ Gemini 3 Auditor initialized
  ```

- [ ] Frontend UI loads
  ```bash
  cd frontend && streamlit run app.py --server.address 0.0.0.0
  # Expected: You can open http://localhost:8501
  ```

- [ ] File upload works
  ```bash
  # Upload any PDF, wait for results
  # Expected: JSON report with claims & contradictions
  ```

- [ ] Error handling works
  ```bash
  # Upload non-PDF file (e.g., .txt)
  # Expected: Graceful error message
  ```

---

## 📚 Documentation Ready

- [ ] README.md looks professional
  ```bash
  # Check: README has badges, clear instructions, architecture diagram
  ```

- [ ] docs/architecture.md explains the system
  ```bash
  # Check: System overview, phase descriptions, API endpoints
  ```

- [ ] PORTFOLIO_GUIDE.md is present
  ```bash
  # Check: Interview prep, hiring talking points
  ```

- [ ] ACTION_PLAN.md guides next steps
  ```bash
  # Check: Priorities, GitHub setup, interview strategy
  ```

---

## 🚀 GitHub Ready

If pushing to public GitHub:

- [ ] Remove test files
  ```bash
  rm -rf __pycache__ .pytest_cache *.pyc
  ```

- [ ] Create `.gitignore`
  ```bash
  echo -e "*.pyc\n__pycache__/\n.env\n.DS_Store\n.venv/" >> .gitignore
  ```

- [ ] Add LICENSE
  ```bash
  echo "MIT License - See LICENSE file" > LICENSE
  ```

- [ ] Set repo description
  ```
  "Multimodal contradiction detector using Gemini 3"
  ```

- [ ] Add topics
  ```
  gemini-3, multimodal, ai, fastapi, streamlit, python
  ```

- [ ] Create initial commit
  ```bash
  git add .
  git commit -m "feat: PaperLens - Gemini 3 multimodal auditor"
  git push origin main
  ```

---

## 🎓 Interview Preparation

- [ ] Memorize 3-phase pipeline
  ```
  Phase 1: Claim extraction (Flash, thinking_level: low)
  Phase 2: Visual verification (Pro, thinking_level: high)
  Phase 3: Contradiction detection (Pro, structured output)
  ```

- [ ] Know why Gemini 3
  ```
  Single transformer for multimodal fusion
  Thinking control for variable reasoning depth
  Media resolution for chart accuracy
  Structured outputs prevent hallucinations
  ```

- [ ] Can explain the architecture in 2 minutes
  ```
  PDF input → Text + image extraction → 3-phase pipeline → JSON report
  ```

- [ ] Have answers ready for:
  - [ ] "Why not GPT-4 Vision?"
  - [ ] "How would you scale this?"
  - [ ] "What's your cost optimization?"
  - [ ] "What would you add next?"

---

## 📊 Portfolio Integration

- [ ] GitHub repo is public
  ```bash
  # Check: https://github.com/YOUR_USER/paperlens accessible
  ```

- [ ] README displays well on GitHub
  ```bash
  # Check: Badges render, code blocks format properly
  ```

- [ ] Portfolio website links to repo
  ```html
  <a href="https://github.com/YOUR_USER/paperlens">
    PaperLens
  </a>
  ```

- [ ] LinkedIn mentions Gemini 3 + multimodal
  ```
  Profile includes: "Built PaperLens, a multimodal auditor using Gemini 3..."
  ```

---

## 🎯 Demo Readiness

- [ ] Can run the app in under 2 minutes
  ```bash
  # Step 1: API key setup (already done if .env exists)
  # Step 2: Start backend
  # Step 3: Start frontend
  # Step 4: Upload PDF
  ```

- [ ] Have a sample PDF ready
  ```bash
  # Prepare a PDF with obvious text-figure contradiction
  # Put in uploads/ folder for quick demo
  ```

- [ ] Can explain results in plain English
  ```
  "This claim says X increased 20%, but Figure 2 shows it decreased. 
   The system flagged this contradiction with 88% confidence."
  ```

- [ ] Screenshot successful run
  ```bash
  # Take screenshot of final audit report for portfolio
  ```

---

## 🔍 Final Pre-Share Checks

Before sending to anyone, verify:

```bash
# 1. Sanitize code
grep -r "test_key" --include="*.py"     # Should find nothing
grep -r "hardcoded" --include="*.py"    # Should find nothing

# 2. Verify file structure
ls -la backend/ frontend/ docs/ .streamlit/

# 3. Check Python version
python3 --version  # Should be 3.10+

# 4. Spot check imports
python3 -c "import fastapi; import google.genai; import streamlit"

# 5. Verify no debug code
grep -r "TODO\|FIXME\|HACK" --include="*.py" backend/ frontend/
```

---

## 🚨 Emergency Troubleshooting

**If backend won't start:**
```bash
# Check API key
. backend/.env && echo $GOOGLE_API_KEY

# Test Gemini connection
python3 -c "from google import genai; genai.Client(api_key='TEST')"
```

**If Streamlit upload fails:**
```bash
# Check config
cat .streamlit/config.toml  # Should have enableCORS = false

# Restart Streamlit
# Ctrl+C and re-run with:
streamlit run app.py --server.address 0.0.0.0 --logger.level=debug
```

**If results are wrong:**
```bash
# Check backend logs
# Backend shows full request/response for debugging
```

---

## ✨ Final Polish

- [ ] Edit `.streamlit/config.toml` if needed
- [ ] Remove any print debugging
- [ ] Add docstrings to key functions
- [ ] Ensure all imports are used
- [ ] Check for type hints on critical functions

---

## 🎉 You're Ready When

✅ Health check passes  
✅ Local demo works end-to-end  
✅ GitHub repo is public  
✅ README looks professional  
✅ You can talk about it confidently  

**Then:** Share with recruiters, GitHub communities, and interviews.

---

**Status: Ready for Deployment** ✅

Use this checklist before EVERY public demo. Small details matter.

