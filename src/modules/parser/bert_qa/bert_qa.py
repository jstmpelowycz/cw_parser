import os
from typing import Optional

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

from src.modules.parser.bert_qa.constants import QA_MODEL_NAME, PIPELINE_TASK_TYPE, CACHE_DIR_PATH
from src.modules.parser.bert_qa.helpers import thresholded, normalize_answer


class BertQaModelClient:
  def __init__(self, context: str) -> None:
    self.context = context

    self.__attach_cache()
    self.__init_tokenizer()
    self.__init_model()
    self.__init_pipeline()

  def ask(self, question: str) -> Optional[str]:
    output = self.pipeline(context=self.context, question=question)  # noqa
    answer = thresholded(output)

    if not answer:
      return None

    return normalize_answer(answer) if answer else None

  def reset_context(self, context: str) -> None:
    self.context = context

  def __init_tokenizer(self) -> None:
    self.tokenizer = AutoTokenizer.from_pretrained(QA_MODEL_NAME, cache_dir=self.cache_dir)

  def __init_model(self) -> None:
    self.model = AutoModelForQuestionAnswering.from_pretrained(QA_MODEL_NAME, cache_dir=self.cache_dir)

  def __init_pipeline(self):
    self.pipeline = pipeline(PIPELINE_TASK_TYPE, model=self.model, tokenizer=self.tokenizer)

  def __attach_cache(self):
    self.cache_dir = os.environ['HF_HOME'] = CACHE_DIR_PATH
