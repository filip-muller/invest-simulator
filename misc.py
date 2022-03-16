"Ruzne doplnujici funkce a exceptions"

from datetime import datetime

def to_datetime(datum: str, format='%Y-%m-%d'):
    return datetime.strptime(datum, format)

def max_dnu_pristi_mesic(mesic, rok):
    dny_mesicu = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dalsi_mesic = mesic + 1 if mesic < 12 else 1
    if dalsi_mesic == 2 and rok % 4 == 0 and (not rok % 100 == 0 or rok % 400 == 0):
        dny_mesicu[2] += 1
    return dny_mesicu[dalsi_mesic]

def max_dnu_mesic(mesic):
    dny_mesicu = [None, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dny_mesicu[mesic]
