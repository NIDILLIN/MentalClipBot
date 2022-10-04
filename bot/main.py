import logger
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Server.exceptions.bot_blocked import reg_block
from Server.handlers.commands import register_notes, register_common_cmd
from Server.handlers.fast_note.fast_note import register_fast_note
from config import config


bot = Bot(config.bot_token.get_secret_value(), parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    reg_block(dp)
    register_common_cmd(dp)
    register_notes(dp)
    register_fast_note(dp)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())