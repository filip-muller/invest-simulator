# Investing Simulator
 A library for simulating investing on historic or fictionary data
 
 ## Getting started
 First, clone the repository. Then find the file invest_simulator.py and copy it to you working folder.
 Then, in your python code type `from invest_simulator import InvestSimulator` to import the key class.
 
 ### Generating data
 Now, you're gonna need to generate data for the simulator to work with. The main method to do this
 is to generate them from a csv file using the method `InvestSimulator.vytvor_data_csv()`. This method takes
 the path to your csv file as the first argument (e.g. `"data.csv"`). The next argument specifies the format of
 the date being used in your csv file. It uses the same codes as the [datetime module](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). The next two arguments specify, which column of the csv includes the date and which includes the price.
 The columns are counted from 0.
 
 ### Creating the simulator
 Once you have generated the data, you can create a new simulator. Create a new instance of the class
 InvestSimulator and pass it the created data as the first argument. The second argument specifies, how much
 money should get added to the simulators balance every year (yearly income). The constructor takes many
 optional arguments, feel free to play around with them.
 
 ### Simulating
 The simulator has two main methods - `dalsi_den()`, which moves the simulation one day forward
 and `nakup()`, which buys stocks for the current market price in the simulation. You can specify the
 amount of cash to be used for the purchase, but by default the simulator will use all the cash.
 
 ## Metody třídy InvestSimulator
 
 #### `__init__(data: dict, rocni_castka: int, puvodni_castka=0, zacatek=None, konec=None, zlomek=True, koef_ceny=1, den_vyplaty=15)`
`data` je dictionary s info a cene vygenerovany nekterou z classmethods, 
`rocni_castka` je castka pripsana kazdy rok k hotovosti,
`puvodni_castka` je hotovost na zacatku simulace,
`zacatek` a konec umoznuje specifikovat custom zacatecni a konecne datum ve formatu YYYY-MM-DD,
`zlomek` urcuje, zda lze nakupovat i pouze zlomky akcii,
`koef_ceny` je hodnota, kterou se pripadne vynasobi vsechny ceny v datech,
`den_vyplaty` je den v mesici, kdy se pripise pravidelna mesicni castka
 
 #### `pridej_automaticky_nakup(mesic, den=1)`
 Prida datum, kdy se kazdy rok automaticky nakoupi za veskerou hotovost.
 
 #### `dalsi_den(opakovani=1)`
Posune simulaci o jeden den dopredu.
Pokud dojde na konec simulacniho obdobi, vyvola exception KonecSimulace.
Pocet dni lze uzpusobit pomoci parametru 'opakovani'.
Aktualizuje datum a ubehlou dobu a pokud dojde na den,
kdy se ma vyplacet pravidelna mesicni castka, zvysi hotovost.

#### `dalsi_mesic(opakovani=1)`
Posune simulaci o jeden mesic dopredu.
Pomoci parametru opakovani lze uzpusobit pocet mesicu.

#### `dalsi_rok(opakovani=1)`
Posune simulaci o jeden rok dopredu.

#### `nakup(castka=None)`
Za momentální tržní cenu v simulaci nakoupí akcie v hodnote `castka`.
Pokud je metoda zavolana bez parametru `castka`,
nakoupi se za veskerou drzenou hotovost. Pokud by
mel nakup probehnout v neobchodni den, metoda ho v tuto
chvili provede tak, jakoby se stal v nejblizsi nadchazejici
obchodni den. Metoda funguje spravne i pokud `castka=0`,
v takovem pripade se nestane nic a obchod se nezaznamena. 
 
#### `simul(nakup_kazdy_den)`
Dosimuluje vyvoj az do posledniho dne dat, provadi nastavene nakupy.
Pomoci parametru `nakup_kazdy_den`, lze urcit, zda se ma kazdy den
nakoupit za vsechny dostupne penize.

#### `simul_do(rok: int, mesic=1, den=1)`
Simuluje vyvoj do urceneho data.

## Metody pro tvorbu dat

#### `InvestSimulator.vytvor_data_csv(csv_path, date_format="%Y-%m-%d", date_column=0, cena_column=1) -> dict`
Ze csv vytvori data, ktera se daji pouzit pro vytvoreni instance InvestSimulator.

Vraci dictionary, ktery je ve spravnem formatu pro parametr `data`
potrebny pro vytvoreni instance tridy.
Pomoci parametru `date_column` a `close_column` lze specifikovat,
z ktereho sloupce souboru ma brat jaka data. Sloupce se pocitaji
od 0, takze prvni sloupec je sloupec 0, druhy cislo 1 atd.
V parametru `date_format` lze speficikovat fomat data pouzivany
v csv souboru. Ten je automaticky preveden na spravny format.
Vyuziva stejny styl zapisu formatu jako modul [datetime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

#### `InvestSimulator.vytvor_data_linearni(let_zpatky: int, cagr_procent=10, pocatecni_cena=1000) -> dict`
Vytvori data, kterych cena roste linearne, stejnou hodnotou kazdy den.

Parametr `let_zpatky` urcuje, kolik let se ma zpetne nasimulovat. Data
zacinaji datem o tento pocet let zpatky a cenou urcenou parametrem
`pocatecni_cena` (default=1000). Na konci simulace se cena linearnim rustem
dostane do takoveho stavu, aby byl za obdobi cagr specifikovany v parametru
`cagr_procent` (default je 10 %).

#### `InvestSimulator.vytvor_data_exponencialni(let_zpatky: int, cagr_procent=10, pocatecni_cena=1000) -> dict`
Vytvori data s odpovidajicim procentnim rustem kazdy den.
