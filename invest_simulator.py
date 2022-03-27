import csv
from datetime import datetime, timedelta

from misc import max_dnu_mesic, to_datetime, max_dnu_pristi_mesic


class InvestSimulator:
    """
    Trida pro simulovani ruznych investicnich strategii na historickych datech
    """

    def __init__(self,
                 data: dict,         # na indexu "YYYY-MM-DD" obsahuje cenu daneho dne
                 rocni_castka: int,  # rocni castka, kterou ma investor k dispozici
                 zacatek=None,       # string, format je YYYY-MM-DD
                 konec=None,         # string, format je YYYY-MM-DD
                 zlomek=True,        # zda lze koupit pouze zlomek akcie
                 den_vyplaty=15,     # den v mesici, kdy se pripise mesicni castka
                 koef_ceny=1,        # cislo, kterym se vynasobi vsechny ceny v 'data'
                 ):

        if not 1 <= den_vyplaty <= 28:
            raise ValueError("Den vyplaty musi byt mezi 1 a 28")
        if koef_ceny <= 0:
            raise ValueError("koef_ceny musi byt kladny")

        if koef_ceny != 1:
            self.data = {k: v*koef_ceny for k, v in data.items()}
        else:
            self.data = dict(data)

        # najde prvni a posledni datum
        list_dat = list(self.data)
        list_dat = sorted(list_dat, key=lambda x: to_datetime(x))
        zacatek_dat = list_dat[0]
        konec_dat = list_dat[-1]
        del list_dat

        if zacatek is not None:
            if len(zacatek) != 10 or zacatek[2] in ['-', '/', '\\', ':', '.']:
                raise ValueError(
                    "Spatny format parametru 'zacatek_datum', pouzij YYYY-MM-DD")
            if to_datetime(zacatek) < to_datetime(zacatek_dat):
                raise ValueError(
                    "Zacatecni datum nemuze byt pred prvnim datem dostupnych dat")
            self.zacatek = to_datetime(zacatek)
        else:
            self.zacatek = to_datetime(zacatek_dat)

        if konec is not None:
            if len(konec) != 10 or konec[2] in ['-', '/', '\\', ':', '.']:
                raise ValueError(
                    "Spatny format parametru 'konec_datum', pouzij YYYY-MM-DD")
            if to_datetime(konec) > to_datetime(konec_dat):
                raise ValueError(
                    "Koncove datum nemuze byt za poslednim datem dostupnych dat")
            self.konec = to_datetime(konec)
        else:
            self.konec = to_datetime(konec_dat)

        # momentalni datum v simulaci
        self.datum = self.zacatek
        self.rocni_castka = rocni_castka
        self.mesicni_castka = rocni_castka / 12
        self.zlomek = zlomek            # bool urcujici, zda lze koupit pouze zlomek akcie
        self.den_vyplaty = den_vyplaty  # den v mesici, kdy se pripise mesicni castka

        # penize dostupne k investovani,
        # kazdy mesic se zvysi o 'mesicni_castka'
        self.hotovost = 0
        self.akcie = 0      # pocet drzenych akcii, muze byt i desetinne
        self.dny = 0        # pocet dnu, ktere ubehly od zacatku simulace
        self.vyplaceno = 0  # pocet mesicnich castek, ktere byly vyplaceny
        # list tuplu obsahujicich datum (string) a castku pro vsechny nakupy
        self.nakupy = []
        # list int tuplu (month, day), kdy se ma automaticky nakupovat
        self.automaticke_nakupy = []

    @classmethod
    def vytvor_data_databaze(cls) -> dict:
        pass

    @classmethod
    def vytvor_data_csv(cls, csv_path, date_format="%Y-%m-%d", date_column=0, close_column=1) -> dict:
        """ Ze csv vytvori data, ktera se daji pouzit pro vytvoreni instance.

        Vraci dictionary, ktery je ve spravnem formatu pro parametr 'data'
        potrebny pro vytvoreni instance tridy.
        Pomoci parametru date_column a close_column lze specifikovat,
        z ktereho sloupce souboru ma brat jaka data. Sloupce se pocitaji
        od 0, takze prvni sloupec je sloupec 0, druhy cislo 1 atd.
        V parametru date_format lze speficikovat fomat data pouzivany
        v csv souboru. Ten je automaticky preveden na spravny format.
        Vyuziva stejny styl zapisu formatu jako modul datetime.
        """
        preformatovat_datum = (date_format != "%Y-%m-%d")
        result = dict()
        with open(csv_path) as f:
            csv_reader = csv.reader(f, delimiter=",")
            next(csv_reader)
            while True:
                try:
                    row = next(csv_reader)
                except StopIteration:
                    break
                if preformatovat_datum:
                    row[date_column] = (datetime.strptime(
                        row[date_column], date_format)).strftime('%Y-%m-%d')
                result[row[date_column]] = float(row[close_column])

        return result

    @classmethod
    def vytvor_data_linearni(cls, let_zpatky: int, cagr_procent=10, pocatecni_cena=1000) -> dict:
        """Vytvori data, kterych cena roste linearne, stejnou hodnotou kazdy den.

        Parametr let_zpatky urcuje, kolik let se ma zpetne nasimulovat. Data
        zacinaji datem o tento pocet let zpatky a cenou urcenou paramentrem
        pocatecni_cena (default=1000). Na konci simulace se cena linearnim rustem
        dostane do takoveho stavu, aby byl za obdobi cagr specifikovany v parametru
        cagr_procent (default je 10 %)"""
        now = datetime.now()
        pocet_dni = (now - datetime(year=now.year - let_zpatky,
                     month=now.month, day=now.day)).days
        celkove_zhodnoceni = pocatecni_cena * \
            (1 + cagr_procent / 100)**let_zpatky - pocatecni_cena
        denni_zhodnoceni = celkove_zhodnoceni / pocet_dni

        datum = now - timedelta(days=pocet_dni)
        cena = pocatecni_cena
        result = {datum.strftime("%Y-%m-%d"): pocatecni_cena}
        for _ in range(pocet_dni):
            datum += timedelta(days=1)
            cena += denni_zhodnoceni
            result[datum.strftime("%Y-%m-%d")] = round(cena, 4)
        return result

    @classmethod
    def vytvor_data_exponencialni(cls, let_zpatky: int, cagr_procent=10, pocatecni_cena=1000) -> dict:
        """Vytvori data s odpovidajicim procentnim rustem kazdy den"""
        now = datetime.now()
        pocet_dni = (now - datetime(year=now.year - let_zpatky,
                     month=now.month, day=now.day)).days
        finalni_relativni_hodnota = (1 + cagr_procent / 100)**let_zpatky
        denni_relativni_zhodnoceni = (
            finalni_relativni_hodnota)**(1 / pocet_dni)

        datum = now - timedelta(days=pocet_dni)
        cena = pocatecni_cena
        result = {datum.strftime("%Y-%m-%d"): pocatecni_cena}
        for _ in range(pocet_dni):
            datum += timedelta(days=1)
            cena *= denni_relativni_zhodnoceni
            result[datum.strftime("%Y-%m-%d")] = round(cena, 4)
        return result

    @property
    def hodnota(self) -> float:
        """Hodnota portfolia spolu s hotovosti, zaokrouhlena na 3 des. mista"""
        return round(self.akcie * self.data[self.posledni_platne_datum] + self.hotovost, 3)

    @property
    def datum_str(self):
        """Aktualni datum simulace ve tvaru YYYY-MM-DD"""
        return self.datum.strftime("%Y-%m-%d")

    @property
    def posledni_platne_datum(self) -> datetime.datetime:
        """Posledni datum od soucasneho data simulace, kdy byl obchodni den"""
        date = self.datum
        while date.strftime("%Y-%m-%d") not in self.data:
            date -= timedelta(days=1)
        return date.strftime("%Y-%m-%d")

    @property
    def pristi_platne_datum(self) -> datetime.datetime:
        """Nejblizsi datum od soucasneho data simulace, kdy bude obchodni den"""
        date = self.datum
        assert date <= self.konec   # pouze kontrola, nedulezite

        while date.strftime("%Y-%m-%d") not in self.data:
            date += timedelta(days=1)
        return date.strftime("%Y-%m-%d")

    @property
    def nakupy_str(self):
        """Vypis vsech nakupu, ktere se na portfoliu za celou dobu provedly"""
        result = ""
        for n in self.nakupy:
            result += f"{n[0]}: ${round(n[1])}\n"
        return result[:-1]

    @property
    def cena(self, mode="pristi") -> float:
        """Soucasna cena na trhu, pripadne cena pristi obchodni den

        Pomoci nastaveni parametru mode na 'posledni' lze v neobchodni dny
        ziskat cenu posledni uplynuly obchodni den misto nejblizsiho budouciho"""
        if mode == "pristi":
            return self.data[self.pristi_platne_datum]
        if mode == "posledni":
            return self.data[self.posledni_platne_datum]
        raise ValueError(
            "neplatna hodnota argumentu mode, muze byt 'pristi' nebo 'posledni'")

    def __str__(self):
        return (f"Soucasne datum: {self.datum_str}\n"
                f"Hodnota portfolia: ${round(self.hodnota, 3)}\n"
                f"Z toho hotovost: ${self.hotovost}\n"
                f"Pocet vlastnenych akcii: {round(self.akcie, 3)}\n"
                #f"Celkova castka za obdobi: ${round(self.mesicni_castka * self.vyplaceno)}\n"
                )[:-1]

    def pridej_automaticky_nakup(self, mesic: int, den=1):
        """ Prida datum, kdy se ma kazdy rok nakoupit za vsechnu hotovost"""
        if not 0 < mesic <= 12:
            raise ValueError("Mesic automatickeho nakupu musi byt mezi 1 a 12")
        if not 0 < den <= max_dnu_mesic(mesic):
            raise ValueError("Den automatickeho nakupu musi byt mezi 1 a 31")

        self.automaticke_nakupy.append((mesic, den,))

    def dalsi_den(self, opakovani=1):
        """ Posune simulaci o jeden den dopredu.

        Pokud dojde na konec simulacniho obdobi, vyvola exception KonecSimulace.
        Pocet dni lze uzpusobit pomoci parametru 'opakovani'.
        Aktualizuje datum a ubehlou dobu a pokud dojde na den,
        kdy se ma vyplacet pravidelna mesicni castka, zvysi hotovost.
        """

        for _ in range(opakovani):
            if self.datum >= self.konec:
                raise KonecSimulace("Simulace došla do konečného data")

            self.datum += timedelta(days=1)
            self.dny += 1
            den = self.datum.day
            mesic = self.datum.month
            if den == self.den_vyplaty:
                self.hotovost += self.mesicni_castka
                self.vyplaceno += 1
            if (mesic, den) in self.automaticke_nakupy:
                self.nakup()

    def dalsi_mesic(self, opakovani=1):
        """ Posune simulaci o jeden mesic dopredu.

        Pomoci parametru opakovani lze uzpusobit pocet mesicu.
        Interne pouze opakuje metodu dalsi_den dokud neubehne mesic.
        """
        for _ in range(opakovani):
            konecny_den = min(
                self.datum.day, max_dnu_pristi_mesic(self.datum.month))
            while True:
                self.dalsi_den()
                if self.datum.day == konecny_den:
                    break

    def dalsi_rok(self, opakovani=1):
        """ Posune simulaci o jeden rok dopredu."""
        for _ in range(opakovani*12):
            self.dalsi_mesic()

    def nakup(self, castka=None):
        """ Za momentální tržní cenu v simulaci nakoupí akcie v hodnote 'castka'.

            Pokud je metoda zavolana bez parametru castka,
            nakoupi se za veskerou drzenou hotovost.Pokud by
            mel nakup probehnout v neobchodni, metoda ho v tuto
            chvili provede tak, jakoby se stal v posledni uplynuly
            obchodni den. Metoda funguje spravne i pokud castka=0,
            v takovem pripade se nestane nic a obchod se nezaznamena. 
        """
        if castka == 0:
            return
        if castka == None:
            castka = self.hotovost

        if self.hotovost < castka:
            raise ValueError(
                f"Nedostatek hotovosti k nakupu, hotovost = {self.hotovost}")
        if castka < 0:
            raise ValueError("Nelze nakoupit za zapornou castku")

        self.nakupy.append((self.datum_str, castka,))

        if self.zlomek:
            self.akcie += castka / self.data[self.posledni_platne_datum]
            self.hotovost -= castka
            return

        self.akcie += castka // self.data[self.posledni_platne_datum]
        self.hotovost -= castka - \
            castka % self.data[self.posledni_platne_datum]

        assert self.hotovost >= 0

    def simul(self, nakup_kazdy_den=False):
        """Dosimuluje vyvoj az do posledniho dne dat, provadi nastavene nakupy.
        Pomoci parametru nakup_kazdy_den, lze urcit, zda se ma kazdy den
        nakoupit za vsechny dostupne penize"""
        while True:
            try:
                self.dalsi_den()
            except KonecSimulace:
                break
            if nakup_kazdy_den:
                self.nakup()

    def simul_do(self, rok: int, mesic=1, den=1):
        """Simuluje az do daneho data."""
        koncove_datum = datetime(rok, mesic, den)
        if koncove_datum <= self.datum:
            return False
        if koncove_datum > self.konec:
            raise ValueError("Koncove datum nesmi presahnout poskytnuta data")

        while not (self.datum.year == rok
                   and self.datum.month == mesic
                   and self.datum.day == den):
            self.dalsi_den()
        return True


class KonecSimulace(Exception):
    """Vyjimka, kterou InvestSimulator vyvola po dosazeni posledniho data"""
    pass


# TODO
# - tvorba dat z databaze
