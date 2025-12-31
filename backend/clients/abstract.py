from typing import Any
from abc import ABC
from enum import Enum

import requests


class Client(ABC):
    class METHODS(Enum):
        GET = "GET"
        POST = "POST"

    API_KEY = None
    TOKEN = None

    HEADERS = {
        "Content-Type": "application/json",
    }

    @property
    def _query_params(self) -> dict[str, str]:
        return {
            "key": self.API_KEY,
            "token": self.TOKEN,
        }

    def request(self, urL: str, query: dict[str, Any] = None, method = METHODS.GET.value) -> list:
        if not self.API_KEY or not self.TOKEN:
            raise ValueError("API_KEY and TOKEN must be set")

        if not query:
            query = {}

        query_params = self._query_params | query

        response = requests.request(
            method=method,
            url=urL,
            params=query_params,
            headers=self.HEADERS
        )
        return response.json()
