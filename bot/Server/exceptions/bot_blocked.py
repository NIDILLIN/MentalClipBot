from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked


def reg_block(dp: Dispatcher) -> None:
    dp.register_errors_handler(callback=error_bot_blocked, exception=BotBlocked)


async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # При блокировке бота:
    # Бот удаляет пользователя из базы данных
    return True