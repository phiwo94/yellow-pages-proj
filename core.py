import requests
import sqlite3 as sql
from bs4 import BeautifulSoup
from time import time


class Database:

    def __init__(self, db_name: str):
        self.db = sql.connect(str(db_name))
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS yellowpages 
                               (personname text, streetname text, zipcode text, town text, phonenumber text)""")

    def insert(self, data: tuple):
        if len(data) == 5:
            self.cursor.execute("""
                INSERT INTO yellowpages VALUES(?, ?, ?, ?, ?)
            """, data)

    def shut_down(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()


def get_soup(url: str):

    """
    :param url:
    :return parsed bs4 elements:
    """

    return BeautifulSoup(requests.get(url).text, features="html.parser")


def main():
    website = "https://telefonbuch-suche.com"
    sub_site = "/a"
    not_in_list = ["telefonbuch", "home", "impressum", "anmelden", "eintragen", "agb", "kontakt", "deutschland"]
    cities, streets = 0, 0
    t_cities = time()
    db = Database("cities/cities.db")
    soup = get_soup(website + sub_site)
    for ort in soup.find_all("a"):
        t_streets = time()
        if ort.get("href")[:2] == "/a" and ort.text.lower().replace(" ", "") not in not_in_list:
            ort_soup = get_soup(website + ort.get("href"))
            for stra in ort_soup.find_all("a"):
                if stra.get("href")[:2] == "/a" and stra.text.lower().replace(" ", "") not in not_in_list:
                    stra_soup = get_soup(website + stra.get("href"))
                    for anw in stra_soup.find_all("a"):
                        if anw.get("href")[:2] != "/a" and anw.text.lower().replace(" ", "") not in not_in_list:
                            temp_soup = get_soup(website + anw.get("href"))
                            pees = list()
                            for temp_elem in temp_soup.find_all("p"):
                                pees.append(temp_elem.contents)
                            temp = (str(pees[2][0]).strip(),
                                    str(pees[2][2]).strip(),
                                    str(pees[2][4]).strip().split(" ")[0],
                                    str(pees[2][4]).strip().split(" ")[1],
                                    str(pees[3][0]).strip())
                            db.insert(temp)
                db.db.commit()
                streets += 1
                print("    " + str(streets) + " Streets in: " + str((time() - t_streets)))
            cities += 1
            print(str(cities) + " in: " + str((time()-t_cities)/60))
    db.db.commit()
    db.shut_down()


def test():
    db = Database("cities/cities.db")
    db.cursor.execute("""SELECT * FROM yellowpages""")
    print(len(db.cursor.fetchall()))
    db.shut_down()


if __name__ == "__main__":
    test()
