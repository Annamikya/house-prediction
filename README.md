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

3. Open `frontend/index.html` in your browser or serve it from a static host.

Replace the placeholder pickles in `backend/artifacts/` with your trained model and preprocessor.

## Deployment on Render

### Backend (Web Service)

1. Create a new **Web Service** on Render.
2. Connect your GitHub repo.
3. Set **Root Directory** to `backend`.
4. Set **Build Command** to:
   pip install -r requirements.txt
5. Set **Start Command** to:
   gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
6. Ensure `backend/artifacts/model.pkl` and `backend/artifacts/preprocessor.pkl` are committed to the repo (or add a download step in the build command if stored elsewhere).
7. Deploy. Note the public URL (e.g., `https://your-backend.onrender.com`).

### Frontend (Static Site)

1. Create a new **Static Site** on Render.
2. Connect your GitHub repo.
3. Set **Root Directory** to `frontend`.
4. Add an **Environment Variable** (critical — this fixes "Backend unreachable"):
   - Key: `BACKEND_URL`
   - Value: `https://your-backend.onrender.com` (replace with your backend's URL from above; must be HTTPS)
5. Set **Build Command** to:
   echo "const BACKEND_URL='${BACKEND_URL}';" > backend-config.js
6. Set **Publish Directory** to `/` (default).
7. Deploy.

**Important**: If you skip setting `BACKEND_URL`, the frontend will default to `http://127.0.0.1:8000`, causing "Backend unreachable" since localhost isn't accessible from Render.

After both are deployed, visit the Static Site URL. The frontend should connect to the backend and work end-to-end.

### Troubleshooting

- If you see "Backend unreachable", ensure `BACKEND_URL` is set correctly in the Static Site and the backend is running.
- Check Render logs for both services.
- For mixed content errors, ensure `BACKEND_URL` uses `https://`.

