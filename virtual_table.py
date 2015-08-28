import sys
import glob
import re
import math
import copy

from os import path
from bs4 import BeautifulSoup as bs4
from bs4.element import NavigableString


class JFRVirtualTable:

    def __parse_filepaths(self, prefix):
        file_path = path.realpath(prefix + '.html')
        tournament_path = path.dirname(file_path)
        tournament_prefix = path.splitext(path.basename(file_path))[0]

        # RegEx matching traveller files for each board
        traveller_files_match = re.compile(
            re.escape(tournament_prefix) + '([0-9]{3})\.txt'
        )

        # converts {prefix}{anything}.{ext} filename to full path
        def get_path(relative_path):
            return path.join(tournament_path, relative_path)

        # filtering out traveller files from all TXT files
        self.__traveller_files = [f for f
                                  in glob.glob(
                                      get_path(tournament_prefix + '*.txt'))
                                  if re.search(traveller_files_match, f)]

        # RegEx for matching pair record files
        records_files_match = re.compile(
            'H-' + tournament_prefix + '-([0-9]{1,3})\.html')
        self.__pair_records_files = [
            f for f
            in glob.glob(get_path('H-' + tournament_prefix + '*.html'))
            if re.search(records_files_match, f)
        ]

        # short rersult list, from side frame
        self.__results_file = get_path(tournament_prefix + 'WYN.txt')
        # full results page
        self.__full_results_file = get_path('W-' + tournament_prefix + '.html')
        # list of pair records links page
        self.__pair_records_list_file = get_path(
            'H-' + tournament_prefix + '-lista.html')
        # collected scores page
        self.__collected_scores_file = get_path(
            tournament_prefix + 'zbior.html')

    # auto-detect virtual pairs by their record file header
    def __detect_virtual_pairs(self):
        virtual_pairs = []
        # RegEx for matching pair number and names in pair record header
        pair_header_match = re.compile('([0-9]{1,}): (.*) - (.*), .*')
        for record_file_path in self.__pair_records_files:
            with file(record_file_path) as record_file:
                record = bs4(record_file)
                # first <td class="o1"> with content matching
                # pair header is what we're after
                header = [con for con
                          in record.select('td.o1')[0].contents
                          if type(con) is NavigableString and re.match(
                                  pair_header_match, con)]
                if len(header):
                    header_match = re.match(pair_header_match, header[0])
                    pair_number = int(header_match.group(1))
                    names = filter(len,
                                   [header_match.group(2),
                                    header_match.group(3)])
                    # virtual pair does not have any names filled
                    if len(names) == 0:
                        virtual_pairs.append(pair_number)
        return sorted(virtual_pairs)

    # wrapper for DOM manipulation
    # wraps the inner function into BS4 invokation and file overwrite
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

    # fix simple results list by removing virtual pair rows
    @__fix_file
    def __fix_results(self, content):
        rows = content.select('tr')
        for row in rows:
            cells = row.select('td')
            # 6 or more cells in a "proper" result row
            # (may contain carry over or penalties)
            if len(cells) >= 6:
                try:
                    # third cell in the row is pair number
                    if int(cells[2].contents[0]) in self.__virtual_pairs:
                        row.extract()
                except ValueError:
                    pass
        return content.table

    # fix full results file by removing virtual pair rows
    @__fix_file
    def __fix_full_results(self, content):
        rows = content.select('tr')
        for row in rows:
            # select rows by cells containing pair records links
            cell_links = [link for link
                          in row.select('td a')
                          if link.has_attr('href') and
                          link['href'].startswith('H-') and
                          not link['href'].endswith('lista.html')]
            # remove these containing links to virtual pairs
            if len(cell_links):
                if int(cell_links[0].contents[0]) in self.__virtual_pairs:
                    row.extract()
        return content

    # fix the page with pair records links list
    @__fix_file
    def __fix_records_list(self, content):
        # read the original column count
        row_cell_count = int(content.table.select('tr td.o')[0]['colspan'])
        rows = content.select('tr')
        # gather rows which containted any links
        link_rows = []
        # gather cells which should stay
        link_cells = []
        for row in rows:
            cells = row.select('td.u')
            cells_found = False
            for cell in cells:
                # select cells by pair records links inside
                cell_links = [link for link
                              in cell.select('a.pa')
                              if link.has_attr('href') and
                              link['href'].startswith('H-') and
                              not link['href'].endswith('lista.html')]
                if len(cell_links):
                    # delete virtual pair cells
                    if int(cell_links[0].contents[0]) in self.__virtual_pairs:
                        cell.extract()
                    # store actual pair cells
                    else:
                        link_cells.append(cell)
                    cells_found = True
            # gather processed rows
            if cells_found:
                link_rows.append(row)
        # detach actual pair cells from the tree
        cells = map(lambda cell: cell.extract(), link_cells)
        for row in link_rows:
            row.extract()
        # first filler cell of each new row
        first_cell = content.new_tag('td', **{'class': 'n'})
        first_cell.string = u'\xa0'
        # arrange cells into rows, full rows first
        while len(cells) >= row_cell_count:
            new_row = content.new_tag('tr')
            new_row.append(copy.copy(first_cell))
            for cell in cells[0:row_cell_count]:
                new_row.append(cell)
            content.table.append(new_row)
            del cells[0:row_cell_count]
        # last row may or may not be full
        last_row = content.new_tag('tr')
        last_row.append(copy.copy(first_cell))
        for cell in cells:
            last_row.append(cell)
        # if it wasn't full, fill it with a col-spanned last cell
        if len(cells) < row_cell_count:
            last_cell = content.new_tag('td',
                                        colspan=row_cell_count-len(cells))
            last_cell.string = u'\xa0'
            last_row.append(last_cell)
        content.table.append(last_row)
        return content

    # fix collected scores tables by removing virtual pair rows
    @__fix_file
    def __fix_collected(self, content):
        rows = content.select('tr')
        for row in rows:
            cells = row.select('td')
            # "proper" rows should have 7 cells
            if len(cells) == 7:
                # ignore cells without proper pair numbers
                try:
                    if int(cells[1].contents[0]) in self.__virtual_pairs:
                        if int(cells[2].contents[0]) in self.__virtual_pairs:
                            row.extract()
                except ValueError:
                    pass
            # there are some clearly broken table cells, just throw them away
            if len(cells) == 1 and cells[0]['colspan'] == '7':
                if cells[0].contents[0] == '&nbsp':
                    row.extract()
        return content

    # fix board travellers, removing virtual tables and leaving one, annotated
    @__fix_file
    def __fix_traveller(self, content):
        # this should only happen if the traveller wasn't already processed
        # as it's the only operaton that may yield any results on second run
        # and it might break stuff
        if not len(content.select('tr.virtualTable')):
            # looking for all the rows with more than 2 cells
            rows = [row for row
                    in content.select('tr')
                    if len(row.select('td')) >= 3]
            # only the first "virtual" row needs to be prefixed with a header
            header_added = False
            virtual_row = None
            for row in rows:
                cells = row.select('td')
                # we're already added a header, meaning we're below the first
                # virtual table, we need to move the row above it
                # or remove it entirely
                if header_added:
                    row_below = row.extract()
                    # only move it if it has meaningful information (10 cells)
                    if len(cells) >= 10:
                        virtual_row.insert_before(row_below)
                # we're looking for a "proper" row, with at least 10 cells
                if len(cells) >= 10:
                    # and with both pair numbers virtual
                    if int(cells[1].contents[0]) in self.__virtual_pairs:
                        if int(cells[2].contents[0]) in self.__virtual_pairs:
                            # if we're already processed the first one,
                            # just drop subsequent virtual tables
                            if header_added:
                                row.extract()
                            # it's the first virtual table
                            # prefix it with a header
                            else:
                                virtual_row = content.new_tag(
                                    'tr',
                                    **{'class': 'virtualTable'})
                                virtual_row.append(
                                    content.new_tag('td', **{'class': 'n'}))
                                virtual_row_header = content.new_tag(
                                    'td',
                                    colspan=10, **{'class': 'noc'})
                                virtual_row_header.string = self.__header_text
                                virtual_row.append(virtual_row_header)
                                row.insert_before(virtual_row)
                                # clear pair numbers
                                for cell in cells[1:3]:
                                    cell.contents = ''
                                header_added = True
        return content.table

    __traveller_files = []
    __pair_records_files = []
    __results_file = None
    __full_results_file = None
    __pair_records_list_file = None
    __collected_scores_file = None
    # text for traveller header row
    __header_text = ''

    def __init__(self, path_prefix, virtual_pairs=None, header_text=''):
        self.__parse_filepaths(path_prefix)
        if virtual_pairs is None or len(virtual_pairs) == 0:
            virtual_pairs = self.__detect_virtual_pairs()
        self.__virtual_pairs = virtual_pairs
        self.__header_text = header_text

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

if __name__ == '__main__':
    import argparse

    argument_parser = argparse.ArgumentParser(
        description='Fix display for virtual tables in JFR Pary result pages')
    argument_parser.add_argument('path', metavar='PATH',
                                 help='tournament path with JFR prefix')
    argument_parser.add_argument('-t', '--text', metavar='HEADER',
                                 default='Wirtualny stolik:',
                                 help='traveller header for virtual score')
    argument_parser.add_argument('pairs', metavar='PAIR_NO', nargs='*',
                                 type=int, help='virtual pair numbers')

    arguments = argument_parser.parse_args()

    table_parser = JFRVirtualTable(
        path_prefix=arguments.path,
        virtual_pairs=arguments.pairs,
        header_text=arguments.text)
    table_parser.fix_results()
    table_parser.fix_full_results()
    table_parser.fix_collected_scores()
    table_parser.fix_records_list()
    table_parser.fix_travellers()
