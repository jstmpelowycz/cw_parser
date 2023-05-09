import re
import src.modules.file_manager.file_manager as fm
import src.modules.udpipe_client.udpipe_client as uc
import src.modules.udpipe_client.helpers as uch
import src.modules.parser.regexs.helpers as reh

from typing import Optional

from src.modules.parser.bert_qa.bert_qa import BertQaModelClient
from src.modules.parser.helpers import logging, normalize_text
from src.modules.parser.regexs.constants import REG_FRAMEWORK_PATTERN
from src.modules.parser.typedefs import ParsedDocument, Commission, CaseSentencing, CasePartiesInfo, CaseParty, Sections

from src.modules.parser.constants import DOCUMENT_PATH, PROCESSED_DOCUMENT_PATH, DOCUMENT_SENTENCES_PATH


class Parser:
  def __init__(self, path: str) -> None:
    self.path = path
    self.parsed_document: Optional[ParsedDocument] = None

    self.__commit_document()
    self.__process_with_udp()
    self.__init_qa_model_client()

  @logging('parsing document...')
  def parse(self) -> ParsedDocument:
    if not self.parsed_document:
      self.parsed_document = ParsedDocument(
        case_form=self.find_case_form(),
        commission=self.find_commission(),
        issue_date=self.find_document_issue_date(),
        court_name=self.find_court_name(),
        sentencing=self.find_case_sentencing(),
        parties_info=self.find_parties_info(),
        sections=self.find_document_sections(),
        regulatory_framework=self.find_regulatory_framework(),
      )

    return self.parsed_document

  @logging('parsing case form...')
  def find_case_form(self) -> Optional[str]:
    return

  @logging('parsing commission...')
  def find_commission(self) -> Commission:
    return Commission(
      judge=self.find_judge(),
      prosecutor=self.find_prosecutor(),
      clerk=self.find_clerk(),
    )

  @logging('parsing parties info...')
  def find_parties_info(self) -> CasePartiesInfo:
    total = self.find_case_parties_total()
    parties = self.find_case_parties(total)

    return CasePartiesInfo(total, parties)

  @logging('parsing case sentencing...')
  def find_case_sentencing(self) -> CaseSentencing:
    return CaseSentencing(
      description=self.find_case_sentencing_description(),
      penalty_sum=self.find_case_sentencing_penalty_sum(),
    )

  @logging('parsing document sections...')
  def find_document_sections(self) -> Sections:
    return Sections(
      ruling=self.find_case_ruling(),
      decision=self.find_case_decision(),
    )

  @logging('parsing regulatory framework...')
  def find_regulatory_framework(self) -> list[str]:
    matches_iter = re.finditer(REG_FRAMEWORK_PATTERN, self.document)
    framework = [match.group() for match in matches_iter]

    return framework

  @logging('parsing case parties total...')
  def find_case_parties_total(self) -> int:
    matches = re.findall(r'ОСОБА_\d+', self.document)
    count = len(set(matches))

    return count

  @logging('parsing case parties...')
  def find_case_parties(self, count: int) -> list[CaseParty]:
    pass

  @logging('parsing case ruling...')
  def find_case_ruling(self):
    pass

  @logging('parsing case decision...')
  def find_case_decision(self) -> Optional[str]:
    pass

  @logging('parsing case sentencing description...')
  def find_case_sentencing_description(self) -> Optional[str]:
    pass

  @logging(message='parsing case sentencing penalty sum...')
  def find_case_sentencing_penalty_sum(self) -> Optional[str]:
    pass

  def find_court_type(self) -> Optional[str]:
    return self.qa_client.ask('Який це тип суду?')

  def find_document_issue_date(self) -> Optional[str]:
    return self.qa_client.ask('Перша дата після іменем України?')

  def find_document_articles(self) -> Optional[str]:
    return self.qa_client.ask('Які правові норми згадані в тексті?')

  def find_judge(self) -> Optional[str]:
    return reh.if_fullname(self.qa_client.ask('ПІБ головуючого судді?'))

  def find_prosecutor(self) -> Optional[str]:
    return reh.if_fullname(self.qa_client.ask('ПІБ прокурора?'))

  def find_clerk(self) -> Optional[str]:
    return reh.if_fullname(self.qa_client.ask('ПІБ секретаря?'))

  def find_court_name(self) -> Optional[str]:
    return self.qa_client.ask('Де розташований суд?')

  @logging('initializing QA model client...')
  def __init_qa_model_client(self) -> None:
    self.qa_client = BertQaModelClient(context=self.document)

  @logging('committing document...')
  def __commit_document(self) -> None:
    raw_document_content = fm.read_pdf(self.path)
    normalized_document_content = normalize_text(raw_document_content)

    fm.write_to_file(path=DOCUMENT_PATH, content=normalized_document_content)

    self.document = normalized_document_content

  @logging('processing with UDPipe, mapping to sentences...')
  def __process_with_udp(self) -> None:  # noqa
    uc.process(src_path=DOCUMENT_PATH, dst_path=PROCESSED_DOCUMENT_PATH, locally=False)

    processed_document = fm.read_json(path=PROCESSED_DOCUMENT_PATH)
    raw_udp_result = uch.get_udp_result(processed_document)
    sentences = uc.make_sentences_from_udp_result(raw_udp_result)

    sentences_dict = [uch.sentence_to_dict(sentence) for sentence in sentences]

    fm.write_to_json(path=DOCUMENT_SENTENCES_PATH, data=sentences_dict)
