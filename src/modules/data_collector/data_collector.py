import os
import requests
from urllib import request
from requests import Response

from src.constants.paths import DATA_DIR_PATH
from src.modules.data_collector.constants import SEARCHER_ENDPOINTS, SEARCHER_DEFAULT_HEADERS


def get_and_download_doc(id: int) -> None:
  doc = get_doc(id)
  download_doc(doc)


def bulk_get_and_download_docs(ids: list[int]) -> None:
  [get_and_download_doc(id) for id in ids]


def bulk_download_docs(docs: list[dict]) -> None:
  [download_doc(doc) for doc in docs]


def bulk_get_docs(ids: list[int]) -> list[dict]:
  docs = [get_doc(id) for id in ids]

  return docs


def request_doc(id: int) -> Response:
  url = f'{SEARCHER_ENDPOINTS["FULL_DOCUMENT"]}/{id}'

  response = requests.get(
    url=url,
    headers=SEARCHER_DEFAULT_HEADERS,
  )

  return response


def get_doc(id: int) -> dict:
  response = request_doc(id)

  return response.json()[0]


def download_doc(doc: dict) -> None:
  os.chdir(DATA_DIR_PATH)

  id = doc.get('id')
  url = doc.get('doc_url')

  if not url:
    return

  try:
    request.urlretrieve(url, f'{id}.rtf')
  except Exception:  # noqa
    throw(f'error occurred while retrieving URL, {url}')


def throw(message):
  raise Exception(f'DataCollector: {message}')
