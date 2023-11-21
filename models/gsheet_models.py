from pydantic import BaseModel


class SheetRowTenderContent(BaseModel):
    id: str
    address: str | None = None
    subway_stations: str | None = None
    region_name: str | None = None
    district_name: str | None = None
    object_area: str | None = None
    floor: str | None = None
    applications_enddate: str | None = None
    deposit: str | None = None
    start_price: str | None = None
    m1_start_price: str | None = None
