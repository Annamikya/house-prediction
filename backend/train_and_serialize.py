"""Train a minimal model using `train.csv` and write artifacts to `backend/artifacts/`.

Usage:
  cd backend
  & 'C:/Users/Annamikya/OneDrive/Desktop/house_price_app/.venv/Scripts/python.exe' train_and_serialize.py

This script trains a simple LinearRegression on GrLivArea and TotRmsAbvGrd
and saves two files: model.pkl and preprocessor.pkl (joblib).
"""
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_CSV = os.path.abspath(os.path.join(BASE_DIR, '..', 'train.csv'))
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'artifacts')
MODEL_PATH = os.path.join(ARTIFACTS_DIR, 'model.pkl')
PREPROC_PATH = os.path.join(ARTIFACTS_DIR, 'preprocessor.pkl')

print('train csv:', TRAIN_CSV)
if not os.path.exists(TRAIN_CSV):
    raise SystemExit('train.csv not found: put the dataset at the repository root')

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

df = pd.read_csv(TRAIN_CSV)
# Select small set of features used by the frontend
features = ['GrLivArea', 'TotRmsAbvGrd']
target = 'SalePrice'

# Drop rows missing target
df = df[[*features, target]].copy()
df = df.dropna(subset=[target])

X = df[features]
y = df[target]

# Preprocessing + model
preprocessor = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

X_proc = preprocessor.fit_transform(X)
model = LinearRegression()
model.fit(X_proc, y)

# Save artifacts
joblib.dump(model, MODEL_PATH)
joblib.dump(preprocessor, PREPROC_PATH)

print('Wrote model ->', MODEL_PATH, 'size:', os.path.getsize(MODEL_PATH))
print('Wrote preprocessor ->', PREPROC_PATH, 'size:', os.path.getsize(PREPROC_PATH))
print('\nDone. Now restart the backend and retry /predict')