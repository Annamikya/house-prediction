// Check backend health on page load and provide clearer error guidance
async function checkBackend() {
    const status = document.getElementById('status');
    try {
        const resp = await fetch('http://127.0.0.1:8000/health');
        if (resp.ok) {
            const info = await resp.json();
            status.innerText = info.status || 'Backend reachable';
        } else {
            status.innerText = `Backend returned ${resp.status}`;
        }
    } catch (e) {
        // Friendly guidance when backend isn't reachable
        status.innerText = 'Backend unreachable — ensure it is running (run: `uvicorn backend.app.main:app --reload --port 8000`) and open the frontend over http (run: `python -m http.server` from project root).';
        console.error('Backend health check failed', e);
    }
}

// Main prediction function (called by button)
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

        // If the fetch succeeds but backend returns an error status, show backend message
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
            console.error('Failed to fetch plot — check that the backend is running and that CORS is enabled', e);
            // Don't override previous messages, but show a small hint
            if (!err.innerText) err.innerText = 'Plot could not be fetched. Check backend console for errors.';
        }

    } catch (e) {
        // More actionable guidance for the common "Failed to fetch" TypeError
        const msg = e && e.message ? e.message : String(e);
        err.innerText = 'Network or server error: ' + msg + '\nMake sure the backend is running (run: `uvicorn backend.app.main:app --reload --port 8000`) and that you opened the frontend using an HTTP server (run: `python -m http.server` from project root).';
        status.innerText = 'Error';
        console.error('Network/server error', e);
    } finally {
        btn.disabled = false;
    }
}

// Run health check when the page loads
window.addEventListener('DOMContentLoaded', checkBackend);
