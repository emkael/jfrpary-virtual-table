# coding=utf-8

import sys
import glob
import re
import math

from os import path
from bs4 import BeautifulSoup as bs4
from bs4.element import NavigableString


class JFRVirtualTable:

    def __parse_filepaths(self, prefix):
        file_path = path.realpath(prefix + '.html')
        tournament_path = path.dirname(file_path)
        tournament_prefix = path.splitext(path.basename(file_path))[0]
        traveller_files_match = re.compile(
            re.escape(tournament_prefix) + '([0-9]{3})\.txt'
        )
        # TODO: refaktoryzacja tych wszystkich path.join
        self.__traveller_files = [
            f for f
            in glob.glob(
                path.join(tournament_path, tournament_prefix) + '*.txt'
            )
            if re.search(traveller_files_match, f)
        ]
        records_files_match = re.compile(
            'H-' + tournament_prefix + '-([0-9]{1,3})\.html'
        )
        self.__pair_records_files = [
            f for f
            in glob.glob(
                path.join(tournament_path, 'H-' + tournament_prefix + '*.html')
            )
            if re.search(records_files_match, f)
        ]
        self.__results_file = path.join(
            tournament_path,
            tournament_prefix + 'WYN.txt'
        )
        self.__full_results_file = path.join(
            tournament_path,
            'W-' + tournament_prefix + '.html'
        )
        self.__pair_records_list_file = path.join(
            tournament_path,
            'H-' + tournament_prefix + '-lista.html'
        )
        self.__collected_scores_file = path.join(
            tournament_path,
            tournament_prefix + 'zbior.html'
        )

    def __detect_virtual_pairs(self):
        virtual_pairs = []
        pair_header_match = re.compile('([0-9]{1,}): (.*) - (.*), .*')
        for record_file_path in self.__pair_records_files:
            with file(record_file_path) as record_file:
                record = bs4(record_file)
                header = [
                    con for con in record.select('td.o1')[0].contents
                    if type(con) is NavigableString and re.match(
                            pair_header_match, con
                    )
                ]
                if len(header):
                    header_match = re.match(pair_header_match, header[0])
                    pair_number = int(header_match.group(1))
                    names = filter(
                        len,
                        [header_match.group(2), header_match.group(3)]
                    )
                    if len(names) == 0:
                        virtual_pairs.append(pair_number)
        return sorted(virtual_pairs)

    def __fix_file(worker):
        def file_wrapper(self, file_path, encoding='utf-8'):
            with file(file_path, 'r+') as content_file:
                content = bs4(content_file, from_encoding=encoding)
                content = worker(self, content)
                content_file.seek(0)
                content_file.write(
                    content.prettify(encoding, formatter='html')
                )
                content_file.truncate()
        return file_wrapper

    @__fix_file
    def __fix_results(self, content):
        rows = content.select('tr')
        for row in rows:
            cells = row.select('td')
            if len(cells) >= 6:
                try:
                    if int(cells[2].contents[0]) in self.__virtual_pairs:
                        row.extract()
                except ValueError:
                    pass
        return content.table

    @__fix_file
    def __fix_full_results(self, content):
        rows = content.select('tr')
        for row in rows:
            cell_links = [
                link for link
                in row.select('td a')
                if link['href'].startswith(
                    'H-'
                ) and not link['href'].endswith(
                    'lista.html'
                )
            ]
            if len(cell_links):
                if int(cell_links[0].contents[0]) in self.__virtual_pairs:
                    row.extract()
        return content

    @__fix_file
    def __fix_records_list(self, content):
        # TODO: ułożyć ponownie komórki w tabelce
        cells = content.select('td.u')
        for cell in cells:
            cell_links = [
                link for link
                in cell.select('a.pa')
                if link['href'].startswith(
                    'H-'
                ) and not link['href'].endswith(
                    'lista.html'
                )
            ]
            if len(cell_links):
                if int(cell_links[0].contents[0]) in self.__virtual_pairs:
                    cell.extract()
        return content

    @__fix_file
    def __fix_collected(self, content):
        rows = content.select('tr')
        for row in rows:
            cells = row.select('td')
            if len(cells) == 7:
                try:
                    if int(cells[1].contents[0]) in self.__virtual_pairs:
                        if int(cells[2].contents[0]) in self.__virtual_pairs:
                            row.extract()
                except ValueError:
                    pass
            if len(cells) == 1 and cells[0]['colspan'] == '7':
                if cells[0].contents[0] == '&nbsp':
                    row.extract()
        return content

    @__fix_file
    def __fix_traveller(self, content):
        if not len(content.select('tr.virtualTable')):
            rows = [
                row for row
                in content.select('tr')
                if len(row.select('td')) >= 10
            ]
            header_added = False
            for row in rows:
                cells = row.select('td')
                if int(cells[1].contents[0]) in self.__virtual_pairs:
                    if int(cells[2].contents[0]) in self.__virtual_pairs:
                        if header_added:
                            row.extract()
                        else:
                            virtual_row = content.new_tag(
                                'tr',
                                **{'class': 'virtualTable'}
                            )
                            virtual_row.append(
                                content.new_tag('td', **{'class': 'n'})
                            )
                            virtual_row_header = content.new_tag(
                                'td',
                                colspan=10, **{'class': 'noc'}
                            )
                            virtual_row_header.string = 'Wirtualny stolik:'
                            virtual_row.append(virtual_row_header)
                            row.insert_before(virtual_row)
                            for cell in cells[1:3]:
                                cell.contents = ''
                            header_added = True
            # TODO: przesunąć wiersz wirtualnego stolika na dół tabeli
        return content.table

    __traveller_files = []
    __pair_records_files = []
    __results_file = None
    __full_results_file = None
    __pair_records_list_file = None
    __collected_scores_file = None

    def __init__(self, path_prefix, virtual_pairs=None):
        self.__parse_filepaths(path_prefix)
        if virtual_pairs is None:
            virtual_pairs = self.__detect_virtual_pairs()
        self.__virtual_pairs = virtual_pairs

    def fix_results(self):
        self.__fix_results(self.__results_file)

    def fix_full_results(self):
        self.__fix_full_results(self.__full_results_file)

    def fix_collected_scores(self):
        self.__fix_collected(self.__collected_scores_file)

    def fix_records_list(self):
        self.__fix_records_list(self.__pair_records_list_file)

    def fix_travellers(self):
        for traveller_file in self.__traveller_files:
            self.__fix_traveller(traveller_file, encoding='iso-8859-2')

table_parser = JFRVirtualTable(
    path_prefix=sys.argv[1],
    virtual_pairs=map(int, sys.argv[2:]) if len(sys.argv) > 2 else None
)
table_parser.fix_results()
table_parser.fix_full_results()
table_parser.fix_collected_scores()
table_parser.fix_records_list()
table_parser.fix_travellers()
