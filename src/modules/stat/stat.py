import matplotlib.pyplot as plt

from operator import itemgetter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud

import src.modules.file_manager.file_manager as fm
import src.modules.stat.lemmatizer.lemmatizer as lm

from src.modules.stat.typedefs import TfIdf
from src.modules.file_manager.file_manager import IdentifiableJSON, IdentifiableFileRecord

from src.constants.paths import ANALYSIS_DATA_DIR_PATH, STATS_PAIRS_DATA_DIR_PATH, STATS_COMMON_DATA_DIR_PATH
from src.modules.stat.constants import \
  BARH_MAX_WORDS_COUNT, CLOUD_MAX_WORDS_COUNT, \
  UGTF_CLOUD_FILE, UGIDF_CLOUD_FILE, \
  UGTF_BARH_FILE, UGIDF_BARH_FILE, \
  BGIDF_BARH_FILE, BGTF_BARH_FILE
from src.modules.stat.helpers import get_ngram_range, get_bg_range_on_ug, resolve_axes


def build_charts() -> None:
  (ug_tf, ug_idf, bg_tf, bg_idf) = evaluate()
  build_cloud(
    freqs=ug_tf,
    title='Unigrams TF cloud',
    savefig=UGTF_CLOUD_FILE,
    reverse=True
  )
  build_cloud(
    freqs=ug_idf,
    title='Unigrams IDF cloud',
    savefig=UGIDF_CLOUD_FILE,
    reverse=False
  )
  build_barh(
    freqs=ug_tf,
    title='Unigrams TF bars',
    savefig=UGTF_BARH_FILE,
    reverse=True
  )
  build_barh(
    freqs=ug_idf,
    title='Unigrams IDF bars',
    savefig=UGIDF_BARH_FILE,
    reverse=False
  )
  build_barh(
    freqs=bg_tf,
    title='Bigrams TF bars',
    savefig=BGTF_BARH_FILE,
    reverse=True
  )
  build_barh(
    freqs=bg_idf,
    title='Bigrams IDF bars',
    savefig=BGIDF_BARH_FILE,
    reverse=False
  )


def parse_and_write_lemmas() -> None:
  jsons = fm.bulk_get_jsons(ANALYSIS_DATA_DIR_PATH, sorting=False, nonempty=True)

  bulk_write_lemmas_to_files(jsons)
  bulk_write_lemmas_to_common_file(jsons)


def bulk_write_lemmas_to_common_file(jsons: list[IdentifiableJSON]) -> None:
  all_lemmas = ''

  for json in jsons:
    next_lemmas_portion = lm.map_upd_result_to_plain_lemmas(json.content)
    all_lemmas += next_lemmas_portion + '\n'

  fm.write_to_file(STATS_COMMON_DATA_DIR_PATH, all_lemmas)


def bulk_write_lemmas_to_files(jsons: list[IdentifiableJSON]) -> None:
  for json in jsons:
    joined_lemmas = lm.map_upd_result_to_plain_lemmas(json.content)

    fm.write_record_to_file(
      dirname=STATS_PAIRS_DATA_DIR_PATH,
      record=IdentifiableFileRecord(id=json.id, content=joined_lemmas),
      ext='txt',
    )


def build_barh(
    freqs: dict,
    title: str,
    savefig: str,
    reverse: bool,
) -> None:
  sorted_freqs = sorted(freqs.items(), key=itemgetter(1), reverse=reverse)

  sorted_freqs = sorted(
    sorted_freqs[:BARH_MAX_WORDS_COUNT],
    key=itemgetter(1),
    reverse=(not reverse)
  )

  plt.figure(figsize=(10, 10))

  (xs, ys) = resolve_axes(sorted_freqs)
  plt.barh(xs, ys)

  plt.tight_layout(pad=10)
  plt.ylabel('N-gram')
  plt.xlabel(f'{title} value')
  plt.title(title)
  plt.savefig(savefig)


def build_cloud(
    freqs: dict,
    title: str,
    savefig: str,
    reverse: bool,
) -> None:
  wordcloud_inst = WordCloud(
    width=1000,
    height=1000,
    background_color='white',
    min_font_size=10,
    max_words=CLOUD_MAX_WORDS_COUNT
  )

  wordcloud = wordcloud_inst.generate_from_frequencies(freqs, reverse=reverse)

  plt.figure(figsize=(15, 15))
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.tight_layout(pad=0)
  plt.title(f'{title} results')
  plt.savefig(savefig)


def evaluate() -> TfIdf:
  records = fm.bulk_get_files_records(STATS_PAIRS_DATA_DIR_PATH, '*.txt')

  tf_unigrams = fm.read_txt(STATS_COMMON_DATA_DIR_PATH)
  idf_unigrams = map_records_content_list(records)
  tf_bigrams = parse_list_to_bigrams(tf_unigrams.split('\n'))
  idf_bigrams = parse_list_to_bigrams(idf_unigrams)

  ug_tf = calculate_ngrams_tf(tf_unigrams, use_bigrams=False)
  ug_idf = calculate_ngrams_idf(idf_unigrams, use_bigrams=False)
  bg_tf = calculate_ngrams_tf('\n'.join(tf_bigrams), use_bigrams=True)
  bg_idf = calculate_ngrams_idf(idf_bigrams, use_bigrams=True)

  return ug_tf, ug_idf, bg_tf, bg_idf


def map_records_content_list(records: list[IdentifiableFileRecord]) -> list[str]:
  return list(map(lambda record: record.content, records))


def parse_list_to_bigrams(unigrams: list[str]) -> list[str]:
  bigrams = []
  range = get_bg_range_on_ug(unigrams)

  for index in range:
    bigram = f'{unigrams[index]} {unigrams[index + 1]}'

    bigrams.append(bigram)

  return bigrams


def calculate_ngrams_idf(ngrams: list[str], use_bigrams: bool) -> dict:
  ngram_range = get_ngram_range(use_bigrams)
  vectorizer = TfidfVectorizer(use_idf=True, ngram_range=ngram_range)

  vectorizer.fit(ngrams)
  idf_values = vectorizer.idf_
  terms = vectorizer.get_feature_names_out()

  idf = dict(zip(terms, idf_values))

  return idf


def calculate_ngrams_tf(ngrams: str, use_bigrams: bool) -> dict:
  vectorizer = CountVectorizer(
    ngram_range=get_ngram_range(use_bigrams)
  )

  term_matrix = vectorizer.fit_transform([ngrams])
  tf_values = term_matrix.toarray()[0]
  terms = vectorizer.get_feature_names_out()

  tf = dict(zip(terms, tf_values))

  return tf
