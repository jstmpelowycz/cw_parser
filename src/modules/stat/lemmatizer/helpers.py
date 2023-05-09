import re

from src.modules.stat.lemmatizer.constants import TYPE_INDEX, LEMMA_INDEX, COMMENT_MARKER


def get_type(result_item: list[str]) -> str:
  return result_item[TYPE_INDEX]


def get_lemma(result_item: list[str]) -> str:
  return result_item[LEMMA_INDEX]


def filter_valid_lemmas(lemmas: list[str]) -> filter:
  return filter(is_valid_line, lemmas)


def filter_empty(filterable: list[str]) -> list[str]:
  return list(filter(None, filterable))


def filter_comments(filterable: list[str]) -> list[str]:
  return list(
    filter(
      lambda line: line[0] != COMMENT_MARKER,
      filterable
    )
  )


def is_valid_line(line: str) -> bool:
  if has_non_valid_char(line):
    return False

  if has_digit_and_char(line):
    return False

  if is_single_letter(line):
    return False

  if line.isdigit():
    return False

  return True


def has_non_valid_char(string: str) -> bool:
  pattern = r'[%№|]+'

  if re.search(pattern, string):
    return True

  return False


def has_digit_and_char(string: str) -> bool:
  has_digit = False
  has_char = False

  for char in string:
    if char.isdigit():
      has_digit = True

    elif char.isalpha():
      has_char = True

  return has_digit and has_char


def is_single_letter(string: str) -> bool:
  return len(string) == 1


def as_string_or_int(value: str) -> str or int:
  return int(value) if value.isdigit() else value
