"""Основной модуль для бота в телеграме"""

__author__ = "dd.sobolev"

from dataclasses import dataclass
from typing import Any, Dict

from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import TeleBot, types
from telebot.custom_filters import AdvancedCustomFilter

from enums import VacancyModerateOptionEnum
from utils.config import Config


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

# FIXME: какой-то бред
moderate_vacancy_factory = CallbackData('moderate_type', prefix='moderate_vacancy')


@dataclass
class __JobSeekerTelegramBot:
    """Класс для работы с ботом в Телеграм"""

    token: str = Config.TG_BOT_TOKEN
    moderator_chat_id: int = Config.TG_MODERATOR_CHAT_ID
    channel_chat_id: int = Config.TG_CHANNEL_CHAT_ID

    def __post_init__(self):
        self.__bot: TeleBot = TeleBot(self.token)
        self.__register_callbacks()

    def send_vacancy_message(self, vacancy: Dict[str, Any]):
        """Отправить сообщение через бота в ТГ"""
        self.__bot.send_message(
            chat_id=self.moderator_chat_id,
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
        self.__bot.send_message(
            chat_id=self.moderator_chat_id,
            text=self.__construct_vacancy_message(vacancy),
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=self.__moderate_keyboard(),
        )

    def __moderate_keyboard(self):
        """Вернуть настройки клавиатуры для модерации"""
        return types.InlineKeyboardMarkup(
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Опубликовать',
                        callback_data=moderate_vacancy_factory.new(
                            moderate_type=VacancyModerateOptionEnum.ACCEPT.value
                        ),
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text='Не подходит',
                        callback_data=moderate_vacancy_factory.new(
                            moderate_type=VacancyModerateOptionEnum.DECLINE.value
                        ),
                    )
                ]
            ]
        )

    def __resolved_keyboard(self):
        return types.InlineKeyboardMarkup(
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text='Вакансия успешно обработана',
                        callback_data='already_moderated'
                    )
                ]
            ]
        )

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
        vacancy["bot_name"] = Config.BOT_USER_NAME

    # TODO: need to be replace
    @property
    def bot(self):
        return self.__bot

    def __register_callbacks(self):
        """Регистрация callback хэндлеров"""
        # accept callback handler
        @self.__bot.callback_query_handler(
            func=None,
            config=moderate_vacancy_factory.filter()
        )
        def _accept_vacancy_callback(call: types.CallbackQuery):
            """Коллбэк на публикаицю вакансии в канал"""
            self.__accept_vacancy_callback(call)

        @self.__bot.callback_query_handler(
            func=lambda c: c.data == 'already_moderated'
        )
        def _vacancy_already_moderated_callback(call: types.CallbackQuery):
            """Callback при повторном нажатии на кнопку Вакансия успешно обработана"""
            self.__vacancy_already_moderated_callback(call)

    def __accept_vacancy_callback(self, call: types.CallbackQuery):
        """Коллбэк на публикаицю вакансии в канал"""
        callback_data: dict = moderate_vacancy_factory.parse(callback_data=call.data)
        moderate_vacancy_state = str(VacancyModerateOptionEnum(int(callback_data['moderate_type'])))
        vacancy_information_with_status = (
            f'*СТАТУС ВАКАНСИИ:* {moderate_vacancy_state}\n\n'
            f'{call.message.text}'
        )
        self.__bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=vacancy_information_with_status,
            reply_markup=self.__resolved_keyboard(),
            parse_mode="Markdown",
        )

    def __vacancy_already_moderated_callback(self, call: types.CallbackQuery):
        """Коллбэк в случае если мы отмодерировали вакансию и пытаемся
            нажать на кнопку 'Вакансия успешно обработана'"""
        self.__bot.answer_callback_query(
            callback_query_id=call.id,
            text='Вакансия уже отмодерирована',
        )


tg_bot = __JobSeekerTelegramBot()


class ModerateVacancyCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


if __name__ == '__main__':
    tg_bot.bot.add_custom_filter(ModerateVacancyCallbackFilter())
    tg_bot.bot.infinity_polling()
