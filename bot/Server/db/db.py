from typing import Optional, Union
import aiosqlite
import sqlite3
import asyncio
from Server.db.tables import *
# from tables import *


class UserDB():
    user_id: int


    def __init__(self, user_id: Union[str, int]) -> None:
        self.user_id = user_id
        self.tokens = Tokens()
        self.notes = Notes()
        self.articles = Articles()

    async def start(self):
        await self.tokens._start(self.user_id)
        await self.notes._start(self.user_id)
        await self.articles._start(self.user_id)

    async def connect(self):
        self.db = await aiosqlite.connect(database=f'C:/Users/write/Desktop/MentalClipBot/db/{self.user_id}.db')
        await self.create_tables()
        await self.start()
        return self

    async def close(self):
        await self.tokens._close()
        await self.notes._close()
        await self.articles._close()
        await self.db.close()

    async def create_tables(self):
        await self.db.execute(
            """CREATE TABLE IF NOT EXISTS tokens (token STRING, short_name STRING, current INTEGER);"""
        )
        await self.db.execute(
            """CREATE TABLE IF NOT EXISTS notes (note STRING, class STRING);"""
        )
        await self.db.execute(
            """CREATE TABLE IF NOT EXISTS articles (title STRING, path STRING, class STRING);"""
        )
        await self.db.commit()


async def main():
    user = await UserDB(1631513712).connect()
    user.tokens.short_name = 'nidillin'
    b = await user.tokens.select_names()
    print(b)

if __name__ == '__main__':
    asyncio.run(main())