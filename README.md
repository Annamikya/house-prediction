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

Quick start:

1. Create a Python virtual environment and install backend dependencies:

   python -m venv venv
   venv\Scripts\activate
   pip install -r backend/requirements.txt

2. Run the backend (from project root):

   uvicorn backend.app.main:app --reload --port 8000

3. Open `frontend/index.html` in your browser or serve it from a static host.

Replace the placeholder pickles in `backend/artifacts/` with your trained model and preprocessor.
