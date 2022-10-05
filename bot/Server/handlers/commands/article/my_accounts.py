from typing import Text
import aiohttp
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from Server.db.db import UserDB


acc = CallbackData('acc', 'short_name')


async def cmd_my_accounts(message: types.Message):
    user = await UserDB(message.from_user.id).connect()
    accounts = await user.tokens.select_names()
    if not accounts:
        await message.answer(
            'У тебя еще нет аккаунтов. Но ты можешь создать их с помощью команды /create_account'
        )
        return
    buttons = [
        types.InlineKeyboardButton(
            text=name, 
            callback_data=acc.new(short_name=name)
        ) for name in accounts]
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    await message.answer(
        'Мои аккаунты',
        reply_markup=keyboard
    )


async def my_accounts(call: types.CallbackQuery):
    user = await UserDB(call.from_user.id).connect()
    accounts = await user.tokens.select_names()
    if not accounts:
        await call.message.answer(
            'У тебя нет аккаунтов. Но ты можешь создать их с помощью команды /create_account'
        )
        return
    buttons = [
        types.InlineKeyboardButton(
            text=name, 
            callback_data=acc.new(short_name=name)
        ) for name in accounts]
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    await call.message.edit_text(
        'Мои аккаунты',
        reply_markup=keyboard
    )


async def my_account(call: types.CallbackQuery, callback_data: dict):
    short_name = callback_data['short_name']
    user = await UserDB(call.from_user.id).connect()
    token = await user.tokens.get_by_short_name(short_name)
    pages = await get_pages(token)
    auth_url = await get_auth_url(token)

    text = f'<b>Аккаунт:</b> {short_name}\n<b>Кол-во статей аккаунта:</b> {pages}'
    log_in = types.InlineKeyboardButton('Войти на этом девайсе', url=auth_url)
    back = types.InlineKeyboardButton('Назад', callback_data='back_accounts')
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(log_in, back)

    await call.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
    await call.answer()


async def get_pages(token):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegra.ph/getPageList?access_token={token}"
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']['total_count']


async def get_auth_url(token):
    async with aiohttp.ClientSession() as session:
        url = f"""https://api.telegra.ph/getAccountInfo?access_token={token}&fields=["auth_url"]"""
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']['auth_url']


def register_my_accounts(dp: Dispatcher):
    dp.register_message_handler(cmd_my_accounts, commands='my_accounts')
    dp.register_callback_query_handler(my_account, acc.filter())
    dp.register_callback_query_handler(my_accounts, Text('back_accounts'))