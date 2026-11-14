async function predictTemperature() {

    const modelName = document.getElementById("model").value;
    const inputText = document.getElementById("temperatures").value;
    const resultDiv = document.getElementById("result");
    const button = document.getElementById("predictBtn");

    // Convert user input into numbers
    const temperatures = inputText
        .split(",")
        .map(value => Number(value.trim()));

    // Check input
    if (inputText.trim() === "" || temperatures.some(value => !Number.isFinite(value))) {
        resultDiv.innerHTML = "Please enter valid numerical temperatures.";
        return;
    }

    // Model requires exactly 30 values
    if (temperatures.length !== 30) {
        resultDiv.innerHTML =
            "Please enter exactly 30 temperatures.";
        return;
    }

    // Show loading message
    button.disabled = true;
    button.innerText = "Predicting...";
    resultDiv.innerHTML = "AI model is processing your data...";

    try {

        // Backend API connection
        const response = await fetch("YOUR_BACKEND_URL/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model_name: modelName,
                temperatures: temperatures
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed.");
        }

        // Display prediction
        resultDiv.innerHTML = `
            <h3>Prediction Result</h3>
            <p>Selected Model: ${data.model}</p>
            <h2>${data.predicted_temperature} ${data.unit}</h2>
            <p>Predicted Temperature for the Next Day</p>
        `;

    } catch (error) {

        resultDiv.innerHTML =
            "Error: " + error.message +
            "<br>Please check your backend connection.";

    } finally {

        button.disabled = false;
        button.innerText = "Predict Temperature";
    }
}