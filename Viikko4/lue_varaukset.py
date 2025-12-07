"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30:00 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45:00 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15:00 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
# Copyright (c) 2025 Jonna Kangas – ratkaisu ja lisäykset
# Copyright (c) 2025 Ville Heikkiniemi – alkuperäinen tehtävän runko

# Ohjelmoinnin perusteet -opintojakso, harjoitustehtävä 4

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# See <https://www.gnu.org/licenses/>.


from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    
    muutettu_varaus = []
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(varaus[1])
    muutettu_varaus.append(varaus[2])
    muutettu_varaus.append(varaus[3])
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(varaus[8].lower() == 'true')
    muutettu_varaus.append(varaus[9])
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus

#Vaihtoehtoinen toteutus äskeiselle:
#def muunna_varaustiedot(varaus: list) -> list:
#    return [int(varaus[0]), varaus[2], varaus[3], datetime.strptime(varaus[4], "%Y-%m-%d").date(), 
#            datetime.strptime(varaus[5], "%H:%M").time(), int(varaus[6]), float(varaus[7]),
#            varaus[8].lower() == 'true', varaus[9], datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")]

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if (varaus[8]):
            print(F" - {varaus[1]}, {varaus[9]}, {varaus[4].strftime("%d.%m.%Y")} klo {varaus[5].strftime("%H.%M")}")

    print()

def pitkat_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if (varaus[6] >= 3):
            print(F" - {varaus[1]}, {varaus[4].strftime("%d.%m.%Y")} klo {varaus[5].strftime("%H.%M")}, kesto {varaus[6]} h, {varaus[9]}")

    print()

def vahvistus_status(varaukset: list):

    for varaus in varaukset[1:]:
        if (varaus[8]):
            print(F"{varaus[1]} -> Vahvistettu")
        else:
            print(F"{varaus[1]} -> EI vahvistettu")

    print()

def vahvistuksien_yhteenveto(varaukset: list):

    vahvistetut_varaukset_kpl = 0
    vahvistamattomat_varaukset_kpl = 0
    
    for varaus in varaukset[1:]:
        if (varaus[8]):
            vahvistetut_varaukset_kpl += 1
        else:
            vahvistamattomat_varaukset_kpl += 1

    print(F" - Vahvistettuja varauksia: {vahvistetut_varaukset_kpl} kpl")
    print(F" - Ei-vahvistettuja varauksia: {vahvistamattomat_varaukset_kpl} kpl")
    print()

def vahvistuksien_kokonaistulo(varaukset: list):
    vahvistettujen_varausten_kokonaistulo = 0
    
    for varaus in varaukset[1:]:
        if (varaus[8]):
            vahvistettujen_varausten_kokonaistulo += varaus[6]*varaus[7]

    print("Vahvistettujen varausten kokonaistulot:", f"{vahvistettujen_varausten_kokonaistulo:.2f}".replace(".", ","), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    vahvistus_status(varaukset)
    print("4) Yhteenveto vahvistuksista")
    vahvistuksien_yhteenveto(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    vahvistuksien_kokonaistulo(varaukset)

if __name__ == "__main__":
    main()