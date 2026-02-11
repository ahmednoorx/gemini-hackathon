# 📚 PAPERLENS — COMPLETE FILE INDEX

Everything you need is here. Start with the files marked **[READ FIRST]**.

---

## 🚀 START HERE

| File | Purpose | Read Time |
|------|---------|-----------|
| **[START_HERE.md](START_HERE.md)** | Quick overview of the project and what you're getting | 3 min |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Step-by-step setup guide (5 steps, ~15 min) | 5 min |
| **[README.md](README.md)** | Full project documentation | 5 min |

---

## 💻 BACKEND (FastAPI + Gemini 3)

Run these to get your API server running.

| File | Purpose | Status |
|------|---------|--------|
| `backend/main.py` | FastAPI entry point - **RUN THIS FIRST** | ✅ Ready |
| `backend/gemini_auditor.py` | 3-phase Gemini 3 pipeline (CORE LOGIC) | ✅ Ready |
| `backend/ingestion.py` | PDF text + image extraction | ✅ Ready |
| `backend/models.py` | Pydantic data schemas | ✅ Ready |
| `backend/requirements.txt` | Python dependencies | ✅ Ready |
| `backend/.env.example` | Template for environment variables | ✅ Copy to .env |

**To run:**
```bash
cd backend
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY
python main.py
```

---

## 🎨 FRONTEND (Streamlit UI)

Beautiful, interactive interface for uploading PDFs and viewing results.

| File | Purpose | Status |
|------|---------|--------|
| `frontend/app.py` | Streamlit UI app - **RUN THIS SECOND** | ✅ Ready |
| `frontend/requirements.txt` | Python dependencies | ✅ Ready |

**To run:**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

**Access at:** http://localhost:8501

---

## 📖 DOCUMENTATION (Read for understanding)

| File | Purpose | When to Read | Priority |
|------|---------|--------------|----------|
| `docs/architecture.md` | System design with diagrams + Gemini 3 details | Want to understand how it works | High |
| `docs/gemini3_api_guide.md` | Gemini 3 API reference, models, thinking levels | Need API implementation details | Medium |
| `docs/demo_script.md` | Word-for-word 3-minute video script | Recording your demo video | High |
| `docs/devpost_submission.md` | Devpost form template + 200-word write-up | Submitting to Devpost | Critical |

---

## 📊 SAMPLE DATA

| File | Purpose |
|------|---------|
| `sample_data/expected_output.json` | Example audit report (what output looks like) |

---

## 🛠️ UTILITIES

| File | Purpose |
|------|---------|
| `setup.sh` | Bash script to auto-install everything (optional) |

---

## 🎯 QUICK REFERENCE

### I want to...

**...get the system running**
1. Read: [START_HERE.md](START_HERE.md)
2. Follow: [GETTING_STARTED.md](GETTING_STARTED.md)
3. Run: `backend/main.py` + `frontend/app.py`

**...understand the architecture**
1. Read: [docs/architecture.md](docs/architecture.md)
2. Reference: [docs/gemini3_api_guide.md](docs/gemini3_api_guide.md)

**...record a demo video**
1. Follow: [docs/demo_script.md](docs/demo_script.md) (word-for-word script)
2. Record: 3 minutes max
3. Upload: YouTube (unlisted)

**...submit to Devpost**
1. Copy: 200-word description from [docs/devpost_submission.md](docs/devpost_submission.md)
2. Fill form with all fields
3. Add links: GitHub repo, demo video, live app
4. Submit!

**...fix errors**
1. Check: [GETTING_STARTED.md](GETTING_STARTED.md) troubleshooting section
2. Read: Backend console output
3. Reference: [docs/gemini3_api_guide.md](docs/gemini3_api_guide.md) for API issues

---

## 📋 ALL FILES AT A GLANCE

```
paperlens-multimodal-auditor/
│
├── START_HERE.md                   ← Project overview & checklist
├── GETTING_STARTED.md              ← Step-by-step setup (READ THIS)
├── README.md                       ← Full documentation
├── FILE_INDEX.md                   ← This file
├── setup.sh                        ← Auto-setup script (optional)
│
├── backend/
│   ├── main.py                     ← RUN: python main.py
│   ├── gemini_auditor.py           ← 3-phase pipeline
│   ├── ingestion.py                ← PDF extraction
│   ├── models.py                   ← Data schemas
│   ├── requirements.txt
│   └── .env.example                ← Copy to .env
│
├── frontend/
│   ├── app.py                      ← RUN: streamlit run app.py
│   └── requirements.txt
│
├── docs/
│   ├── architecture.md             ← System design (READ THIS)
│   ├── gemini3_api_guide.md        ← API reference
│   ├── demo_script.md              ← Video script (READ THIS)
│   └── devpost_submission.md       ← Devpost template (READ THIS)
│
└── sample_data/
    └── expected_output.json        ← Example output
```

---

## ⏱️ RECOMMENDED READING ORDER

For someone brand new (estimated time: 25 minutes):

1. **[START_HERE.md](START_HERE.md)** (3 min) - Quick overview
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** (5 min) - Setup steps
3. **Try it** (5 min) - Run backend + frontend
4. **[docs/architecture.md](docs/architecture.md)** (5 min) - How it works
5. **[docs/devpost_submission.md](docs/devpost_submission.md)** (5 min) - What to submit
6. **[docs/demo_script.md](docs/demo_script.md)** (2 min) - Video demo

After reading/doing this, you'll be 90% ready to submit.

---

## 🚨 CRITICAL FILES TO NOT SKIP

| File | Why |
|------|-----|
| `backend/.env.example` | You MUST copy to `.env` and add your API key |
| `docs/devpost_submission.md` | Contains the 200-word description for Devpost |
| `docs/demo_script.md` | Script for recording your demo video |
| `README.md` | Goes in GitHub repo (judges will read it) |

---

## ✅ BEFORE YOU SUBMIT

Make sure you've:
- [ ] Read [START_HERE.md](START_HERE.md)
- [ ] Followed [GETTING_STARTED.md](GETTING_STARTED.md)
- [ ] Tested backend + frontend
- [ ] Read [docs/architecture.md](docs/architecture.md)
- [ ] Used [docs/demo_script.md](docs/demo_script.md) for your video
- [ ] Filled Devpost form using [docs/devpost_submission.md](docs/devpost_submission.md)

---

## 📞 HELP

- **Setup questions?** → [GETTING_STARTED.md - Troubleshooting](GETTING_STARTED.md#-troubleshooting)
- **How does it work?** → [docs/architecture.md](docs/architecture.md)
- **API questions?** → [docs/gemini3_api_guide.md](docs/gemini3_api_guide.md)
- **Video script?** → [docs/demo_script.md](docs/demo_script.md)
- **Devpost help?** → [docs/devpost_submission.md](docs/devpost_submission.md)

---

## 🎯 YOUR MISSION

1. **Setup** (15 min) - Follow [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Test** (10 min) - Upload a PDF and verify results
3. **Demo** (30 min) - Record 3-minute video using [docs/demo_script.md](docs/demo_script.md)
4. **Deploy** (20 min) - Push to GitHub, deploy to Streamlit Cloud
5. **Submit** (10 min) - Fill Devpost form using [docs/devpost_submission.md](docs/devpost_submission.md)

**Total: ~85 minutes. You can do this!** 🚀

---

*Last updated: Feb 3, 2026*  
*Deadline: Feb 10, 2026 @ 6:00pm PST*  
*Time remaining: ~7 days*
