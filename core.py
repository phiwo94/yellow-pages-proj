import requests
from bs4 import BeautifulSoup
from time import time


class Anwohner:
    def __init__(self, name, strasse, plz, ort, telefon):
        self.name = str(name)
        self.strasse = str(strasse)
        self.plz = str(plz)
        self.ort = str(ort)
        self.telefon = str(telefon)

    def print_all(self):
        return str(self.name) + ";" + str(self.strasse) + ";" + str(self.plz) + ";" + str(self.ort) + ";" + str(self.telefon)


def get_soup(url: str):
    return BeautifulSoup(requests.get(url).text, features="html.parser")


def list_join(arr, sep=" "):
    result = ""
    for i in range(len(arr)):
        if i < len(arr)-1:
            result = result + arr[i] + sep
        else:
            result = result + arr[i] + "\n"
    return result


if __name__ == "__main__":
    website = "https://telefonbuch-suche.com"
    sub_site = "/a"
    soup = get_soup(website + sub_site)
    yellow_pages = list()
    not_in_list = ["telefonbuch", "home", "impressum", "anmelden", "eintragen", "agb", "kontakt", "deutschland"]
    cities, streets, names = 0, 0, 0
    t_cities = time()
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
                            yellow_pages.append(Anwohner(str(pees[2][0]).strip(), str(pees[2][2]).strip(), str(pees[2][4]).strip().split(" ")[0], str(pees[2][4]).strip().split(" ")[1], str(pees[3][0]).strip()))
                streets += 1
                print("    " + str(streets) + " Streets (" + str(len(yellow_pages)) + " people) in: " + str((time()-t_streets)))
            with open("cities" + ort.text + ".csv", "w") as file:
                file.write("Name;Straße;PLZ;Ort;Telefon\n")
                for elem in yellow_pages:
                    file.write(elem.print_all() + "\n")
            yellow_pages = list()
            cities += 1
            print(str(cities) + " in: " + str((time()-time())/60))
