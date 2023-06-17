"""Загрузчик вакансий с HH по API"""

__author__ = "dd.sobolev"

import schedule
import time

from sources.headhunter.api_client import HeadHunterAPIClient
from sources.headhunter.processor import HeadHunterVacancyProcessor
from sources.headhunter.vacancy_model import HeadHunterVacancyModel
from sources.headhunter.vacancy_parser import HeadHunterVacancyParser
from telegram_bot.bot import tg_bot


# TODO: вынести в базовую сущность Scheduler - пока что написал просто чтобы проверить что работает


def vacancy_loader_job():
    hh_api_client = HeadHunterAPIClient()
    vacancies = hh_api_client.find_vacancies()
    for vacancy_content in vacancies[::-1]:
        vacancy_processor = HeadHunterVacancyProcessor(
            content=vacancy_content,
            parser=HeadHunterVacancyParser,
            model=HeadHunterVacancyModel,
        )
        vacancy_entity = vacancy_processor.do_process()
        tg_bot.moderate_publication(vacancy_entity)
        time.sleep(1)
        print("Вакансия обработана")


# schedule.every(1).minutes.do(vacancy_loader_job)


vacancy_loader_job()
