from aiogram.types import Message


class Note():
    tag: str
    text: str

    def __init__(self, message: Message, tag: str, text: str) -> None:
        self.msg = message
        self.tag = tag
        self.text = text