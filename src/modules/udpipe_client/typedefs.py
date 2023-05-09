from dataclasses import dataclass


@dataclass
class SentenceMember:
  id: int
  word: str
  lemma: str
  type: str
  features: str
  ref_id: int
  pos: str


@dataclass
class Sentence:
  id: int
  sentence: str
  data: list[SentenceMember]
