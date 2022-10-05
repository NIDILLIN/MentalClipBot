import aiohttp
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegraph.aio import Telegraph

from Server.db.db import UserDB



article = State()


async def cmd_new_article(message: types.Message) -> None:
    to_telegraph = types.InlineKeyboardButton(text='Перейти в telegraph', url='https://telegra.ph/')
    keyboard = types.InlineKeyboardMarkup().add(to_telegraph)
    await message.answer(
        'Напиши статью',
        disable_web_page_preview=True,
        protect_content=True,
        reply_markup=keyboard
    )

async def my_articles(message: types.Message):
    articles_list = types.InlineKeyboardMarkup()
    article = types.InlineKeyboardButton(
        'title',
        url=article_url
    )
    user = await UserDB(message.from_user.id).connect()
    data={'access_token': user.token}
    await get_pages(data)


async def get_pages(data):
    async with aiohttp.ClientSession() as session:
        url = "https://api.telegra.ph/getPageList?"
        async with session.get(url, params=data) as resp:
            result = await resp.json()
    return result


async def get_auth_url(token):
    async with aiohttp.ClientSession() as session:
        url = f"""https://api.telegra.ph/getAccountInfo?access_token={token}&fields=["auth_url"]"""
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']['auth_url']


def register_article_creating(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_new_article, commands='new_article', state='*')
    # dp.register_message_handler(cmd_new_article, commands='my_articles', state='*')