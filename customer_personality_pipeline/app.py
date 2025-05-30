from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()
model = joblib.load("C:/Users/user/PycharmProjects/PythonProject1/customer_personality_pipeline/outputs/models/rf_model.pkl")

@app.post("/predict/")
def predict(data: dict):
    df = pd.DataFrame([data])
    pred = model.predict(df)[0]
    return {"prediction": int(pred)}
