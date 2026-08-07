import os
from pathlib import Path
from dotenv import load_dotenv

# Define project root directory and locate .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# Load environment variables from .env
load_dotenv(dotenv_path=ENV_FILE)

# Fetch PORT from .env with fallback and integer conversion
try:
    PORT = int(os.getenv("PORT", 8000))
except ValueError:
    PORT = 8000  # Fallback if PORT in .env is not a valid integer