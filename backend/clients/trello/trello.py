import os

import requests

from backend.clients.abstract import Client
from backend.data.ticket import Ticket


class TrelloClient(Client):
    API_KEY = None
    TOKEN = None

    BOARD_NAME = os.environ.get("TRELLO_BOARD_NAME")
    BOARD_ID = os.environ.get("TRELLO_BOARD_ID")
    LIST_NAME = os.environ.get("TRELLO_LIST_NAME")
    LIST_ID = os.environ.get("TRELLO_LIST_ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.API_KEY = os.environ.get("TRELLO_API_KEY")
        self.TOKEN = os.environ.get("TRELLO_API_TOKEN")

    def get_boards(self) -> list[dict]:
        url = f"https://api.trello.com/1/members/me/boards"

        query = {
            "fields": "name",
        }

        boards = self.request(url, query)
        return boards

    def get_lists(self, board_name: str = BOARD_NAME, board_id: str = BOARD_ID) -> list[dict]:
        if not board_id and not board_name:
            raise ValueError("Board Name or Board ID must be provided")

        if not board_id:
            board_id = [board["id"] for board in self.get_boards() if board["name"] == board_name][0]

        url = f"https://api.trello.com/1/boards/{board_id}/lists"

        query = {
            "fields": "name",
        }

        lists = self.request(url, query)
        return lists

    def get_cards(self, list_name: str = LIST_NAME, list_id: str = LIST_ID, fields: list = None) -> list[dict]:
        if not list_name and not list_id:
            raise ValueError("List Name or List ID must be provided")

        if not list_id:
            list_id = [list["id"] for list in self.get_lists() if list["name"] == list_name][0]

        if not fields:
            fields = ["id", "name", "desc"]

        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        cards = self.request(url, query={"fields": ",".join(fields)})
        return cards

    def get_tickets(self) -> list[Ticket]:
        cards = self.get_cards()

        tickets = [Ticket(card["id"], card["name"], card["desc"]) for card in cards]
        return tickets