"""Базовый http клиент для загрузки данных с внешних источников"""

__author__ = "dd.sobolev"

from typing import Any, Dict, Optional
import requests


class BaseHTTPClient:
    def __init__(
        self,
        timeout: Optional[int] = 10,
    ):
        self.timeout = timeout

    def request(
        self,
        url: str,
        query_params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        body: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        cookies: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        """Выполнить запрос через библиотеку requests"""
        client = requests.Session()
        return client.request(
            method=method,
            url=url,
            params=query_params,
            data=body,
            headers=headers,
            timeout=timeout or self.timeout,
            cookies=cookies,
        )
