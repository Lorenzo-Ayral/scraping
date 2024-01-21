from bs4 import BeautifulSoup
import requests

url = 'https://codeavecjonathan.com/scraping/recette/'

response = requests.get(url)
response.encoding = response.apparent_encoding

if response.status_code == 200:

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    title_content = soup.title.string

    print(title_content)

    # f = open("recette.html", "w")
    # f.write(html)
    # f.close()

else:
    print("Erreur :", response.status_code)

print(response)
