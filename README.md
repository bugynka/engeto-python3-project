#  Elections Scraper

Třetí projekt na Python akademii od Engeta.

###  Popis projektu

Tento projekt slouží ke stahování a ukládání výsledků voleb do Poslanecké sněmovny z roku 2017. Rozcestník se nachází pod [tímto odkazem](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

###  Instalace knihoven

Knihovny, které jsou použity v kódu, jsou vypsané v souboru `requirements.txt`. Pro instalaci je nejvhodnější použít nové virtuální prostředí a s nainstalovaným manažerem spustit takto:

```bash
$ pip3 --version                       # overime verzi manazeru
$ pip3 install -r requirements.txt     # nainstalujeme knihovny
```

###  Spuštění knihoven

Spuštění souboru `Script.py` v příkazovém řádku vyžaduje zadání dvou povinných argumentů.

```python
python Script <odkaz-uzemniho-celku> <nazev-vystupniho-souboru.csv>
```

Program zkontroluje správnost vstupu a v případě, že jsou zadané argumenty v pořádku, vygeneruje CSV soubor s volebními výsledky.

###  Ukázka projektu

Výsledky hlasování pro okres Třebíč:
1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104`
2. argument: `vysledky_Trebic.csv`

###  Spuštění programu

```bash
python Script.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104" vysledky_Trebic.csv
```

###  Průběh stahování

```bash
Ověřuji správnost vstupu
Získávám údaje pro obec Babice.
Získávám údaje pro obec Bačice.
Získávám údaje pro obec Bačkovice.
...
CSV soubor byl úspěšně vytvořen.
```

###  Částečný výstup


```csv
kód obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,Občanská demokratická strana,...
590274,Babice,167,126,126,9,0,0,11,0,8,9,0,0,3,0,0,16,0,1,40,0,19,0,1,0,0,7,2
590282,Bačice,165,104,104,1,1,0,5,0,6,23,0,1,0,0,0,5,1,2,33,1,7,0,0,0,0,14,4
...
```
