import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Server.handlers.commands.registration import register_all
from config import config


bot = Bot(config.bot_token.get_secret_value(), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    await register_all(dp)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())