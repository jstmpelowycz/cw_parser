from src.utils.decorators import make_logging_decorator

from src.modules.parser.regexs.constants import \
  NBSP_PATTERN, \
  FF_PATTERN, \
  HTTP_PATTERN, \
  NON_24_DATE_PATTERN, \
  UTF_START_BYTE_PATTERN


def normalize_text(text: str) -> str:
  modified_text = purify_text(text)
  modified_text = modified_text.replace('м.', 'місто ')
  modified_text = modified_text.replace('ст.', 'стаття ')
  modified_text = modified_text.replace('ч.', 'частина ')
  modified_text = modified_text.replace('п.', 'пункт ')

  return modified_text


def purify_text(text: str) -> str:
  modified_text = NBSP_PATTERN.sub(" ", text)
  modified_text = UTF_START_BYTE_PATTERN.sub(" ", modified_text)
  modified_text = FF_PATTERN.sub("", modified_text)
  modified_text = HTTP_PATTERN.sub("", modified_text)
  modified_text = NON_24_DATE_PATTERN.sub("", modified_text)

  return modified_text


def logging(message: str):
  return make_logging_decorator(log)(message)


def log(message: str):
  print(f'Parser: {message}')
