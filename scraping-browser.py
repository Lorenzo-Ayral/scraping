import asyncio
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.async_api import async_playwright

SBR_WS_CDP = 'wss://brd-customer-hl_d532bd73-zone-scraping_browser1:g1n2qxu9rdg0@brd.superproxy.io:9222'

URLS = [
    "https://www.codeavecjonathan.com/scraping/techsport/",
    "https://www.codeavecjonathan.com/scraping/techsport/index.html?id=fitness-pro",
    "https://www.codeavecjonathan.com/scraping/techsport/index.html?id=solac-sync",
    "https://www.codeavecjonathan.com/scraping/techsport/index.html?id=tech-wizard"
]


BYPASS_SCRAPING = False


def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None


def extract_product_infos(html):
    infos = {}

    bs = BeautifulSoup(html, 'html5lib')
    infos['title'] = get_text_if_not_none(bs.find("span", id='productTitle'))

    infos['nb_ratings'] = 0
    ratings_text = get_text_if_not_none(bs.find("span", id='customer-review-text'))
    if ratings_text:
        nb_ratings_str = ratings_text.split()[0]
        if nb_ratings_str.isdigit():
            infos['nb_ratings'] = int(nb_ratings_str)

    infos['price'] = 0.0
    price_whole_str = get_text_if_not_none(bs.find("span", class_='price-whole'))
    price_fraction_str = get_text_if_not_none(bs.find("span", class_='price-fraction'))
    if price_whole_str and price_fraction_str.isdigit():
        price = float(price_whole_str)
        if price_fraction_str and price_fraction_str.isdigit():
            price += float(price_fraction_str)/100
        infos['price'] = price

    infos['description'] = get_text_if_not_none(bs.find("div", id='product-description'))

    return infos


async def run(pw):
    if not BYPASS_SCRAPING:
        print('Connecting to Scraping Browser...')
        browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        i = 0
        for url in URLS:
            i = i+1
            parsed_url = urlparse(url)
            domain_name = parsed_url.netloc.split('.')[1]
            directory = domain_name
            output_filename = os.path.join(directory, f'{domain_name}{i}')
            if not os.path.exists(directory):
                os.makedirs(directory)
            print(f"Page {i}/{len(URLS)}")
            if not BYPASS_SCRAPING:
                page = await browser.new_page()
                print('Connected! Navigating to ' + str(URLS) + '...')
                await page.goto(url)
                await page.screenshot(path='./' + output_filename + '.png', full_page=True)
                print('Navigated! Scraping page content...')
                html = await page.content()
                f = open(output_filename + '.html', "w")
                f.write(html)
                f.close()

            else:
                print('Bypassing scraping...')
                if os.path.isfile(output_filename):
                    f = open(output_filename, "r")
                    html = f.read()
                    f.close()
                else:
                    print(f"File {output_filename} does not exist.")
            print('Scraping page content...')
            infos = extract_product_infos(html)
            print(infos)

    finally:
        if not BYPASS_SCRAPING:
            await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())
