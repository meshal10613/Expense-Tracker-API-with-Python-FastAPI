import os
from pathlib import Path
from dotenv import load_dotenv

# Define project root directory and locate .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# Load environment variables from .env
load_dotenv(dotenv_path=ENV_FILE)

# Database file paths
DB_USER_FILE = BASE_DIR / "db" / "user.json"

# Fetch PORT from .env with fallback and integer conversion
try:
    PORT = int(os.getenv("PORT", 5000))
except ValueError:
    PORT = 5000  # Fallback if PORT in .env is not a valid integer

