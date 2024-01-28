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


url = 'https://www.amazon.fr/dp/B0C2427W39/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B0C2427W39&pd_rd_w=Pmmmh&content-id=amzn1.sym.67940124-f33c-4507-afdc-9e790fb9d33b&pf_rd_p=67940124-f33c-4507-afdc-9e790fb9d33b&pf_rd_r=E06TVEP9P676SK1J394A&pd_rd_wg=EcV5Q&pd_rd_r=68d968fd-9f54-4a39-bf3e-2b6828361dfc&s=kitchen&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM'
parsed_url = urlparse(url)
domain_name = parsed_url.netloc.split('.')[1]
directory = domain_name
if not os.path.exists(directory):
    os.makedirs(directory)
output_filename = os.path.join(directory, f'{domain_name}{counter}.html')

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({
        'http': http_proxy,
        'https': https_proxy
    }))

html = opener.open(url).read().decode('utf-8')
f = open(output_filename, "w")
f.write(html)
f.close()

with open('counter.txt', 'w') as f:
    f.write(str(counter + 1))
