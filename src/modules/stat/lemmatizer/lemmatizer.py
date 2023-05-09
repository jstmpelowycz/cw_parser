from json import JSONDecodeError

from src.modules.stat.lemmatizer.helpers import \
  get_lemma, get_type, as_string_or_int, \
  filter_empty, filter_comments, filter_valid_lemmas

from src.modules.stat.lemmatizer.constants import INCLUSIVE_TAGS, REQUIRED_ITEMS_INDICES


def map_upd_result_to_plain_lemmas(content: dict) -> str:
  lemmas = get_lemmas_from_content(content)
  valid_lemmas = filter_valid_lemmas(lemmas)
  joined_valid_lemmas = '\n'.join(valid_lemmas)

  return joined_valid_lemmas


def get_lemmas_from_content(content: dict) -> list[str] or None:
  udp_result = get_udp_result(content)
  parsed_result = get_parsed_result(udp_result)
  only_required_lines = get_with_inclusive_tags(parsed_result)
  lemmas = bulk_get_lemmas(only_required_lines)

  return lemmas


def get_parsed_result(udp_result: str) -> list[list[str]]:
  lines = filter_empty(udp_result.split('\n'))
  no_comment_lines = filter_comments(lines)

  all_result_items = [
    filter_empty(line.split('\t'))
    for line in no_comment_lines
  ]

  required_result_items = [
    [as_string_or_int(item[index]) for index in REQUIRED_ITEMS_INDICES]
    for item in all_result_items
  ]

  return required_result_items


def get_with_inclusive_tags(p_result: list[list[str]]) -> list[list[str]]:
  return list(
    filter(
      lambda item: get_type(item) in INCLUSIVE_TAGS,
      p_result
    )
  )


def bulk_get_lemmas(p_result: list[list[str]]) -> list[str]:
  return [get_lemma(item) for item in p_result]


def get_udp_result(json: dict) -> str or None:
  try:
    return json['result']
  except JSONDecodeError:
    return None
