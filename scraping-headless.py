import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Créez une instance des Options Chrome
chrome_options = Options()

# Supprimez l'option --headless
# chrome_options.add_argument("--headless")

# Utilisez WebDriverManager pour obtenir le pilote
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Naviguez vers une page web
driver.get('https://codeavecjonathan.com/scraping/recette_js/')

time.sleep(5)

# Obtenez le contenu HTML de la page web
html = driver.page_source

f = open("recette_js.html", "w")
f.write(html)
f.close()

# Analysez le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html, 'html5lib')

# Trouvez et imprimez le titre
titre = soup.find("h1").text
print(titre)

# Trouvez et imprimez la description
description = soup.find("p", class_="description").text
print(description)

# Trouvez et imprimez les ingrédients
div_ingredients = soup.find("div", class_="ingredients")
e_ingredients = div_ingredients.find_all("p")
for e_ingredient in e_ingredients:
    print("Ingrédient :", e_ingredient.text)

# Trouvez et imprimez les étapes de préparation
table_preparation = soup.find("table", class_="preparation")
e_preparations = table_preparation.find_all("td", class_="preparation_etape")
for e_preparation in e_preparations:
    print("Étapes :", e_preparation.text)

print(driver.title)

# N'oubliez pas de fermer le driver à la fin
driver.quit()
