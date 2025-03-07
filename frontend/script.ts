interface Anomaly {
    id: number;
    category: string;
    explanation: string;
}

const anomalies: Anomaly[] = [
    { id: 1, category: "Hoher Betrag", explanation: "Dieser Buchungssatz enthält einen ungewöhnlich hohen Betrag im Vergleich zu anderen." },
    { id: 2, category: "Unbekanntes Profitcenter", explanation: "Das Profitcenter existiert nicht in der üblichen Liste." },
];

const select = document.getElementById("anomalySelect") as HTMLSelectElement;
const explanationDiv = document.getElementById("explanation") as HTMLDivElement;

// Dropdown befüllen
anomalies.forEach(anomaly => {
    const option = document.createElement("option");
    option.value = anomaly.id.toString();
    option.textContent = anomaly.category;
    select.appendChild(option);
});

// Erklärung anzeigen
select.addEventListener("change", () => {
    const selectedId = parseInt(select.value);
    const anomaly = anomalies.find(a => a.id === selectedId);
    explanationDiv.textContent = anomaly ? anomaly.explanation : "Keine Erklärung verfügbar.";
});
