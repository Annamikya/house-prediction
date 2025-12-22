async function predictPrice() {
    const btn = document.getElementById('predictBtn');
    const status = document.getElementById('status');
    const err = document.getElementById('error');
    const result = document.getElementById('result');
    const plotImg = document.getElementById('plot');

    err.innerText = '';
    result.innerText = '';
    plotImg.src = '';

    const payload = {
        GrLivArea: Number(document.getElementById("area").value),
        TotRmsAbvGrd: Number(document.getElementById("rooms").value)
    };

    btn.disabled = true;
    status.innerText = 'Predicting...';

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) {
            const detail = data.detail || JSON.stringify(data);
            err.innerText = 'Prediction error: ' + detail;
            status.innerText = 'Error';
            console.error('Prediction error', detail);
            return;
        }

        result.innerText = `Predicted Price: ₹ ${data.predicted_price.toFixed(2)}`;
        status.innerText = 'Prediction complete';

        // Fetch plot image and display as blob
        try {
            const plotResp = await fetch("http://127.0.0.1:8000/plot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            if (plotResp.ok) {
                const blob = await plotResp.blob();
                const url = URL.createObjectURL(blob);
                plotImg.src = url;
            } else {
                console.warn('Plot endpoint returned non-OK', plotResp.status);
            }
        } catch (e) {
            console.error('Failed to fetch plot', e);
        }

    } catch (e) {
        err.innerText = 'Network or server error: ' + e.message;
        status.innerText = 'Error';
        console.error(e);
    } finally {
        btn.disabled = false;
    }
}
