import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import base64

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
from starlette.responses import Response
from anomaly_reasoner import AnomalyReasoner
from llm_explanation import get_explanation

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security (e.g., only allow frontend domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a model for the input data
class CSVData(BaseModel):
    belnr: str

# Define a model for the anomaly response
class Anomaly(BaseModel):
    category: str
    explanation: str
    image_buf_1: str
    image_buf_2: str
    image_buf_3: str

@app.post("/analyze", response_model=Anomaly)
async def analyze(data: CSVData):
    try:
        anomalyReasoner = AnomalyReasoner()
        categories, probability, image_buf_1, image_buf_2, image_buf_3 = anomalyReasoner.calculate_categories(data.belnr)
        explanation = "Test"
        # explanation = get_explanation(categories, probability)
        
        # Encode image buffers to base64 strings
        image_buf_1_str = base64.b64encode(image_buf_1.getvalue()).decode('utf-8')
        image_buf_2_str = base64.b64encode(image_buf_2.getvalue()).decode('utf-8')
        image_buf_3_str = base64.b64encode(image_buf_3.getvalue()).decode('utf-8')
        
        return Anomaly(category=categories, explanation=explanation, image_buf_1=image_buf_1_str, image_buf_2=image_buf_2_str, image_buf_3=image_buf_3_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the data: {str(e)}")