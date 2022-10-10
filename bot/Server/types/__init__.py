
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