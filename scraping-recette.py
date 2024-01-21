from bs4 import BeautifulSoup
import requests

url = 'https://codeavecjonathan.com/scraping/recette/'


def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None


response = requests.get(url)
response.encoding = response.apparent_encoding

if response.status_code == 200:

    html = response.text

    f = open("recette.html", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, 'html5lib')

    titre = soup.find("h1").text
    print(titre)

    description = get_text_if_not_none(soup.find("p", class_="description"))
    print(description)

else:
    print("Erreur :", response.status_code)

print(response)
