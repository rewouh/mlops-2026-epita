from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import joblib
import numpy as np
from eurybia import SmartDrift
from pathlib import Path
import json
from datetime import datetime

app = FastAPI(
    title="house price detection with drift detection",
    description="explicit",
    version="1.0.0"
)

MODEL_PATH = Path("../data/regression.joblib")
TRAIN_DATA_PATH = Path("../data/houses.csv")
PROD_DATA_PATH = Path("production_data.csv")

model = joblib.load(MODEL_PATH)
df_train = pd.read_csv(TRAIN_DATA_PATH)

class HouseFeatures(BaseModel):
    size: float
    nb_rooms: int
    garden: int
    orientation: str

class PredictionResponse(BaseModel):
    prediction: float
    features: Dict[str, Any]
    timestamp: str
    message: str

class DriftDetectionResponse(BaseModel):
    drift_detected: bool
    auc_score: float
    n_train_samples: int
    n_prod_samples: int
    message: str
    details: Dict[str, Any]

def preprocess_features(features: HouseFeatures) -> pd.DataFrame:
    data = {
        'size': [features.size],
        'nb_rooms': [features.nb_rooms],
        'garden': [features.garden],
        'orientation': [features.orientation]
    }
    df = pd.DataFrame(data)
    return df


def save_production_data(features: HouseFeatures):
    data = {
        'size': features.size,
        'nb_rooms': features.nb_rooms,
        'garden': features.garden,
        'orientation': features.orientation,
        'timestamp': datetime.now().isoformat()
    }
    
    df_new = pd.DataFrame([data])
    
    if PROD_DATA_PATH.exists():
        df_existing = pd.read_csv(PROD_DATA_PATH)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(PROD_DATA_PATH, index=False)
    else:
        df_new.to_csv(PROD_DATA_PATH, index=False)
    
    print(f"Production data saved (total: {len(pd.read_csv(PROD_DATA_PATH))} samples)")


@app.post("/predict", response_model=PredictionResponse)
def predict(features: HouseFeatures):
    try:
        df_input = preprocess_features(features)
        prediction = model.predict(df_input)[0]
        
        save_production_data(features)
        
        return PredictionResponse(
            prediction=float(prediction),
            features=features.dict(),
            timestamp=datetime.now().isoformat(),
            message="Prediction success, data stored for drift detection."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/detect-drift", response_model=DriftDetectionResponse)
def detect_drift(threshold: float = 0.6):
    if not PROD_DATA_PATH.exists():
        raise HTTPException(
            status_code=404, 
            detail="No data vailable, make predictions first using /predict endpoint."
        )
    
    try:
        df_prod = pd.read_csv(PROD_DATA_PATH)
        if 'timestamp' in df_prod.columns:
            df_prod = df_prod.drop(columns=['timestamp'])
        
        if len(df_prod) < 10:
            return DriftDetectionResponse(
                drift_detected=False,
                auc_score=0.5,
                n_train_samples=len(df_train),
                n_prod_samples=len(df_prod),
                message=f"Insufficient production data for drift detection (need at least 10, got {len(df_prod)})",
                details={"status": "insufficient_data"}
            )
        
        df_baseline = df_train.drop(columns=['price']) if 'price' in df_train.columns else df_train
        
        smd = SmartDrift(
            df_current=df_prod,
            df_baseline=df_baseline,
        )
        
        smd.compile()
        auc_score = smd.auc if hasattr(smd, 'auc') else 0.5
        drift_detected = auc_score > threshold
        
        details = {
            "auc_score": float(auc_score),
            "threshold": threshold,
            "drift_status": "DRIFT DETECTED" if drift_detected else "No drift",
        }
        
        return DriftDetectionResponse(
            drift_detected=drift_detected,
            auc_score=float(auc_score),
            n_train_samples=len(df_baseline),
            n_prod_samples=len(df_prod),
            message=(
                f"DATA DRIFT. AUC={auc_score:.3f} > {threshold}" 
                if drift_detected 
                else f"No drift detected. AUC={auc_score:.3f} ≤ {threshold}"
            ),
            details=details
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drift detection error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print('Starting.')

    print(f"Model: {MODEL_PATH}")
    print(f"Training data: {TRAIN_DATA_PATH}")
    print(f"Production data: {PROD_DATA_PATH}")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
