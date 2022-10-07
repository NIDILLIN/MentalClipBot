from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from Server.handlers.commands.article.telegraph_requests import telegraphSession

from Server.db.db import UserDB


async def cmd_my_profile(message: types.Message):
    user = await UserDB(message.from_user.id).connect()
    account = await user.tokens.get_current_acc()
    token = await user.tokens.get_current_token()
    pages = await telegraphSession.get_pages_count(token)
    notes = await user.notes.get_notes_count()
    groups = await user.notes.get_groups_count()
    text = (
        f'<b>Текущий аккаунт:</b> {account}\n'+
        f'<b>Статей аккаунта:</b> {pages}\n'+
        f'<b>Заметок:</b> {notes}\n'
        f'<b>Групп:</b> {groups}\n'
    )
    await message.answer(text)


def register_my_profile(dp: Dispatcher):
    dp.register_message_handler(cmd_my_profile, commands='profile')