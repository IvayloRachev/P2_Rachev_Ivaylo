import requests
from bs4 import BeautifulSoup

from P2_02_categorie import categorie
from P2_01_livre import livre

main_page = "https://books.toscrape.com/"

def prendre_url_requests(url_req):
    url_requests = requests.get(url_req)
    soup = BeautifulSoup(url_requests.content, "html.parser")
    return(soup)

class scrapeLivres:

    def __init__(self):
        self.liste_categories = []

    def prendre_toutes_categories(self):
        soup = prendre_url_requests(main_page)
        prendre_premier_ul = soup.find("ul", {"class": "nav-list"})
        prendre_ul = prendre_premier_ul.find("ul")
        liste_livres_categorie = prendre_ul.find_all("li")
        for li in liste_livres_categorie:
            categorie_nom_dans_lien = li.find("a")["href"].split('/')[3]
            categories = categorie(categorie_nom_dans_lien)
            self.liste_categories.append(categories)

    def prendre_tous_livres(self):
        for categorie in self.liste_categories:
            soup = prendre_url_requests("https://books.toscrape.com/catalogue/category/books/" + categorie.nom + "/index.html")
            page = (soup.find("li", {"class" : "current"}))
            if page is None:
                tout_h3 = soup.find_all("h3")
                for h3 in tout_h3:
                    lien_vers_livres = h3.select("a")
                    for a in lien_vers_livres:
                        lien_vers_livre = a["href"].strip("../../../")
                        url_livre = main_page + 'catalogue/' + lien_vers_livre
                        categorie.ajout_livres(self.prendre_livre_infos(url_livre))
            else:
                page = str(page)
                page = page.split()[5]
                nombre_pages = int(page)
                for i in range(nombre_pages + 1):
                    url = f"https://books.toscrape.com/catalogue/category/books/" + categorie.nom + "/page"
                    str(i) + ".html"
                    reponse = requests.get(url)
                    if reponse.ok:
                        soup = BeautifulSoup(reponse.content, "html.parser")
                        tout_h3 = soup.find_all("h3")
                        for h3 in tout_h3:
                            lien_vers_livres = h3.select("a")
                            for a in lien_vers_livres:
                                lien_vers_livre = a["href"].strip("../../../")
                                url_livre = main_page + 'catalogue/' + lien_vers_livre
                                categorie.ajout_livre(self.prendre_livre_infos(url_livre))

    def prendre_livre_infos(self, url_livre):
        soup = prendre_url_requests(url_livre)
        title_livre = soup.find("h1").text
        
        ul_categorie = soup.select('ul.breadcrumb')
        for element in ul_categorie:
            categorie_livre = element.select("li")[2].text.strip()

            image_livre = soup.select("img")[0]
            image_src = main_page + image_livre.get("src").strip("../../")

            description_livre = soup.select("article > p")[0].text

            review_rating = soup.find("p", class_="star-rating").get("class")[1] + " stars"

            produit_info = soup.select("table.table")
            for info in produit_info:
                universal_product_code = info.select("tr > td")[0].text
                price_excluding_tax = info.select("tr > td")[2].text
                price_including_tax = info.select("tr > td")[3].text
                number_available = info.select("tr > td")[5].text

            details_livre = livre(title_livre, categorie_livre, description_livre, universal_product_code, price_including_tax,
            price_excluding_tax, number_available, review_rating, url_livre, image_src)  
            return(details_livre)

    def creer_livres_csv(self):
        for categorie in self.liste_categories:
            categorie.creer_csv()

    def telecharger_images_livres(self):
        for categorie in self.liste_categories:
            categorie.telecharger_image()

