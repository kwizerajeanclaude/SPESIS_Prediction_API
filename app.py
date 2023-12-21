from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import uvicorn
import os

# call the app
app = FastAPI(title="SPESISS PREDICTION")

# Load the model and scaler
def load_model_and_scaler():
    with open("model/xgbmodel.joblib", "rb") as f1, open("model/encoder.joblib", "rb") as f2:
        return pickle.load(f1), pickle.load(f2)

model, scaler = load_model_and_scaler()

def predict(df, endpoint="simple"):
    # Scaling
    scaled_df = scaler.transform(df)

    # Prediction
    prediction = model.predict_proba(scaled_df)

    highest_proba = prediction.max(axis=1)

    predicted_labels = ["Patient does not have sepsis" if i == 0 else f"Patient has sepsis" for i in highest_proba]
    print(f"Predicted labels: {predicted_labels}")
    print(highest_proba)

    response = []
    for label, proba in zip(predicted_labels, highest_proba):
        output = {
            "prediction": label,
            "probability of prediction": str(round(proba * 100)) + '%'
        }
        response.append(output)

    return response


class Patient(BaseModel):
    PRG: int
    PL: int 
    PR: int 
    SK: int 
    TS: int
    M11: float 
    BD2: float
    Age: int 
    Insurance: int

class Patients(BaseModel):
    all_patients: list[Patient]

    @classmethod
    def return_list_of_dict(cls, patients: "Patients"):
        patient_list = []
        for patient in patients.all_patients:
            patient_dict = patient.dict()
            patient_list.append(patient_dict)
        return patient_list
    
# Endpoints
# Root Endpoint
@app.get("/")
def root():
    return {"API": "This is an API for sepsis prediction."}

# Prediction endpoint
@app.post("/predict")
def predict_sepsis(patient: Patient):
    # Make prediction
    data = pd.DataFrame(patient.dict(), index=[0])
    parsed = predict(df=data)
    return {"output": parsed}

