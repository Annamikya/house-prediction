from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import os

# Create FastAPI app
app = FastAPI(title="House Price Prediction API")

# Allow CORS (development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base dir for artifacts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lazy-loaded artifacts
MODEL = None
PREPROCESSOR = None


def load_artifacts():
    global MODEL, PREPROCESSOR
    if MODEL is None or PREPROCESSOR is None:
        model_path = os.path.join(BASE_DIR, "artifacts", "model.pkl")
        preproc_path = os.path.join(BASE_DIR, "artifacts", "preprocessor.pkl")
        if not os.path.exists(model_path) or not os.path.exists(preproc_path):
            raise FileNotFoundError("Model or preprocessor not found. Place them under backend/artifacts/")
        MODEL = joblib.load(model_path)
        PREPROCESSOR = joblib.load(preproc_path)


@app.get("/health")
def health_check():
    # Report whether artifacts are available
    artifacts_available = os.path.exists(os.path.join(BASE_DIR, "artifacts", "model.pkl")) and os.path.exists(os.path.join(BASE_DIR, "artifacts", "preprocessor.pkl"))
    return {"status": "Backend is running", "artifacts_available": artifacts_available}


@app.post("/predict")
def predict(data: dict):
    """
    Takes JSON input from frontend,
    preprocesses it,
    returns predicted house price
    """
    try:
        load_artifacts()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model/preprocessor: {e}")

    df = pd.DataFrame([data])
    try:
        processed_data = PREPROCESSOR.transform(df)
        prediction = MODEL.predict(processed_data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return {"predicted_price": float(prediction)}

