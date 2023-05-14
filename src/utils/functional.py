def rounded(value: float):
  return round(value, 3)

def flatten(list):
  return [item for sublist in list for item in sublist]

def is_list_empty(list: list) -> bool:
  return len(list) == 0

def remove_leading_zeros(string):
  return string.lstrip('0')