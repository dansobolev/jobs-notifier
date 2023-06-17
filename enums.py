"""Модуль для работы с enums"""

__author__ = "dd.sobolev"


from enum import Enum, IntEnum


class Source(IntEnum):
    """Идентификаторы работных источников"""
    HeadHunter = 1

    def __str__(self):
        return HumanReadableSourceEnum[self.name].value


class HumanReadableSourceEnum(Enum):
    """Человекочитаемое название стороннего источника"""
    HeadHunter = "HeadHunter"


class VacancyModerateOptionEnum(Enum):
    """Опции при модерации вакансии"""
    DECLINE = 0
    ACCEPT = 1

    def __str__(self):
        return HumanReadableVacancyModerateOption[self.name].value


class HumanReadableVacancyModerateOption(Enum):
    """Человекочитаемые опции при модерации вакансии"""
    DECLINE = 'Отклонено'
    ACCEPT = 'Опубликовано'
