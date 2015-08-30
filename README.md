
JFR Pary - wirtualne stoliki
============================

Narz�dzie sprz�taj�ce strony wynik�w z JFR Pary z danych dodanych celem
por�wnania uczestnik�w z wirtualnym sto�em.

Ukrywane s�:
* wyniki par ze stolik�w wirtualnych, r�wnie� ze zbior�wek oraz pe�nych wynik�w
* linki w li�cie historii par
* zapisy w protoko�ach

Pierwszy z wirtualnych zapis�w jest pozostawiany na dole protoko�u, opatrzony
nag��wkiem.

Przyk�adowe efekty dzia�ania:
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

�ci�gnij zawarto�� tego repozytorium.

Ju�, gotowe.

U�ycie
------

```
python virtual_table.py [-t OPIS_STOLIKA] KATALOG_ROBOCZY_Z_PREFIKSEM_TURNIEJU [NR_PARY NR_PARY ...]
```

Parametry wej�ciowe:
* �cie�ka do katalogu stron generowanych przez JFR Pary, wraz z prefiksem
turnieju

Opcjonalne parametry:
* `-t OPIS_STOLIKA` lub `--text OPIS_STOLIKA` pozwala ustawi� w�asny nag��wek
stolika w protoko�ach, zamiast domy�lnego "Wirtualny stolik"
* `NR_PARY ...` pozwala samodzielnie okre�li� numery par na wirtualnych stolikach

W przypadku nieokre�lenia numer�w par, jako pary na stolikach wirtualnych
traktowane s� wszystkie pary, kt�rych imiona i nazwiska s� puste (wg nag��wk�w
plik�w historii par).

Lista przysz�ych usprawnie�
---------------------------

Patrz: [`TODO.md`](TODO.md)

Autor
-----

Micha� Klichowicz (mkl)

Licencja
--------

Patrz: [`LICENSE.md`](LICENSE.md)
