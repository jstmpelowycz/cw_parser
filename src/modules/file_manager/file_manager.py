import json
import os
from glob import glob
from json import JSONDecodeError
from typing import Any
from striprtf import striprtf
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from src.modules.file_manager.constants import PDF_FILE_MARKER, TXT_FILE_MARKER
from src.modules.file_manager.typedefs import IdentifiablePath, IdentifiableJSON, IdentifiableFileRecord


def map_to_identifiable_path(path: str) -> IdentifiablePath:
  return IdentifiablePath(
    id=get_file_id(path),
    path=path
  )


def get_parsed_paths(dirname: str, pattern: str) -> list[IdentifiablePath]:
  raw_paths = get_paths(dirname, pattern)
  mapped_paths = get_mapped_paths(raw_paths)
  sorted_paths = get_sorted_paths(mapped_paths)

  return sorted_paths


def get_mapped_paths(raw_paths: list[str]) -> list[IdentifiablePath]:
  return list(map(map_to_identifiable_path, raw_paths))


def get_sorted_paths(m_paths: list[IdentifiablePath]) -> list[IdentifiablePath]:
  return sorted(m_paths, key=lambda m_path: int(m_path.id))


def get_paths(dirname: str, pattern: str) -> list[str]:
  paths_in_dir = f'{dirname}/{pattern}'

  return glob(paths_in_dir)


def get_file_id(path: str) -> str:
  slash_split_path = path.split('/')
  filename = slash_split_path[-1]

  period_split_filename = filename.split('.')
  file_id = period_split_filename[0]

  return file_id


def get_files_count(dirname: str, pattern: str = '*') -> int:
  files_paths = get_paths(dirname, pattern)

  return len(files_paths)


def read_json(path: str) -> dict or None:
  try:
    with open(path, 'r') as json_file:
      json_dict = json.load(json_file)
      json_file.close()

    return json_dict
  except JSONDecodeError:
    return None


def read_file(path: str) -> str:
  if PDF_FILE_MARKER in path:
    return read_pdf(path)
  elif TXT_FILE_MARKER in path:
    return read_txt(path)
  else:
    throw('file format is not acceptable!')


def read_txt(path: str) -> str:
  try:
    with open(path, 'r', encoding='utf-8') as file:
      lines = file.readlines()
      file.close()

    content = ' '.join(map(str, lines))

    return content
  except:  # noqa
    throw(f'cannot read file, {path}')


def read_pdf(path: str) -> str:
  try:
    manager = PDFResourceManager()
    buffer = StringIO()
    converter = TextConverter(manager, buffer, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    with open(path, 'rb') as file:
      pages = PDFPage.get_pages(file, caching=True, check_extractable=True)

      [interpreter.process_page(page) for page in pages]

      text = buffer.getvalue()

    converter.close()
    buffer.close()

    return text
  except:  # noqa
    throw(f'cannot read PDF file, {path}')


def bulk_get_jsons(dirname: str, sorting: bool, nonempty: bool) -> list[IdentifiableJSON]:
  jsons = []
  pattern_with_dir = f'{dirname}/*.json'

  for path in glob(pattern_with_dir):
    jsons.append(
      IdentifiableJSON(
        id=get_file_id(path),
        content=read_json(path)
      )
    )

  if sorting:
    jsons = sorted(jsons, key=lambda json: int(json.id))

  if nonempty:
    jsons = list(filter(lambda json: json.content is not None, jsons))

  return jsons


def bulk_get_files_records(
    dirname: str,
    pattern: str
) -> list[IdentifiableFileRecord]:
  records = []
  pattern_with_dir = f'{dirname}/{pattern}'

  for path in glob(pattern_with_dir):
    records.append(
      IdentifiableFileRecord(
        id=get_file_id(path),
        content=read_txt(path)
      )
    )

  return records


def write_record_to_file(
    record: IdentifiableFileRecord,
    dirname: str,
    ext: str
) -> None:
  filename = f'{record.id}.{ext}'
  path = f'{dirname}/{filename}'

  write_to_file(path, record.content)


def write_to_file(path: str, content: str):
  try:
    with open(path, 'w') as file:
      file.write(content)
      file.close()
  except:  # noqa
    throw(f'cannot write to file, {path}')


def write_to_json(path: str, data: Any):
  try:
    with open(path, 'w', encoding='utf-8') as file:
      json.dump(data, file, ensure_ascii=False)
      file.close()
  except:  # noqa
    throw(f'cannot write to json, {path}')


def bulk_write_records_to_files(
    records: list[IdentifiableFileRecord],
    dirname: str,
    ext: str,
) -> None:
  [
    write_record_to_file(record, dirname, ext)
    for record in records
  ]


def delete_file(path: str) -> bool:
  try:
    os.remove(as_absolute_path(path))
    return True
  except Exception as error:
    throw(error.__str__())
    return False


def process_rtf_to_text(
    record: IdentifiableFileRecord
) -> IdentifiableFileRecord:
  try:
    return IdentifiableFileRecord(
      id=record.id,
      content=striprtf.rtf_to_text(record.content)
    )
  except:  # noqa
    throw(f'cannot process from RTF, file id {record.id}')


def as_absolute_path(path: str) -> str:
  rt_cwd = os.getcwd()

  return f'{rt_cwd}/{path}'


def throw(message: str):
  raise Exception(f'FileManager: {message}')
