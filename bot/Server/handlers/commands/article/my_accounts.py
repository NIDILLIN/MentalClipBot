from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Server.db.db import UserDB

async def cmd_my_accounts(message: types.Message):
    user = await UserDB(message.from_user.id).connect()
    names = await user.tokens.select_names()
    buttons = [types.InlineKeyboardButton(name) for name in names]
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)

    message.answer(
        'Мои аккаунты',
        reply_markup=keyboard
    )


def register_my_accounts(dp: Dispatcher):
    dp.register_message_handler(cmd_my_accounts, commands='my_accounts')