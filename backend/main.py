from fastapi import FastAPI
from pydantic import BaseModel
from anomaly_reasoner import AnomalyReasoner
from llm_explanation import get_explanation

app = FastAPI()

# Define a model for the input data
class CSVData(BaseModel):
    csv_data: str

# Define a model for the anomaly response
class Anomaly(BaseModel):
    category: str
    explanation: str


@app.post("/analyze", response_model=Anomaly)
async def analyze(data: CSVData):
    anomalyReasoner = AnomalyReasoner()
    categories, probability = anomalyReasoner.calculate_categories(data.csv_data)
    explanation = get_explanation(categories)
    return Anomaly(category=categories, explanation=explanation)
