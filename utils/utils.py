"""Модуль с вспомогательыми функциями"""

__author__ = "dd.sobolev"

import re


def extract_text_from_html(html: str) -> str:
    """Достает текст из html-тега, сохраняя переносы строк

    Args:
        html: сырая html строка
    Returns:
        очищенный текст без html тегов
    """
    # если в строке нету ни одного html тега - просто вернем ее
    if not re.findall(r"<[^>]+>", html):
        return html
    # иначе избавимся от всех html тегов
    cleantext = re.sub(re.compile("<.*?>"), "", html)
    extracted_text = [
        element
        for element in [item_.strip() for item_ in cleantext.split("\n")]
        if element
    ]
    return "\n".join(extracted_text)
