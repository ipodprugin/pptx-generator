import aiohttp


async def _get_tender(
    session: aiohttp.ClientSession, 
    tender_id: str
) -> tuple[int, dict]:
    url = f'https://api.investmoscow.ru/investmoscow/tender/v1/object-info/getTenderObjectInformation?tenderId={tender_id}'
    async with session.get(url) as response:
        return response.status, await response.json()


async def get_tender(
    tender_id, 
    session: aiohttp.ClientSession | None = None
) -> tuple[int, dict]:
    headers = {
        'authority': "api.investmoscow.ru",
        'accept': "application/json",
        'accept-language': "ru-RU",
        'origin': "https://investmoscow.ru",
        'referer': "https://investmoscow.ru/",
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.2271 YaBrowser/23.9.0.2271 Yowser/2.5 Safari/537.36",
        'x-requested-with': "XMLHttpRequest"
    }

    if not session:
        async with aiohttp.ClientSession(headers=headers) as session:
            return await _get_tender(session=session, tender_id=tender_id)
    else:
        return await _get_tender(session=session, tender_id=tender_id)
