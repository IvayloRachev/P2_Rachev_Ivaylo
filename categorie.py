import requests
import csv
import os
import re

from livre import livre

class categorie:

    def __init__(self, nom):
        self.nom = nom
        self.livres = []

    def ajout_livres(self, livre):
        self.livres.append(livre)

    def creer_csv(self):
        path = "fichier_csv"
        if not os.path.exists(path):
            os.makedirs(path)

        with open(path + "/" + self.nom + "info_livre.csv", "w", encoding="utf-8-sig") as fichiercsv:
            writer = csv.writer(fichiercsv)
            fichiercsv.write("title, category, product_description, universal_product_code, price_including_tax, price_excluding_tax,"
                "number_available, review_rating, product_page_url, image_url: \n")
            for livre in self.livres:
                writer.writerow([livre.title, livre.category, livre.product_description, livre.universal_product_code, livre.price_including_tax,
                livre.price_excluding_tax, livre.number_available, livre.review_rating, livre.product_page_url,   livre.image_url])      

    def telecharger_image(self):
        path = "images"
        if not os.path.exists(path):
            os.makedirs(path)

        for livre in self.livres:
            title = re.sub("[^a-zA-Z0-9 \n]", '', livre.title)

            with open(path + "/" + title + ".jpg", "wb") as fichier:
                reponse = requests.get(livre.image_url)
                fichier.write(reponse.content)
