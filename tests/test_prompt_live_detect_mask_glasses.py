import os
import pathlib
import pytest
import ast
from pprint import pprint

from prompt_utils.prompt_dispatch import dispatch_prompt_detect


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


def test_live_detect_mask_or_glasses_from_prompt_local(
    monkeypatch, face_credentials
):
    prompt = "Check all the faces inside detection1.jpg wearing the mask or glasses"

    repo_root = pathlib.Path(__file__).resolve().parents[1]
    img_path = _find_file_upwards("detection1.jpg", repo_root)
    if img_path is None:
        pytest.skip("detection1.jpg not found in repo")

    old_cwd = pathlib.Path.cwd()
    try:
        os.chdir(img_path.parent)  # so bare relative 'detection1.jpg' works
        result_raw = dispatch_prompt_detect(prompt)
    finally:
        os.chdir(old_cwd)

    # Show the raw output for debugging/inspection
    pprint(result_raw)

    if isinstance(result_raw, tuple):
        result_str = "".join(result_raw)
    else:
        result_str = str(result_raw)

    assert "Azure AI Face API Detection Results" in result_str

    # Find the dict part after the colon and parse it
    colon_index = result_str.find(":")
    assert colon_index != -1, "No ':' found in result string"
    dict_str = result_str[colon_index + 1 :].strip()

    try:
        result_dict = ast.literal_eval(dict_str)
    except Exception as e:
        pytest.fail(f"Could not parse result into dict: {e}\nRaw string:\n{dict_str}")

    # Assertions on parsed dict
    assert isinstance(result_dict, dict), f"Expected dict, got {type(result_dict)}"
    assert "faceId" in result_dict, "faceId missing"
    assert "faceRectangle" in result_dict, "faceRectangle missing"
    assert "faceAttributes" in result_dict, "faceAttributes missing"

    attrs = result_dict["faceAttributes"]
    assert "glasses" in attrs, "'glasses' missing in faceAttributes"
    assert "mask" in attrs, "'mask' missing in faceAttributes"

    # Optional debug print (use pytest -s to see it)
    print("Glasses:", attrs["glasses"])
    print("Mask:", attrs["mask"])


def test_live_detect_mask_or_glasses_from_prompt_url(monkeypatch, face_credentials):
    # Use a public image URL with faces, mask or glasses for testing
    image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
    prompt = f"Check all the faces inside {image_url} wearing the mask or glasses"

    result_raw = dispatch_prompt_detect(prompt)

    pprint(result_raw)


"""
    if isinstance(result_raw, tuple):
        result_str = "".join(result_raw)
    else:
        result_str = str(result_raw)

    assert "Azure AI Face API Detection Results" in result_str

    colon_index = result_str.find(":")
    assert colon_index != -1, "No ':' found in result string"
    dict_str = result_str[colon_index + 1 :].strip()

    try:
        result_dict = ast.literal_eval(dict_str)
    except Exception as e:
        pytest.fail(f"Could not parse result into dict: {e}\nRaw string:\n{dict_str}")

    assert isinstance(result_dict, dict), f"Expected dict, got {type(result_dict)}"
    assert "faceId" in result_dict, "faceId missing"
    assert "faceRectangle" in result_dict, "faceRectangle missing"
    assert "faceAttributes" in result_dict, "faceAttributes missing"

    attrs = result_dict["faceAttributes"]
    assert "glasses" in attrs, "'glasses' missing in faceAttributes"
    assert "mask" in attrs, "'mask' missing in faceAttributes"

    print("Glasses:", attrs["glasses"])
    print("Mask:", attrs["mask"])
"""
