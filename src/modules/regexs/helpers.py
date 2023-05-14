import re
from re import Pattern
from typing import Optional

from src.modules.regexs.constants import \
  FULLNAME_PATTERN, \
  CASE_RULING_START_MARKERS, \
  CASE_DECISION_START_MARKERS, \
  CASE_DECISION_END_MARKER, \
  CASE_FORM_MARKERS, MONTH_MARKERS


def define_date_pattern(value: str) -> Pattern[str]:
  if does_month_marker_occur(value):
    return make_date_labeled_pattern()
  return make_date_digital_pattern()


def does_month_marker_occur(value: str) -> bool:
  return any(marker in value for marker in MONTH_MARKERS)


def make_date_labeled_pattern() -> Pattern[str]:
  return re.compile((
      r'"?(\d{2})\"?\s+('
      + r'|'.join(MONTH_MARKERS)
      + r')\s+(\d{4})\s*'
  ), re.IGNORECASE)


def make_date_digital_pattern() -> Pattern[str]:
  return re.compile(r'(\d{2}).(\d{2}).(\d{4})')


def make_case_header_pattern() -> Pattern[str]:
  return re.compile(make_case_header_regex(), re.IGNORECASE | re.DOTALL)


def make_case_ruling_pattern() -> Pattern[str]:
  return re.compile(make_case_ruling_regex(), re.IGNORECASE | re.DOTALL)


def make_case_decision_pattern() -> Pattern[str]:
  return re.compile(make_case_decision_regex(), re.IGNORECASE | re.DOTALL)


def make_case_form_patterns() -> list[Pattern[str]]:
  return [
    re.compile(make_case_form_regex(marker))
    for marker in CASE_FORM_MARKERS
  ]


def make_case_header_regex() -> str:
  end_regex = r'|'.join([
    r'\s*'.join([char for char in marker]) + r'\s*(в\s*|л\s*а)'
    for marker in CASE_RULING_START_MARKERS
  ])

  return (
      r'^(.*?)'
      + end_regex
      + r'\s*:'
  )


def make_case_ruling_regex() -> str:
  start_regex = r'|'.join([
    r'\s*'.join([char for char in marker]) + r'\s*(в\s*|л\s*а)'
    for marker in CASE_RULING_START_MARKERS
  ])

  end_regex = r'|'.join([
    r'\s*'.join([char for char in marker]) + r'\s*(в\s*|л\s*а)'
    for marker in CASE_DECISION_START_MARKERS
  ])

  return (
      r'('
      + start_regex
      + r')\s*:(.*?)('
      + end_regex
      + r')\s*:'
  )


def make_case_decision_regex() -> str:
  regex_elements = [
    r'\s*'.join([char for char in marker]) + r'\s*(в\s*|л\s*а)'
    for marker in CASE_DECISION_START_MARKERS
  ]

  return (
      r'('
      + r'|'.join(regex_elements)
      + r')\s*:(.*?)'
      + '\s*'.join([char for char in CASE_DECISION_END_MARKER])
      + r'\s*:?'
  )


def make_case_form_regex(lowercase_word: str) -> str:
  return r'\s*'.join([
    char.strip()
    for char in lowercase_word.upper()
    if char.strip()
  ])


def is_fullname(attempt_input: Optional[str]) -> bool:
  if not attempt_input:
    return False
  return bool(re.match(FULLNAME_PATTERN, attempt_input))


def only_if_fullname(attempt_input: str) -> Optional[str]:
  return attempt_input if is_fullname(attempt_input) else None
