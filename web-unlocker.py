# import sys
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import ssl
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()

http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")

try:
    with open('counter.txt', 'r') as f:
        content = f.read()
        counter = int(content) if content else 0
except FileNotFoundError:
    counter = 0

url = 'https://www.woodbrass.com/guitares/guitares+electriques/retro+vintage#filtre-liste-categ'
parsed_url = urlparse(url)
domain_name = parsed_url.netloc.split('.')[1]
output_filename = f'{domain_name}{counter}.html'

with open(output_filename, 'w') as f:
    f.write('Hello world')

with open('counter.txt', 'w') as f:
    f.write(str(counter + 1))


opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({
        'http': http_proxy,
        'https': https_proxy
    }))
html = opener.open(url).read().decode('utf-8')

f = open("web-unlocker.html", "w")
f.write(html)
f.close()
