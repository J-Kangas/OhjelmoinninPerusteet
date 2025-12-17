# Copyright (c) 2025 Jonna Kangas

# Ohjelmoinnin perusteet -opintojakso, harjoitustehtävä 6

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# See <https://www.gnu.org/licenses/>.

from datetime import datetime, date

# Rivi: (aika, kulutus (netotettu) kWh, tuotanto (netotettu) kWh, vuorokauden keskilämpötila)
Rivi = tuple[datetime, float, float, float]

def muunna_tiedot(tietue: list[str]) -> Rivi:
    """
    Muuntaa puolipiste-erotellun CSV-rivin kentät oikeiksi tietotyypeiksi.

    Odotettu syöte:
        tietue: Lista, jossa täsmälleen 4 merkkijonoa:
            [ISO8601 datetime, float, float, float]
            - datetime: esim. "2025-01-01T00:00:00.000+02:00" (ISO 8601; mahdollinen aikavyöhykkeen offset)
            - kulutus (netotettu) kWh: desimaaliluku (pilkku- tai piste-erottimella)
            - tuotanto (netotettu) kWh: desimaaliluku (pilkku- tai piste-erottimella)
            - vuorokauden keskilämpötila °C: desimaaliluku (pilkku- tai piste-erottimella)
    
    Palauttaa:
        Rivi: tuple (datetime, float, float, float), jossa kulutus/tuotanto ovat kWh-yksiköissä
              ja lämpötila °C-yksiköissä. Datetime on aikavyöhyketietoinen, jos syötteessä on offset.

    Poikkeukset:
        ValueError: jos kenttiä ei ole täsmälleen 4, datetime ei ole ISO8601-muodossa
                    tai jokin kenttä ei ole muutettavissa float-muotoon.
    """
    # Antaa selkeämmän virheilmoituksen kuin IndexError
    if len(tietue) != 4:
        raise ValueError(f"Odotettiin 4 kenttää, saatiin {len(tietue)}: {tietue}")

    # Palautetaan tuple, jotta se vastaa Rivi-tyyppivihjettä
    # datetime.fromisoformat tukee sekä murto-osia että aikavyöhykkeen offsetin (+02:00)
    # Korvaa pilkku pisteellä eurooppalaisesta desimaalimuodosta
    return (
        datetime.fromisoformat(tietue[0]),
        float(tietue[1].replace(",", ".")),
        float(tietue[2].replace(",", ".")),
        float(tietue[3].replace(",", ".")),
    )

def lue_data(tiedoston_nimi: str) -> list[Rivi]:
    """
    Lukee puolipiste-erotellun CSV-tiedoston ja palauttaa rivit tupleina (Rivi) oikeilla tietotyypeillä.

    Odotettu syöte:
        - tiedoston_nimi (str): Polku CSV-tiedostoon, jossa ensimmäinen rivi on otsikko.
          Otsikot esim.: "Aika; Kulutus (netotettu) kWh; Tuotanto (netotettu) kWh; Vuorokauden keskilämpötila"
          Datassa desimaalierotin voi olla pilkku tai piste (esim. 1,569).

    Toiminta:
        - Ohittaa otsikkorivin turvallisesti.
        - Pilkkoo rivit puolipisteellä ja muuntaa kentät funktiolla muunna_tiedot().

    Palauttaa:
        - list[Rivi]: Lista tupleja (datetime, float, float, float), arvot kWh/°C.

    Poikkeukset:
        - FileNotFoundError / OSError: jos tiedostoa ei löydy tai lukeminen epäonnistuu.
        - ValueError: jos rivin kenttiä ei ole 4, datetime ei ole ISO8601-muotoinen
                      tai jokin kenttä ei ole muunnettavissa desimaaliluvuksi.
    """
    tietokanta: list[Rivi] = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f, None)  # Ohittaa ensimmäisen rivin (otsikon) turvallisesti, myös tyhjässä tiedostossa
        for rivi in f:
            rivi = rivi.strip() # Poistaa kaikki alusta ja lopusta löytyvät whitespace-merkit (välilyönti, rivinvaihto, jne.)
            if not rivi:
                continue # Ohita tyhjät rivit
            tietue = rivi.split(";")
            tietokanta.append(muunna_tiedot(tietue))

    return tietokanta

