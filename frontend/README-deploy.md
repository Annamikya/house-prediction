Deploying the frontend as a Render Static Site

1) Create a new Static Site on Render
   - Connect your repo, set the branch to `main`.
   - Set the **Root** to `frontend` (so Render serves that directory).

2) Add an environment variable in Render (for the Static Site):
   - Key: `BACKEND_URL`
   - Value: `https://<your-backend-service>.onrender.com` (your deployed backend URL)

3) Build Command (so `backend-config.js` is created from the env var):
   - Use this exact command (no Markdown):
     echo "const BACKEND_URL='${BACKEND_URL}';" > backend-config.js

   This writes `backend-config.js` into the published site so the frontend knows where the API is.

4) Publish Directory: leave as `/` (the `frontend` folder is the repo root for this site)

5) CORS: Your backend already allows CORS from any origin (development setting). If you lock it down, ensure the frontend origin is allowed.

6) Verify:
   - Visit your static site URL. The frontend should load and call the backend set in `BACKEND_URL`.
   - Test `/health` via the UI (status line) and make a `Predict` request.

Notes:
- If you want to commit a static `backend-config.js` instead of using Render env vars, copy `backend-config.js.example` to `backend-config.js` and edit the URL directly.
- Keep `backend` deployed (as a Web Service) and ensure it is reachable from the public internet (Render web service URL works).
