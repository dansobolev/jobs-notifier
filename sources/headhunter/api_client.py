"""API клиент для источника HeadHunter"""

__author__ = 'dd.sobolev'

from typing import Any, Dict, Optional, List, Union
from sources.base.api_client import BaseHTTPClient


class HeadHunterAPIClientException(Exception):
    """HeadHunter вернул ответ > 200"""


class HeadHunterAPIClient(BaseHTTPClient):
    """API клиент для источника HeadHunter"""

    __base_url = 'https://api.hh.ru/'
    __find_vacancies_url = 'vacancies/'

    def find_vacancies(self, search_words: Optional[str] = 'Python') -> List[Dict[str, Any]]:
        """Находит вакансии (пока что только по ключевому слову Python"""
        vacancies = self.request(
            url=f'{self.__base_url}{self.__find_vacancies_url}',
            query_params={
                'order_by': 'publication_time',
                'responses_count_enabled': True,
                'text': search_words,
                # поля в которых будет происходить поиск по ключевому слову
                'vacancy_search_fields': 'name, description',
            }
        )
        # FIXME: add more status codes handlers
        if vacancies.status_code > 200:
            raise HeadHunterAPIClientException("HeadHunter вернул ответ > 200")
        return vacancies.json()['items']

    def vacancy_read(self, vacancy_id: Union[str, int]) -> Dict[str, Any]:
        """Получение одной вакансии по vacancy_id"""
        vacancy = self.request(
            url=f'{self.__base_url}{self.__find_vacancies_url}{vacancy_id}'
        )
        # FIXME: add more status codes handlers
        if vacancy.status_code > 200:
            raise HeadHunterAPIClientException("HeadHunter вернул ответ > 200")
        return vacancy.json()
