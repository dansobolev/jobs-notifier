"""Модуль для работы с переменными среды"""

__author__ = 'dd.sobolev'

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Класс для работы с конфигом всего приложения"""

    # telegram bot
    TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
    TG_CHAT_ID = os.getenv('TG_CHAT_ID')
