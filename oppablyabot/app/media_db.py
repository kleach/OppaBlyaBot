import logging
from enum import Enum
from typing import Dict
import sqlite3

log = logging.getLogger('MediaLinksDB')

sqlite3.Connection()


class MediaLinksDB:
    class LinkType(str, Enum):
        Joined = 'joined'
        Left = 'left'

    _NOT_UPLOADED_VALUE = ''

    _db: Dict[int, Dict[LinkType, str]]

    def __init__(self):
        self._db = {}

    def has_chat(self, chat_id: int) -> bool:
        res = chat_id in self._db.keys()

        log.info(f'chat {chat_id} present: {res}')

        return res

    def add_chat(self, chat_id: int):
        if self.has_chat(chat_id):
            return

        self._db[chat_id] = {
            MediaLinksDB.LinkType.Joined: MediaLinksDB._NOT_UPLOADED_VALUE,
            MediaLinksDB.LinkType.Left: MediaLinksDB._NOT_UPLOADED_VALUE,
        }

        log.info(f'chat {chat_id} added')

    def has_link(self, chat_id: int, key: LinkType) -> bool:
        if not self.has_chat(chat_id):
            return False

        res = self._db[chat_id][key] != MediaLinksDB._NOT_UPLOADED_VALUE

        log.info(f'chat {chat_id} has link for {key}: {res}')

        return res

    def add_link(self, chat_id: int, key: LinkType, link: str):
        if not self.has_chat(chat_id):
            self.add_chat(chat_id)

        self._db[chat_id][key] = link

        log.info(f'{key} link {link} added to chat {chat_id}')

    def get_link(self, chat_id: int, key: LinkType) -> str:
        if not self.has_chat(chat_id):
            return MediaLinksDB._NOT_UPLOADED_VALUE

        res = self._db[chat_id][key]

        log.info(f'{key} link for chat {chat_id}: {res}')

        return res
