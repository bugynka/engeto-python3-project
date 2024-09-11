"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Kateřina Bálint
email: k.svobodova.8@seznam.cz
discord: katerinabalint_41161
"""

# import použítých knihoven

import csv
from requests import get
from bs4 import BeautifulSoup
from funkce import *

# definování proměnných a rozčlenění HTML kódu pro další práci

odkaz_volby = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
odpoved_odkaz = get(odkaz_volby)
rozdeleny_odkaz = BeautifulSoup(odpoved_odkaz.text, "html.parser")
vsechny_a_tagy = rozdeleny_odkaz.select(".center > a")
platne_odkazy = []

# vytvoření seznamu všech odkazů, které může uživatel zadat

for a_tag in vsechny_a_tagy:
     platne_odkazy.append("volby.cz/pls/ps2017nss/"+a_tag.attrs["href"])

# získání vstupů od uživatele a příprava odkazu na porovnání se seznamem možných odkazů z předchozího kroku

zadany_odkaz = sys.argv[1]
cisty_odkaz = zadany_odkaz.replace("https://", "").replace("http://", "").replace("www.", "")
vysledny_soubor = sys.argv[2]

# ověření, zda uživatel zadal správné argumenty

print("Ověřuji správnost vstupu")

over_vstup(cisty_odkaz, platne_odkazy, vysledny_soubor)

# úprava HTML kódu v zadaném odkazu pro další použití

odpoved = get(zadany_odkaz)
rozdelene_html = BeautifulSoup(odpoved.text, "html.parser")

vsechny_a_tagy_obce = rozdelene_html.select(".cislo > a")
vsechny_odkazy_obce = []

# vytvoření seznamu všech odkazů s volebními výsledky obcí, které se nacházejí v HTML kódu uživatelem zadaného odkazu

for a_tag_obce in vsechny_a_tagy_obce:
    vsechny_odkazy_obce.append("https://volby.cz/pls/ps2017nss/" + a_tag_obce.attrs["href"])

# definování proměnných pro zápis do CSV souboru

zahlavi = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"]
vsechny_radky = []
strany_pridany = False

# postupné procházení všech odkazů a získávání požadovaných informací do proměnných

for odkaz_obce in vsechny_odkazy_obce:
    rozdeleny_odkaz_obce = uprav_odkaz_obce(odkaz_obce)
    radek = [ziskej_kod_obce(odkaz_obce)]
    radek = radek + ziskej_nazev_obce(rozdeleny_odkaz_obce)

    print(f'Získávám údaje pro obec {ziskej_nazev_obce(rozdeleny_odkaz_obce)[0]}.')

    radek.append(ziskej_volice_v_seznamu(rozdeleny_odkaz_obce))
    radek.append(ziskej_vydane_obalky(rozdeleny_odkaz_obce))
    radek.append(ziskej_platne_hlasy(rozdeleny_odkaz_obce))

    if not strany_pridany:
        zahlavi += ziskej_kandidujici_strany(rozdeleny_odkaz_obce)
        strany_pridany = True

    radek = radek + list(ziskej_hlasy_pro_stranu(rozdeleny_odkaz_obce).values())
    vsechny_radky.append(radek)

# vytvoření CSV souboru a příprava na zápis řádků

nove_csv = open(vysledny_soubor, mode="w", newline="", encoding="utf-8")
zapisovac = csv.writer(nove_csv)

# vložení řádků do CSV souboru

zapisovac.writerow(zahlavi)

for jeden_radek in vsechny_radky:
    zapisovac.writerow(jeden_radek)

# zavření CSV souboru

nove_csv.close()

print("CSV soubor byl úspěšně vytvořen.")