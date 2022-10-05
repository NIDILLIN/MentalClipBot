from typing import Optional, Union
import aiosqlite
import asyncio


class Table():
    async def connect(self, user_id):
        self.db = await aiosqlite.connect(f'C:/Users/write/Desktop/MentalClipBot/db/{user_id}.db')
        
    async def start(self, user_id):
        await self.connect(user_id)
        return self

    async def insert(self): ...


class Articles(Table):
    title: str = 'none'
    description: str = 'none'
    url: str = 'none'
    group: str = 'none'

    async def insert(self):
        await self.db.execute(
            f'INSERT INTO articles VALUES (?, ?, ?, ?)', 
            (self.title, self.description, self.url, self.group)
        )
        await self.db.commit()

    async def update(self, col: str, value: str):
        await self.db.execute(
            f'UPDATE articles SET {col}={value} where title={self.title}'
        )
        await self.db.commit()


class Tokens(Table):
    token: str = 'none'
    short_name: str = 'none'


    async def insert(self):
        try:
            await self.db.execute(
                f'DELETE FROM tokens token where short_name={self.short_name}'
            )
        except:
            pass
        await self.db.execute(
            f'INSERT INTO tokens VALUES (?, ?)', 
            (self.token, self.short_name)
        )
        await self.db.commit()

    async def update(self, col: str, value: str):
        await self.db.execute(
            f'UPDATE tokens SET {col}={value} where short_name={self.short_name}'
        )
        await self.db.commit()

    async def select_names(self):
        cursor = await self.db.execute(
            f'SELECT short_name FROM tokens'
        )
        names = await cursor.fetchall()
        names = [name[0] for name in names]
        return names


class Notes(Table):
    note: str = 'none'
    group: str = 'none'


    async def insert(self):
        await self.db.execute(
            f'INSERT INTO notes VALUES (?, ?)', 
            (self.note, self.group)
        )
        await self.db.commit()

    async def update(self, col: str, value: str):
        await self.db.execute(
            f'UPDATE tokens SET {col}={value} where note={self.note}'
        )
        await self.db.commit()


class UserDB():
    user_id: int


    def __init__(self, user_id: Union[str, int]) -> None:
        self.user_id = user_id
        self.tokens = Tokens()
        self.notes = Notes()
        self.articles = Articles()

    async def start(self):
        await self.tokens.start(self.user_id)
        await self.notes.start(self.user_id)
        await self.articles.start(self.user_id)

    async def connect(self):
        self.db = await aiosqlite.connect(f'C:/Users/write/Desktop/MentalClipBot/db/{self.user_id}.db')
        await self.create_tables()
        await self.start()
        return self

    async def create_tables(self):
        await self.db.execute(
            """CREATE TABLE IF NOT EXISTS tokens (token STRING, short_name STRING);"""
        )
        await self.db.execute(
            """CREATE TABLE IF NOT EXISTS notes (note STRING, class STRING);"""
        )
        await self.db.execute(
            """CREATE TABLE IF NOT EXISTS articles (title STRING, description TEXT, url STRING, class STRING);"""
        )
        await self.db.commit()


async def main():
    user = await UserDB(1631513712).connect()
    user.tokens.short_name = 'nidi'
    b = await user.tokens.select_names()
    print(b)

if __name__ == '__main__':
    asyncio.run(main())