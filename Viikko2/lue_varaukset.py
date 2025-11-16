"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime, timedelta

def main():

    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    varaus = varaus.split('|')
    varausnumero = int(varaus[0])
    varaajan_nimi = str(varaus[1])
    varauspaiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    suomalainen_varauspaiva = varauspaiva.strftime("%d.%m.%Y")
    aloitusaika = datetime.strptime(varaus[3], "%H:%M")
    suomalainen_aloitusaika = aloitusaika.strftime("%H.%M")
    tuntimaara = int(varaus[4])
    tuntihinta = float(varaus[5])
    suomalainen_tuntihinta = f"{tuntihinta:.2f}".replace(".", ",")
    kokonaishinta = float(tuntimaara*tuntihinta)
    suomalainen_kokonaishinta = f"{kokonaishinta:.2f}".replace(".", ",")
    maksettu = bool(varaus[6])
    varauskohde = str(varaus[7])
    puhelin = str(varaus[8])
    sahkoposti = str(varaus[9])
    loppumisaika = aloitusaika + timedelta(hours=tuntimaara)
    suomalainen_loppumisaika = loppumisaika.strftime("%H.%M")

    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {varaajan_nimi}")
    print(f"Päivämäärä: {suomalainen_varauspaiva}")
    print(f"Aloitusaika: {suomalainen_aloitusaika}")
    print(f"Tuntimäärä: {tuntimaara}")
    print(f"Loppumisaika: {suomalainen_loppumisaika}")
    print(f"Tuntihinta: {suomalainen_tuntihinta} €")
    print(f"Kokonaishinta: {suomalainen_kokonaishinta} €")
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    print(f"Kohde: {varauskohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {sahkoposti}")


    # Tulostetaan varaus konsoliin
    # print(varaus)

    # Kokeile näitä
    #print(varaus.split('|'))
    #varausId = varaus.split('|')[0]
    #print(varausId)
    #print(type(varausId))
    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    main()