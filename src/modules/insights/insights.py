from collections import Counter

from matplotlib import pyplot as plt
import src.modules.file_manager.file_manager as fm

from src.utils.functional import flatten
from src.modules.insights.helpers import eval_top_strings_freqs, get_week_day, limit_articles

from src.modules.parser.constants import SEX

from src.modules.insights.constants import \
  PRODUCT_INSIGHT_FILE, \
  WEEKDAYS, \
  TOP_ARTICLES_INSIGHT_FILE, \
  SEXES_DISTRIB_INSIGHT_FILE


class Insights:
  def __init__(self, dirname: str):
    self.dirname = dirname

    self.parsed_documents_jsons = fm.bulk_get_jsons(dirname, sorting=False, nonempty=True)

  def build_sexes_distribution_chart(self) -> None:
    parties = flatten([
      json.content['case_parties_info']['parties']
      for json in self.parsed_documents_jsons
    ])

    existing_sexes = [
      party['sex']
      for party in parties
      if party['sex']
    ]

    gender_counts = Counter(existing_sexes)

    men_count = gender_counts.get(SEX['M'], 0)
    women_count = gender_counts.get(SEX['F'], 0)

    counts = [men_count, women_count]

    plt.bar(['Men', 'Women'], counts)
    plt.xlabel('Sex')
    plt.ylabel('Count')
    plt.title('Distribution of Men and Women')

    for i, count in enumerate(counts):
      plt.text(i, count, str(count), ha='center', va='bottom')

    plt.savefig(SEXES_DISTRIB_INSIGHT_FILE)

  def build_productivity_chart(self) -> None:
    existing_issue_dates = [
      json.content['document_issue_date']
      for json in self.parsed_documents_jsons
      if json.content['document_issue_date']
    ]

    week_days = [
      get_week_day(unparsed_date)
      for unparsed_date in existing_issue_dates
      if get_week_day(unparsed_date)
    ]

    weekday_counts = {}

    for day in week_days:
      weekday_counts[day] = weekday_counts.get(day, 0) + 1

    weekday_counts = {
      day: weekday_counts.get(day, 0) for day in WEEKDAYS
    }

    x_values = range(len(WEEKDAYS))
    y_values = [weekday_counts[day] for day in WEEKDAYS]

    plt.bar(x_values, y_values)
    plt.xlabel("Weekdays")
    plt.ylabel("Occurrences")
    plt.title("Productivity by Weekday")
    plt.xticks(x_values, WEEKDAYS, rotation=45)
    plt.tight_layout()
    plt.savefig(PRODUCT_INSIGHT_FILE)

  def build_frequent_articles_chart(self) -> None:
    articles = flatten([
      json.content['document_regulatory_framework']
      for json in self.parsed_documents_jsons
    ])

    most_common_freqs = eval_top_strings_freqs(limit_articles(articles))

    article_names = [article[0] for article in most_common_freqs]
    freqs = [article[1] for article in most_common_freqs]

    plt.bar(article_names, freqs)
    plt.xlabel("Article")
    plt.ylabel("Frequency")
    plt.title("Most Frequent Articles")
    plt.xticks(rotation=90)
    plt.tight_layout(pad=50)
    plt.savefig(TOP_ARTICLES_INSIGHT_FILE)
