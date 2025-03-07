from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Define a model for the input data
class CSVData(BaseModel):
    csv_data: str

# Define a model for the anomaly response
class Anomaly(BaseModel):
    category: str
    explanation: str

# Simulated anomaly categories
anomalies = [
    {"category": "Hoher Betrag", "explanation": "Der Betrag ist im Vergleich zu anderen Buchungen ungewöhnlich hoch."},
    {"category": "Unbekanntes Profitcenter", "explanation": "Das Profitcenter ist nicht in der üblichen Liste enthalten."},
]

@app.post("/analyze", response_model=Anomaly)
async def analyze(csv_data: CSVData):
    # Simulate anomaly detection
    anomaly = random.choice(anomalies)
    return Anomaly(category=anomaly["category"], explanation=anomaly["explanation"])

