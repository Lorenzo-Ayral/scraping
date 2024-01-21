from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Créez une instance des Options Chrome
chrome_options = Options()

# Ajoutez l'option --headless
chrome_options.add_argument("--headless")

# Utilisez WebDriverManager pour obtenir le pilote
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Naviguez vers une page web
driver.get('https://codeavecjonathan.com/scraping/recette_js/')

# Imprimez le titre de la page
print(driver.title)

# N'oubliez pas de fermer le driver à la fin
driver.quit()
