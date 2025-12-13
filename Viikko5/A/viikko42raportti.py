# Copyright (c) 2025 Jonna Kangas

# Ohjelmoinnin perusteet -opintojakso, harjoitustehtävä 5A

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# See <https://www.gnu.org/licenses/>.

from datetime import datetime, date
from typing import List, Tuple

# Rivi: (aikaleima, kulutus_v1_Wh, kulutus_v2_Wh, kulutus_v3_Wh, tuotanto_v1_Wh, tuotanto_v2_Wh, tuotanto_v3_Wh)
Rivi = Tuple[datetime, int, int, int, int, int, int]

def muunna_tiedot(tietue: list[str]) -> Rivi:
    """
    Muuntaa puolipiste-erotellun CSV-rivin kentät oikeiksi tietotyypeiksi.

    Odotettu syöte:
        tietue: Lista, jossa täsmälleen 7 merkkijonoa:
            [ISO8601 datetime, int, int, int, int, int, int]
            - datetime: esim. "2025-10-13T12:00:00" (ISO 8601, ilman aikavyöhykemerkintää)
            - loput kentät: kokonaislukuja (Wh)

    Palauttaa:
        Rivi: Tuple (datetime, int, int, int, int, int, int), jossa kulutus/tuotantoarvot ovat Wh-yksiköissä.

    Poikkeukset:
        ValueError: jos kenttiä ei ole täsmälleen 7, datetime ei ole ISO8601-muodossa
                tai jokin kenttä ei ole muutettavissa int-muotoon.
    """
    # Antaa selkeämmän virheilmoituksen kuin IndexError
    if len(tietue) != 7:
        raise ValueError(f"Odotettiin 7 kenttää, saatiin {len(tietue)}: {tietue}")

    # Palautetaan tuple, jotta se vastaa Rivi-tyyppivihjettä
    return (
        datetime.fromisoformat(tietue[0]),
        int(tietue[1]),
        int(tietue[2]),
        int(tietue[3]),
        int(tietue[4]),
        int(tietue[5]),
        int(tietue[6]),
    )

def lue_data(tiedoston_nimi: str) -> List[Rivi]:
    """
    Lukee puolipiste-erotellun CSV-tiedoston ja palauttaa rivit tupleina (Rivi) oikeilla tietotyypeillä.

    Oletukset:
        - Ensimmäinen rivi on otsikko (ohitetaan automaattisesti).
        - Jokaisella seuraavalla rivillä on 7 kenttää:
          [ISO8601 datetime, int, int, int, int, int, int]
        - Tyhjät rivit ohitetaan.
        - Kenttien muunnos tehdään muunna_tiedot()-funktiolla.
  
    Parametrit:
        tiedoston_nimi (str): Polku CSV-tiedostoon, jossa kentät erotellaan puolipisteellä ';'.

    Palauttaa:
        List[Rivi]: Lista rivejä, jossa jokainen rivi on tuple:
            (datetime, int, int, int, int, int, int)

    Poikkeukset:
        FileNotFoundError / OSError: jos tiedosto puuttuu tai sitä ei voi lukea.
        ValueError: jos jokin rivi ei noudata odotettua muotoa
                    (esim. väärä datetime-muoto tai ei-kokonaislukuarvo).
    """
    tietokanta: List[Rivi] = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f, None)  # Ohittaa ensimmäisen rivin (otsikon) turvallisesti, myös tyhjässä tiedostossa
        for rivi in f:
            rivi = rivi.strip() # Poistaa kaikki alusta ja lopusta löytyvät whitespace-merkit (välilyönti, rivinvaihto, jne.)
            if not rivi:
                continue # Ohita tyhjät rivit
            tietue = rivi.split(";")
            tietokanta.append(muunna_tiedot(tietue))

    return tietokanta

