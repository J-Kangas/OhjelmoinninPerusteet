"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus):
    varausnumero = int(varaus[0])
    print(f"Varausnumero: {varausnumero}")

def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def hae_paiva(varaus):
    varauspaiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    suomalainen_varauspaiva = varauspaiva.strftime("%d.%m.%Y")
    print(f"Päivämäärä: {suomalainen_varauspaiva}")

def hae_aloitusaika(varaus):
    aloitusaika = datetime.strptime(varaus[3], "%H:%M")
    suomalainen_aloitusaika = aloitusaika.strftime("%H.%M")
    print(f"Aloitusaika: {suomalainen_aloitusaika}")

def hae_tuntimaara(varaus):
    tuntimaara = int(varaus[4])
    print(f"Tuntimäärä: {tuntimaara}")

def hae_tuntihinta(varaus):
    tuntihinta = float(varaus[5])
    suomalainen_tuntihinta = f"{tuntihinta:.2f}".replace(".", ",")
    print(f"Tuntihinta: {suomalainen_tuntihinta} €")

def laske_kokonaishinta(varaus):
    kokonaishinta = int(varaus[4]) * float(varaus[5])
    suomalainen_kokonaishinta = f"{kokonaishinta:.2f}".replace(".", ",")
    print(f"Kokonaishinta: {suomalainen_kokonaishinta} €")

def hae_maksettu(varaus):
    maksettu = bool(varaus[6])
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")

def hae_kohde(varaus):
    varauskohde = str(varaus[7])
    print(f"Varauskohde: {varauskohde}")

def hae_puhelin(varaus):
    puhelin = str(varaus[8])
    print(f"Puhelin: {puhelin}")   

def hae_sahkoposti(varaus):
    sahkoposti = str(varaus[9])
    print(f"Sähköposti: {sahkoposti}")

def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        varaus = varaus.split('|')

    # Toteuta loput funktio hae_varaaja(varaus) mukaisesti
    # Luotavat funktiota tekevat tietotyyppien muunnoksen
    # ja tulostavat esimerkkitulosteen mukaisesti

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)

if __name__ == "__main__":
    main()