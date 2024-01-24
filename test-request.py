from bs4 import BeautifulSoup
import requests

url = 'https://codeavecjonathan.com/scraping/techsport/'

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}

response = requests.get(url, headers=HEADERS)
response.encoding = response.apparent_encoding

if response.status_code == 200:

    html = response.text

    f = open("amazon.html", "w")
    f.write(html)
    f.close()

else:
    print("Erreur :", response.status_code)

print(response)