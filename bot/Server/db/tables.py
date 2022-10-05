from dataclasses import dataclass
from typing import Optional
import aiosqlite


class Table():
    async def _connect(self, user_id):
        self.db = await aiosqlite.connect(database=f'C:/Users/write/Desktop/MentalClipBot/db/{user_id}.db')
        
    async def _start(self, user_id):
        await self._connect(user_id)
        return self

    async def insert(self): ...


class Articles(Table):
    title: str = 'none'
    description: str = 'none'
    url: str = 'none'
    group: str = 'none'

    @dataclass(frozen=True)
    class Column():
        title = 'title'
        description = 'description'
        url = 'url'
        group = 'group'


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
    current: str = 'none'

    @dataclass(frozen=True)
    class Column():
        token = 'token'
        short_name = 'short_name'
        current = 'current'


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

    async def get_by_short_name(self, value) -> str:
        cursor = await self.db.execute(
            f'SELECT {Tokens.Column.token} FROM tokens WHERE short_name=?', (value, )
        )
        token = await cursor.fetchone()
        return token[0]

    async def get_current_acc(self) -> Optional[str]:
        cursor = await self.db.execute(
            f'SELECT short_name FROM tokens WHERE current=?', (1, )
        )
        name = await cursor.fetchone()
        return name[0]

    async def set_current_acc(self, short_name: str):
        await self.db.execute(
            f'UPDATE tokens SET current=0'
        )
        await self.db.execute(
            f'UPDATE tokens SET current=1 where short_name={short_name}'
        )
        await self.db.commit()

class Notes(Table):
    note: str = 'none'
    group: str = 'none'

    @dataclass(frozen=True)
    class Column():
        note = 'note'
        group = 'group'


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
