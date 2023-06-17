"""Загрузка и обработка данных с источника HeadHunter"""

__author__ = 'dd.sobolev'

from sources.base.json_parser import JSONParser


class HeadHunterVacancyParser(JSONParser):
    """Парсер данных с внешнего источника HeadHunter"""
