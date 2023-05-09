import os

import src.modules.udpipe_client.script_runner.script_runner as sr

from src.modules.udpipe_client.constants import UDP_MODEL_NAME, START_UDP_SH_PATH, STOP_UDP_SH_PATH
from src.modules.udpipe_client.helpers import filter_extra_comments, sub_split_into_semistruct, \
  map_semistruct_to_sentences, define_parser, is_process_request_succeeded, throw, is_udp_running, log, delayed
from src.modules.udpipe_client.typedefs import Sentence


def make_sentences_from_udp_result(raw_udp_result: str) -> list[Sentence]:
  lines = raw_udp_result.split('\n')
  no_extra_comment_lines = filter_extra_comments(lines)
  semistruct_records = sub_split_into_semistruct(no_extra_comment_lines)
  sentences = map_semistruct_to_sentences(semistruct_records)

  return sentences


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
