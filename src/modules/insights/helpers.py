import re
from datetime import date
from fuzzywuzzy import process
from src.utils.functional import remove_leading_zeros

import src.modules.regexs.helpers as reh

from src.modules.insights.constants import MATCHES_LIMIT, DEF_MATCH_SCORE
from src.modules.regexs.constants import MONTH_MARKERS


def get_week_day(value: str) -> str:
  return capture_issue_date(value).strftime('%A')


def capture_issue_date(value: str) -> date:
  match = re.search(reh.define_date_pattern(value), value)
  groups = match.groups()
  (unparsed_day, unparsed_month, unparsed_year) = groups

  parsed_day = int(remove_leading_zeros(unparsed_day))
  parsed_month = parse_month(unparsed_month)
  parsed_year = int(unparsed_year)

  return date(year=parsed_year, month=parsed_month, day=parsed_day)


def eval_top_strings_freqs(strings: list[str]):
  strings_freqs = {}

  for string in strings:
    matches = process.extract(string, strings, limit=MATCHES_LIMIT)

    for match, score in matches:
      if score > DEF_MATCH_SCORE:
        strings_freqs.setdefault(match, 0)
        strings_freqs[match] += 1

  most_common_strings = sorted(
    strings_freqs.items(),
    key=lambda item: item[1],
    reverse=True
  )

  return most_common_strings[:MATCHES_LIMIT]


def get_month_index(label: str) -> int:
  for index, marker in enumerate(MONTH_MARKERS, start=1):
    if label == marker:
      return index

  return -1


def parse_month(value: str) -> int:
  return get_month_index(value) \
    if reh.does_month_marker_occur(value) \
    else int(remove_leading_zeros(value))
