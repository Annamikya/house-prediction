# House Price App

Project skeleton for a house price predictor.

Structure:

- backend/
  - app/main.py  (FastAPI app)
  - artifacts/   (place your model.pkl and preprocessor.pkl here)
  - requirements.txt

- frontend/
  - index.html
  - style.css
  - script.js

## Quick start (local development):

1. Create a Python virtual environment and install backend dependencies:

   python -m venv venv
   venv\Scripts\activate
   pip install -r backend/requirements.txt

2. Run the backend (from project root):

   uvicorn backend.app.main:app --reload --port 8000

3. Set the backend URL for frontend (replace with your deployed backend URL if testing remotely):

   cd frontend
   python set_backend_url.py http://127.0.0.1:8000

4. Open `frontend/index.html` in your browser or serve it from a static host.

Replace the placeholder pickles in `backend/artifacts/` with your trained model and preprocessor.

## Deployment on Render

**Critical**: You must deploy the backend **before** the frontend. The frontend needs the backend URL to work. If you see "Backend unreachable" with localhost, the backend isn't deployed or BACKEND_URL isn't set.

### Backend (Web Service)

1. Create a new **Web Service** on Render (separate from your Static Site).
2. Connect your GitHub repo.
3. Set **Root Directory** to `backend`.
4. Set **Build Command** to:
   pip install -r requirements.txt
5. Set **Start Command** to (choose one):
   - Recommended: `gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - If gunicorn fails: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Ensure `backend/artifacts/model.pkl` and `backend/artifacts/preprocessor.pkl` are committed.
7. Deploy. Note the public URL (e.g., `https://your-backend.onrender.com`).

### Frontend (Static Site)

1. Create a new **Static Site** on Render.
2. Connect your GitHub repo.
3. Set **Root Directory** to `frontend`.
4. **Add Environment Variable** (this is required — without it, frontend uses localhost):
   - Key: `BACKEND_URL`
   - Value: `https://your-backend.onrender.com` (from step 7 above; must be HTTPS)
5. Set **Build Command** to:
   echo "const BACKEND_URL='${BACKEND_URL}';" > backend-config.js
6. Set **Publish Directory** to `/`.
7. Deploy.

**If still not working**: Check Render Static Site logs — the build command should output the echo. If BACKEND_URL is empty, re-check the env var.

After both are deployed, visit the Static Site URL. The frontend should connect to the backend and work end-to-end.

### Troubleshooting

- If you see "Backend unreachable", ensure `BACKEND_URL` is set correctly in the Static Site and the backend is running.
- Check Render logs for both services.
- For mixed content errors, ensure `BACKEND_URL` uses `https://`.

