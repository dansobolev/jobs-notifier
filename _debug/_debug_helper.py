"""Ручные тесты"""

from pprint import pprint
import json

from sources.headhunter.api_client import HeadHunterAPIClient
from sources.headhunter.processor import HeadHunterVacancyProcessor
from sources.headhunter.vacancy_model import HeadHunterVacancyModel
from sources.headhunter.vacancy_parser import HeadHunterVacancyParser
from telegram_bot.bot import tg_bot


class __DebugHelper:
    """Класс для локального отлаживаняи всего и вся"""

    _hh_api_client = HeadHunterAPIClient()

    def load_and_send_to_telegram(self):
        vacancies_path = r"C:\Users\danii\Desktop\Programming\jobs-notifier\_debug\test_one_vacancy.json"
        with open(vacancies_path, "r", encoding="utf-8") as file:
            content = file.read()
        vacancy_processor = HeadHunterVacancyProcessor(
            content=content,
            parser=HeadHunterVacancyParser,
            model=HeadHunterVacancyModel,
        )
        vacancy_entity = vacancy_processor.do_process()
        # print(vacancy_entity["published_at"])
        # pprint(vacancy_entity)
        tg_bot.moderate_publication(vacancy_entity)

    def get_vacancy_from_file(self):
        vacancies_path = r"C:\Users\danii\Desktop\Programming\jobs-notifier\_debug\hh_vacancies_pack.json"
        with open(vacancies_path, "r", encoding="utf-8") as file:
            content = file.read()
        loaded_content = HeadHunterVacancyParser().parse(content)

        one_vacancy = loaded_content[2]
        pprint(one_vacancy)
        # with open('test_one_vacancy.json', 'w', encoding='utf-8') as file:
        #     file.write(json.dumps(one_vacancy))
        #     print('written successfully')

    def load_pack_of_vacancies_and_save_to_json(self):
        vacancies = self._hh_api_client.find_vacancies()
        with open("hh_vacancies_pack.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(vacancies))

    def get_one_vacancy_from_hh(self):
        external_vacancy_id = "80664458"
        vacancy_data = self._hh_api_client.vacancy_read(external_vacancy_id)
        pprint(vacancy_data)


_debug_helper = __DebugHelper()
_debug_helper.load_and_send_to_telegram()
