from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Server.handlers.commands.new_note import add_note, add_tag


def register_fast_note(dp: Dispatcher) -> None:
    dp.register_message_handler(add_note, content_types=types.ContentTypes.TEXT)