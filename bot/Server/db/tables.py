from dataclasses import dataclass
from typing import Optional
import aiosqlite


class Table():
    async def _connect(self, user_id):
        self.db = await aiosqlite.connect(database=f'C:/Users/write/Desktop/MentalClipBot/db/{user_id}.db')

    async def _close(self):
        await self.db.close()
        
    async def _start(self, user_id):
        await self._connect(user_id)
        return self

    async def insert(self): ...


class Articles(Table):
    title: str = 'none'
    path: str = 'none'
    group: str = 'none'

    @dataclass(frozen=True)
    class Column():
        path = 'path'
        group = 'group'


    async def insert(self):
        await self.db.execute(
            f'INSERT INTO articles VALUES (?, ?, ?)', 
            (self.title, self.path, self.group)
        )
        await self.db.commit()

    async def insert_by(self, title, path, group):
        await self.db.execute(
            'INSERT INTO articles VALUES (?, ?, ?)', 
            (title, path, group)
        )
        await self.db.commit()

    async def update_group(self, title: str, new_group: str, path: str):
        try:
            await self.db.execute(
                f'DELETE FROM articles WHERE path=?', (path, )
            )
            await self.insert_by(title, path, new_group)
            await self.db.commit()
        except Exception as e:
            print(e)
        
    async def get_article_group(self, path: str) -> str:
        try:
            cursor = await self.db.execute(
                f"""SELECT class FROM articles where path=\'{path}\'"""
            )
            names = await cursor.fetchone()
            name = names[0] if names else None
            return name
        except:
            return None

    async def select_groups(self):
        cursor = await self.db.execute(
            f'SELECT class FROM articles'
        )
        names = await cursor.fetchall()
        names = [name[0] for name in names]
        return names

    async def get_articles_for_group(self, group: str):
        cursor = await self.db.execute(
            f"""SELECT title, path FROM articles where class='{group}'"""
        )
        names = await cursor.fetchall()
        names = {name[0]: name[1] for name in names}
        return names


class Tokens(Table):
    token: str = 'none'
    short_name: str = 'none'
    current: str = 'none'

    @dataclass(frozen=True)
    class Column():
        token = 'token'
        short_name = 'short_name'
        current = 0


    async def insert(self):
        await self.db.execute(
            f'INSERT INTO tokens VALUES (?, ?, ?)', 
            (self.token, self.short_name, self.current)
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
        return token[0] if token else None

    async def get_current_acc(self) -> Optional[str]:
        cursor = await self.db.execute(
            f'SELECT short_name FROM tokens WHERE current=?', (1, )
        )
        name = await cursor.fetchone()
        return name[0] if name else None

    async def get_current_token(self) -> Optional[str]:
        cursor = await self.db.execute(
            f'SELECT token FROM tokens WHERE current=?', (1, )
        )
        token = await cursor.fetchone()
        return token[0] if token else None

    async def set_current_acc(self, short_name: str):
        current = await self.get_current_acc()
        await self.db.execute(
            f'UPDATE tokens SET current=0 WHERE short_name=?', (current,)
        )
        await self.db.execute(
            f'UPDATE tokens SET current=1 WHERE short_name=?', (short_name, )
        )
        await self.db.commit()


class Notes(Table):
    note: str = 'none'
    group: str = 'none'

    @dataclass(frozen=True)
    class Column():
        note = 'note'
        group = 'group'


    async def insert(self, note, group):
        await self.db.execute(
            f'INSERT INTO notes VALUES (?, ?)', 
            (note, group)
        )
        await self.db.commit()

    async def update(self, col: str, value: str):
        await self.db.execute(
            f'UPDATE tokens SET {col}={value} where note={self.note}'
        )
        await self.db.commit()

    async def get_notes_count(self) -> int:
        cursor = await self.db.execute(
            f'SELECT note FROM notes'
        )
        notes = await cursor.fetchall()
        return len(notes) if notes else 0

    async def get_groups_count(self) -> int:
        cursor = await self.db.execute(
            f'SELECT class FROM notes'
        )
        groups = await cursor.fetchall()
        return len(groups) if groups else 0
