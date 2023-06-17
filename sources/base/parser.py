"""Базовый парсер для сущностей со сторонних источников"""

__author__ = 'dd.sobolev'

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Parser(ABC):

    def __init__(self, extra: Optional[Dict[str, Any]] = None):
        self._extra = extra or {}

    def parse(self, content: Any) -> Dict[str, Any]:
        """Парсинг сущности"""
        self._preprocess_extra(self._extra)
        loaded_content = self._load_content(content)
        self._validate(loaded_content)
        self._postprocess_extra(self._extra)
        return loaded_content

    def _preprocess_extra(self, extra_data: Dict[str, Any]):
        """Пре обработка экстра данных"""

    @abstractmethod
    def _load_content(self, content: Any) -> Dict[str, Any]:
        """Загрузить (распарсить) данные"""

    def _validate(self, content: Dict[str, Any]) -> bool:
        """Валидация контента"""

    def _postprocess_extra(self, extra_data: Dict[str, Any]):
        """Постобработка экстра данных после загрузки данных и валдации"""
