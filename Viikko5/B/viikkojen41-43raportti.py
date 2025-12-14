# Copyright (c) 2025 Jonna Kangas

# Ohjelmoinnin perusteet -opintojakso, harjoitustehtävä 5A

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# See <https://www.gnu.org/licenses/>.

from datetime import datetime, date, timedelta

# Rivi: (aikaleima, kulutus_v1_Wh, kulutus_v2_Wh, kulutus_v3_Wh, tuotanto_v1_Wh, tuotanto_v2_Wh, tuotanto_v3_Wh)
Rivi = tuple[datetime, int, int, int, int, int, int]

def muunna_tiedot(tietue: list[str]) -> Rivi:
    """
    Muuntaa puolipiste-erotellun CSV-rivin kentät oikeiksi tietotyypeiksi.

    Odotettu syöte:
        tietue: Lista, jossa täsmälleen 7 merkkijonoa:
            [ISO8601 datetime, int, int, int, int, int, int]
            - datetime: esim. "2025-10-13T12:00:00" (ISO 8601, ilman aikavyöhykemerkintää)
            - loput kentät: kokonaislukuja (Wh)

    Palauttaa:
        Rivi: tuple (datetime, int, int, int, int, int, int), jossa kulutus/tuotantoarvot ovat Wh-yksiköissä.

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

def lue_data(tiedoston_nimi: str) -> list[Rivi]:
    """
    Lukee puolipiste-erotellun CSV-tiedoston ja palauttaa rivit tupleina (Rivi) oikeilla tietotyypeillä.

    Odotettu syöte:
        - tiedoston_nimi (str): Polku CSV-tiedostoon, jossa ensimmäinen rivi on otsikko.
            Kentät: [ISO8601 datetime, int, int, int, int, int, int]; tyhjät rivit ohitetaan.

    Toiminta:
    - Ohittaa otsikkorivin, pilkkoo kentät puolipisteellä, ja kutsuu muunna_tiedot() jokaiselle riville.

    Palauttaa:
    - list[Rivi]: Lista tuple (datetime, int x 6), arvot Wh-yksiköissä.

    Poikkeukset:
    - FileNotFoundError / OSError: jos tiedostoa ei löydy tai lukeminen epäonnistuu.
    - ValueError: jos rivin kenttiä ei ole 7, datetime ei ole ISO8601-muotoinen
      tai jokin kenttä ei ole muunnettavissa kokonaisluvuksi.

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

