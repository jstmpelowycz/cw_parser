import os

from src.modules.udpipe_client.typedefs import Sentence

import src.modules.file_manager.file_manager as fm
import src.modules.udpipe_client.script_runner.script_runner as sr

from src.modules.udpipe_client.helpers import \
  filter_extra_comments, \
  sub_split_into_semistruct, \
  map_semistruct_to_sentences, \
  define_parser, \
  is_process_request_succeeded, \
  is_udp_running, \
  delayed, \
  throw, \
  log

from src.modules.udpipe_client.constants import UDP_MODEL_NAME, START_UDP_SH_PATH, STOP_UDP_SH_PATH
from src.constants.paths import TXT_DATA_DIR_PATH, ANALYSIS_DATA_DIR_PATH


def make_sentences_from_udp_result(raw_udp_result: str) -> list[Sentence]:
  lines = raw_udp_result.split('\n')
  no_extra_comment_lines = filter_extra_comments(lines)
  semistruct_records = sub_split_into_semistruct(no_extra_comment_lines)
  sentences = map_semistruct_to_sentences(semistruct_records)

  return sentences


def bulk_process_by_paths() -> None:
  paths = fm.get_parsed_paths(TXT_DATA_DIR_PATH, '*.txt')

  start()
  [process_by_path(path.path) for path in paths]
  stop()


def process_by_path(in_file_path: str) -> None:
  out_file_path = get_dst_file_path(in_file_path)

  process(in_file_path, out_file_path, locally=True)


def get_dst_file_path(src_file_path: str) -> str:
  file_id = fm.get_file_id(src_file_path)

  return f'{ANALYSIS_DATA_DIR_PATH}/{file_id}.json'


def start():
  stop()
  sr.run_script_separately(START_UDP_SH_PATH)
  verify_running()


def stop():
  sr.run_script_separately(STOP_UDP_SH_PATH)
  verify_stopped()


def process(src_path: str, dst_path: str, locally=False) -> None:
  exec_code = os.system(
    'curl --silent '
    f'-F model={UDP_MODEL_NAME} -F tokenizer= -F tagger= '
    f'-F data=@{src_path} '
    f'-F parser= {define_parser(locally)} > {dst_path}'
  )
  if not is_process_request_succeeded(exec_code):
    throw('failed to run!')


@delayed
def verify_running():
  if not is_udp_running():
    throw('nothing running, ensure it is on')
  else:
    log('fine, running')


@delayed
def verify_stopped():
  if is_udp_running():
    throw('still running, ensure it is off')
  else:
    log('fine, stopped')
