"""Модуль для работы с разными валютами"""

__author__ = 'dd.sobolev'

from enums import Source

CURRENCY = {
    Source.HeadHunter.value: {
        'USD': '$',
        'EUR': '€',
        'RUR': '₽',
    }
}
