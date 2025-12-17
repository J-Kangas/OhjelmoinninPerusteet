# Copyright (c) 2025 Jonna Kangas

# Ohjelmoinnin perusteet -opintojakso, harjoitustehtävä 7
    # Harjoitustehtävässä käytän sanakirjaa. Sanakirjaversio on paljon helpommin luettavissa kuin alkuperäinen listaversio.
    # Avain-arvo-pari antaa selkeämmän kuvan, että mitä arvo on kuin indeksit esim. varaus[1]. Kun koodia lukee, niin saa paremmin
    # ja nopeammin käsityksen, että mitä koodirivillä on ja mikä sen tarkoitus on.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# See <https://www.gnu.org/licenses/>.

from datetime import datetime

def muunna_varaustiedot(varaus_lista: list[str]) -> dict:
    """
    Muuntaa yhden varauksen kentät (merkkijonolista) sanakirjaksi.

    Parametrit:
        varaus_lista (list[str]): Kentät järjestyksessä:
            [id, nimi, sähköposti, puhelinnumero, päivämäärä, kellonaika,
             kesto, tuntihinta, vahvistettu, varauskohde, luotu]

        Odotetut formaatit:
            - id: kokonaisluku (esim. "201")
            - päivämäärä: 'YYYY-MM-DD' (esim. "2025-11-12")
            - kellonaika: 'HH:MM' (esim. "09:00")
            - kesto: kokonaisluku tunteina (esim. "2")
            - tuntihinta: liukuluku (esim. "18.50")
            - vahvistettu: "true"/"false" (kirjainkoolla ei väliä)
            - luotu: 'YYYY-MM-DD HH:MM:SS' (esim. "2025-08-12 14:33:20")

    Palauttaa:
        dict: Sanakirja, jonka kentät on muunnettu sopiviin Python-tyyppeihin
        (int, float, bool, date, time, datetime).

    Huomio:
        Jos kentissä on väärä muoto tai kenttiä puuttuu, Python voi nostaa
        esim. ValueError- tai IndexError-poikkeuksia muunnosten yhteydessä.
    """
    return {
        "id": int(varaus_lista[0]),
        "nimi": varaus_lista[1],
        "sahkoposti": varaus_lista[2],
        "puhelinnumero": varaus_lista[3],
        "paivamaara": datetime.strptime(varaus_lista[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus_lista[5], "%H:%M").time(),
        "kesto": int(varaus_lista[6]),
        "tuntihinta": float(varaus_lista[7]),
        "vahvistettu": varaus_lista[8].lower() == "true",
        "varauskohde": varaus_lista[9],
        "luotu": datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S")
    }

def hae_varaukset(varaustiedosto: str) -> list[dict]:
    """
    Lukee varaukset tiedostosta ja muuntaa jokaisen rivin sanakirjaksi.

    Parametrit:
        varaustiedosto (str): Polku tekstitiedostoon, jossa jokainen rivi
            kuvaa yhden varauksen. Kentät on eroteltu '|' -merkillä.

    Palauttaa:
        list[dict]: Lista sanakirjoja, joissa on yhden varauksen tiedot.

    Huomio:
        - Tyhjät rivit eivät ole käsitelty erikseen.
        - Kenttämäärää ei tarkisteta; puutteelliset/virheelliset rivit
          voivat aiheuttaa poikkeuksia muunnosvaiheessa.
        - Jos tiedostoa ei löydy, Python nostaa FileNotFoundErrorin.
    """
    varaukset: list[dict] = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varausrivi in f:
            varausrivi = varausrivi.strip()
            varauksen_tiedot = varausrivi.split('|')
            varaukset.append(muunna_varaustiedot(varauksen_tiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list):
    """
    Tulostaa vahvistetut varaukset kompaktissa muodossa.

    Parametrit:
        varaukset (list[dict]): Varauksia sisältävä lista, jossa jokainen alkio on sanakirja.

    Tulostus:
        Kirjoittaa raportin näytölle (konsoliin) käyttäen print()-komentoja.
    """
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"- {varaus['nimi']}, {varaus['varauskohde']}, {varaus['paivamaara'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: list[dict]) -> None:   
    """
    Tulostaa varaukset, joiden kesto on vähintään 3 tuntia.

    Parametrit:
        varaukset (list[dict]): Varauksia sisältävä lista, jossa jokainen alkio on sanakirja.

    Tulostus:
        Kirjoittaa raportin näytölle (konsoliin) käyttäen print()-komentoja.
    """
    for varaus in varaukset:
        if(varaus['kesto'] >= 3):
            print(f"- {varaus['nimi']}, {varaus['paivamaara'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['varauskohde']}")
    print()

def varausten_vahvistusstatus(varaukset: list[dict]) -> None: 
    """
    Tulostaa kunkin varauksen vahvistusstatuksen.

    Parametrit:
        varaukset (list[dict]): Varauksia sisältävä lista, jossa jokainen alkio on sanakirja.

    Tulostus:
        Kirjoittaa raportin näytölle (konsoliin) käyttäen print()-komentoja.
    """
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")
    print()

def varausten_lkm(varaukset: list[dict]) -> None:
    """
    Laskee ja tulostaa vahvistettujen ja ei-vahvistettujen varausten lukumäärät.

    Parametrit:
        varaukset (list[dict]): Varauksia sisältävä lista, jossa jokainen alkio on sanakirja.

    Tulostus:
        Kirjoittaa raportin näytölle (konsoliin) käyttäen print()-komentoja.

    """
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list[dict]) -> None:
    """
    Laskee ja tulostaa vahvistettujen varausten kokonaistulot euroina.

    Parametrit:
        varaukset (list[dict]): Varauksia sisältävä lista, jossa jokainen alkio on sanakirja.

    Tulostus:
        Kirjoittaa raportin näytölle (konsoliin) käyttäen print()-komentoja.
    """
    varaustenTulot = 0
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            varaustenTulot += varaus['kesto']*varaus['tuntihinta']

    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()

def main():
    """
    Pääohjelma: lukee varaukset tiedostosta ja tulostaa useita raportteja.

    Tulostus:
        Kirjoittaa raportit näytölle (konsoliin) käyttäen print()-komentoja.
    """
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()