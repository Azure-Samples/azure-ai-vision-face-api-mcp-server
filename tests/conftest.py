# conftest.py
from pathlib import Path
import sys

try:
    from dotenv import load_dotenv  # pip install python-dotenv

    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    print(f"[pytest] .env loaded from {env_path}")
except Exception as e:
    print(f"[pytest] Could not load .env: {e}")

# Ensure the package modules under src/ are importable without installation.
repo_root = Path(__file__).resolve().parents[1]
src_dir = repo_root / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))
