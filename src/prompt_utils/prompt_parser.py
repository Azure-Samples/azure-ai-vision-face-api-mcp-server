import re
from dataclasses import dataclass


_IMG_EXT = r"(?:jpg|jpeg|png|bmp|gif|webp)"
_URL_RE = rf"(https?://\S+?\.(?:{_IMG_EXT}))"
_LOCAL_IMG_RE = rf"([^\s\"']+?\.(?:{_IMG_EXT}))"


@dataclass
class ParsedDetect:
    # Exact args your function needs
    file_path: str
    is_url: bool
    return_MASK: bool
    return_GLASSES: bool
    # keep these for completeness (all False for this prompt)
    return_HEAD_POSE: bool = False
    return_OCCLUSION: bool = False
    return_BLUR: bool = False
    return_EXPOSURE: bool = False
    return_QUALITY_FOR_RECOGNITION: bool = False
    return_AGE: bool = False
    return_landmarks: bool = False


def parse_prompt_for_detect(prompt: str) -> ParsedDetect:
    """
    Handles prompts like:
        'Check all the faces inside detection1.jpg wearing the mask or glasses'
        'Check all the faces inside https://.../detection1.jpg wearing the mask or glasses'
    """
    p = prompt.strip()
    m_url = re.search(_URL_RE, p, re.IGNORECASE)
    m_local = None if m_url else re.search(_LOCAL_IMG_RE, p, re.IGNORECASE)

    if not (m_url or m_local):
        raise ValueError("Could not find image path or URL in prompt.")

    has_mask = "mask" in p.lower()
    has_glasses = "glasses" in p.lower()

    if m_local:
        return ParsedDetect(
            file_path=m_local.group(1),
            is_url=False,
            return_MASK=has_mask,
            return_GLASSES=has_glasses,
        )
    else:
        return ParsedDetect(
            file_path=m_url.group(1),
            is_url=True,
            return_MASK=has_mask,
            return_GLASSES=has_glasses,
        )


@dataclass
class ParsedCompare:
    left: str  # local path or URL
    right: str  # local path or URL
    left_is_url: bool
    right_is_url: bool


_COMPARE_RE = re.compile(
    rf"""
    \bcompare\s+
    (?:the\s+)?                          # optional 'the' before left
    (?P<left>{_LOCAL_IMG_RE}|{_URL_RE})   # left path or URL
    \s+with\s+
    (?:the\s+)?                          # optional 'the' before right
    (?P<right>{_LOCAL_IMG_RE}|{_URL_RE})  # right path or URL
    """,
    re.IGNORECASE | re.VERBOSE,
)


def parse_prompt_for_compare(prompt: str) -> ParsedCompare:
    """
    Parse prompts like:
      'Compare the identification1.jpg with https://.../findsimilar.jpg'
    """
    p = prompt.strip()
    m = _COMPARE_RE.search(p)

    if not m:
        raise ValueError("Unrecognized compare prompt format")

    left = m.group("left")
    right = m.group("right")
    left_is_url = bool(re.fullmatch(_URL_RE, left, re.IGNORECASE))
    right_is_url = bool(re.fullmatch(_URL_RE, right, re.IGNORECASE))

    return ParsedCompare(
        left=left, right=right, left_is_url=left_is_url, right_is_url=right_is_url
    )


@dataclass
class ParsedEnroll:
    file_path_list: list  # list of local paths or URLs
    person_name: str
    group_uuid: str
    is_url: bool = False
    check_quality: bool = True


_ENROLL_RE = re.compile(
    rf"""
    \benroll\s+(?:the\s+)?face[s]?\s+in\s+
    (?P<file>(?:{_LOCAL_IMG_RE}|{_URL_RE})(?:\s*,\s*(?:{_LOCAL_IMG_RE}|{_URL_RE}))*)
    \s+to\s+(?:the\s+)?person\s+group\s+['"]?(?P<group>[\w\-]+)['"]?
    \s+as\s+['"]?(?P<person>[\w\-]+)['"]?
    """,
    re.IGNORECASE | re.VERBOSE,
)


def parse_prompt_for_enroll(prompt: str) -> ParsedEnroll:
    """
    Parse prompts like:
      'Enroll the face in detection1.jpg to the person group "test-group" as "test-person"'
      'Enroll the face in https://.../detection1.jpg to the person group test-group as test-person'
      'Enroll the faces in img1.jpg, img2.jpg to the person group test-group as test-person'
    """
    p = prompt.strip()
    m = _ENROLL_RE.search(p)
    if not m:
        raise ValueError("Unrecognized enroll prompt format")
    file_str = m.group("file")
    # Split by comma and strip whitespace
    file_path_list = [f.strip() for f in re.split(r",\s*", file_str)]
    is_url = all(re.fullmatch(_URL_RE, f, re.IGNORECASE) for f in file_path_list)
    person_name = m.group("person")
    group_uuid = m.group("group")
    return ParsedEnroll(
        file_path_list=file_path_list,
        person_name=person_name,
        group_uuid=group_uuid,
        is_url=is_url,
        check_quality=True,
    )


__all__ = [
    "ParsedDetect",
    "parse_prompt_for_detect",
    "ParsedCompare",
    "parse_prompt_for_compare",
    "ParsedEnroll",
    "parse_prompt_for_enroll",
]
