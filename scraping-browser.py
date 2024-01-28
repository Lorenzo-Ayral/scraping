import asyncio
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.async_api import async_playwright

SBR_WS_CDP = 'wss://brd-customer-hl_d532bd73-zone-scraping_browser1:g1n2qxu9rdg0@brd.superproxy.io:9222'


try:
    with open('counter.txt', 'r') as f:
        content = f.read()
        counter = int(content) if content else 0
except FileNotFoundError:
    counter = 0

url ="https://www.codeavecjonathan.com/scraping/techsport/"
parsed_url = urlparse(url)
domain_name = parsed_url.netloc.split('.')[1]
directory = domain_name
if not os.path.exists(directory):
    os.makedirs(directory)
output_filename = os.path.join(directory, f'{domain_name}{counter}.html')

async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        print('Connected! Navigating to ' + url + '...')
        await page.goto(url)
        await page.screenshot(path='./'+ directory +'/scraping-browser' + str(counter) + '.png', full_page=True)
        print('Navigated! Scraping page content...')
        html = await page.content()
        f = open(output_filename, "w")
        f.write(html)
        f.close()

        with open('counter.txt', 'w') as f:
            f.write(str(counter + 1))
    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())