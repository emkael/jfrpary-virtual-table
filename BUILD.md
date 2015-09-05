
JFR Pary - wirtualne stoliki: Informacje dla programistów
=========================================================

Struktura repozytorium kodu
---------------------------

Katalog [`src`](src) zawiera komponenty źródłowe programu:

* [kod skryptu Pythona](src/virtual_table.py), który wykonuje całą robotę
* [ikonę programu](src/icon.ico) wraz ze [źródłami](src/icon.xcf)
* [metadane programu](src/version) dla PyInstallera

Katalogi `dist` i `build` są domyślnie puste i są katalogami roboczymi
PyInstallera.

W katalogu głównym znajdują się rozmaite README oraz skrypty budujące program.

Od zera do bohatera - proces budowania programu
-----------------------------------------------

Jedynym wymaganym do działania narzędzia elementem repozytorium jest źródłowy
skrypt [`virtual_table.py`](src/virtual_table.py). Cała reszta to tylko
fajerwerki i opakowanie w plik wykonywalny.

Skrypt można uruchomić w dowolnym środowisku, w którym działa Python, a jego
wymagania wymienione są poniżej. `virtual_table.py` przyjmuje parametry
identycznie do wynikowego pliku wykonywalnego.

---

Pliku źródłowego można użyć jako modułu, jeśli kogoś to kręci, importując go
do swojej aplikacji poprzez:
```
from virtual_table import JFRVirtualTable
```

---

Skrypt można samodzielnie skompilować do pliku wykonywalnego, używając do tego
PyInstallera. Można to zrobić z pomocą dołączonego pliku [`virtual_table.spec`](virtual_table.spec):
```
pyinstaller virtual_table.spec
```
lub samodzielnie, podając odpowiednie parametry do PyInstallera:
```
pyinstaller --onefile --version-file=src\version --icon=src\icon.ico src\virtual_table.py
```
Zarówno metadane z pliku `src/version`, jak i ikona programu są w 100% opcjonalne.

Wynik działania PyInstallera (pojedynczy plik wykonywalny) znajdzie się w katalogu `dist`.

Wymagania systemowe
-------------------

Skrypt [`virtual_table.py`](src/virtual_table.py):

* python 2.x (testowane i tworzone w wersji 2.7.10)
* BeautifulSoup4
* lxml (jako parser dla BS4)
* argparse

Kompilacja do EXE:

* [PyInstaller](http://pythonhosted.org/PyInstaller/)
* PyWin32

Znane problemy
--------------

* PyInstaller nie lubi kompilować ze ścieżek ze znakami nie-ASCII. `¯\_(ツ)_/¯`
* co więcej, wersja stabilna produkuje .exe, które nie odpala się z niektórych
ścieżek nie-ASCII: https://github.com/pyinstaller/pyinstaller/issues/1396
(.exe dostarczane w `dist` powinno działać)

Kod żródłowy
------------

Kod źródłowy stara się, z grubsza:

* zgadzać ze standardami [PEP8](https://www.python.org/dev/peps/pep-0008/)
* nie robić [głupich rzeczy](http://stackoverflow.com/a/1732454)
* nie psuć raz przekształconej strony przy próbie ponownego przekształcenia
* komentować rzeczy nieoczywiste

Operacje na stronach JFR
------------------------

Ramowy algorytm działania programu:

0. Jeśli na wejściu nie podano konkretnych numerów "wirtualnych" par,
skanowane są nagłówki plików historii (H-[PREFIKS]-[PARA].html). Puste
nazwiska przyjmowane są jako pary z wirtualnych stolików.
1. Z wyników ([PREFIKS]WYN.txt), pełnych wyników (W-[PREFIKS].html)
oraz zbiorówek (jeśli istnieją, [PREFIKS]zbior.html) usuwane są wiersze,
w których występują pary wirtualne.
2. Z listy historii (H-[PREFIKS]-lista.html) usuwane są linki do historii
par wirtualnych, a cała tabelka jest magicznie układana z powrotem w rządki.
3. Z protokołów usuwane są zapisy par wirtualnych, poza jednym, który dostaje
schludny nagłówek i przesuwany jest w dół protokołu.

---

`It will end no other way.`
