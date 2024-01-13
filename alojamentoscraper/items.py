# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import ClassVar, Dict, Protocol


class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]

@dataclass
class Place:
    address: str | None
    name: str
    al_num: str | None
    contact: str
    link: str
