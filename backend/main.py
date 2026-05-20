from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
import os
import sys

# Add project root to sys path to import core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.predict import CarbonPredictor
import json

app = FastAPI(title="Carbon Footprint Tracker API")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = CarbonPredictor()
OPTIONS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core', 'options.json')
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')

class PredictionRequest(BaseModel):
    features: Dict[str, Any]

@app.get("/api/options")
def get_options():
    try:
        with open(OPTIONS_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict")
def predict_footprint(req: PredictionRequest):
    try:
        footprint = predictor.predict(req.features)
        return {"carbon_emission_kg": float(footprint)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount frontend
from fastapi.staticfiles import StaticFiles

# Create frontend dir check just in case it doesn't exist yet but we'll add files later
os.makedirs(FRONTEND_DIR, exist_ok=True)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
