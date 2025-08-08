from importlib import import_module
from typing import Any, Callable
from .prompt_parser import (
    ParsedDetect,
    parse_prompt_for_detect,
    ParsedCompare,
    parse_prompt_for_compare,
)


def _load_func(module_path: str, func_name: str) -> Callable[..., Any] | None:
    try:
        mod = import_module(module_path)
        fn = getattr(mod, func_name, None)
        return fn if callable(fn) else None
    except Exception:
        return None


def dispatch_prompt_detect(prompt: str) -> Any:
    """
    Parse the prompt and call tools.AzureFaceAttrib.get_face_dect(...)
    with the exact kwargs expected by that function.
    """
    intent: ParsedDetect = parse_prompt_for_detect(prompt)

    fn = _load_func("tools.AzureFaceAttrib", "get_face_dect")

    return fn(
        file_path=intent.file_path,
        is_url=intent.is_url,
        return_HEAD_POSE=intent.return_HEAD_POSE,
        return_GLASSES=intent.return_GLASSES,
        return_OCCLUSION=intent.return_OCCLUSION,
        return_BLUR=intent.return_BLUR,
        return_EXPOSURE=intent.return_EXPOSURE,
        return_MASK=intent.return_MASK,
        return_QUALITY_FOR_RECOGNITION=intent.return_QUALITY_FOR_RECOGNITION,
        return_AGE=intent.return_AGE,
        return_landmarks=intent.return_landmarks,
    )


def dispatch_prompt_compare(prompt: str) -> Any:
    intent: ParsedCompare = parse_prompt_for_compare(prompt)
    fn = _load_func("tools.CompareImages", "compare_source_image_to_target_image")
    print(f"Dispatching compare with: {intent}")
    return fn(
        source_image=intent.left,
        target_image=intent.right,
        comparison_mode="most_similar",
        is_source_image_url=intent.left_is_url,
        is_target_image_url=intent.right_is_url,
        identical_threshold=0.5,
    )
