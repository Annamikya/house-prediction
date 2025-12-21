async function predictPrice() {
    const payload = {
        GrLivArea: Number(document.getElementById("area").value),
        TotRmsAbvGrd: Number(document.getElementById("rooms").value)
    };

    const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    document.getElementById("result").innerText =
        "Predicted Price: ₹ " + data.predicted_price.toFixed(2);
}
