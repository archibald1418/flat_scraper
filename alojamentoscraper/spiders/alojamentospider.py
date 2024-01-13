import scrapy
from typing import Iterable, Any, Generator
from scrapy import Request
from scrapy.http import TextResponse
import os
print(os.getcwd())
from ..items import Place, IsDataclass

from scrapy_playwright.page import PageMethod

class AlojamentospiderSpider(scrapy.Spider):
    name = "alojamentospider"
    #allowed_domains = ["findoutnazare.pt"]
    #start_urls = ["https://findoutnazare.pt"]

    def start_requests(self) -> Iterable[Request]:
        url = 'https://findoutnazare.pt/category/onde-dormir/'
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.lf-item')
            ],
            errback = self.errback
        )
    )

    def parse(self, response: TextResponse, **kwargs: Any) -> Generator[scrapy.Item | IsDataclass , None, None]:
        cs = response.xpath('//*[@id="finderListings"]/div[2]/div/div/div/a')
        print("LEN = ", len(cs))
        for container in cs:
            link = container.attrib['href']
            info = (container.xpath("div[@class='lf-item-info']/h4/text()").get() or 'unknown').strip()
            name, *al_num = info.split('|')
            al_num = al_num[0].strip() if al_num else None
            contact = (container.xpath("div[@class='lf-item-info']/ul/li/text()[2]").get() or 'unknown').strip()
            address = None
            # print("TEXT=", atext)
            # address, contact = atext.split('\n')
            print(link, name, al_num, contact)
            yield Place(link=link, name=name, al_num=al_num, contact=f"'{contact}", address=address)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
