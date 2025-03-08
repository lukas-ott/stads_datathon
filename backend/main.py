from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
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
    input_format = re.compile(r".+,.+,.+,.+,.+,.+,.+,.+,.+,.+")
    if not input_format.match(data.csv_data):
        raise HTTPException(status_code=400, detail="Invalid input format. Please provide a valid CSV line.")
    
    try:
        anomalyReasoner = AnomalyReasoner()
        categories, probability = anomalyReasoner.calculate_categories(data.csv_data)
        explanation = get_explanation(categories, probability)
        return Anomaly(category=categories, explanation=explanation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the data: {str(e)}")