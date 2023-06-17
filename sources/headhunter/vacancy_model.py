"""Модель данных для вакансий для источника HeadHunter"""

__author__ = 'dd.sobolev'

from typing import Any, Dict
from datetime import datetime
from enums import Source
from sources.base.base_model import BaseVacancyModel
from utils.currency import CURRENCY
from utils.utils import extract_text_from_html


class HeadHunterVacancyModel(BaseVacancyModel):
    """Модель данных для вакансий для источника HeadHunter"""

    _source_id = Source.HeadHunter.value

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data=data)

    @property
    def title(self):
        """Заголовок вакансии"""
        return self._data.get('name')

    @property
    def schedule(self):
        """График работы"""
        schedule = self._data.get('schedule') or {}
        return schedule.get('name')

    @property
    def employment(self):
        """Тип занятости"""
        employment = self._data.get('employment') or {}
        return employment.get('name')

    @property
    def salary(self) -> str:
        """Информация о зарплате"""
        result_salary = 'Договорная'
        _salary = self._data.get('salary')
        if not _salary:
            return result_salary
        salary_from, salary_to = _salary['from'], _salary['to']
        currency_symbol = CURRENCY[self._source_id][_salary['currency']]
        # gross=True - это зарплата до вычета все налогов
        is_gross = 'до вычета налогов' if _salary['gross'] else 'на руки'
        if salary_from and salary_to:
            result_salary = f'{salary_from} - {salary_to} {currency_symbol} ({is_gross})'
        elif any((salary_from, salary_to)):
            salary = salary_from or salary_to
            result_salary = f'{salary} {currency_symbol} ({is_gross})'
        return result_salary

    @property
    def experience(self):
        """Необходимый опыт работы"""
        return self._data.get('experience', {}).get('name')

    @property
    def company_title(self):
        """Название компании"""
        return self._data.get('employer', {}).get('name')

    @property
    def requirements(self):
        """Требования к вакансии"""
        snippet = self._data.get('snippet') or {}
        requirements = snippet.get('requirement', '')
        return extract_text_from_html(requirements)

    @property
    def responsibilities(self):
        """Задачи (что нужно будет делать)"""
        snippet = self._data.get('snippet') or {}
        responsibilities = snippet.get('responsibility', '')
        return extract_text_from_html(responsibilities)

    @property
    def location(self):
        """Примерный адрес вакансии"""
        return self._data.get('area').get('name')

    @property
    def url(self):
        """Урл вакансии"""
        return self._data.get('alternate_url')

    @property
    def published_at(self):
        """Дата публикации"""
        _published_at = self._data.get('published_at')
        datetime_obj = datetime.fromisoformat(_published_at)
        return datetime(
            year=datetime_obj.year,
            month=datetime_obj.month,
            day=datetime_obj.day,
            hour=datetime_obj.hour,
            minute=datetime_obj.minute,
            second=datetime_obj.second,
        )
