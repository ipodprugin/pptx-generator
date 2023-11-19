from generator.settings.config import settings


async def download_item(session, path: str, filename: str):
    params = {'path': path}
    url = 'https://cloud-api.yandex.net/v1/disk/resources/download'
    download_link  = None

    async with session.get(url, params=params) as response:
        if response.status != 200:
            return None
        resp = await response.json()
        download_link = resp.get('href')

    zippath = f'{settings.IMGS_PATH}/{filename}.zip'
    async with session.get(download_link) as resp:
        with open(zippath, 'wb') as fd:
            async for chunk in resp.content.iter_chunked(1024):
                fd.write(chunk)
    return zippath


async def find_plan_img(images):
    for index, img in enumerate(images):
        if img.find('План этажа') != -1:
            return index
    return None


async def find_facade_img(images):
    for index, img in enumerate(images):
        if img.find('Общий фасад здания.jpg') != -1:
            return index
    return None
