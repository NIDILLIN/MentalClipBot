from typing import Optional
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Server.handlers.commands.common import startState
from Server.types import Note
from Server.utils import dumps
from Server.db.db import UserDB


class AddNote(StatesGroup):
    note = State('note')
    tag = State('tag')
    photo = State()
    document = State()


async def cmd_new_note(message: Message, state: FSMContext) -> None:
    await message.answer('Напиши заметку')
    await state.set_state(AddNote.note.state)


async def add_note(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer('Мне нужен текст, напиши еще раз')
        return
    text = message.html_text
    await state.update_data(text=text)
    await message.answer('Теперь тэг. Он должен начинаться с #.\nЕсли не хочешь добавлять тэг, нажми\n/empty_tag')
    await state.set_state(AddNote.tag.state)


async def add_tag(message: Message, state: FSMContext) -> None:
    if not message.text:
        message.answer('Тэг должен быть текстом и начинаться с #.\nЕсли тэг не нужен нажми /empty_tag')
        return
    tag = message.text
    await state.update_data(tag=tag)
    await _send_note(message, state)
    await state.finish()


async def empty_tag(message: Message, state: FSMContext) -> None:
    tag = ''
    await state.update_data(tag=tag)
    await _send_note(message, state)
    await state.finish()
    await state.set_state(startState.state)


async def _send_note(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    get = lambda x: data.get(x, None)
    note = Note(
        get('tag'), 
        get('text'),
        get('photo'),
        get('document')
    )
    await _save_note(message.from_user.id, note, get('group'))
    message.answer(
        text=note['tagged_text']
    )


async def _save_note(user_id: int, note: Note, group: Optional[str]=None):
    user = await UserDB(user_id).connect()
    d_note = dumps(note)
    await user.notes.insert(d_note, group)
    await user.close()


# async def add_photo(message: Message, state: FSMContext) -> None:
#     photo = message.photo[-1]
#     state.update_data(photo=photo)
#     state.set_state(AddNote.document.state)


# async def add_document(message: Message, state: FSMContext) -> None:
#     pass


def register_notes(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_new_note, commands='new_note', state='*')
    dp.register_message_handler(add_note, state=AddNote.note)
    dp.register_message_handler(empty_tag, commands='empty_tag', state=AddNote.tag)
    dp.register_message_handler(add_tag, state=AddNote.tag)
    # dp.register_message_handler(add_photo, state=AddNote.photo)
    # dp.register_message_handler(add_document, state=AddNote.document)