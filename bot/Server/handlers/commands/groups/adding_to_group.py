from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Server.handlers.commands.article.telegraph_requests import telegraphSession
from Server.db.db import UserDB

cb_article = CallbackData('article', 'path')
group = CallbackData('group', 'article_group', 'page_path')
cb_new_group = CallbackData('new_group', 'path')
cb_adding_group = CallbackData('adding_group', 'new_group', 'path')


class AddingGroup(StatesGroup):
    choose = State()
    groups = State()


async def new_group(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    page_path = callback_data['path']
    page_info = await telegraphSession.get_page_info(page_path)
    existing = types.InlineKeyboardButton('В существующую', callback_data=cb_adding_group.new(path=page_path, new_group='1'))
    create = types.InlineKeyboardButton('Создать новую', callback_data=2)
    back = types.InlineKeyboardButton('Назад', callback_data=cb_article.new(path=page_path)) 
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(existing, create, back)
    await call.message.edit_text(
        text=f"В какую группу добавить статью {page_info['title']}?",
        reply_markup=keyboard
    )
    await state.set_state(AddingGroup.groups.state)
    await call.answer()


async def cb_add_to_existing_group(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user = await UserDB(call.from_user.id).connect()
    groups = await user.articles.select_groups()
    buttons = []
    for group in groups:
        buttons.append(
            types.InlineKeyboardButton(
                text=group,
                callback_data=cb_adding_group.new(new_group=group, path=callback_data['path'])
            )
        )
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    await call.message.edit_text(
        'Список существующих групп',
        reply_markup=keyboard
    )
    await state.set_state(AddingGroup.choose.state)
    await call.answer()


async def add_to_group(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user = await UserDB(call.from_user.id).connect()
    title = await telegraphSession.get_page_info(callback_data['path'])
    title = title['title']
    await user.articles.update_group(title, callback_data['new_group'], callback_data['path'])
    await call.message.delete()
    await state.finish()
    await call.answer(f"Статья добавлена в группу {callback_data['new_group']}", show_alert=True)


def register_adding_articles_to_group(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(new_group, cb_new_group.filter())

    dp.register_callback_query_handler(cb_add_to_existing_group, cb_adding_group.filter(), state=AddingGroup.groups)
    dp.register_callback_query_handler(add_to_group, cb_adding_group.filter(), state=AddingGroup.choose)