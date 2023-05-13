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

CASE_RULING_START_MARKERS = [
  'встанови',
  'постанови',
]

CASE_DECISION_START_MARKERS = [
  'виріши',
  'ухвали',
]

CASE_DECISION_END_MARKER = 'суддя'

FULLNAME_PATTERN = re.compile(r'^[А-ЩЬЮЯІЇЄҐ][а-щьюяіїєґ\'’]+\s?[А-ЩЬЮЯІЇЄҐ]\.\s?[А-ЩЬЮЯІЇЄҐ]\.$')
REG_FRAMEWORK_PATTERN = re.compile(r'(пункт|частина|стаття).*України', re.MULTILINE | re.IGNORECASE)
UDP_GENDER_PATTERN = re.compile(r'(Neut|Masc|Fem)')
DECISION_STATUS_PATTERN = re.compile(r'(задовольнити|відмовити)', re.IGNORECASE)
PROSECUTOR_PATTERN = re.compile(r'прокурор', re.IGNORECASE)
CLERK_PATTERN = re.compile(r'секретар', re.IGNORECASE)
JUDGE_PATTERN = re.compile(r'судд', re.IGNORECASE)

NBSP_PATTERN = re.compile(r'\xA0')
UTF_START_BYTE_PATTERN = re.compile(r'\xd0')
FF_PATTERN = re.compile(r'\f')
HTTP_PATTERN = re.compile(r'https?://\S+')
NON_24_DATE_PATTERN = re.compile(r'\b\d+/\d+/\d+, \d+:\d+ [AP]M\b')
