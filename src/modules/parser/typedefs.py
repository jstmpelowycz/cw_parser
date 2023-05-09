from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Commission:
  judge: Optional[str]
  prosecutor: Optional[str]
  clerk: Optional[str]


@dataclass
class CaseSentencing:
  description: Optional[str]
  penalty_sum: Optional[str]


class Sex(Enum):
  M = 'Masc'
  F = 'Fem'


@dataclass
class CaseParty:
  name: Optional[str]
  sex: Sex


@dataclass
class CasePartiesInfo:
  total: int
  parties: list[CaseParty]


@dataclass
class Sections:
  ruling: Optional[str]
  decision: Optional[str]


@dataclass
class ParsedDocument:
  case_form: Optional[str]
  commission: Commission
  issue_date: Optional[str]
  sentencing: CaseSentencing
  court_name: Optional[str]
  parties_info: CasePartiesInfo
  sections: Sections
  regulatory_framework: list[str]
