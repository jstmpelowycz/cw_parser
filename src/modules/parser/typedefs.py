from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class CourtCommission:
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
  sex: Optional[Sex]


@dataclass
class CasePartiesInfo:
  total: int
  parties: list[CaseParty]


@dataclass
class DocumentSections:
  ruling: Optional[str]
  decision: Optional[str]


@dataclass
class ParsedDocument:
  case_form: Optional[str]
  case_sentencing: CaseSentencing
  case_parties_info: CasePartiesInfo

  document_issue_date: Optional[str]
  document_sections: DocumentSections
  document_regulatory_framework: list[str]

  court_type: Optional[str]
  court_commission: CourtCommission
  court_location: Optional[str]
