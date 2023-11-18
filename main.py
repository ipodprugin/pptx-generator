import pprint

import asyncio
import aiohttp

import re, os
import shutil
import zipfile

import jinja2
import pygsheets

from config import settings

from helpers.tenders import get_tender
from helpers.images import download_item, find_plan_img, find_facade_img
from helpers.pptx_render import replace_images_by_shape_text, render_text

from models.gsheet_models import SheetRowTenderContent

from template_pptx_jinja.render import PPTXRendering


async def gen_pptx(tender: SheetRowTenderContent, pictures: dict):
    input_path = 'templates/template.pptx'

    model = {
        "address": tender.address,
        "subway_stations": tender.subway_stations,
        "region_name": tender.region_name,
        "district_name": tender.district_name,
        "object_area": tender.object_area,
        "floor": tender.floor,
        "applications_enddate": tender.applications_enddate,
        "deposit": tender.deposit,
        "start_price": tender.start_price,
    }

    jinja2_env = jinja2.Environment()

    output_path = f'generated/{tender.id}.pptx'
    await render_text(input_path, model, output_path, jinja2_env)

    await replace_images_by_shape_text(images=pictures, template_path=output_path, output_path=output_path)


async def get_user_input() -> tuple[list[str], int]:
    data = []
    print(f'Таблица: {settings.GSHEETURL}')
    print('Введите tender_id объектов, для которых необходимо сгенерировать презентацию (каждый на новой строке). \nЧтобы закончить ввод, введите "y" на отдельной строке: ')
    while True:
        _input = input()
        if _input == 'y':
            break
        elif _input:
            valid_tender_id = TENDER_ID_REGEX.findall(_input)
            if valid_tender_id:
                data.append(_input)
            else:
                print('Неверный формат tender_id. Попробуйте еще раз')
        else:
            print('Таких объектов я точно не найду)')

    return data


async def get_data_from_google_sheet(sh: pygsheets.Spreadsheet, search_data: list) -> list[SheetRowTenderContent]:
    # row example:
    # ['', '19337217', 'Волжский бульвар, дом 1, корпус 1, этаж 4 , м/м 513', 'ЮВАО', 'Рязанский район', 'Открытый аукцион в электронной форме', '290000', '58000', 'нет', '1.12.2023', '772', '4', 'Многоуровневая парковка', 'https://investmoscow.ru/tenders/tender/19337217', '', '', '', '', '', '', '', '', '513', '11.9', 'https://yadi.sk/i/Dh2Q0tPs4dCCGA | https://yadi.sk/i/CsyijPdB2pYSdg | https://yadi.sk/i/PIov1138K4CftQ | https://yadi.sk/i/jP4D-M9RB6oFag | https://yadi.sk/i/bEqgvIR5k6994Q | https://yadi.sk/i/vkX7NaIWYhkrlA | https://yadi.sk/i/y5LnNfDAlz9xxw | https://yadi.sk/i/Ku1NAJR8sp-6_A | https://yadi.sk/i/s6qXr7HsnLIbIw | https://yadi.sk/i/V5dgi2tz7jG5xA', '', '', '', '', '', '', '']
    wks_list = sh.worksheets()
    wks = wks_list[1]
    rows = []

    for d in search_data:
        cell = wks.find(d)
        if cell:
            row_id = cell[0].row
            row = wks.get_row(row_id)
            try:
                row = SheetRowTenderContent(
                    id=row[1],
                    address=row[2],
                    region_name=row[3],
                    district_name=row[4],
                    object_area=row[-10],
                    floor=row[8],
                    applications_enddate=row[10],
                    deposit=row[7],
                    start_price=row[6],
                )
                rows.append(row)
            except IndexError as e:
                print(f'При обработке строки с id {d} произошла ошибка: {e}')
    return rows


async def form_pictures_dict(imgs_folder: str):
    pictures = {}
    images = os.listdir(imgs_folder)

    plan_img_index = await find_plan_img(images)
    if plan_img_index is not None:
        pictures['plan'] = f'{imgs_folder}/{images[plan_img_index]}'
        images.pop(plan_img_index)

    facade_img_index = await find_facade_img(images)
    if facade_img_index is not None:
        pictures['map'] = f'{imgs_folder}/{images[facade_img_index]}'
        images.pop(facade_img_index)

    for index, img in enumerate(images):
        if index == 9:
            break
        pictures[f'Img{index + 1}'] = f'{imgs_folder}/{img}'
    
    return pictures


async def main():
    sa = pygsheets.authorize(service_file=settings.GSHEETS_CREDS_PATH)
    sh = sa.open_by_url(settings.GSHEETURL)

    search_data = await get_user_input()
    tenders = await get_data_from_google_sheet(sh, search_data)

    imgzip_paths = []
    basepath = 'app:/nonresidential/'
    DISK_AUTH_HEADERS: str = {'accept': 'application/json', 'Authorization': 'OAuth %s' % settings.YADISK_OAUTH_TOKEN}
    async with aiohttp.ClientSession(headers=DISK_AUTH_HEADERS) as session:
        for tender in tenders:
            zippath = await download_item(session=session, path=basepath + tender.id, filename=tender.id)
            imgzip_paths.append(zippath)

    for zippath in imgzip_paths:
        with zipfile.ZipFile(zippath, "r") as zip_ref:
            zip_ref.extractall(f"img/")

    for zippath, tender in zip(imgzip_paths, tenders):
        imgs_folder, _ = os.path.splitext(zippath)
        pictures = await form_pictures_dict(imgs_folder)
        await gen_pptx(tender=tender, pictures=pictures)

    for zippath in imgzip_paths:
        imgs_folder, _ = os.path.splitext(zippath)
        shutil.rmtree(imgs_folder)
        os.remove(zippath)


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    TENDER_ID_REGEX = re.compile("^\d{8,}$")

    asyncio.run(main())
