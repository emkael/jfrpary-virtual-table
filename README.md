
JFR Pary - wirtualne stoliki
============================

Narzêdzie sprz¹taj¹ce strony wyników z JFR Pary z danych dodanych celem
porównania uczestników z wirtualnym sto³em.

Ukrywane s¹:
* wyniki par ze stolików wirtualnych, równie¿ ze zbiorówek oraz pe³nych wyników
* linki w liœcie historii par
* zapisy w protoko³ach

Pierwszy z wirtualnych zapisów jest pozostawiany na dole protoko³u, opatrzony
nag³ówkiem.

Przyk³adowe efekty dzia³ania:
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

Œci¹gnij zawartoœæ tego repozytorium.

Ju¿, gotowe.

U¿ycie
------

```
python virtual_table.py [-t OPIS_STOLIKA] KATALOG_ROBOCZY_Z_PREFIKSEM_TURNIEJU [NR_PARY NR_PARY ...]
```

Parametry wejœciowe:
* œcie¿ka do katalogu stron generowanych przez JFR Pary, wraz z prefiksem
turnieju

Opcjonalne parametry:
* `-t OPIS_STOLIKA` lub `--text OPIS_STOLIKA` pozwala ustawiæ w³asny nag³ówek
stolika w protoko³ach, zamiast domyœlnego "Wirtualny stolik"
* `NR_PARY ...` pozwala samodzielnie okreœliæ numery par na wirtualnych stolikach

W przypadku nieokreœlenia numerów par, jako pary na stolikach wirtualnych
traktowane s¹ wszystkie pary, których imiona i nazwiska s¹ puste (wg nag³ówków
plików historii par).

Lista przysz³ych usprawnieñ
---------------------------

Patrz: [`TODO.md`](TODO.md)

Autor
-----

Micha³ Klichowicz (mkl)

Licencja
--------

Patrz: [`LICENSE.md`](LICENSE.md)
