interface Anomaly {
    category: string;
    explanation: string;
}

const anomalies: Anomaly[] = [
    { category: "Hoher Betrag", explanation: "Der Betrag ist im Vergleich zu anderen Buchungen ungewöhnlich hoch." },
    { category: "Unbekanntes Profitcenter", explanation: "Das Profitcenter ist nicht in der üblichen Liste enthalten." },
];

const inputField = document.getElementById("csvInput") as HTMLInputElement;
const processBtn = document.getElementById("processBtn") as HTMLButtonElement;
const explanationField = document.getElementById("explanation") as HTMLTextAreaElement;
const chartContainer = document.getElementById("chartContainer") as HTMLDivElement;

// Simulierte Anomalie-Erkennung
function analyzeData(csvData: string) {
    const anomaly = anomalies[Math.floor(Math.random() * anomalies.length)];
    explanationField.value = `Kategorie: ${anomaly.category}\nErklärung: ${anomaly.explanation}`;
    chartContainer.innerHTML = `<strong>Visualisierung der Anomalie (${anomaly.category})</strong>`;
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
