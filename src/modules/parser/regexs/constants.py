import re

CASE_FORM_MARKERS = [
  'вирок',
  'постанова',
  'рішення',
  'судовий наказ',
  'ухвала',
  'окрема ухвала',
  'окрема думка',
  'додаткове рішення',
]

FULLNAME_REGEX = r'^[А-ЩЬЮЯІЇЄҐ][а-щьюяіїєґ\'’]+\s?[А-ЩЬЮЯІЇЄҐ]\.\s?[А-ЩЬЮЯІЇЄҐ]\.$'
FULLNAME_PATTERN = re.compile(FULLNAME_REGEX)

REG_FRAMEWORK_REGEX = r'(пункт|частина|стаття).*України'
REG_FRAMEWORK_PATTERN = re.compile(REG_FRAMEWORK_REGEX, re.MULTILINE | re.IGNORECASE)

UDP_GENDER_REGEX = r'(Neut|Masc|Fem)'
UDP_GENDER_PATTERN = re.compile(UDP_GENDER_REGEX)

NBSP_PATTERN = re.compile(r'\xA0')
FF_PATTERN = re.compile(r'\f')
HTTP_PATTERN = re.compile(r'https?://\S+')
NON_24_DATE_PATTERN = re.compile(r'\b\d+/\d+/\d+, \d+:\d+ [AP]M\b')
