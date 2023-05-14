from dataclasses import dataclass

@dataclass
class MethodEfficiency:
  entity: str
  percentage: float


@dataclass
class ParserEfficiency:
  average_percentage: float
  methods_efficiencies: list[MethodEfficiency]