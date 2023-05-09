from typing import Optional

from src.modules.parser.bert_qa.constants import ANSWER_SCORE_THRESH


def thresholded(output: dict) -> Optional[str]:
  if output['score'] <= ANSWER_SCORE_THRESH:
    return None

  return output['answer']


def normalize_answer(text: str) -> str:
  modified_text = text.strip()
  modified_text = modified_text.replace('\n', ' ')

  return modified_text