def nayta_paavalikko() -> int:  
    """
    Tulostaa päävalikon ja kysyy käyttäjän valinnan.

    Toiminta:
        - Näyttää päävalikon vaihtoehdot (1–4).
        - Kysyy valinnan numerona ja toistaa, kunnes käyttäjä antaa kelvollisen arvon.

    Palauttaa:
        - int: Käyttäjän valinta väliltä 1–4.
            1 = Aikavälin raportti
            2 = Kuukausiraportti
            3 = Vuosiraportti
            4 = Lopeta ohjelma
    """
    while True:
        print("---------------------------------------------------------")
        print("Valitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
        print("3) Vuoden 2025 kokonaisyhteenveto")
        print("4) Lopeta ohjelma")
        print("---------------------------------------------------------")
        try:
            valinta = int(input("Anna valinta (numero 1-4): "))
            if 1 <= valinta <= 4:
                return valinta
        except ValueError:
            pass
        print("Virheellinen valinta, yritä uudelleen.\n")

def nayta_jatkovalikko() -> int:   
    """
    Tulostaa jatkovalikon (raportin luonnin jälkeen) ja kysyy käyttäjän valinnan.

    Toiminta:
        - Näyttää jatkovalikon vaihtoehdot (1–3).
        - Kysyy valinnan numerona ja toistaa, kunnes käyttäjä antaa kelvollisen arvon.

    Palauttaa:
        - int: Käyttäjän valinta väliltä 1–3.
            1 = Kirjoita raportti tiedostoon
            2 = Luo uusi raportti
            3 = Lopeta ohjelma
    """
    while True:
        print("---------------------------------------------------------")
        print("Mitä haluat tehdä seuraavaksi?")
        print("1) Kirjoita raportti tiedostoon raportti.txt")
        print("2) Luo uusi raportti")
        print("3) Lopeta")
        print("---------------------------------------------------------")
        try:
            valinta = int(input("Anna valinta (numero 1-3): "))
            if 1 <= valinta <= 3:
                return valinta
        except ValueError:
            pass
        print("Virheellinen valinta, yritä uudelleen.\n")

def luo_aikavalin_raportti(alkupaiva: str, loppupaiva: str, tietokanta: list[Rivi]) -> str:
    """
    Muodostaa yhteenvedon valitulta aikaväliltä (päivärajat mukaan luettuina).

    Odotettu syöte:
        - alkupaiva (str): Päivämäärä muodossa 'pv.kk.vvvv'
        - loppupaiva (str): Päivämäärä muodossa 'pv.kk.vvvv'
        - tietokanta (list[Rivi]): Luettu data, jossa datetime voi olla aikavyöhyketietoinen.
          Päivärajauksessa käytetään tietue[0].date().

    Toiminta:
        - Summaa kulutuksen ja tuotannon (kWh) sekä keskiarvoistaa päivän keskilämpötilan (°C)
          niiltä tietueilta, jotka osuvat aikavälin sisään.

    Palauttaa:
        - str: Muotoiltu raporttiteksti.
    
    Poikkeukset:
        - ValueError: jos päivämäärien muoto on virheellinen (esim. "31.02.2025")
    """
    alku_paiva = int(alkupaiva.split('.')[0])
    alku_kuukausi = int(alkupaiva.split('.')[1])
    alku_vuosi = int(alkupaiva.split('.')[2])
    alku = date(alku_vuosi, alku_kuukausi, alku_paiva)
    loppu_paiva = int(loppupaiva.split('.')[0])
    loppu_kuukausi = int(loppupaiva.split('.')[1])
    loppu_vuosi = int(loppupaiva.split('.')[2])
    loppu = date(loppu_vuosi, loppu_kuukausi, loppu_paiva)
    kulutus = 0
    tuotanto = 0
    vuorokauden_keskilampotila = 0
    tietue_lkm = 0
    for tietue in tietokanta:
        if alku <= tietue[0].date() <= loppu:
            kulutus += tietue[1]
            tuotanto += tietue[2]
            vuorokauden_keskilampotila += tietue[3]
            tietue_lkm += 1
    raportti = "--------------------------------------------------\n"
    raportti += f"Raportti aikaväliltä: {alkupaiva}-{loppupaiva}\n"
    raportti += f"Aikavälin kokonaiskulutus: {kulutus:.2f} kWh\n".replace(".", ",")
    raportti += f"Aikavälin kokonaistuotanto: {tuotanto:.2f} kWh\n".replace(".", ",")
    raportti += f"Aikavälin keskilämpötila: {vuorokauden_keskilampotila/tietue_lkm:.2f} °C\n".replace(".", ",")
    raportti += "--------------------------------------------------\n"
    return raportti

def luo_kuukausiraportti(kuukausi: str, tietokanta: list[Rivi]) -> str:
    """
    Muodostaa yhteenvedon valitulle kuukaudelle.

    Odotettu syöte:
        - kuukausi (str): Kuukauden numero merkkijonona ('1'–'12').
        - tietokanta (list[Rivi]): Luettu data.
    
    Toiminta:
        - Summaa kulutuksen ja tuotannon (kWh) sekä keskiarvoistaa päivän keskilämpötilan (°C)
          valitulta kuukaudelta.

    Palauttaa:
        - str: Muotoiltu raporttiteksti.

    Poikkeukset:
        - ValueError: jos kuukauden numero ei ole kelvollinen ('1'–'12').
    """
    kuukaudet = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu",
                 "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    
    kuukausi = int(kuukausi)
    if not (1 <= kuukausi <= 12):
        raise ValueError(f"Virheellinen kuukauden numero: {kuukausi}")

    kulutus = 0
    tuotanto = 0
    vuorokauden_keskilampotila = 0
    tietue_lkm = 0
    for tietue in tietokanta:
        if tietue[0].date().month == kuukausi:
            kulutus += tietue[1]
            tuotanto += tietue[2]
            vuorokauden_keskilampotila += tietue[3]
            tietue_lkm += 1
    
    raportti = "--------------------------------------------------\n"
    raportti += f"Raportti kuukaudelta: {kuukaudet[kuukausi-1]}\n"
    raportti += f"- kokonaiskulutus: {kulutus:.2f} kWh\n".replace(".", ",")
    raportti += f"- kokonaistuotanto: {tuotanto:.2f} kWh\n".replace(".", ",")
    raportti += f"- keskilämpötila: {vuorokauden_keskilampotila/tietue_lkm:.2f} °C\n".replace(".", ",")
    raportti += "--------------------------------------------------\n"
    return raportti

def luo_vuosiraportti(tietokanta: list[Rivi]) -> str:
    """
    Muodostaa koko datan kattavan vuosiyhteenvedon.

    Toiminta:
        - Summaa kaikkien tietueiden kulutuksen ja tuotannon (kWh),
          sekä laskee keskimääräisen vuorokauden keskilämpötilan (°C).
    
    Huom:
        - Otsikkoteksti on kiinteä "Raportti vuodelta 2025". Jos data kattaa muun vuoden,
          otsikkoa voi parametrisoida jatkossa.

    Palauttaa:
        - str: Muotoiltu raporttiteksti.
    """
    kulutus = 0
    tuotanto = 0
    vuorokauden_keskilampotila = 0
    tietue_lkm = 0
    for tietue in tietokanta:
        kulutus += tietue[1]
        tuotanto += tietue[2]
        vuorokauden_keskilampotila += tietue[3]
        tietue_lkm += 1
    
    raportti = "--------------------------------------------------\n"
    raportti += "Raportti vuodelta 2025\n"
    raportti += f"- kokonaiskulutus: {kulutus:.2f} kWh\n".replace(".", ",")
    raportti += f"- kokonaistuotanto: {tuotanto:.2f} kWh\n".replace(".", ",")
    raportti += f"- keskilämpötila: {vuorokauden_keskilampotila/tietue_lkm:.2f} °C\n".replace(".", ",")
    raportti += "--------------------------------------------------\n"
    return raportti
    
def tulosta_raportti_konsoliin(raportti: str) -> None:
    """
    Tulostaa raportin konsoliin.

    Odotettu syöte:
        - raportti (str): Raporttiteksti.
    """
    print(raportti)

def kirjoita_raportti_tiedostoon(raportti: str) -> None:
    """
    Kirjoittaa raportin tiedostoon 'raportti.txt'.

    Odotettu syöte:
        - raportti (str): Raporttiteksti.

    Toiminta:
        - Luo tai ylikirjoittaa tiedoston 'raportti.txt' ja kirjoittaa raportin sinne.
    
    Poikkeukset:
        - OSError: jos tiedostoon kirjoittaminen epäonnistuu.
    """
    with open("raportti.txt", "w", encoding="utf-8") as f:
        f.write(raportti)

def main() -> None:
    """
    Ohjelman pääfunktio: lukee datan, näyttää valikot ja ohjaa raporttien luomista.

    Toiminta:
        - Lukee datan tiedostosta '2025.csv'.
        - Näyttää päävalikon; valinnat 1–3 tuottavat raportin ja vievät jatkovalikkoon.
        - Valinta 4 lopettaa ohjelman välittömästi.
        - Jatkovalikon valinta 1 kirjoittaa raportin tiedostoon,
          valinta 2 palaa päävalikkoon, valinta 3 lopettaa ohjelman.
    """
    # Luetaan data tiedostosta
    kulutus_ja_tuotanto_2025: list[Rivi] = lue_data("2025.csv")

    while True:
        # Päävalikon käsittely
        ensimmainen_valinta = nayta_paavalikko()
        if ensimmainen_valinta == 1:
            alkupaiva = input("Anna alkupäivä (pv.kk.vvvv): ")
            loppupaiva = input("Anna loppupäivä (pv.kk.vvvv): ")
            raportti = luo_aikavalin_raportti(alkupaiva, loppupaiva, kulutus_ja_tuotanto_2025)
            tulosta_raportti_konsoliin(raportti)
        elif ensimmainen_valinta == 2:
            kuukausi = input("Anna kuukauden numero (1–12): ")
            raportti = luo_kuukausiraportti(kuukausi, kulutus_ja_tuotanto_2025)
            tulosta_raportti_konsoliin(raportti)
        elif ensimmainen_valinta == 3:
            raportti = luo_vuosiraportti(kulutus_ja_tuotanto_2025)
            tulosta_raportti_konsoliin(raportti)
        elif ensimmainen_valinta == 4:
            print("Lopetaan ohjelma!")
            break
        else:
            continue  
        # Jatkovalikon käsittely
        toinen_valinta = nayta_jatkovalikko()
        if toinen_valinta == 1:
            kirjoita_raportti_tiedostoon(raportti)
            print("Raportti kirjoitettu tiedostoon.")
        elif toinen_valinta == 2:
            # Uusi raportti -> palaa päävalikkoon
            continue
        elif toinen_valinta == 3:
            print("Lopetaan ohjelma!")
            return  # lopeta koko ohjelma
        else:
            continue

if __name__ == "__main__":
    main()