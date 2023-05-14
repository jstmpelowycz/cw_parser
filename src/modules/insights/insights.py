import src.modules.file_manager.file_manager as fm
from src.modules.insights.helpers import eval_top_strings_freqs, get_week_day
from src.modules.parser.parser import Parser
from src.utils.functional import flatten


class Insights:
  def __init__(self, dirname: str, dst_path: str):
    self.dirname = dirname
    self.dst_path = dst_path

    self.parsed_documents_jsons = fm.bulk_get_jsons(dirname, sorting=False, nonempty=True)

  def find_major_sex(self) -> str:
    parties = flatten([
      json.content['case_parties_info']['parties']
      for json in self.parsed_documents_jsons
    ])

    existing_sexes = [
      party['sex']
      for party in parties
      if party['sex']
    ]

    return Parser.defined_major_sex(sexes=existing_sexes)

  def build_productivity_chart(self) -> None:
    existing_issue_dates = flatten([
      json.content['document_issue_date']
      for json in self.parsed_documents_jsons
      if json.content['document_issue_date']
    ])

    week_days = [
      get_week_day(unparsed_date)
      for unparsed_date in existing_issue_dates
    ]

  def build_frequent_articles_chart(self) -> None:
    articles = flatten([
      json.content['document_regulatory_framework']
      for json in self.parsed_documents_jsons
    ])

    most_common_freqs = eval_top_strings_freqs(articles)
