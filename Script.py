"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Kateřina Bálint
email: k.svobodova.8@seznam.cz
discord: katerinabalint_41161
"""

# import použitých knihoven

import sys
import re
import csv
from requests import get
from bs4 import BeautifulSoup


# definování jednotlivých funkcí


def vytvor_mozne_odkazy() -> list:
    """Tato funkce slouží k získání seznamu všech odkazů, které může uživatel zadat."""

    odkaz_volby = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    odpoved_odkaz = get(odkaz_volby)
    rozdeleny_odkaz = BeautifulSoup(odpoved_odkaz.text, "html.parser")
    vsechny_a_tagy = rozdeleny_odkaz.select(".center > a")
    platne_odkazy = ["volby.cz/pls/ps2017nss/" + a_tag.attrs["href"] for a_tag in vsechny_a_tagy]

    return platne_odkazy


def ziskej_vstup_od_uzivatele() -> str:
    """Tato funkce slouží k získání vstupu od uživatele a úpravě zadaného odkazu."""

    zadany_odkaz = sys.argv[1]
    vysledny_soubor = sys.argv[2]
    cisty_odkaz = zadany_odkaz.replace("https://", "").replace("http://", "").replace("www.", "")

    return zadany_odkaz, vysledny_soubor, cisty_odkaz


def over_vstup(cisty_odkaz, platne_odkazy, vysledny_soubor) -> None:
    """Tato funkce ověřuje, zda uživatel zadal 2 argumenty a zda je jejich formát správný.
    Pokud ne, upozorní ho a nepokračuje."""

    print("Ověřuji správnost vstupu")

    if len(sys.argv) != 3:
        print("Nezadal jsi všechny argumenty")
        sys.exit(1)
    if cisty_odkaz not in platne_odkazy:
        print("Zadal jsi neplatný odkaz.")
        sys.exit(1)
    if not vysledny_soubor.endswith(".csv"):
        print("Zadal jsi nesprávný formát výstupu.")
        sys.exit(1)


def uprav_zadany_odkaz(zadany_odkaz) -> BeautifulSoup:
    """úprava HTML kódu v zadaném odkazu pro další použití."""

    odpoved = get(zadany_odkaz)
    rozdelene_html = BeautifulSoup(odpoved.text, "html.parser")

    return rozdelene_html


def vytvor_vsechny_odkazy(rozdelene_html) -> list:
    """Vytvoří seznam všech odkazů s volebními výsledky obcí, které se nacházejí v HTML kódu uživatelem zadaného odkazu."""

    vsechny_a_tagy_obce = rozdelene_html.select(".cislo > a")
    vsechny_odkazy_obce = ["https://volby.cz/pls/ps2017nss/" + a_tag_obce.attrs["href"] for a_tag_obce in vsechny_a_tagy_obce]

    return vsechny_odkazy_obce


def ziskej_kod_obce(odkaz_obce) -> str:
    """Funkce z odkazu v HTML kódu zadané stánky extrahuje kód obce."""

    nalezene_cislo = re.search(r"xobec=(\d+)", odkaz_obce)
    kod = nalezene_cislo.group(1)

    return kod


def ziskej_nazev_obce(rozdeleny_odkaz_obce) -> list:
    """Funkce v HTML kódu vyhledá názvy obcí."""

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
    """Funkce v HTML kódu vyhledá názvy kandidujících stran."""

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


def ziskej_udaje(vsechny_odkazy_obce) -> list:
    """Funkce upraví HTML kód v jednotlivých odkazech a získá z něj potřebné údaje pro vytvoření výsledného souboru."""

    zahlavi = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"]
    vsechny_radky = []
    strany_pridany = False

    for odkaz_obce in vsechny_odkazy_obce:
        odpoved_obce = get(odkaz_obce)
        rozdeleny_odkaz_obce = BeautifulSoup(odpoved_obce.text, "html.parser")
        radek = [ziskej_kod_obce(odkaz_obce)]
        radek = radek + ziskej_nazev_obce(rozdeleny_odkaz_obce)

        print(f"Získávám údaje pro obec {ziskej_nazev_obce(rozdeleny_odkaz_obce)[0]}")

        radek.append(ziskej_volice_v_seznamu(rozdeleny_odkaz_obce))
        radek.append(ziskej_vydane_obalky(rozdeleny_odkaz_obce))
        radek.append(ziskej_platne_hlasy(rozdeleny_odkaz_obce))

        if not strany_pridany:
            zahlavi += ziskej_kandidujici_strany(rozdeleny_odkaz_obce)
            strany_pridany = True

        radek = radek + list(ziskej_hlasy_pro_stranu(rozdeleny_odkaz_obce).values())
        vsechny_radky.append(radek)

    return zahlavi, vsechny_radky


def zapis_do_csv(vysledny_soubor, zahlavi, vsechny_radky):
    """Zapíše data do CSV souboru"""

    with open(vysledny_soubor, mode="w", newline="", encoding="utf-8") as nove_csv:
        zapisovac = csv.writer(nove_csv)
        zapisovac.writerow(zahlavi)

        for jeden_radek in vsechny_radky:
            zapisovac.writerow(jeden_radek)

    print("CSV soubor byl úspěšně vytvořen.")


def main():

    """Hlavní funkce, ve které se postupně spouštějí předchozí funkce."""

    # získání všech platných odkazů, které může uživatel zadat
    platne_odkazy = vytvor_mozne_odkazy()

    # získání vstupů od uživatele
    zadany_odkaz, vysledny_soubor, cisty_odkaz = ziskej_vstup_od_uzivatele()

    # ověření vstupů od uživatele
    over_vstup(cisty_odkaz, platne_odkazy, vysledny_soubor)

    # zpracování HTML uživatelem zadaného odkazu
    rozdelene_html = uprav_zadany_odkaz(zadany_odkaz)

    # získání odkazů na obce z HTML kódu
    vsechny_odkazy_obce = vytvor_vsechny_odkazy(rozdelene_html)

    # získání dat pro všechny obce
    zahlavi, vsechny_radky = ziskej_udaje(vsechny_odkazy_obce)

    # zápis dat do CSV souboru
    zapis_do_csv(vysledny_soubor, zahlavi, vsechny_radky)

 # spuštění hlavní funkce

if __name__ == "__main__":
    main()
