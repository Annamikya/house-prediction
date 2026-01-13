// Default backend config used when no build-time BACKEND_URL is generated.
// For production, override by setting Render Static Site env var BACKEND_URL
// and using the build command: echo "const BACKEND_URL='${BACKEND_URL}';" > backend-config.js

const BACKEND_URL = 'http://127.0.0.1:8000';

// Helpful console hint in deployed sites to remind you to set BACKEND_URL
if (location.hostname !== 'localhost' && BACKEND_URL.includes('127.0.0.1')) {
  console.warn('Using default BACKEND_URL (127.0.0.1). Set Render env var BACKEND_URL to the deployed backend URL and add the build command to generate backend-config.js at build time.');
}
