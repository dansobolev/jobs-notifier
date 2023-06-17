"""JSON парсер для загрузки сущностей с внешних источников"""

__author__ = 'dd.sobolev'

from typing import Any, Dict, Union
import json
from sources.base.parser import Parser


class JSONParser(Parser):

    def _load_content(self, content: Union[str, Dict]) -> Dict[str, Any]:
        """"Загрузить (распарсить) данные"""
        # если к нам все таки пришел уже словарь, то не будем падать а просто вернем его
        if isinstance(content, dict):
            return content
        return json.loads(content)
