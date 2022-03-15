from scrape_livres import scrapeLivres

if __name__ == '__main__':
    scraper = scrapeLivres()
    scraper.prendre_toutes_categories()
    scraper.prendre_tous_livres()
    scraper.creer_livres_csv()
    scraper.telecharger_images_livres()