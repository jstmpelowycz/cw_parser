import re
from re import Pattern
from typing import Optional

from src.modules.parser.regexs.constants import FULLNAME_REGEX, CASE_FORM_MARKERS


def make_case_form_patterns() -> list[Pattern[str]]:
  return [
    re.compile(make_case_form_regex(marker))
    for marker in CASE_FORM_MARKERS
  ]


def make_case_form_regex(lowercase_word: str) -> str:
  return r'\s*'.join([
    char.strip()
    for char in lowercase_word.upper()
    if char.strip()
  ])


def is_fullname(attempt_input: Optional[str]) -> bool:
  if not attempt_input:
    return False
  return bool(re.match(FULLNAME_REGEX, attempt_input))


def if_fullname(attempt_input: str) -> Optional[str]:
  return attempt_input if is_fullname(attempt_input) else None
