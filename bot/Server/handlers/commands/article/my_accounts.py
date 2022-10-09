from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
from Server.db.db import UserDB
from Server.handlers.commands.article.telegraph_requests import telegraphSession


acc = CallbackData('acc', 'short_name')
log_acc = CallbackData('log', 'short_name')


async def cmd_my_accounts(message: types.Message):
    user = await UserDB(message.from_user.id).connect()
    accounts = await user.tokens.select_names()
    current_acc = await user.tokens.get_current_acc()
    await user.close()
    if not current_acc:
        current_acc = 'не установлен'
    if not accounts:
        await message.answer(
            'У тебя еще нет аккаунтов. Но ты можешь создать их с помощью команды /create_account'
        )
        return
    buttons = [
        types.InlineKeyboardButton(
            text=name, 
            callback_data=acc.new(short_name=name)) 
        for name in accounts
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    await message.answer(
        'Мои аккаунты\n'+
        f'Текущий: {current_acc}',
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
    current_acc = await user.tokens.get_current_acc()
    await user.close()
    if not current_acc:
        current_acc = 'не установлен'
    await call.message.edit_text(
        'Мои аккаунты\n'+
        f'Текущий: {current_acc}',
        reply_markup=keyboard
    )
    call.answer()


async def my_account(call: types.CallbackQuery, callback_data: dict):
    short_name = callback_data['short_name']
    user = await UserDB(call.from_user.id).connect()
    token = await user.tokens.get_by_short_name(short_name)
    pages = await telegraphSession.get_pages_count(token)
    auth_url = await telegraphSession.get_auth_url(token)
    await user.close()

    text = f'<b>Аккаунт:</b> {short_name}\n<b>Кол-во статей аккаунта:</b> {pages}'
    log_in = types.InlineKeyboardButton('Войти на этом девайсе', url=auth_url)
    change_to = types.InlineKeyboardButton('Переключиться на этот аккаунт', callback_data=log_acc.new(short_name=short_name))
    back = types.InlineKeyboardButton('Назад', callback_data='back_accounts')
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(log_in, change_to, back)

    await call.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
    await call.answer()


async def set_current_acc(call: types.CallbackQuery, callback_data: dict):
    user = await UserDB(call.from_user.id).connect()
    await user.tokens.set_current_acc(callback_data['short_name'])
    await user.close()
    await call.answer('Вы переключились на этот аккаунт', show_alert=True)


def register_my_accounts(dp: Dispatcher):
    dp.register_message_handler(cmd_my_accounts, commands='my_accounts')
    dp.register_callback_query_handler(my_account, acc.filter())
    dp.register_callback_query_handler(my_accounts, Text('back_accounts'))
    dp.register_callback_query_handler(set_current_acc, log_acc.filter())