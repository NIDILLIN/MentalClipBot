from aiogram import Dispatcher
from aiogram.types import Message
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


article = State('note')


async def cmd_new_article(message: Message, state: FSMContext) -> None:
    await message.answer('Напиши <b>Заголовок</b>')
    await state.set_state(article.state)


async def add_title(message: Message, state: FSMContext) -> None:
    button = types.InlineKeyboardButton(text='Перейти в telegraph', url='https://telegra.ph/')
    keyboard = types.InlineKeyboardMarkup().add(button)
    await message.answer(f'Статья {message.text}', disable_web_page_preview=True, reply_markup=keyboard)


def register_article(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_new_article, commands='new_article', state='*')
    dp.register_message_handler(add_title, state=article)