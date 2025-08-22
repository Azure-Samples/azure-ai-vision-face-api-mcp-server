# conftest.py
from pathlib import Path

try:
    from dotenv import load_dotenv  # pip install python-dotenv

    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    print(f"[pytest] .env loaded from {env_path}")
except Exception as e:
    print(f"[pytest] Could not load .env: {e}")
