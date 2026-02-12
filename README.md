# gemini-hackathon

## Getting started

### 1) Open the project
```bash
cd /workspaces/gemini-hackathon/paperlens-multimodal-auditor
```

### 2) Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 4) Configure the API key
Create a file at backend/.env with:
```
GOOGLE_API_KEY=your_key_here
```

### 5) Run the app (RECOMMENDED - auto-launches both servers)
```bash
cd /workspaces/gemini-hackathon/paperlens-multimodal-auditor
./launch.sh
```

This script automatically:
- Activates the virtual environment
- Starts the backend on port 8000
- Starts the frontend on port 8501 with proper configuration
- Fixes the upload 403 error by disabling XSRF protection

**OR run manually:**

### 5a) Run the backend (Terminal 1)
```bash
cd backend
python main.py
```
Backend runs on http://localhost:8000

### 6) Run the frontend (Terminal 2)
```bash
cd frontend
python -m streamlit run app.py --server.enableXsrfProtection false --server.enableCORS false
```
Frontend runs on http://localhost:8501

**IMPORTANT:** The `--server.enableXsrfProtection false` flag is required to fix the "403 Forbidden" error when uploading files in Codespaces.

### 7) If you are using a dev container
Your browser is outside the container, so the frontend must call the backend using the external forwarded URL.

In the Streamlit sidebar, change “Backend URL” from:
```
http://localhost:8000
```
to:
```
http://<EXTERNAL_IP>:8000
```

The frontend URL shown in the terminal looks like:
```
External URL: http://<EXTERNAL_IP>:8501
```
Use the same <EXTERNAL_IP> for the backend URL.

### 8) Quick health check (optional)
```bash
curl http://localhost:8000/health
```

If you see a JSON response, the backend is working.
