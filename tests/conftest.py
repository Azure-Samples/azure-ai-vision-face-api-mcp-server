# conftest.py
import os
from pathlib import Path
import sys

import pytest

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


def _require_face_credentials() -> tuple[str, str]:
    endpoint = os.getenv("AZURE_FACE_ENDPOINT")
    key = os.getenv("AZURE_FACE_API_KEY")
    if not endpoint or not key:
        pytest.fail(
            "Live tests require AZURE_FACE_ENDPOINT and AZURE_FACE_API_KEY environment variables."
        )
    sanitized_endpoint = endpoint.strip()
    sanitized_key = key.strip()
    placeholder_markers = ("<", "example", "REPLACE", "YOUR", "{", "}")
    if any(marker in sanitized_endpoint for marker in placeholder_markers):
        pytest.fail(
            "AZURE_FACE_ENDPOINT appears to be a placeholder. Provide the real endpoint before running live tests."
        )
    if any(marker in sanitized_key for marker in placeholder_markers):
        pytest.fail(
            "AZURE_FACE_API_KEY appears to be a placeholder. Provide the real key before running live tests."
        )
    return sanitized_endpoint, sanitized_key


@pytest.fixture(scope="session")
def face_credentials() -> tuple[str, str]:
    """Ensure Face API credentials are available before running live tests."""
    return _require_face_credentials()
