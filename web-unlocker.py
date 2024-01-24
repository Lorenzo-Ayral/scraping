# import sys
from dotenv import load_dotenv
import os
import ssl
import urllib.request

load_dotenv()

http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")

ssl._create_default_https_context = ssl._create_unverified_context

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({
        'http': http_proxy,
        'https': https_proxy
    }))
print(opener.open('http://lumtest.com/myip.json').read())
