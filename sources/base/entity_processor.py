"""Базовый процессор для сущности"""

__author__ = "dd.sobolev"

from dataclasses import dataclass
from typing import Any, Type

from sources.base.base_model import BaseEntityModel
from sources.base.parser import Parser


class BaseProcessor:
    """Базовый процессор сущности"""


@dataclass(frozen=True)
class VacancyProcessor(BaseProcessor):
    """Процессор для сущности 'Вакансия'"""

    content: Any
    parser: Type[Parser]
    model: Type[BaseEntityModel]

    def do_process(self):
        parsed_data = self.parser().parse(self.content)
        model_dictionary = self.model(parsed_data).get_dict()
        return model_dictionary
