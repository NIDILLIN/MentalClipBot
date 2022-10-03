from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# 1. Напиши текст (str or None)
# 2. Тэг (str or None)
# 3. Прикрепить документ (Да или Нет)
# Нет = закончить (finish)
# Да
# 4. Фото or Файл or Альбом  

class Note():
    tag: str
    text: str

    def __init__(self, message: Message, tag: str, text: str) -> None:
        self.msg = message
        self.tag = tag
        self.text = text

    async def send(self) -> None:
        msg = self.tag + '\n\n' + self.text
        await self.msg.answer(msg)


class AddNote(StatesGroup):
    note = State()
    tag = State()
    photo = State()
    document = State()


async def cmd_new_note(message: Message, state: FSMContext) -> None:
    await message.answer('Напиши заметку')
    await state.set_state(AddNote.note.state)


async def add_note(message: Message, state: FSMContext) -> None:
    if message.html_text:
        text = message.html_text
    else:
        message.answer('Мне нужен текст, напиши еще раз')
        return
    await state.update_data(text=text)
    await message.answer('Тепер тэг')
    await state.set_state(AddNote.tag.state)


async def _send_note(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await Note(message, data['tag'], data['text']).send()


async def add_tag(message: Message, state: FSMContext) -> None:
    tag = message.text
    await state.update_data(tag=tag)
    await _send_note(message, state)
    await state.finish()


# async def add_photo(message: Message, state: FSMContext) -> None:
#     photo = message.photo[-1]
#     state.update_data(photo=photo)
#     state.set_state(AddNote.document.state)


# async def add_document(message: Message, state: FSMContext) -> None:
#     pass


def register_notes(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_new_note, commands='new_note', state='*')
    dp.register_message_handler(add_note, state=AddNote.note)
    dp.register_message_handler(add_tag, state=AddNote.tag)
    # dp.register_message_handler(add_photo, state=AddNote.photo)
    # dp.register_message_handler(add_document, state=AddNote.document)