import asyncio
from requests_html import HTML, AsyncHTMLSession, HTMLResponse
from typing import cast, Awaitable

results = []

async def main():
    url = 'https://findoutnazare.pt/category/onde-dormir/'

    s = AsyncHTMLSession() # cycles through different user-agents
    future = cast(Awaitable[HTMLResponse], s.get(url))
    r: HTMLResponse = await future


    await r.html.arender(sleep=3)
    print(r.status_code)

    xpath = '//*[@id="finderListings"]'
    # css = 'div.lf-item-container'

    #products = r.html.xpath(xpath, first=True)
    products = r.html.xpath(xpath, first=True)

    print(products)
    results.extend([
        products,
        # products.absolute_links # typ e:ignore
    ])

    await s.close()

asyncio.run(main())
