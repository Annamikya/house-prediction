// Use BACKEND_URL from a generated config (backend-config.js) or default to localhost
const BACKEND = (typeof BACKEND_URL !== 'undefined' && BACKEND_URL) ? BACKEND_URL.replace(/\/$/, '') : 'http://127.0.0.1:8000';

// Check backend health on page load and provide clearer error guidance
async function checkBackend() {
    const status = document.getElementById('status');
    const net = document.getElementById('networkDetails');
    try {
        const resp = await fetch(`${BACKEND}/health`);
        if (resp.ok) {
            const info = await resp.json();
            status.innerText = info.status || 'Backend reachable';
            if (net) net.innerText = `Backend: ${BACKEND} — /health OK`;
        } else {
            status.innerText = `Backend returned ${resp.status}`;
            if (net) net.innerText = `Backend: ${BACKEND} — /health returned ${resp.status}`;
        }
    } catch (e) {
        // Friendly guidance when backend isn't reachable
        status.innerText = 'Backend unreachable — check the backend URL and that it is running.';
        if (net) net.innerText = `Error: ${e.message || e}\nBackend tried: ${BACKEND}\nIf running locally, start with: uvicorn app.main:app --host 0.0.0.0 --port 8000`;
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
        const response = await fetch(`${BACKEND}/predict`, {
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
            const net = document.getElementById('networkDetails');
            if (net) net.innerText = `Response status: ${response.status} ${response.statusText}\nBackend URL: ${BACKEND}`;
            console.error('Prediction error', detail);
            return;
        }

        result.innerText = `Predicted Price: ₹ ${data.predicted_price.toFixed(2)}`;
        status.innerText = 'Prediction complete';

        // Fetch plot image and display as blob
        try {
            const plotResp = await fetch(`${BACKEND}/plot`, {
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
        const msg = e && e.message ? e.message : String(e);
        err.innerText = 'Network or server error. See details below.';
        status.innerText = 'Error';
        const net = document.getElementById('networkDetails');
        if (net) net.innerText = `Error: ${msg}\nBackend URL: ${BACKEND}\nBrowser online: ${navigator.onLine}`;
        console.error('Network/server error', e);
    } finally {
        btn.disabled = false;
    }
}

// Run health check when the page loads
window.addEventListener('DOMContentLoaded', () => {
    const backendEl = document.getElementById('backendUrl');
    if (backendEl) backendEl.innerText = BACKEND;
    const netEl = document.getElementById('networkDetails');
    if (netEl) netEl.innerText = '';

    // Common deployment mistakes: warn when site is HTTPS but backend is HTTP (mixed content),
    // or when frontend is hosted remotely but BACKEND points to localhost.
    try {
        if (location.protocol === 'https:' && BACKEND.startsWith('http:')) {
            if (netEl) netEl.innerText = `Warning: page served via HTTPS but backend is HTTP. Browsers block mixed content. Set BACKEND_URL to an https:// backend.`;
        } else if (window.location.hostname !== 'localhost' && BACKEND.includes('127.0.0.1')) {
            if (netEl) netEl.innerText = `Warning: frontend is hosted remotely but BACKEND_URL points to localhost (${BACKEND}). Update BACKEND_URL to the deployed backend URL.`;
        }
    } catch (e) {
        console.warn('Unable to perform deployment heuristics check', e);
    }

    checkBackend();
});

