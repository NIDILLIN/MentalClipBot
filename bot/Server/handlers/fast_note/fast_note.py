from aiogram import Dispatcher
from aiogram import types
from Server.handlers.commands.common import startState

from Server.handlers.commands.notes.new_note import add_note


def register_fast_note(dp: Dispatcher) -> None:
    dp.register_message_handler(add_note, content_types=types.ContentTypes.TEXT, state=startState)