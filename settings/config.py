import re

from typing import Pattern
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    TGBOT_TOKEN: SecretStr

    # in .env file
    PAGENUMBER: int
    PAGESIZE: int
    GSHEETS_CREDS_PATH: str = 'service_account_secret.json'
    GSHEETURL: str = 'https://docs.google.com/spreadsheets/d/13uQGQqIcttvEyjCzpD1bJl1fPFQRNacjepl0y0iDyTQ/edit?usp=sharing'
    PARKING_PLACES_WORKSHEET_NAME: str
    NONRESIDENTIAL_SPACES_WORKSHEET_NAME: str
    YADISK_OAUTH_TOKEN: str

    # defaults
    IMGS_PATH: str = 'generator/img/'
    PPTX_TEMPLATE_PATH: str = 'generator/templates/template.pptx'
    PPTX_OUTPUT_DIRPATH: str = 'generator/generated'
    PARK_OBJTYPE_ID: int = 30011578
    NONRESIDENTIAL_OBJTYPE_ID: int = 30011569
    BASEURL: str = 'https://investmoscow.ru'
    DATETIME_FORMAT: str = '%Y-%m-%dT%H:%M:%S.%f0000Z'
    PARKING_SHEET_COLUMNS: list = [
        '№', 
        'tender_id', 
        'Адрес', 
        'Округ', 
        'Район', 
        'Форма', 
        'Начальная цена', 
        'Задаток', 
        'Проведены', 
        'Дата окончания приема заявок', 
        'Колличество', 
        'Этаж', 
        'Тип парковки', 
        'Ссылка на investmoscow', 
        'ссылка на авито', 
        'ссылка на циан', 
        'Рыночная цена', 
        'Цена на прошедших торгах', 
        'Ставка на торгах', 
        'Выставлены на авито', 
        'Примечание', 
        'Интересный', 
        'Место', 
        'Площадь'
    ]
    NONRESIDENTIAL_SHEET_COLUMNS: list = [
        '№', 
        'tender_id', 
        'Адрес', 
        'Округ', 
        'Район', 
        'Форма', 
        'Начальная цена', 
        'Задаток', 
        'Этаж', 
        'Проведены', 
        'Дата окончания приема заявок', 
        'Ссылка на investmoscow', 
        'Ставка на торгах', 
        'Выставленны на авито', 
        'Примечание', 
        'Цена за кв м', 
        'Рыночная', 
        'Площадь',
        'Вход'
    ]
    PICTURES: dict = {
        'map': None,
        'plan': None,
        'Img1': None,
        'Img2': None,
        'Img3': None,
        'Img4': None,
        'Img5': None,
        'Img6': None,
        'Img7': None,
        'Img8': None,
        'Img9': None,
    }
    GET_PARKPLACE_REGEX: Pattern = re.compile(r"(м/м №|м/м|мм)\s*(.+)")
    GET_PRICE_REGEX: Pattern = re.compile(r"\d[\d ]+,?\d+")
    TENDER_ID_REGEX: Pattern = re.compile("^\d{8,}$")


settings = Settings()
