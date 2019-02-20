import requests
import sqlite3 as sql
from time import time
import lxml.html as lx


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

    def shut_down(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()


def test_lxml(rel_path):
    http = requests.get(website + rel_path)
    doc = lx.fromstring(http.text)
    content = doc.xpath("//div[@class=\"content\"]")
    links = content[0].iterlinks()
    result = list()
    for link in links:
        if link[2][:2] != "//":
            result.append(link[2])
    return result


def personell_lxml(rel_path, street_link):
    http = requests.get(website + rel_path)
    doc = lx.fromstring(http.text)
    content = doc.xpath("//div[@class=\"content\"]")
    text = str(content[0].text_content())
    anschrift = text[text.find("Adresse:")+8:text.find("Telefonnummer:")].strip().split()
    telefon_nummer = text[text.find("Telefonnummer:")+14:text.find("Kontaktdaten:")].strip()
    sep = str(street_link).split("/")
    ort, plz, strasse, hs_nr, name = "", "", "", "", ""
    for word in reversed(anschrift):
        if word.isdigit() and len(word) == 5:
            plz = word
            break
        else:
            ort += word
    anschrift.pop(anschrift.index(plz))
    anschrift.pop(anschrift.index(ort))
    if anschrift[len(anschrift)-1].isdigit():
        hs_nr = anschrift[len(anschrift)-1]
        anschrift.pop()
    elif anschrift[len(anschrift)-2].isdigit():
        hs_nr = anschrift[len(anschrift)-2] + " " + anschrift[len(anschrift)-1]
        anschrift.pop()
        anschrift.pop()
    k = len(anschrift)
    while strasse.strip().replace(" ", "-").lower() != sep[3]:
        k = k - 1
        strasse = anschrift[k] + " " + strasse
    for j in range(k):
        name = name + " " + anschrift[j]
    result = tuple([str(name.strip()), str(strasse.strip() + " " + hs_nr), str(plz), str(ort), telefon_nummer])
    return result


def main_lxml():
    t = time()
    db = Database("cities/cities.db")
    cities = test_lxml(sub_site)
    for i, city in enumerate(cities):
        streets = test_lxml(str(city))
        for j, street in enumerate(streets):
            citizens = test_lxml(str(street))
            people = list()
            for citizen in citizens:
                people.append(personell_lxml(citizen, street))
            db.insert(people)
            print("    " + str(j+1) + " streets in: " + str(time()-t))

    pers_data = personell_lxml(citizens[0], streets[0])
    print(pers_data)


website = "https://telefonbuch-suche.com"
sub_site = "/a"

if __name__ == "__main__":
    main_lxml()