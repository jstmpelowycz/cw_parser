from json import JSONDecodeError
from typing import Optional

from src.utils.decorators import make_delayed_decorator
import src.modules.udpipe_client.script_runner.script_runner as sr

from src.modules.udpipe_client.typedefs import Sentence, SentenceMember

from src.modules.udpipe_client.constants import \
  UDP_EXEC_CODES, \
  IS_UDP_RUNNING_SH_PATH, \
  UDP_PROCESS_ENDPOINTS, \
  AWAITING_START_DURATION

from src.modules.udpipe_client.constants import \
  NEWPAR_MARKER, SENT_ID_MARKER, SENT_TEXT_MARKER, \
  NON_EXTRA_COMMENT_START_INDEX, SUB_DELIMITER_MARKER, \
  NON_SENT_INFO_START_INDEX, SENT_ID_INDEX, SENT_TEXT_INDEX, REQUIRED_INFO_INDICES


def sentence_to_dict(sentence: Sentence) -> dict:
  data = []
  for member in sentence.data:
    member_dict = {
      "id": member.id,
      "word": member.word,
      "lemma": member.lemma,
      "type": member.type,
      "features": member.features,
      "ref_id": member.ref_id,
      "pos": member.pos
    }
    data.append(member_dict)
  sentence_dict = {
    "id": sentence.id,
    "sentence": sentence.sentence,
    "data": data
  }
  return sentence_dict


def map_semistruct_to_sentences(semistruct_records: list[list[str]]) -> list[Sentence]:
  sentences: list[Sentence] = []

  for record in semistruct_records:
    data: list[SentenceMember] = []
    sentence_id, sentence = get_sent_info(record)

    for line in record[NON_SENT_INFO_START_INDEX:]:
      data.append(make_sent_member(line))

    sentences.append(
      Sentence(id=int(sentence_id), sentence=sentence, data=data)
    )

  return sentences


def make_sent_member(record_line: str) -> SentenceMember:
  word_payload = record_line.split('\t')

  return SentenceMember(
    id=int(word_payload[REQUIRED_INFO_INDICES[0]]),
    word=word_payload[REQUIRED_INFO_INDICES[1]],
    lemma=word_payload[REQUIRED_INFO_INDICES[2]],
    type=word_payload[REQUIRED_INFO_INDICES[3]],
    features=word_payload[REQUIRED_INFO_INDICES[4]],
    ref_id=int(word_payload[REQUIRED_INFO_INDICES[5]]),
    pos=word_payload[REQUIRED_INFO_INDICES[6]],
  )


def get_sent_info(record: list[str]) -> [str, str]:
  sentence_id = record[SENT_ID_INDEX].replace(SENT_ID_MARKER, '')
  sentence = record[SENT_TEXT_INDEX].replace(SENT_TEXT_MARKER, '')

  return sentence_id, sentence


def sub_split_into_semistruct(lines: list[str]) -> list[list[str]]:
  sublists = []
  current_sublist = []

  for line in lines:
    if line == SUB_DELIMITER_MARKER:
      sublists.append(current_sublist)
      current_sublist = []
    else:
      current_sublist.append(line)
  sublists.append(current_sublist)
  sublists = [sublist for sublist in sublists if sublist]

  return sublists


def filter_extra_comments(lines: list[str]) -> list[str]:
  return list(
    filter(
      lambda line: NEWPAR_MARKER not in line,
      lines[NON_EXTRA_COMMENT_START_INDEX:]
    )
  )


def get_udp_result(json: dict) -> Optional[str]:
  try:
    return json['result']
  except JSONDecodeError:
    return None


def define_parser(locally: bool) -> str:
  return UDP_PROCESS_ENDPOINTS[
    'local' if locally else 'remote'
  ]


def is_udp_running():
  exec_code = sr.run_script(IS_UDP_RUNNING_SH_PATH)
  return (
    True if exec_code == UDP_EXEC_CODES['RUNNING_SUCCESS']
    else False
  )


def is_process_request_succeeded(exec_code: int) -> bool:
  return exec_code == UDP_EXEC_CODES['PROCESS_REQUEST_SUCCESS']


def throw(message):
  raise Exception(format_message(message))


def log(message: str):
  print(format_message(message))


def format_message(message: str) -> str:
  return f'UDPipe client: {message}'


delayed = make_delayed_decorator(AWAITING_START_DURATION)
