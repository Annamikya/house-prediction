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

Troubleshooting (404 on /backend-config.js)
- A 404 for `/backend-config.js` means the build command did not create the file (or the env var `BACKEND_URL` is not set).
- Ensure you set the Static Site environment variable `BACKEND_URL` in Render (Site Settings → Environment) to your backend URL (e.g., `https://<your-backend>.onrender.com`).
- Use this exact build command in Render (no Markdown formatting):

  echo "const BACKEND_URL='${BACKEND_URL}';" > backend-config.js

  This will write `backend-config.js` into the published site and prevent 404s.
- After changing env vars or build command, re-deploy the static site and inspect the Deploy logs; you should see the echo command run and the file created. If you still see 404s, confirm the published site contains `backend-config.js` (via the Render UI or by fetching `https://<your-site>/backend-config.js`).

Additional notes:
- If your site is served over HTTPS, ensure `BACKEND_URL` uses `https://` (browsers block mixed content — an HTTPS site can't call an HTTP backend).
- I added a default `frontend/backend-config.js` to this repo so you won't see a 404 while testing. Be sure to override it for production by setting the env var and build command above.
