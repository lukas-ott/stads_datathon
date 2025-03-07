"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const inputField = document.getElementById("csvInput");
const processBtn = document.getElementById("processBtn");
const explanationField = document.getElementById("explanation");
const chartContainer = document.getElementById("chartContainer");
// API request to backend for anomaly analysis
function analyzeData(csvData) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch("http://localhost:8000/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ csv_data: csvData }),
            });
            if (!response.ok) {
                throw new Error("An error occurred while analyzing the data.");
            }
            const data = yield response.json();
            explanationField.value = `Kategorie: ${data.category}\nErklärung: ${data.explanation}`;
            chartContainer.innerHTML = `<strong>Visualisierung der Anomalie (${data.category})</strong>`;
        }
        catch (error) {
            explanationField.value = "Fehler beim Abrufen der Anomalie-Daten.";
            console.error(error);
        }
    });
}
// Button-Eventlistener
processBtn.addEventListener("click", () => {
    const csvData = inputField.value.trim();
    if (csvData) {
        analyzeData(csvData);
    }
    else {
        explanationField.value = "Bitte geben Sie eine CSV-Zeile ein.";
    }
});
