document.addEventListener("DOMContentLoaded", () => {
    const processBtn = document.getElementById("processBtn") as HTMLButtonElement;
    const csvInput = document.getElementById("csvInput") as HTMLInputElement;
    const explanationBox = document.getElementById("explanation") as HTMLTextAreaElement;
    const chartContainer = document.getElementById("chartContainer") as HTMLDivElement;

    processBtn.addEventListener("click", async () => {
        const transactionNumber = csvInput.value.trim();
        if (!transactionNumber) {
            alert("Please enter a transaction number.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ belnr: transactionNumber }),
            });

            if (!response.ok) {
                switch (response.status) {
                    case 401:
                        throw new Error("Error 401: Unauthorized.");
                    case 500:
                        throw new Error("Error 500: Internal Server Error.");
                    default:
                        throw new Error(`Server error ${response.status}: Unexpected error.`);
                }
            }

            const result = await response.json();
            explanationBox.value = `${result.explanation}`;

            chartContainer.innerHTML = "";

            if (result.image_buf_1 !== null) {
                const graphImg1 = document.createElement("img");
                graphImg1.src = `data:image/png;base64,${result.image_buf_1}`;
                graphImg1.alt = "Anomaly Analysis Graph 1";
                graphImg1.style.maxWidth = "100%";
                chartContainer.appendChild(graphImg1);
            }
            if (result.image_buf_2 !== null) {
                const graphImg2 = document.createElement("img");
                graphImg2.src = `data:image/png;base64,${result.image_buf_2}`;
                graphImg2.alt = "Anomaly Analysis Graph 2";
                graphImg2.style.maxWidth = "100%";
                chartContainer.appendChild(graphImg2);
            }

            if (result.image_buf_3 !== null) {
                const graphImg3 = document.createElement("img");
                graphImg3.src = `data:image/png;base64,${result.image_buf_3}`;
                graphImg3.alt = "Anomaly Analysis Graph 3";
                graphImg3.style.maxWidth = "100%";
                chartContainer.appendChild(graphImg3);
            }
        } catch (error) {
            console.error("Error:", error);
            alert(error instanceof Error ? error.message : "An unknown error occurred.");
        }
    });
});