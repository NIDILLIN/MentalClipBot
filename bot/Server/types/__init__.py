from typing import Optional


class Note(dict):
    tag: Optional[str]=None
    text: Optional[str]=None
    photo: Optional[str]=None
    document: Optional[str]=None
    tagged_text: Optional[str]=None


    def __init__(
        self, 
        tag: Optional[str]=None,
        text: Optional[str]=None, 
        photo: Optional[str]=None, 
        document: Optional[str]=None
    ) -> None:
        self['tag'] = tag
        self['text'] = text
        self['photo'] = photo
        self['document'] = document
        self.tag_text()

    def tag_text(self) -> None:
        self['tagged_text'] = (
            f"{self['tag']}"+
            '\n\n'+
            f"{self['text']}"
        )


class Article():
    title: str
    description: str
    url: str


    def __init__(self, title, description, url) -> None:
        self.title = title
        self.description = description
        self.url = url

    async def text(self):
        t = (
            '<b>Заголовок:</b> '
            +f"""<a href="{self.url}">{self.title}</a>"""
            +'\n\n'
            +'<b>Описание:</b>\n'
            +f'{self.description}'
        )
        return t