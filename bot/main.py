import logger
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Server.exceptions.bot_blocked import reg_block
from Server.handlers.commands import register_notes, register_common_cmd
from Server.handlers.commands.article import register_creating_telegraph_acc, register_article_creating, register_my_accounts
from Server.handlers.fast_note.fast_note import register_fast_note
from config import config


bot = Bot(config.bot_token.get_secret_value(), parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    await dp.bot.set_my_commands(
        [
            types.BotCommand("new_article", "Создать новую статью"),
            types.BotCommand("my_articles", "Список моих статей"),
            types.BotCommand("my_accounts", "Список моих аккаунтов"),
            types.BotCommand("profile", "Мой профиль"),
            types.BotCommand("create_account", "Создать telegraph аккаунт"), 
        ]
    )
    reg_block(dp)
    register_common_cmd(dp)
    register_notes(dp)
    register_creating_telegraph_acc(dp)
    register_article_creating(dp)
    register_my_accounts(dp)
    # register_fast_note(dp)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())