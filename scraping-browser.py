import asyncio
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.async_api import async_playwright

SBR_WS_CDP = 'wss://brd-customer-hl_d532bd73-zone-scraping_browser1:g1n2qxu9rdg0@brd.superproxy.io:9222'

url ="https://www.codeavecjonathan.com/scraping/techsport/"
parsed_url = urlparse(url)
domain_name = parsed_url.netloc.split('.')[1]
directory = domain_name
if not os.path.exists(directory):
    os.makedirs(directory)
output_filename = os.path.join(directory, f'{domain_name}.html')

BYPASS_SCRAPING = os.path.exists(output_filename)

async def run(pw):
    if not BYPASS_SCRAPING:
        print('Connecting to Scraping Browser...')
        browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        if not BYPASS_SCRAPING:
            page = await browser.new_page()
            print('Connected! Navigating to ' + url + '...')
            await page.goto(url)
            await page.screenshot(path='./'+ directory +'/scraping-browser.png', full_page=True)
            print('Navigated! Scraping page content...')
            html = await page.content()
            f = open(output_filename, "w")
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
    finally:
        if not BYPASS_SCRAPING:
            await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())