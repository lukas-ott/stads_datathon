import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
import io
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
    csv_data: str

# Define a model for the anomaly response
class Anomaly(BaseModel):
    category: str
    explanation: str

@app.post("/analyze", response_model=Anomaly)
async def analyze(data: CSVData):
    try:
        anomalyReasoner = AnomalyReasoner()
        categories, probability = anomalyReasoner.calculate_categories(data.csv_data)
        explanation = get_explanation(categories, probability)
        return Anomaly(category=categories, explanation=explanation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the data: {str(e)}")

@app.get("/get_graph")
async def get_graph():
    """Generates and returns a graph as an image."""
    try:
        # Create a simple plot (Replace with actual visualization logic)
        plt.figure(figsize=(5, 4))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker="o", linestyle="-", color="b")
        plt.title("Anomaly Analysis Graph")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")

        # Save the image to a BytesIO object
        img_io = io.BytesIO()
        plt.savefig(img_io, format="png")
        plt.close()
        img_io.seek(0)

        return Response(img_io.read(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating graph: {str(e)}")