def paivan_tiedot(paiva: date, tietokanta: list[Rivi]) -> list[str]:
    """
    Laskee annetun päivän kulutus- ja tuotantosummat vaiheittain ja palauttaa ne tulostusystävällisinä merkkijonoina.

    Odotettu syöte:
    - paiva (date): Päivä, jolta summat lasketaan.
    - tietokanta (list[Rivi]): Mittausrivit muodossa
      (datetime, kulutus_v1_Wh, kulutus_v2_Wh, kulutus_v3_Wh,
       tuotanto_v1_Wh, tuotanto_v2_Wh, tuotanto_v3_Wh).

    Toiminta:
    - Summaa Wh-arvot (v1-v3 kulutus, v1-v3 tuotanto) ja muuntaa ne kWh:ksi (Wh / 1000),
      muotoillen luvut kahden desimaalin tarkkuudella ja pilkun desimaalierottimena.

    Palauttaa:
    - list[str]: ["dd.mm.yyyy", "kulutus_v1_kWh", "kulutus_v2_kWh", "kulutus_v3_kWh",
                  "tuotanto_v1_kWh", "tuotanto_v2_kWh", "tuotanto_v3_kWh"].
      Kaikki numerot muodossa "0,00".

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

def viikkoraportti(viikon_numero: int, aloituspaiva: date, tietokanta: list[Rivi]) -> str: 
    """
    Muodostaa kiinteäleveyksisen viikkoraportin annetun viikon päiville.

    Odotettu syöte:
    - viikon_numero (int): Raportoitavan viikon numero.
    - aloituspaiva (date): Viikon maanantai.
    - tietokanta (list[Rivi]): Mittausrivit (datetime + 6 × Wh).

    Toiminta:
    - Laskee jokaiselle viikonpäivälle (maanantai–sunnuntai) kulutuksen ja tuotannon (v1..v3),
      hyödyntäen paivan_tiedot()-funktiota, ja tuottaa vasemmalle tasattuun tekstiin otsikot, erotinrivit ja päivärivit.

    Palauttaa:
    - str: Raporttiteksti (otsikot + erotinrivit + 7 päiväriviä).
    """
    # Lista viikonpäivistä
    viikonpaivat: list[str] = [
        "maanantai", "tiistai", "keskiviikko", "torstai",
        "perjantai", "lauantai", "sunnuntai"
    ]

    # Sarakeleveydet
    leveys_viikonpaiva: int = 13   # "Viikonpäivä"-sarakkeen leveys
    leveys_paivamaara: int = 13  # "Päivämäärä"-sarakkeen leveys (dd.mm.yyyy)
    leveys_numero: int = 8    # Numeroiden (v1–v3 kulutus ja v1–v3 tuotanto) leveys
    vaiheiden_leveys = 3 * leveys_numero  # leveys = 3 * leveys_numero = yhden ryhmän leveys (v1..v3)
    tekstin_leveys = leveys_viikonpaiva + leveys_paivamaara  # teksti-osuuden yhteisleveys

    # Otsikkorivit
    r: list[str] = []
    r.append(f"\nViikon {viikon_numero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    
    header1 = (
        f"{'Viikonpäivä':<{leveys_viikonpaiva}}" # Tasattu vasempaan reunaan
        f"{'Päivämäärä':<{leveys_paivamaara}}" # Tasattu vasempaan reunaan
         f"{'Kulutus [kWh]':<{vaiheiden_leveys}}" # Tasattu vasempaan reunaan
         f"{'Tuotanto [kWh]':<{vaiheiden_leveys}}" # Tasattu vasempaan reunaan
    )

    # Alarivi: v1 v2 v3 -otsikot molemmille lohkoille
    header2 = (
        f"{'':<{tekstin_leveys}}" # Tasattu vasempaan reunaan
        f"{'v1':<{leveys_numero}}" # Tasattu vasempaan reunaan
        f"{'v2':<{leveys_numero}}" # Tasattu vasempaan reunaan
        f"{'v3':<{leveys_numero}}" # Tasattu vasempaan reunaan
        f"{'v1':<{leveys_numero}}" # Tasattu vasempaan reunaan
        f"{'v2':<{leveys_numero}}" # Tasattu vasempaan reunaan
        f"{'v3':<{leveys_numero}}" # Tasattu vasempaan reunaan
    )

    r.append(header1)
    r.append(header2)
    # Erotinrivi: 2 tekstikenttää + 6 numeroa → pituus leveys_viikonpaiva + leveys_paivamaara + 6*leveys_numero
    r.append("-" * (leveys_viikonpaiva + leveys_paivamaara + leveys_numero*6))

    # Rivit: yksi per viikonpäivä
    for i, paiva in enumerate(viikonpaivat):
        # Oletus: paivan_tiedot palauttaa listan (list[str]):
        # [pvm, kulutus_v1, kulutus_v2, kulutus_v3, tuotanto_v1, tuotanto_v2, tuotanto_v3]
        paivan_arvot = paivan_tiedot(aloituspaiva + timedelta(days=i), tietokanta)
        pvm = paivan_arvot[0]
        kulutus_v1, kulutus_v2, kulutus_v3, tuotanto_v1, tuotanto_v2, tuotanto_v3 = paivan_arvot[1:7]

        row = (
                f"{paiva:<{leveys_viikonpaiva}}" # Tasattu vasempaan reunaan
                f"{pvm:<{leveys_paivamaara}}" # Tasattu vasempaan reunaan
                f"{kulutus_v1:<{leveys_numero}}" # Tasattu vasempaan reunaan
                f"{kulutus_v2:<{leveys_numero}}" # Tasattu vasempaan reunaan
                f"{kulutus_v3:<{leveys_numero}}" # Tasattu vasempaan reunaan
                f"{tuotanto_v1:<{leveys_numero}}" # Tasattu vasempaan reunaan
                f"{tuotanto_v2:<{leveys_numero}}" # Tasattu vasempaan reunaan
                f"{tuotanto_v3:<{leveys_numero}}" # Tasattu vasempaan reunaan
            )
        r.append(row)

    r.append("-" * (leveys_viikonpaiva + leveys_paivamaara + leveys_numero*6))
    r.append("")  # Lisätään yksi tyhjä rivi luettavuuden parantamiseksi
    return "\n".join(r)

def kirjoita_raportit_tiedostoon(tiedoston_nimi: str, raportit: list[str]) -> None:
    """
    Kirjoittaa annetut raportit samaan tekstitiedostoon annetussa järjestyksessä.

    Odotettu syöte:
    - tiedoston_nimi (str): Kohdetiedoston polku/nimi (esim. "yhteenveto.txt").
    - raportit (list[str]): Raporttitekstit, jotka kirjoitetaan peräkkäin.

    Palauttaa:
    - None

    Poikkeukset:
    - OSError: jos tiedostoon kirjoittaminen epäonnistuu.
    """
    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        for raportti in raportit:
            f.write(raportti)

def main() -> None:
    """
    Lukee viikon 41-43 CSV-data, tuottaa viikkoraportit ja tallentaa ne tiedostoon.

    Odotettu syöte:
    - Ei parametreja; käyttää kovakoodattuja tiedostonimiä ja päivämääriä.

    Palauttaa:
    - None
    """
    # Luetaan data CSV-tiedostoista kutsumalla lue_data -funktiota
    kulutus_ja_tuotanto_viikko_41 = lue_data("viikko41.csv")
    kulutus_ja_tuotanto_viikko_42 = lue_data("viikko42.csv")
    kulutus_ja_tuotanto_viikko_43 = lue_data("viikko43.csv")

    # Luodaan viikkoraportit viikkoraportti-funktiota kutsumalla
    raportti_viikko_41 = viikkoraportti(41, date(2025, 10, 6), kulutus_ja_tuotanto_viikko_41)
    raportti_viikko_42 = viikkoraportti(42, date(2025, 10, 13), kulutus_ja_tuotanto_viikko_42)
    raportti_viikko_43 = viikkoraportti(43, date(2025, 10, 20), kulutus_ja_tuotanto_viikko_43)

    # Kirjoitetaan viikkoraportit tiedostoon kutsumalla kirjoita_raportit_tiedostoon -funktiota
    kirjoita_raportit_tiedostoon("yhteenveto.txt", [
        raportti_viikko_41,
        raportti_viikko_42,
        raportti_viikko_43,
    ])

    print("Raportti on valmis")

if __name__ == "__main__":
    main()
