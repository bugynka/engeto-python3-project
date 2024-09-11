# tento soubor slouží k uložení funkcí

# import použítých knihoven
import sys
import re
from bs4 import BeautifulSoup
from requests import get


# funkce a jejich popis

def over_vstup(cisty_odkaz, platne_odkazy, vysledny_soubor) -> None:
    """Tato funkce ověřuje, zda uživatel zadal 2 argumenty a zda je jejich formát správný.
    Pokud ne, upozorní ho a nepokračuje."""

    if len(sys.argv) != 3:
        print("Nezadal jsi všechny argumenty")
        sys.exit(1)
    if cisty_odkaz not in platne_odkazy:
        print("Zadal jsi neplatný odkaz.")
        sys.exit(1)
    if not vysledny_soubor.endswith(".csv"):
        print("Zadal jsi nesprávný formát výstupu.")
        sys.exit(1)


def ziskej_kod_obce(odkaz_obce) -> str:
    """Funkce z odkazu v HTML kódu zadané stánky extrahuje kód obce."""

    nalezene_cislo = re.search(r"xobec=(\d+)", odkaz_obce)
    kod = nalezene_cislo.group(1)

    return kod


def uprav_odkaz_obce(odkaz_obce) -> BeautifulSoup:
    """Funkce rozčlení HTML kód v jednotlivých odkazech na výsledky obcí tak, abychom v něm mohli snadno vyhledávat."""

    odpoved_obce = get(odkaz_obce)

    return BeautifulSoup(odpoved_obce.text, "html.parser")


def ziskej_nazev_obce(rozdeleny_odkaz_obce) -> list:
    """Funkce v HTML kódu vyhledá název obce."""

    nazev_obce = rozdeleny_odkaz_obce.select(".topline > h3")
    nazvy_obci = [td.text.strip().replace("Obec: ", "") for td in nazev_obce[2]]

    return nazvy_obci


def ziskej_volice_v_seznamu(rozdeleny_odkaz_obce) -> str:
    """Funkce v HTML kódu vyhledá počet voličů v seznamu."""

    volici_z_odkazu = rozdeleny_odkaz_obce.find("td", {"headers": "sa2"})
    seznam_volici = volici_z_odkazu.text.strip().replace("\xa0", " ")

    return seznam_volici


def ziskej_vydane_obalky(rozdeleny_odkaz_obce) -> str:
    """Funkce v HTML kódu vyhledá počet vydaných obálek."""

    obalky_z_odkazu = rozdeleny_odkaz_obce.find("td", {"headers": "sa3"})
    seznam_obalky = obalky_z_odkazu.text.strip().replace('\xa0', ' ')

    return seznam_obalky


def ziskej_platne_hlasy(rozdeleny_odkaz_obce) -> str:
    """Funkce v HTML kódu vyhledá počet platných hlasů."""

    hlasy_celkem_z_odkazu = rozdeleny_odkaz_obce.find("td", {"headers": "sa6"})
    seznam_hlasy_celkem = hlasy_celkem_z_odkazu.text.strip().replace("\xa0", " ")

    return seznam_hlasy_celkem


def ziskej_kandidujici_strany(rozdeleny_odkaz_obce) -> list:
    """Funkce v HTML kódu vyhledá počet kandidující strany."""

    strany_z_odkazu = rozdeleny_odkaz_obce.find_all("td", {"class": "overflow_name"})
    seznam_strany = [td.text.strip() for td in strany_z_odkazu]

    return seznam_strany


def ziskej_hlasy_pro_stranu(rozdeleny_odkaz_obce) -> dict:
    """Funkce v HTML kódu vyhledá počet hlasů pro jednotlivé kandidující strany."""

    strany_z_odkazu = rozdeleny_odkaz_obce.select(".overflow_name")
    seznam_hlasy_strana = {}
    for strana in strany_z_odkazu:
        seznam_hlasy_strana[strana.text] = strana.find_next_sibling("td").text.replace("\xa0", " ")

    return seznam_hlasy_strana