def paivan_tiedot(paiva: date, tietokanta: List[Rivi]) -> List[str]:
    """
    Laskee annetulle päivälle (date) kulutus- ja tuotantosummat vaiheittain ja palauttaa tulostusystävällisen listan merkkijonoja.

    Laskenta:
        - Summataan vaiheittain Wh (v1, v2, v3), sekä tuotanto Wh (v1, v2, v3).
        - Muunnetaan summat kWh-yksikköön (Wh / 1000).
        - Muotoillaan luvut kahden desimaalin tarkkuudella ja pilkulla desimaalierottimena.

    Parametrit:
        paiva (date): Päivä, jolta summat lasketaan.
        tietokanta (List[Rivi]): Luettu tietokanta, jossa jokainen rivi on
            (datetime, kulutus_v1_Wh, kulutus_v2_Wh, kulutus_v3_Wh, tuotanto_v1_Wh, tuotanto_v2_Wh, tuotanto_v3_Wh).
    
    Palauttaa:
        List[str]: Seuraavassa järjestyksessä:
            [
                "dd.mm.yyyy",
                "kulutus_v1_kWh",
                "kulutus_v2_kWh",
                "kulutus_v3_kWh",
                "tuotanto_v1_kWh",
                "tuotanto_v2_kWh",
                "tuotanto_v3_kWh",
            ]
            missä kaikki numerot ovat muotoa "0,00".

    Huomio:
        - Jos päivälle ei ole tietoja, summat ovat 0,00.
    """
    # Summataan ensin Wh, jotta vältytään pyöristysvirheiltä
    kulutus_v1_wh = kulutus_v2_wh = kulutus_v3_wh = 0
    tuotanto_v1_wh = tuotanto_v2_wh = tuotanto_v3_wh = 0

    for tietue in tietokanta:
        if tietue[0].date() == paiva:
            kulutus_v1_wh += tietue[1]
            kulutus_v2_wh += tietue[2]
            kulutus_v3_wh += tietue[3]
            tuotanto_v1_wh += tietue[4]
            tuotanto_v2_wh += tietue[5]
            tuotanto_v3_wh += tietue[6]

    # Muutetaan Wh kWh:ksi
    wh_muunnos_kwh = 1 / 1000.0
    kulutus_v1_kwh = kulutus_v1_wh * wh_muunnos_kwh
    kulutus_v2_kwh = kulutus_v2_wh * wh_muunnos_kwh
    kulutus_v3_kwh = kulutus_v3_wh * wh_muunnos_kwh
    tuotanto_v1_kwh = tuotanto_v1_wh * wh_muunnos_kwh
    tuotanto_v2_kwh = tuotanto_v2_wh * wh_muunnos_kwh
    tuotanto_v3_kwh = tuotanto_v3_wh * wh_muunnos_kwh
    
    # Palautetaan merkkijonot, jotta "\t".join toimii suoraan
    pvm = paiva.strftime("%d.%m.%Y")
    return [
        pvm,
        f"{kulutus_v1_kwh:.2f}".replace(".", ","),
        f"{kulutus_v2_kwh:.2f}".replace(".", ","),
        f"{kulutus_v3_kwh:.2f}".replace(".", ","),
        f"{tuotanto_v1_kwh:.2f}".replace(".", ","),
        f"{tuotanto_v2_kwh:.2f}".replace(".", ","),
        f"{tuotanto_v3_kwh:.2f}".replace(".", ","),
    ]


def main() -> None:
    """
    Pääfunktio:
      - Lukee CSV-datan tiedostosta 'viikko42.csv'
      - Laskee vaiheittaiset kulutus- ja tuotantosummat jokaiselle viikonpäivälle
      - Tulostaa taulukkoraportin (kWh, 2 desimaalia, pilkku desimaalierottimena)
    """
    kulutus_tuotanto_tietokanta = lue_data("viikko42.csv")
    print("\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")
    print("Päivä\t\tPvm\t\tKulutus [kWh]\t\tTuotanto [kWh]")
    print("\t\t(pv.kk.vvvv)\tv1\tv2\tv3\tv1\tv2\tv3")
    print("---------------------------------------------------------------------------")
    print("maanantai\t" + "\t".join(paivan_tiedot(date(2025, 10, 13), kulutus_tuotanto_tietokanta)))
    print("tiistai\t" + "\t" + "\t".join(paivan_tiedot(date(2025, 10, 14), kulutus_tuotanto_tietokanta)))
    print("keskiviikko\t" + "\t".join(paivan_tiedot(date(2025, 10, 15), kulutus_tuotanto_tietokanta)))
    print("torstai\t" + "\t" + "\t".join(paivan_tiedot(date(2025, 10, 16), kulutus_tuotanto_tietokanta)))
    print("perjantai\t" + "\t".join(paivan_tiedot(date(2025, 10, 17), kulutus_tuotanto_tietokanta)))
    print("lauantai\t" + "\t".join(paivan_tiedot(date(2025, 10, 18), kulutus_tuotanto_tietokanta)))
    print("sunnuntai\t" + "\t".join(paivan_tiedot(date(2025, 10, 19), kulutus_tuotanto_tietokanta)))

if __name__ == "__main__":
    main()
