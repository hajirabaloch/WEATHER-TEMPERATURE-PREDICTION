import os
import numpy as np
import joblib

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow.keras.models import load_model


# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# Load trained models
rnn_model = load_model(os.path.join(MODEL_DIR, "rnn_model.keras"))
lstm_model = load_model(os.path.join(MODEL_DIR, "lstm_model.keras"))
gru_model = load_model(os.path.join(MODEL_DIR, "gru_model.keras"))

# Load scaler
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))


# Create FastAPI app
app = FastAPI(title="Weather Temperature Prediction API")


# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input format
class PredictionInput(BaseModel):
    model_name: str
    temperatures: list[float]


@app.get("/")
def home():
    return {"message": "Weather Prediction API is running!"}


@app.post("/predict")
def predict(data: PredictionInput):

    if len(data.temperatures) != 30:
        raise HTTPException(
            status_code=400,
            detail="Please enter exactly 30 temperatures."
        )

    models = {
        "rnn": rnn_model,
        "lstm": lstm_model,
        "gru": gru_model
    }

    model_name = data.model_name.lower()

    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail="Choose RNN, LSTM, or GRU."
        )

    try:
        values = np.array(data.temperatures).reshape(-1, 1)

        scaled_values = scaler.transform(values)
        input_data = scaled_values.reshape(1, 30, 1)

        prediction = models[model_name].predict(
            input_data, verbose=0
        )

        predicted_temp = scaler.inverse_transform(
            prediction.reshape(-1, 1)
        )[0][0]

        return {
            "model": model_name.upper(),
            "predicted_temperature": round(float(predicted_temp), 2),
            "unit": "°C"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))