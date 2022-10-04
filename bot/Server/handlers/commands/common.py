from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Я бот для заметок! У меня ты можешь создавать любые заметки, класть их в папки, давать им тэги, прикреплять фото и т.д.",
        reply_markup=types.ReplyKeyboardRemove()
    )

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Отменено", 
        reply_markup=types.ReplyKeyboardRemove()
    )


def register_common_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
