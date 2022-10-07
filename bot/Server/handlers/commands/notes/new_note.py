from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Server.types import Note


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


async def _send_note(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await Note(message, data['tag'], data['text']).send()


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