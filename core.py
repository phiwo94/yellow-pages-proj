import requests
import sqlite3 as sql
from bs4 import BeautifulSoup
from time import time
import re


class Database:

    def __init__(self, db_name: str):
        self.db = sql.connect(str(db_name))
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS yellowpages 
                               (personname text, streetname text, zipcode text, town text, phonenumber text)""")

    def insert(self, data):
        self.cursor.executemany("""
            INSERT INTO yellowpages VALUES(?, ?, ?, ?, ?)
        """, data)
        self.db.commit()

    def select_from(self, fil=None):
        if fil is not None:
            self.cursor.execute("""
                SELECT DISTINCT streetname FROM yellowpages WHERE town = ?
            """, fil)
        else:
            self.cursor.execute("""
                SELECT DISTINCT town FROM yellowpages
            """)
        return self.cursor.fetchall()

    def db_length(self):
        self.cursor.execute("""
            SELECT personname FROM yellowpages
        """)
        l = self.cursor.fetchall()
        return len(l)

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


def get_personell_data(soup):
    temp = list()
    for anw in soup.find_all("a"):
        if anw.get("href")[:2] != "/a" and anw.text.lower().replace(" ", "") not in not_in_list:
            temp_soup = get_soup(website + anw.get("href"))
            pees = list()
            for temp_elem in temp_soup.find_all("p"):
                pees.append(temp_elem.contents)
            try:
                temp.append((str(pees[2][0]).strip(),
                             str(pees[2][2]).strip(),
                             str(pees[2][4]).strip().split(" ")[0],
                             str(pees[2][4]).strip().split(" ")[1],
                             str(pees[3][0]).strip()))
            except:
                pass
    return temp


def get_last_point():
    db = Database("cities/cities.db")
    t_towns = db.select_from()
    t_streets = db.select_from(fil=t_towns[len(t_towns)-1])
    towns = list()
    streets = list()
    nums_regex = re.compile(r"\d+")
    for town in t_towns:
        towns.append(str(list(town).pop()))
    for street in t_streets:
        streets.append(nums_regex.sub("", str(list(street).pop()))[:-1].strip())
    db.shut_down()
    return towns, list(set(streets))


def main():
    cities, streets = 0, 0
    t_cities = time()
    db = Database("cities/cities.db")
    f_towns, f_streets = get_last_point()
    soup = get_soup(website + sub_site)
    for ort in soup.find_all("a"):
        t_streets = time()
        if ort.get("href")[:2] == "/a" and ort.text.lower().replace(" ", "") not in not_in_list and ort.text not in f_towns:
            ort_soup = get_soup(website + ort.get("href"))
            for stra in ort_soup.find_all("a"):
                if stra.get("href")[:2] == "/a" and stra.text.lower().replace(" ", "") not in not_in_list and ort.text not in f_streets:
                    stra_soup = get_soup(website + stra.get("href"))
                    data = get_personell_data(stra_soup)
                    db.insert(data)
                streets += 1
                print("    " + str(streets) + " Streets in: " + str((time() - t_streets)))
            cities += 1
            print(str(cities) + " in: " + str((time()-t_cities)/60))
    db.shut_down()


website = "https://telefonbuch-suche.com"
sub_site = "/a"
not_in_list = ["telefonbuch", "home", "impressum", "anmelden", "eintragen", "agb", "kontakt", "deutschland"]

if __name__ == "__main__":
    main()
