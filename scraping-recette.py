from bs4 import BeautifulSoup
import requests

url = 'https://codeavecjonathan.com/scraping/recette_ua/'

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"}


def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None


response = requests.get(url, headers=HEADERS)
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

    # Ingrédients
    div_ingredients = soup.find("div", class_="ingredients")
    e_ingredients = div_ingredients.find_all("p")
    for e_ingredient in e_ingredients:
        print("Ingrédient :", e_ingredient.text)

    # Étapes
    table_preparation = soup.find("table", class_="preparation")
    e_preparations = table_preparation.find_all("td", class_="preparation_etape")
    for e_preparation in e_preparations:
        print("Étapes :", e_preparation.text)

else:
    print("Erreur :", response.status_code)

print(response)
