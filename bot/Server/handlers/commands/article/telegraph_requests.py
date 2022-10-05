import aiohttp


async def get_pages_count(token):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegra.ph/getPageList?access_token={token}"
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']['total_count']


async def get_pages_list(token):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegra.ph/getPageList?access_token={token}"
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']['pages']


async def get_auth_url(token):
    async with aiohttp.ClientSession() as session:
        url = f"""https://api.telegra.ph/getAccountInfo?access_token={token}&fields=["auth_url"]"""
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']['auth_url']


async def get_page_info(page_url: str) -> dict:
    page = page_url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        url = f"""https://api.telegra.ph/getPage/{page}"""
        async with session.get(url) as resp:
            result = await resp.json()
    return result['result']