
JFR Pary - wirtualne stoliki
============================

Narzędzie sprzątające strony wyników z JFR Pary z danych dodanych celem
porównania uczestników z wirtualnym stołem.

Ukrywane są:
* wyniki par ze stolików wirtualnych, również ze zbiorówek oraz pełnych wyników
* linki w liście historii par
* zapisy w protokołach

Pierwszy z wirtualnych zapisów jest pozostawiany na dole protokołu, opatrzony
nagłówkiem.

Przykładowe efekty działania:
[rozdania szkoleniowe z BOOM 2015](http://www.pzbs.pl/wyniki/boom/2015/boom_wirtualne_me.html),
[Kadra U-20 z butlerem ligowym](http://emkael.info/brydz/wyniki/2015/u20_szczyrk/ligowe.html).

Wymagania systemowe
-------------------

* python 2.x (testowane i tworzone w wersji 2.7.10)
* BeautifulSoup4
* lxml (jako parser dla BS4)
* argparse

Instalacja
----------

Ściągnij zawartość tego repozytorium.

Już, gotowe.

Użycie
------

```
python virtual_table.py [-t OPIS_STOLIKA] PLIK_TURNIEJU.html [NR_PARY NR_PARY ...]
```

Parametry wejściowe:
* ścieżka do pliku PREFIKS.html strony generowanej przez JFR Pary

Opcjonalne parametry:
* `-t OPIS_STOLIKA` lub `--text OPIS_STOLIKA` pozwala ustawić własny nagłówek
stolika w protokołach, zamiast domyślnego "Wirtualny stolik"
* `NR_PARY ...` pozwala samodzielnie określić numery par na wirtualnych stolikach

W przypadku nieokreślenia numerów par, jako pary na stolikach wirtualnych
traktowane są wszystkie pary, których imiona i nazwiska są puste (wg nagłówków
plików historii par).

Lista przyszłych usprawnień
---------------------------

Patrz: [`TODO.md`](TODO.md)

Autor
-----

Michał Klichowicz (mkl)

Licencja
--------

Patrz: [`LICENSE.md`](LICENSE.md)
