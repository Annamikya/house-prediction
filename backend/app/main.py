from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import joblib
import os
import io
import matplotlib.pyplot as plt

# Create FastAPI app
app = FastAPI(title="House Price Prediction API")

# Allow CORS (development only)
# NOTE: set allow_credentials=False when using a wildcard origin to avoid CORS rejections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Small helper logging to make debugging easier
import logging
logger = logging.getLogger("uvicorn.error")

logger.debug("App initialized; CORS set (allow_origins='*')")

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
        try:
            MODEL = joblib.load(model_path)
            PREPROCESSOR = joblib.load(preproc_path)
        except Exception as e:
            import traceback
            traceback.print_exc()
            # Raise with repr so the HTTP response has a useful message for debugging
            raise Exception(repr(e))


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


@app.post("/plot")
def plot_image(data: dict):
    """Generates a matplotlib PNG showing the training price distribution with a vertical
    line for the predicted price (if training data available), or a single-bar plot otherwise."""
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

    # Try to load training data to plot distribution
    train_path = os.path.abspath(os.path.join(BASE_DIR, "..", "train.csv"))
    if os.path.exists(train_path):
        try:
            train = pd.read_csv(train_path)
            if "SalePrice" in train.columns:
                prices = train["SalePrice"].dropna()
                fig, ax = plt.subplots(figsize=(6,4))
                ax.hist(prices, bins=30, color="#4a90e2", alpha=0.75)
                ax.axvline(prediction, color="red", linewidth=2, label=f"Predicted: {prediction:.2f}")
                ax.set_xlabel("SalePrice")
                ax.set_ylabel("Frequency")
                ax.legend()
                ax.set_title("Price Distribution with Prediction")
            else:
                # fallback single bar
                fig, ax = plt.subplots(figsize=(4,3))
                ax.bar([0], [prediction], color="#4a90e2")
                ax.set_ylabel("Predicted Price")
                ax.set_xticks([])
                ax.set_title("Predicted Price")
        except Exception:
            fig, ax = plt.subplots(figsize=(4,3))
            ax.bar([0], [prediction], color="#4a90e2")
            ax.set_ylabel("Predicted Price")
            ax.set_xticks([])
            ax.set_title("Predicted Price")
    else:
        fig, ax = plt.subplots(figsize=(4,3))
        ax.bar([0], [prediction], color="#4a90e2")
        ax.set_ylabel("Predicted Price")
        ax.set_xticks([])
        ax.set_title("Predicted Price")

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# Serve frontend static files (if project has a sibling /frontend dir)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
if os.path.isdir(FRONTEND_DIR):
    logger.info(f"Mounting frontend static files from {FRONTEND_DIR}")
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

