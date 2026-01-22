# Set BACKEND_URL for local testing
# Run this before serving frontend locally: python set_backend_url.py https://your-backend-url

import sys
import os

if len(sys.argv) != 2:
    print("Usage: python set_backend_url.py <backend_url>")
    sys.exit(1)

backend_url = sys.argv[1]
config_path = os.path.join(os.path.dirname(__file__), "backend-config.js")

with open(config_path, "w") as f:
    f.write(f"const BACKEND_URL = '{backend_url}';")

print(f"Set BACKEND_URL to {backend_url} in {config_path}")