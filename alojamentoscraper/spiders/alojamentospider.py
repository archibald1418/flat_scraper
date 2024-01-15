import os
from typing import Iterable, Any, Generator, Text, Unpack, TypedDict

import scrapy
from scrapy import Request
from scrapy.http import TextResponse
from ..items import Place, IsDataclass, Address

from scrapy_playwright.page import PageMethod


class CallbackKwargs(TypedDict):
    place: Place


class AlojamentospiderSpider(scrapy.Spider):
    name = "alojamentospider"
    # allowed_domains = ["findoutnazare.pt"]
    # start_urls = ["https://findoutnazare.pt"]

    def start_address_request(self, url) -> Iterable[Request]:
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.pf-body')
            ],
            errback=self.errback
        ))

    def start_requests(self) -> Iterable[Request]:
        url = 'https://findoutnazare.pt/category/onde-dormir/'
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.lf-item')
            ],
            errback=self.errback
        )
        )

    def parse_address(self, response: TextResponse, **kwargs: Unpack[CallbackKwargs]) -> Generator[Place, None, None]:
        addr: str | None = response.xpath('//div[@class="map-block-address"]/ul/li/p/text()').get()
        place: Place = kwargs['place']
        if addr:
            place.address = addr
        yield kwargs['place']

    def parse(self, response: TextResponse, **kwargs: Any) -> Generator[scrapy.Item | IsDataclass | Request, None, None]:
        cs = response.xpath('//*[@id="finderListings"]/div[2]/div/div/div/a')
        print("LEN = ", len(cs))
        for container in cs:
            link = container.attrib['href']
            info = (container.xpath(
                "div[@class='lf-item-info']/h4/text()").get() or 'unknown').strip()
            name, *al_num = info.split('|')
            al_num = al_num[0].strip() if al_num else None
            contact = (container.xpath(
                "div[@class='lf-item-info']/ul/li/text()[2]").get() or 'unknown').strip()
            # address = None
            # print("TEXT=", atext)
            # address, contact = atext.split('\n')
            print(link, name, al_num, contact)
            # address = yield response.follow(link, callback=self.parse_address)
            yield response.follow(
                link,
                callback=self.parse_address,
                cb_kwargs=CallbackKwargs(
                    place=Place(
                        link=link,
                        name=name,
                        al_num=al_num,
                        contact=f"'{contact}", # shield for '+' in phone numbers
                        address=None
                    )
                )
            )

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
