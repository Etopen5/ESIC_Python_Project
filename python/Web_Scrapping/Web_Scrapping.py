import csv
import requests
from bs4 import BeautifulSoup

def scrape_page(soup, quotes):
    # On récupère toutes les balises <div> de classe 'quote' HTML sur la page
    quote_elements = soup.find_all('div', class_='quote')

    # On itère sur la liste de citation pour récupérer les données qui nous interresse
    for quote_element in quote_elements:
    # on récupère le texte de la quote
        text = quote_element.find(
	        'span',
	        class_='text'
        ).text
        # on récupere l'auteur de la citation
        author = quote_element.find(
	        'small',
	        class_='author'
        ).text

        # On récupère tout les tag liés a la citation
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        # On place ses tag dans une liste
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        # On ajoute nos données dans une lsite qui stock une liste de dictionnaires
        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)  # on regroupe tous les tags en un seul string
            }
        )

# L'URL de la page que l'on scrap
base_url = 'https://quotes.toscrape.com'

# On défini le User-Agent a utiliser dans notre requete
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# On recupere la page web
page = requests.get(base_url, headers=headers)

# On analyse la page web avec Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# Variable qui contient la liste des données de citation
quotes = []

# On scrap la page
scrape_page(soup, quotes)

# on recupere l'element next de la page html
next_li_element = soup.find('li', class_='next')

# s'il y a une next page
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # on récupère la nouvelle page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # on l'analyse
    soup = BeautifulSoup(page.text, 'html.parser')

    # et on la scrap
    scrape_page(soup, quotes)

    # on passe a la page suivante
    next_li_element = soup.find('li', class_='next')

# On ouvre le fichier citation.csv et s'il n'existe pas on le créer
# On utilise l'utf-16 pour permettre la bonne corespondance des guillemnts dans le document finale.
# Point negatif, le fichier est donc plus lourd.
csv_file = open('citation.csv', 'w', encoding ='utf-16', newline='')

# On initialiser l'outil d'ecriture pour ecrire des données dans le fichier
writer = csv.writer(csv_file, delimiter="\t", lineterminator="\n")

# On écrit les titres de colonnes
writer.writerow(['Text', 'Author', 'Tags'])

# On écrit toutes les lignes
for quote in quotes:
    writer.writerow(quote.values())

# et on ferme le fichier
csv_file.close()
