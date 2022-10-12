import pymongo
from Server.db.tables import *


class _Filter(dict): pass


class _Token(_Filter):
    def by_name(self, name: str) -> str:
        """
        {
            name: token,
            name_1: token,
        }
        """
        for k, v in self.items():
            if name == k: 
                return v


class DB:
    def __init__(self) -> None:
        pass

    @property
    def token(self) -> _Token:
        # select token in user table
        # and return _Token object
        pass