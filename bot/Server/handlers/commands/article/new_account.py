from typing import Optional
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from Server.db.db import UserDB
from Server.handlers.commands.article.telegraph_requests import telegraphSession


class CreateArticle(StatesGroup):
    Chooser = State()
    Changing = State()
    SetShortName = State()
    SetAuthorName = State()
    SetUrl = State()
    Default = State()


async def _create_account(short_name: Optional[str]=None, 
                          author_name: Optional[str]=None, 
                          author_url: Optional[str]=None) -> tuple[str, str]:
    """
    Returns:
        tuple[str, str]: access_token, auth_url
    """
    response = await telegraphSession.create_account(
        short_name=short_name, 
        author_name=author_name, 
        author_url=author_url
    )

    return response['access_token'], response['auth_url']


async def cmd_create_account(message: types.Message, state: FSMContext):
    user = await UserDB(message.from_user.id).connect()
    accs = await user.tokens.select_names()
    await user.close()
    if len(accs) == 10:
        message.answer('Создать более 10 аккаунтов нельзя')
        return
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    default = types.KeyboardButton('По умолчанию')
    change = types.KeyboardButton('Изменить')
    keyboard.add(default, change)
    await message.answer(
        '<b>Создание аккаунта.</b>\n'+
        'Ты можешь оставить данные по умолчанию:\n'+
        f'<i>Короткое имя:</i> {message.from_user.username}\n'+
        f'<i>Имя автора:</i> {message.from_user.full_name}\n'+
        '<i>Без ссылки на себя</i>',
        reply_markup=keyboard
    )
    await state.set_state(CreateArticle.Changing.state)


# Default choice
async def default_account(message: types.Message, state: FSMContext):
    user = await UserDB(message.from_user.id).connect()
    accs = await user.tokens.select_names()
    if len(accs) == 10:
        await message.answer('Создать более 10 аккаунтов нельзя')
        return
    if message.from_user.username in accs:
        await message.answer('Создать аккаунт с таким же именем нельзя')
        return
    token, url = await _create_account(
        short_name=message.from_user.username
    )
    user.tokens.token = token
    user.tokens.short_name = message.from_user.username
    await user.tokens.insert()
    await user.tokens.set_current_acc(user.tokens.short_name)
    await user.close()
    await state.finish()
    await send_url(message, url)


async def send_url(message: types.Message, url):
    create_article = types.InlineKeyboardButton(
        text='Перейти в telegraph',
        url=url
    )
    keyboard = types.InlineKeyboardMarkup().add(create_article)
    await message.reply(
        'Аккаунт создан\n'+
        'Переключиться на него можно в меню\n/my_accounts', 
        reply_markup=keyboard, 
        disable_web_page_preview=True, 
        protect_content=True
    )


# What to change? Changing State
async def changing(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    ShortName = types.KeyboardButton('Короткое имя')
    AuthorName = types.KeyboardButton('Имя автора')
    Url = types.KeyboardButton('Включить ссылку на себя')
    done = types.KeyboardButton('На этом все')
    keyboard.add(ShortName, AuthorName, Url, done)
    user_data = await state.get_data()
    sn = user_data.get('shortName', message.from_user.username)
    an = user_data.get('authorName', message.from_user.full_name)
    url = user_data.get('Url', '<i>Без ссылки на себя</i>')
    await message.answer(
        'Что изменить?\n'+
        f'<i>Короткое имя:</i> {sn}\n'+
        f'<i>Имя автора:</i> {an}\n'+
        url,
        reply_markup=keyboard
    )
    await state.set_state(CreateArticle.Changing.state)


# Changing state
async def change_short_name(message: types.Message, state: FSMContext):
    await message.answer(
        'Напиши короткое имя'
    )
    await state.set_state(CreateArticle.SetShortName.state)
# SetShortName state
async def short_name(message: types.Message, state: FSMContext):
    shortName = message.text
    await state.update_data(shortName=shortName)
    await changing(message, state)


# Changing state
async def change_author_name(message: types.Message, state: FSMContext):
    await message.answer(
        'Напиши имя автора'
    )
    await state.set_state(CreateArticle.SetAuthorName.state)
# SetAuthorName state
async def author_name(message: types.Message, state: FSMContext):
    author = message.text
    await state.update_data(authorName=author)
    await changing(message, state)


# Changing state
async def set_url(message: types.Message, state: FSMContext):
    await message.answer(
        'Ссылка включена'
    )
    await state.update_data(Url='<i>С ссылкой на себя</i>')
    await state.update_data(authorUrl=f'https://t.me/{message.from_user.username}')
    await state.set_state(CreateArticle.Changing.state)
    await changing(message, state)


# Changing State
async def done(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    token, url = await _create_account(
        short_name=user_data.get('shortName', message.from_user.username),
        author_name=user_data.get('authorName', None),
        author_url=user_data.get('authorUrl', None)
    )
    user = await UserDB(message.from_user.id).connect()
    user.tokens.token = token
    user.tokens.short_name = user_data.get('shortName', message.from_user.username)
    await user.tokens.insert()
    await user.tokens.set_current_acc(user.tokens.short_name)
    await user.close()
    await state.finish()
    await send_url(message, url)


def register_creating_telegraph_acc(dp: Dispatcher):
    dp.register_message_handler(cmd_create_account, commands='create_account', state='*')
    dp.register_message_handler(default_account, Text(equals='По умолчанию'), state=CreateArticle.Changing)
    dp.register_message_handler(changing, Text(equals='Изменить'), state=CreateArticle.Changing)

    dp.register_message_handler(change_short_name, Text(equals='Короткое имя'), state=CreateArticle.Changing)
    dp.register_message_handler(short_name, state=CreateArticle.SetShortName)

    dp.register_message_handler(change_author_name, Text(equals='Имя автора'), state=CreateArticle.Changing)
    dp.register_message_handler(author_name, state=CreateArticle.SetAuthorName)

    dp.register_message_handler(set_url, Text(equals='Включить ссылку на себя'), state=CreateArticle.Changing)

    dp.register_message_handler(done, Text(equals='На этом все'), state=CreateArticle.Changing)