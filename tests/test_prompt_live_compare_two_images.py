import os
import pathlib
import pytest
from pprint import pprint

from prompt_utils.prompt_dispatch import dispatch_prompt_compare

endpoint = os.getenv("AZURE_FACE_ENDPOINT")
key = os.getenv("AZURE_FACE_API_KEY")

if not (endpoint and key):
    print(
        "❌ Live test skipped: Set AZURE_FACE_ENDPOINT and AZURE_FACE_API_KEY environment variables."
    )

LIVE = pytest.mark.skipif(
    not (endpoint and key),
    reason="Set AZURE_FACE_ENDPOINT and AZURE_FACE_API_KEY to run live tests",
)


def _find_file_upwards(filename: str, start: pathlib.Path) -> pathlib.Path | None:
    """Search upwards and in common sample folders for the given file."""
    candidates = [
        start / filename,
        start / "example" / filename,
        start / "examples" / filename,
        start / "samples" / filename,
        start / "assets" / filename,
        start / "testdata" / filename,
    ]
    for c in candidates:
        if c.is_file():
            return c
    for p in start.rglob(filename):
        if p.is_file():
            return p
    return None


@LIVE
def test_live_compare_two_images_from_prompt():
    prompt = (
        "Compare the identification1.jpg with "
        "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/"
        "refs/heads/master/Face/images/findsimilar.jpg"
    )

    repo_root = pathlib.Path(__file__).resolve().parents[1]
    img_path = _find_file_upwards("identification1.jpg", repo_root)
    if img_path is None:
        pytest.skip("identification1.jpg not found in repo")

    # Run in the image directory so the relative path works
    old_cwd = pathlib.Path.cwd()
    try:
        os.chdir(img_path.parent)
        result_raw = dispatch_prompt_compare(prompt)
    finally:
        os.chdir(old_cwd)

    # Show the raw output for debugging/inspection
    pprint(result_raw)

    # Your tool tends to return a tuple/pretty string; normalize to a single string
    result_str = (
        "".join(result_raw) if isinstance(result_raw, tuple) else str(result_raw)
    )

    print("Result string:", result_str)

    expected_start = (
        "Most similar comparison is requested. For each face in the image file: identification1.jpg, "
        "the most similar face from the image file: https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/refs/heads/master/Face/images/findsimilar.jpg will be determined."
    )
    assert result_str.startswith(expected_start)
    assert "Verification result: True, Confidence: 0.95746" in result_str
    assert "The current comparison mode is: most_similar." in result_str
