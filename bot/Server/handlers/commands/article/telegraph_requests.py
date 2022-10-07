import aiohttp
from typing import Optional, Union


PROXY = 'http://proxy.server:3128'

"""
Возможно синглтон сломает self._result -- одни пользователи будут получать данные других...
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TelegraphSession(metaclass=Singleton):
    _result: Union[dict, str, int]


    def __init__(self, proxy: Optional[str]=None) -> None:
        self._proxy = proxy if proxy else None
     
    async def get(self, *keys, method: str, params: Optional[dict]=None) -> Optional[dict]:
        API_URL = 'https://api.telegra.ph/'
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL+method, params=params, proxy=self._proxy) as resp:
                result: dict = await resp.json()
        print(result)
        for key in keys:
            result = result.get(key, 'none')

        self._result = result

    async def get_pages_count(self, token):
        await self.get(
            'result', 'total_count',
            method="getPageList?",
            params={'access_token': token}
        )
        return self._result

    async def get_pages_list(self, token):
        await self.get(
            'result', 'pages',
            method="getPageList?",
            params={'access_token': token}
        )
        return self._result

    async def get_auth_url(self, token):
        await self.get(
            'result', 'auth_url',
            method='getAccountInfo?',
            params={
                'access_token': token,
                'fields': '["auth_url"]'
            }
        )
        return self._result

    async def get_page_info(self, page_path: str):
        await self.get(
            'result',
            method=f'getPage/{page_path}'
        )
        return self._result

    @property 
    def result(self):
        return self._result


telegraphSession = TelegraphSession(proxy=PROXY)