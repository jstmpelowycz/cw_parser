from typing import Optional
from dataclasses import asdict

from matplotlib import pyplot as plt
import src.modules.file_manager.file_manager as fm
from src.utils.functional import is_list_empty, flatten, rounded

from src.modules.eff_analyzer.typedefs import ParserEfficiency, MethodEfficiency
from src.modules.eff_analyzer.constants import PARSER_EFF_FILE


class ParserEfficiencyAnalyzer:
  def __init__(self, dirname: str, dst_path: str):
    self.dirname = dirname
    self.dst_path = dst_path

    self.parser_eff: Optional[ParserEfficiency] = None

    self.parsed_documents_count = fm.get_files_count(dirname)
    self.parsed_documents_jsons = fm.bulk_get_jsons(dirname, sorting=False, nonempty=True)

  def analyze(self) -> None:
    self.__eval_eff_results()
    self.__commit_results()
    self.__build_chart()

  def __commit_results(self) -> None:
    fm.write_to_json(path=self.dst_path, data=asdict(self.parser_eff))

  def __build_chart(self) -> None:
    method_names = [
      method.entity
      for method in self.parser_eff.methods_efficiencies
    ]
    efficiencies = [
      method.percentage
      for method in self.parser_eff.methods_efficiencies
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(method_names, efficiencies)
    plt.xlabel('Methods')
    plt.ylabel('Efficiency')
    plt.title(f'Parser efficiency — {self.parser_eff.average_percentage}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(PARSER_EFF_FILE)

    plt.show()

  def __eval_eff_results(self) -> None:
    document_header_section_eff, \
    document_ruling_section_eff, \
    document_decision_section_eff \
      = self.document_sections()

    court_judge_eff, \
    court_prosecutor_eff, \
    court_clerk_eff \
      = self.court_commission()

    document_issue_date_eff = self.document_issue_date()
    document_reg_framework_eff = self.document_regulatory_framework()
    document_decision_status_eff = self.document_decision_status()

    case_form_eff = self.case_form()
    case_parties_sexes_eff = self.case_parties_sexes()
    court_location_eff = self.court_location()

    effs = [
      document_header_section_eff,
      document_ruling_section_eff,
      document_decision_section_eff,
      document_issue_date_eff,
      document_reg_framework_eff,
      document_decision_status_eff,
      case_form_eff,
      case_parties_sexes_eff,
      court_judge_eff,
      court_prosecutor_eff,
      court_clerk_eff,
      court_location_eff,
    ]

    self.parser_eff = ParserEfficiency(
      average_percentage=self.__eval_average_percentage(effs),
      methods_efficiencies=effs,
    )

  def document_sections(self) -> [MethodEfficiency, MethodEfficiency, MethodEfficiency]:
    nonempty_headers_count = 0
    nonempty_rulings_count = 0
    nonempty_decisions_count = 0

    for json in self.parsed_documents_jsons:
      sections = json.content['document_sections']

      if sections['header']:
        nonempty_headers_count += 1
      if sections['ruling']:
        nonempty_rulings_count += 1
      if sections['decision']:
        nonempty_decisions_count += 1

    return [
      MethodEfficiency(
        entity='document_sections_header',
        percentage=self.__compare_to_general_count(nonempty_headers_count),
      ),
      MethodEfficiency(
        entity='document_sections_ruling',
        percentage=self.__compare_to_general_count(nonempty_rulings_count),
      ),
      MethodEfficiency(
        entity='document_sections_decision',
        percentage=self.__compare_to_general_count(nonempty_decisions_count)
      )
    ]

  def document_issue_date(self) -> MethodEfficiency:
    nonempty_issue_dates_count = 0

    for json in self.parsed_documents_jsons:
      issue_date = json.content['document_issue_date']

      if issue_date:
        nonempty_issue_dates_count += 1

    return MethodEfficiency(
      entity='document_issue_date',
      percentage=self.__compare_to_general_count(nonempty_issue_dates_count)
    )

  def document_regulatory_framework(self) -> MethodEfficiency:
    nonempty_frameworks_count = 0

    for json in self.parsed_documents_jsons:
      framework = json.content['document_regulatory_framework']

      if not is_list_empty(framework):
        nonempty_frameworks_count += 1

    return MethodEfficiency(
      entity='document_regulatory_framework',
      percentage=self.__compare_to_general_count(nonempty_frameworks_count)
    )

  def document_decision_status(self) -> MethodEfficiency:
    nonempty_statuses_count = 0

    for json in self.parsed_documents_jsons:
      status = json.content['document_decision_status']
      sections = json.content['document_sections']

      if status and sections['decision']:
        nonempty_statuses_count += 1

    return MethodEfficiency(
      entity='document_decision_status',
      percentage=self.__compare_to_general_count(nonempty_statuses_count),
    )

  def case_form(self) -> MethodEfficiency:
    nonempty_forms_count = 0

    for json in self.parsed_documents_jsons:
      form = json.content['case_form']

      if form:
        nonempty_forms_count += 1

    return MethodEfficiency(
      entity='case_form',
      percentage=self.__compare_to_general_count(nonempty_forms_count),
    )

  def case_parties_sexes(self) -> MethodEfficiency:
    parties_total_count = sum([
      int(json.content['case_parties_info']['total'])
      for json in self.parsed_documents_jsons
    ])

    parties = flatten([
      json.content['case_parties_info']['parties']
      for json in self.parsed_documents_jsons
    ])

    nonempty_sexes_count = 0

    for party in parties:
      if party['sex']:
        nonempty_sexes_count += 1

    return MethodEfficiency(
      entity='case_parties_info_sex',
      percentage=rounded(nonempty_sexes_count / parties_total_count)
    )

  def court_commission(self) -> [MethodEfficiency, MethodEfficiency, MethodEfficiency]:
    nonempty_judges_count = 0
    nonempty_prosecutors_count = 0
    nonempty_clerks_count = 0

    for json in self.parsed_documents_jsons:
      commission = json.content['court_commission']
      sections = json.content['document_sections']

      judge = commission['judge']
      prosecutor = commission['prosecutor']
      clerk = commission['clerk']

      if judge and sections['header']:
        nonempty_judges_count += 1
      if prosecutor and sections['header']:
        nonempty_prosecutors_count += 1
      if clerk and sections['header']:
        nonempty_clerks_count += 1

    return [
      MethodEfficiency(
        entity='court_commission_judge',
        percentage=self.__compare_to_general_count(nonempty_judges_count),
      ),
      MethodEfficiency(
        entity='court_commission_prosecutor',
        percentage=self.__compare_to_general_count(nonempty_prosecutors_count),
      ),
      MethodEfficiency(
        entity='court_commission_clerk',
        percentage=self.__compare_to_general_count(nonempty_clerks_count)
      )
    ]

  def court_location(self) -> MethodEfficiency:
    nonempty_locations_count = 0

    for json in self.parsed_documents_jsons:
      location = json.content['court_location']

      if location:
        nonempty_locations_count += 1

    return MethodEfficiency(
      entity='court_location',
      percentage=self.__compare_to_general_count(nonempty_locations_count),
    )

  def __compare_to_general_count(self, value) -> float:
    return rounded(value / self.parsed_documents_count)

  @staticmethod
  def __eval_average_percentage(effs: list[MethodEfficiency]) -> float:
    effs_percentages = [eff.percentage for eff in effs]

    return rounded(sum(effs_percentages) / len(effs_percentages))
