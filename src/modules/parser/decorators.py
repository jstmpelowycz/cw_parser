from typing import Optional

from src.modules.parser.typedefs import DocumentSectionType


class WithSectionContext:
  def __init__(self, section_type: DocumentSectionType) -> None:
    self.section_type = section_type

    self.instance: Optional = None
    self.document_context: Optional[str] = None
    self.section_context: Optional[str] = None

  def __call__(self, func):
    def wrapped_func(instance, *args, **kwargs):
      self.instance = instance
      self.document_context = self.instance.document
      self.section_context = self.instance.get_section(section_type=self.section_type)

      if self.section_context:
        self.instance.qa_client.reset_context(context=self.section_context)

      return func(self.instance, *args, **kwargs)

    if self.section_context:
      self.instance.qa_client.reset_context(context=self.document_context)

    return wrapped_func
