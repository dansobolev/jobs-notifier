"""Базовая модель вакансии"""

__author__ = 'dd.sobolev'

from abc import ABC, abstractmethod
from typing import Any, Dict

from enums import Source


class BaseEntityModel(ABC):
    """Базовая модель сущности"""

    _fields = ()

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def get_dict(self):
        """Получить словарь с маппингом поле модели: значение"""
        return {key: getattr(self, key) for key in self._fields}


class BaseVacancyModel(BaseEntityModel):
    """Базовая модель сущности 'Вакансия'"""

    _source_id: int = NotImplemented
    _fields = (
        'title',
        'schedule',
        'employment',
        'salary',
        'experience',
        'company_title',
        'requirements',
        'responsibilities',
        'location',
        'url',
        'published_at',
        'source_name',
    )

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data=data)

    @property
    @abstractmethod
    def title(self):
        """Заголовок вакансии"""

    @property
    @abstractmethod
    def schedule(self):
        """График работы"""

    @property
    @abstractmethod
    def employment(self):
        """Тип занятости"""

    @property
    @abstractmethod
    def salary(self):
        """Информация о зарплате"""

    @property
    @abstractmethod
    def experience(self):
        """Необходимый опыт работы"""

    @property
    @abstractmethod
    def company_title(self):
        """Название компании"""

    @property
    @abstractmethod
    def requirements(self):
        """Требования к вакансии"""

    @property
    @abstractmethod
    def responsibilities(self):
        """Задачи (что нужно будет делать)"""

    @property
    @abstractmethod
    def location(self):
        """Примерный адрес вакансии"""

    @property
    @abstractmethod
    def url(self):
        """Урл вакансии"""

    @property
    @abstractmethod
    def published_at(self):
        """Дата публикации"""

    @property
    def source_name(self):
        """Название источника"""
        return str(Source(self._source_id))
