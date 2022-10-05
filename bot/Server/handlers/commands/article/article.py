from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
import Server.handlers.commands.article.telegraph_requests as telegraph_requests

from Server.db.db import UserDB

cb_article = CallbackData('article', 'path')

class Article():
    title: str
    description: str
    url: str


    def __init__(self, title, description, url) -> None:
        self.title = title
        self.description = description
        self.url = url

    async def text(self):
        t = (
            '<b>Заголовок:</b> '
            +f"""<a href="{self.url}">{self.title}</a>"""
            +'\n\n'
            +'<b>Описание:</b>\n'
            +f'{self.description}'
        )
        return t


async def cmd_new_article(message: types.Message) -> None:
    to_telegraph = types.InlineKeyboardButton(text='Перейти в telegraph', url='https://telegra.ph/')
    keyboard = types.InlineKeyboardMarkup().add(to_telegraph)
    await message.answer(
        'Создать статью',
        disable_web_page_preview=True,
        protect_content=True,
        reply_markup=keyboard
    )

async def cmd_my_articles(message: types.Message):
    user = await UserDB(message.from_user.id).connect()
    token = await user.tokens.get_current_token()
    account = await user.tokens.get_current_acc()
    pages = await telegraph_requests.get_pages_count(token)
    if pages == 0:
        await message.answer(f'Нет статей для текущего аккаунта ({account})')
        return
    pages_list = await telegraph_requests.get_pages_list(token)
    articles_list = types.InlineKeyboardMarkup()
    buttons = []
    for page in pages_list:
        buttons.append(
            types.InlineKeyboardButton(
                text=page['title'],
                callback_data=cb_article.new(path=page['path'])
            )
        )
    articles_list.add(*buttons)
    await message.answer(
        f'Статьи для текущего аккаунта ({account})',
        reply_markup=articles_list
    )


async def articles(call: types.CallbackQuery):
    user = await UserDB(call.from_user.id).connect()
    token = await user.tokens.get_current_token()
    pages = await telegraph_requests.get_pages_count(token)
    if pages == 0:
        await call.message.answer(f'Нет статей для текущего аккаунта ({account})')
        return
    account = await user.tokens.get_current_acc()
    pages_list = await telegraph_requests.get_pages_list(token)
    articles_list = types.InlineKeyboardMarkup()
    buttons = []
    for page in pages_list:
        buttons.append(
            types.InlineKeyboardButton(
                text=page['title'],
                callback_data=cb_article.new(path=page['path'])
            )
        )
    articles_list.add(*buttons)
    await call.message.edit_text(
        f'Статьи для текущего аккаунта ({account})',
        reply_markup=articles_list
    )


async def article(call: types.CallbackQuery, callback_data: dict):
    page_info = await telegraph_requests.get_page_info(callback_data['path'])
    text = await Article(
        title=page_info['title'],
        description=page_info['description'],
        url=page_info['url']
    ).text()
    back = types.InlineKeyboardButton('Назад', callback_data='back_articles')
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(back)
    await call.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


def register_article_creating(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_new_article, commands='new_article', state='*')
    dp.register_message_handler(cmd_my_articles, commands='my_articles', state='*')

    dp.register_callback_query_handler(article, cb_article.filter())
    dp.register_callback_query_handler(articles, Text('back_articles'))