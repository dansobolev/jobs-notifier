"""Основной модуль для бота в телеграме"""

__author__ = "dd.sobolev"

from dataclasses import dataclass
from typing import Any, Dict
from telebot import TeleBot

from utils.config import Config

_BOT_NAME = "Job Seeker"
_BOT_USER_NAME = "@jobs\_seeker\_bot"


_VACANCY_MESSAGE_FORMAT = (
    "[{title}]({url}) - {source_name}\n"
    "{schedule_employment}\n"
    "*ЗП:* {salary}\n"
    "*Опыт:* {experience}\n"
    "*Локация:* {location}\n"
    "*Компания:* {company_title}\n\n"
    "*Требования:* {requirements}\n\n"
    "*Задачи:* {responsibilities}\n\n"
    "*Дата публикации:* {published_at}\n\n"
    "by {bot_name}"
)


@dataclass
class __JobSeekerTelegramBot:
    """Класс для работы с ботом в Телеграм"""

    token: str = Config.TG_BOT_TOKEN
    chat_id: int = Config.TG_CHAT_ID

    def __post_init__(self):
        self.__bot = TeleBot(self.token)

    def send_vacancy_message(self, vacancy: Dict[str, Any]):
        """Отправить сообщение через бота в ТГ"""
        self.__bot.send_message(
            chat_id=self.chat_id,
            text=self.__construct_vacancy_message(vacancy),
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )

    def __construct_vacancy_message(self, vacancy: Dict[str, Any]) -> str:
        """Сконструировать сообщение, которое будет опубликовано в телеграме"""
        self.__fill_schedule_employment(vacancy)
        self.__fill_meta_info(vacancy)
        return _VACANCY_MESSAGE_FORMAT.format(**vacancy)

    def moderate_publication(self, vacancy: Dict[str, Any]):
        """Модерация публикации перед отправкой в канал"""
        # vacancy_message = self.__construct_vacancy_message(vacancy)

    @staticmethod
    def __fill_schedule_employment(vacancy: Dict[str, Any]):
        """Заполнить расписание и занятость"""
        schedule = vacancy.pop("schedule")
        employment = vacancy.pop("employment")
        schedule_employment = list({schedule, employment} - {None})
        # TODO: fix
        if len(schedule_employment) > 1:
            schedule_employment = ", ".join([schedule, employment])
        else:
            schedule_employment = (
                schedule_employment[0] if schedule_employment else "Полная занятость"
            )
        vacancy.update({"schedule_employment": schedule_employment})

    @staticmethod
    def __fill_meta_info(vacancy: Dict[str, Any]):
        """Заполнить мета информацию (полезные ссылки и тд)"""
        vacancy["bot_name"] = _BOT_USER_NAME


tg_bot = __JobSeekerTelegramBot()
