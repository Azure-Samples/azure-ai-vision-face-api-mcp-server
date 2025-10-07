from prompt_utils import prompt_dispatch
from prompt_utils.prompt_parser import ParsedDetect, ParsedCompare, ParsedEnroll


def test_dispatch_prompt_detect_forwards_all_arguments(monkeypatch):
    intent = ParsedDetect(
        file_path="local.jpg",
        is_url=False,
        return_MASK=True,
        return_GLASSES=False,
        return_HEAD_POSE=True,
        return_OCCLUSION=True,
        return_BLUR=True,
        return_EXPOSURE=True,
        return_QUALITY_FOR_RECOGNITION=True,
        return_AGE=True,
        return_landmarks=True,
    )

    monkeypatch.setattr(prompt_dispatch, "parse_prompt_for_detect", lambda prompt: intent)

    captured = {}

    def fake_detect(**kwargs):
        captured.update(kwargs)
        return "detect-result"

    monkeypatch.setattr(prompt_dispatch, "_load_func", lambda module, fn_name: fake_detect)

    result = prompt_dispatch.dispatch_prompt_detect("any prompt")

    assert result == "detect-result"
    assert captured == {
        "file_path": "local.jpg",
        "is_url": False,
        "return_HEAD_POSE": True,
        "return_GLASSES": False,
        "return_OCCLUSION": True,
        "return_BLUR": True,
        "return_EXPOSURE": True,
        "return_MASK": True,
        "return_QUALITY_FOR_RECOGNITION": True,
        "return_AGE": True,
        "return_landmarks": True,
    }


def test_dispatch_prompt_compare_uses_expected_defaults(monkeypatch):
    intent = ParsedCompare(
        left="left.jpg",
        right="right.jpg",
        left_is_url=False,
        right_is_url=True,
    )
    monkeypatch.setattr(prompt_dispatch, "parse_prompt_for_compare", lambda prompt: intent)

    captured = {}

    def fake_compare(**kwargs):
        captured.update(kwargs)
        return "compare-result"

    monkeypatch.setattr(prompt_dispatch, "_load_func", lambda module, fn_name: fake_compare)

    result = prompt_dispatch.dispatch_prompt_compare("compare")

    assert result == "compare-result"
    assert captured == {
        "source_image": "left.jpg",
        "target_image": "right.jpg",
        "comparison_mode": "most_similar",
        "is_source_image_url": False,
        "is_target_image_url": True,
        "identical_threshold": 0.5,
    }


def test_dispatch_prompt_enroll_forwards_arguments(monkeypatch):
    intent = ParsedEnroll(
        file_path_list=["img1.jpg", "img2.jpg"],
        person_name="alice",
        group_uuid="group-123",
        is_url=False,
        check_quality=False,
    )
    monkeypatch.setattr(prompt_dispatch, "parse_prompt_for_enroll", lambda prompt: intent)

    captured = {}

    def fake_enroll(**kwargs):
        captured.update(kwargs)
        return "enroll-result"

    monkeypatch.setattr(prompt_dispatch, "_load_func", lambda module, fn_name: fake_enroll)

    result = prompt_dispatch.dispatch_prompt_enroll("enroll")

    assert result == "enroll-result"
    assert captured == {
        "file_path_list": ["img1.jpg", "img2.jpg"],
        "person_name": "alice",
        "group_uuid": "group-123",
        "is_url": False,
        "check_quality": False,
    }
