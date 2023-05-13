from dataclasses import dataclass
from enum import Enum
from typing import Optional, Pattern

FindOption = Pattern or str


class DocumentSectionType(Enum):
  Header = 1
  Ruling = 2
  Decision = 3


@dataclass
class CourtCommission:
  judge: Optional[str]
  prosecutor: Optional[str]
  clerk: Optional[str]


@dataclass
class CaseParty:
  name: Optional[str]
  sex: Optional[str]


@dataclass
class CasePartiesInfo:
  total: int
  parties: list[CaseParty]


@dataclass
class DocumentSections:
  header: Optional[str]
  ruling: Optional[str]
  decision: Optional[str]


@dataclass
class ParsedDocument:
  document_sections: DocumentSections
  document_issue_date: Optional[str]
  document_regulatory_framework: list[str]

  case_form: Optional[str]
  case_parties_info: CasePartiesInfo

  court_commission: CourtCommission
  court_location: Optional[str]

  document_decision_status: Optional[str]
