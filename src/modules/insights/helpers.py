import re
from datetime import date
from typing import Optional

from fuzzywuzzy import process
from src.utils.functional import remove_leading_zeros

import src.modules.regexs.helpers as reh

from src.modules.regexs.constants import MONTH_MARKERS
from src.modules.insights.constants import \
  ARTICLE_STR_LENGTH_LIMIT, \
  SCORE_CUTOFF, \
  OUTPUT_MATCHES_LIMIT, \
  PROCESS_MATCHES_LIMIT


def get_week_day(value: str) -> Optional[str]:
  date = capture_issue_date(value)

  return date.strftime('%A') if date else None


def capture_issue_date(value: str) -> Optional[date]:
  match = re.search(reh.define_date_pattern(value), value)

  if not match:
    return None

  groups = match.groups()
  (unparsed_day, unparsed_month, unparsed_year) = groups

  parsed_day = int(remove_leading_zeros(unparsed_day))
  parsed_month = parse_month(unparsed_month)
  parsed_year = int(unparsed_year)

  return date(year=parsed_year, month=parsed_month, day=parsed_day)


def eval_top_strings_freqs(strings: list[str]):
  log(f'totally {len(strings)} strings to process')

  strings_freqs = {}

  for string in strings:
    matches = process.extractBests(
      query=string,
      choices=strings,
      limit=PROCESS_MATCHES_LIMIT,
      score_cutoff=SCORE_CUTOFF
    )

    log(f'{matches}')

    for match in matches:
      strings_freqs.setdefault(match, 0)
      strings_freqs[match] += 1

  most_common_strings = sorted(
    strings_freqs.items(),
    key=lambda item: item[1],
    reverse=True
  )

  return most_common_strings[:OUTPUT_MATCHES_LIMIT]


def limit_articles(articles: list[str]) -> list[str]:
  return list(
    filter(
      lambda article: len(article) <= ARTICLE_STR_LENGTH_LIMIT,
      sorted(articles, key=lambda article: len(article))
    )
  )


def get_month_index(label: str) -> int:
  for index, marker in enumerate(MONTH_MARKERS, start=1):
    if label == marker:
      return index

  return -1


def parse_month(value: str) -> int:
  return get_month_index(value) \
    if reh.does_month_marker_occur(value) \
    else int(remove_leading_zeros(value))


def log(message: str) -> None:
  print(f'Insights: {message}')
