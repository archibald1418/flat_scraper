# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from __future__ import annotations

from dataclasses import dataclass, Field
from typing import ClassVar, Dict, Protocol


class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]

@dataclass()
class Place:
    name: str
    contact: str
    link: str
    address: str | None
    al_num: str | None

@dataclass
class Address:
    address: str