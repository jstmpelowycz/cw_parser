def resolve_axes(freqs: list[dict]):
  return [
    [
      f'{item[0]} ({round(item[1], 2)})',
      item[1]
    ]
    for item in freqs
  ]


def get_bg_range_on_ug(unigrams: list[str]):
  return range(0, len(unigrams), 2)


def get_ngram_range(use_bigrams: bool) -> (int, int):
  return (2, 2) if use_bigrams else (1, 1)
