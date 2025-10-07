import pytest

from prompt_utils.prompt_parser import (
    ParsedDetect,
    parse_prompt_for_detect,
    parse_prompt_for_compare,
    parse_prompt_for_enroll,
)


def test_parse_prompt_for_detect_local_image():
    prompt = "Check all the faces inside detection1.jpg wearing the mask or glasses"
    parsed = parse_prompt_for_detect(prompt)
    assert parsed == ParsedDetect(
        file_path="detection1.jpg",
        is_url=False,
        return_MASK=True,
        return_GLASSES=True,
    )


def test_parse_prompt_for_detect_url_image():
    url = "https://example.com/detection1.jpg"
    prompt = f"Check all the faces inside {url} wearing the mask"
    parsed = parse_prompt_for_detect(prompt)
    assert parsed == ParsedDetect(
        file_path=url,
        is_url=True,
        return_MASK=True,
        return_GLASSES=False,
    )


def test_parse_prompt_for_detect_invalid_prompt():
    with pytest.raises(ValueError):
        parse_prompt_for_detect("No image reference here")


def test_parse_prompt_for_compare_local_and_url():
    prompt = "Compare the identification1.jpg with https://example.com/findsimilar.jpg"
    parsed = parse_prompt_for_compare(prompt)
    assert parsed.left == "identification1.jpg"
    assert parsed.right == "https://example.com/findsimilar.jpg"
    assert parsed.left_is_url is False
    assert parsed.right_is_url is True


def test_parse_prompt_for_compare_invalid_prompt():
    with pytest.raises(ValueError):
        parse_prompt_for_compare("Compare nothing")


def test_parse_prompt_for_enroll_multiple_images_local():
    prompt = "Enroll the faces in img1.jpg, img2.jpg to the person group test-group as test-person"
    parsed = parse_prompt_for_enroll(prompt)
    assert parsed.file_path_list == ["img1.jpg", "img2.jpg"]
    assert parsed.person_name == "test-person"
    assert parsed.group_uuid == "test-group"
    assert parsed.is_url is False
    assert parsed.check_quality is True


def test_parse_prompt_for_enroll_all_urls():
    prompt = (
        "Enroll the faces in https://example.com/a.jpg, https://example.com/b.png"
        " to the person group group-123 as alice"
    )
    parsed = parse_prompt_for_enroll(prompt)
    assert parsed.file_path_list == [
        "https://example.com/a.jpg",
        "https://example.com/b.png",
    ]
    assert parsed.is_url is True
    assert parsed.person_name == "alice"
    assert parsed.group_uuid == "group-123"


def test_parse_prompt_for_enroll_mixed_sources():
    prompt = (
        "Enroll the faces in img1.jpg, https://example.com/b.png"
        " to the person group group-456 as bob"
    )
    parsed = parse_prompt_for_enroll(prompt)
    assert parsed.file_path_list == ["img1.jpg", "https://example.com/b.png"]
    assert parsed.is_url is False
    assert parsed.person_name == "bob"
    assert parsed.group_uuid == "group-456"


def test_parse_prompt_for_enroll_invalid_prompt():
    with pytest.raises(ValueError):
        parse_prompt_for_enroll("Enroll something without enough info")
