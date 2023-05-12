import re
from typing import Optional, Pattern, Match

import src.modules.file_manager.file_manager as fm
import src.modules.udpipe_client.udpipe_client as uc
import src.modules.udpipe_client.helpers as uch
import src.modules.parser.regexs.helpers as reh

from src.modules.parser.bert_qa.bert_qa import BertQaModelClient
from src.modules.parser.decorators import WithSectionContext
from src.modules.parser.helpers import logging, normalize_text

from src.modules.parser.regexs.constants import \
  REG_FRAMEWORK_PATTERN, \
  CASE_FORM_MARKERS, \
  UDP_GENDER_PATTERN

from src.modules.parser.typedefs import \
  ParsedDocument, \
  CourtCommission, \
  CaseSentencing, CasePartiesInfo, CaseParty, Sex, \
  DocumentSections, DocumentSectionType

from src.modules.parser.constants import DOCUMENT_PATH, PROCESSED_DOCUMENT_PATH, DOCUMENT_SENTENCES_PATH


class Parser:
  def __init__(self, path: str) -> None:
    self.path = path

    self.parsed_document: Optional[ParsedDocument] = None
    self.document_sections: Optional[DocumentSections] = None

    self.__commit_document()
    self.__process_with_udp()
    self.__init_qa_model_client()

  def parse(self) -> ParsedDocument:
    if not self.parsed_document:
      self.parsed_document = ParsedDocument(
        document_sections=self.find_document_sections(),
        document_issue_date=self.find_document_issue_date(),
        document_regulatory_framework=self.find_document_regulatory_framework(),
        case_form=self.find_case_form(),
        case_sentencing=self.find_case_sentencing(),
        case_parties_info=self.find_case_parties_info(),
        court_type=self.find_court_type(),
        court_commission=self.find_court_commission(),
        court_location=self.find_court_location(),
      )

    return self.parsed_document

  @logging('parsing document sections...')
  def find_document_sections(self) -> DocumentSections:
    if not self.document_sections:
      self.document_sections = DocumentSections(
        header=self.find_case_header(),
        ruling=self.find_case_ruling(),
        decision=self.find_case_decision(),
      )

    return self.document_sections

  @logging('parsing document issue date...')
  @WithSectionContext(section_type=DocumentSectionType.Header)
  def find_document_issue_date(self) -> Optional[str]:
    return self.qa_client.ask('Перша дата після іменем України?')

  @logging('parsing regulatory framework...')
  def find_document_regulatory_framework(self) -> list[str]:
    matches_iter = re.finditer(REG_FRAMEWORK_PATTERN, self.document)
    framework = [match.group() for match in matches_iter]

    return framework

  @logging('parsing case form...')
  @WithSectionContext(section_type=DocumentSectionType.Header)
  def find_case_form(self) -> Optional[str]:
    for case_form_id, case_form_pattern in enumerate(reh.make_case_form_patterns()):
      if self.__search(case_form_pattern):
        return CASE_FORM_MARKERS[case_form_id]

  @logging('parsing case sentencing...')
  def find_case_sentencing(self) -> CaseSentencing:
    return CaseSentencing(
      description=self.find_case_sentencing_description(),
      penalty_sum=self.find_case_sentencing_penalty_sum(),
    )

  @logging('parsing parties info...')
  def find_case_parties_info(self) -> CasePartiesInfo:
    total = self.find_case_parties_total()
    parties = self.find_case_parties(total)

    return CasePartiesInfo(total, parties)

  @logging('parsing court type...')
  def find_court_type(self) -> Optional[str]:
    pass

  @logging('parsing court commission...')
  @WithSectionContext(section_type=DocumentSectionType.Header)
  def find_court_commission(self) -> CourtCommission:
    return CourtCommission(
      judge=self.find_court_judge(),
      prosecutor=self.find_court_prosecutor(),
      clerk=self.find_court_clerk(),
    )

  @logging('parsing court location...')
  @WithSectionContext(section_type=DocumentSectionType.Header)
  def find_court_location(self) -> Optional[str]:
    return self.qa_client.ask('Де розташований суд?')

  def find_case_sentencing_description(self) -> Optional[str]:
    pass

  def find_case_sentencing_penalty_sum(self) -> Optional[str]:
    pass

  def find_case_parties_total(self) -> int:
    matches = re.findall(r'ОСОБА_\d+', self.document)
    count = len(set(matches))

    return count

  def find_case_parties(self, count: int) -> list[CaseParty]:
    case_parties: list[CaseParty] = []

    case_parties_with_assumed_genders = self.__assume_case_parties_genders(count)

    for party_name, assumed_genders in case_parties_with_assumed_genders.items():
      sex = Parser.__defined_major_sex(assumed_genders)

      case_parties.append(CaseParty(name=party_name, sex=sex))

    return case_parties

  def __assume_case_parties_genders(self, count: int) -> dict[str, list[str]]:
    case_parties_with_assumed_genders = dict()

    for party_id in range(1, count + 1):
      party_name_to_find = f'ОСОБА_{party_id}'
      assumed_genders = []

      for sentence in self.sentences:
        if party_name_to_find in sentence.sentence:
          for member in sentence.data:
            if member.word == party_name_to_find:
              assumed_gender_match = re.search(UDP_GENDER_PATTERN, member.features)

              if assumed_gender_match:
                assumed_gender = assumed_gender_match.group()

                assumed_genders.append(assumed_gender)

      case_parties_with_assumed_genders[party_name_to_find] = assumed_genders

    return case_parties_with_assumed_genders

  @staticmethod
  def __defined_major_sex(assumed_genders: list[str]) -> Sex:
    masc_count = assumed_genders.count(str(Sex.M.value))
    fem_count = assumed_genders.count(str(Sex.F.value))

    if masc_count > fem_count:
      sex = Sex.M
    elif masc_count < fem_count:
      sex = Sex.F
    else:
      sex = None

    return sex

  def find_case_ruling(self) -> Optional[str]:
    return self.__find_by_pattern(reh.make_case_ruling_pattern())

  def find_case_decision(self) -> Optional[str]:
    return self.__find_by_pattern(reh.make_case_decision_pattern())

  def find_case_header(self) -> Optional[str]:
    return self.__find_by_pattern(reh.make_case_header_pattern())

  def find_court_judge(self) -> Optional[str]:
    return reh.only_if_fullname(self.qa_client.ask('ПІБ головуючого судді?'))

  def find_court_prosecutor(self) -> Optional[str]:
    return reh.only_if_fullname(self.qa_client.ask('ПІБ прокурора?'))

  def find_court_clerk(self) -> Optional[str]:
    return reh.only_if_fullname(self.qa_client.ask('ПІБ секретаря?'))

  def get_section(self, section_type: DocumentSectionType) -> Optional[str]:
    if section_type == DocumentSectionType.Header:
      return self.document_sections.header

    if section_type == DocumentSectionType.Ruling:
      return self.document_sections.ruling

    return self.document_sections.decision

  def __find_by_pattern(self, pattern: Pattern[str]) -> Optional[str]:
    match = self.__search(pattern)

    if not match:
      return None

    desc_sorted_groups = sorted(
      match.groups(),
      key=lambda group: len(group) if group else 0,
      reverse=True,
    )

    desired_group = desc_sorted_groups[0]

    return desired_group.strip()

  def __search(self, pattern: Pattern) -> Match:
    return re.search(pattern, self.document)

  @logging('committing document...')
  def __commit_document(self) -> None:
    raw_document_content = fm.read_pdf(self.path)
    normalized_document_content = normalize_text(raw_document_content)

    fm.write_to_file(path=DOCUMENT_PATH, content=normalized_document_content)

    self.document = normalized_document_content

  @logging('initializing QA model client...')
  def __init_qa_model_client(self) -> None:
    self.qa_client = BertQaModelClient(context=self.document)

  @logging('processing with UDPipe, mapping to sentences...')
  def __process_with_udp(self) -> None:  # noqa
    uc.process(src_path=DOCUMENT_PATH, dst_path=PROCESSED_DOCUMENT_PATH, locally=False)

    processed_document = fm.read_json(path=PROCESSED_DOCUMENT_PATH)
    raw_udp_result = uch.get_udp_result(processed_document)

    self.sentences = uc.make_sentences_from_udp_result(raw_udp_result)

    sentences_dict = [
      uch.sentence_to_dict(sentence)
      for sentence in self.sentences
    ]

    fm.write_to_json(path=DOCUMENT_SENTENCES_PATH, data=sentences_dict)
