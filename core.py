import requests
from bs4 import BeautifulSoup
from time import time


class People:

    """
    class for personal data
    """

    def __init__(self, name, street, zip_code, town, phone):
        self.name = str(name)
        self.street = str(street)
        self.zip_code = str(zip_code)
        self.town = str(town)
        self.phone = str(phone)

    def print_all(self):

        """
        function to concatenate into csv
        :return semicolon separated string:
        """

        return str(self.name) + ";" + str(self.street) + ";" + str(self.zip_code) + ";" + str(self.town) + ";" + str(self.phone)


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
    yellow_pages = list()
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
                            yellow_pages.append(Anwohner(str(pees[2][0]).strip(),
                                                         str(pees[2][2]).strip(),
                                                         str(pees[2][4]).strip().split(" ")[0],
                                                         str(pees[2][4]).strip().split(" ")[1],
                                                         str(pees[3][0]).strip()))
                streets += 1
                print("    " + str(streets) + " Streets (" + str(len(yellow_pages)) + " people) in: " + str((time()-t_streets)))
            with open("cities" + ort.text + ".csv", "w") as file:
                file.write("Name;Straße;PLZ;Ort;Telefon\n")
                for elem in yellow_pages:
                    file.write(elem.print_all() + "\n")
            yellow_pages = list()
            cities += 1
            print(str(cities) + " in: " + str((time()-t_cities)/60))


if __name__ == "__main__":
    main()
