from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from Server.handlers.commands.groups.adding_to_group import cb_new_group, group
from Server.db.db import UserDB


cb_article = CallbackData('article', 'path')


async def group_for_article(call: types.CallbackQuery, callback_data: dict):
    article_group = callback_data['article_group']
    page_path = callback_data.get('page_path', 'none')
    back = types.InlineKeyboardButton('Назад', callback_data=cb_article.new(path=page_path))
    if article_group == "Нет группы":
        add_article_group = types.InlineKeyboardButton("Добавить", callback_data=cb_new_group.new(path=page_path))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(add_article_group, back)
        await call.message.edit_text(
            f"Нет группы для статьи {page_path}",
            reply_markup=keyboard
        )
        await call.answer()
        return
    user = await UserDB(call.from_user.id).connect()
    group_articles = await user.articles.get_articles_for_group(article_group)
    await user.close()
    buttons = []
    for title, path in group_articles.items():
        buttons.append(
            types.InlineKeyboardButton(
                text=title,
                callback_data=cb_article.new(path=path)
            )
        )
    if not page_path == 'none':
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons, back)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    await call.message.edit_text(
        f'Группа {article_group}',
        reply_markup=keyboard
    )
    await call.answer()


async def cmd_groups(message: types.Message):
    user = await UserDB(message.from_user.id).connect()
    groups = await user.articles.select_groups()
    if not groups:
        await message.answer('Нет групп')
        return
    await user.close()
    buttons = []
    for gr in groups:
        buttons.append(
            types.InlineKeyboardButton(
                text=gr,
                callback_data=group.new(article_group=gr, page_path='none')
            )
        )

    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    await message.answer(
        f'Группы',
        reply_markup=keyboard
    )


def register_article_groups(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(group_for_article, group.filter())

    dp.register_message_handler(cmd_groups, commands='my_groups')