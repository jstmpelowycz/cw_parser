from dataclasses import dataclass


@dataclass
class IdentifiableFileRecord:
  id: str
  content: str


@dataclass
class IdentifiableJSON:
  id: str
  content: dict


@dataclass
class IdentifiablePath:
  id: str
  path: str
