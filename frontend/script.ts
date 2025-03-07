interface Anomaly {
    category: string;
    explanation: string;
}

const inputField = document.getElementById("csvInput") as HTMLInputElement;
const processBtn = document.getElementById("processBtn") as HTMLButtonElement;
const explanationField = document.getElementById("explanation") as HTMLTextAreaElement;
const chartContainer = document.getElementById("chartContainer") as HTMLDivElement;

// API request to backend for anomaly analysis
async function analyzeData(csvData: string) {
    try {
        const response = await fetch("http://localhost:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ csv_data: csvData }),
        });

        if (!response.ok) {
            throw new Error("An error occurred while analyzing the data.");
        }

        const data = await response.json();
        explanationField.value = `Kategorie: ${data.category}\nErklärung: ${data.explanation}`;
        chartContainer.innerHTML = `<strong>Visualisierung der Anomalie (${data.category})</strong>`;
    } catch (error) {
        explanationField.value = "Fehler beim Abrufen der Anomalie-Daten.";
        console.error(error);
    }
}

// Button-Eventlistener
processBtn.addEventListener("click", () => {
    const csvData = inputField.value.trim();
    if (csvData) {
        analyzeData(csvData);
    } else {
        explanationField.value = "Bitte geben Sie eine CSV-Zeile ein.";
    }
});
