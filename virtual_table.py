import sys, glob, re, math
from os import path
from bs4 import BeautifulSoup as bs4

tournament_path_prefix = sys.argv[1] + '.html'

output_path = path.dirname(tournament_path_prefix)
tournament_prefix = path.splitext(path.realpath(tournament_path_prefix))[0]

tournament_files_match = re.compile(re.escape(tournament_prefix) + '([0-9]{3})\.txt')
tournament_files = [f for f in glob.glob(tournament_prefix + '*.txt') if re.search(tournament_files_match, f)]

virtual_pairs = []

for tournament_file in tournament_files:
    with file(tournament_file, 'r+') as board_text:
        board_text_content = bs4(board_text, from_encoding='iso-8859-2')
        if not len(board_text_content.select('tr.virtualTable')):
            rows = [row for row in board_text_content.select('tr') if len(row.select('td')) == 11]
            virtual_count = int(math.ceil(len(rows) / 2.0))
            header_added = False
            for row in rows[virtual_count-1:]:
                for cell in row.select('td')[1:3]:
                    pair_no = int(cell.contents[0])
                    virtual_pairs.append(pair_no)
                if header_added:
                    row.extract()
                else:
                    row.insert_before(bs4('<tr class="virtualTable"><td class="n"></td><td class="noc" colspan="10">Wirtualny stolik:</td></tr>'))
                    for cell in row.select('td')[1:3]:
                        cell.contents = ''
                    header_added = True
            board_text.seek(0)
            board_text.write(board_text_content.table.prettify('iso-8859-2', formatter='html'))
            board_text.truncate()

with file(tournament_prefix + 'WYN.txt', 'r+') as results_file:
    results_text_content = bs4(results_file, from_encoding='iso-8859-2')
    rows = results_text_content.select('tr')
    for row in rows:
        cells = row.select('td')
        if len(cells) == 6:
            try:
                if int(cells[2].contents[0]) in virtual_pairs:
                    row.extract()
            except ValueError:
                pass
    results_file.seek(0)
    results_file.write(results_text_content.table.prettify('iso-8859-2'))
    results_file.truncate()

with file(tournament_prefix + 'zbior.html', 'r+') as results_file:
    results_content = bs4(results_file)
    rows = results_content.select('tr')
    for row in rows:
        cells = row.select('td')
        if len(cells) == 7:
            try:
                if int(cells[1].contents[0]) in virtual_pairs:
                    row.extract()
            except ValueError:
                pass
        if len(cells) == 1 and cells[0]['colspan'] == '7' and cells[0].contents[0] == '&nbsp':
            row.extract()
    results_file.seek(0)
    results_file.write(results_content.prettify('utf-8'))
    results_file.truncate()
