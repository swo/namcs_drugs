#!/usr/bin/env python3

import argparse, re

class Word:
    def __init__(self, line, char_column, content):
        self.line = line
        self.char_column = char_column
        self.content = content
        self.code = self.is_code(self.content)

    def __str__(self):
        return str({'line': self.line, 'col': self.char_column, 'word': self.content, 'code': self.code})

    @staticmethod
    def is_code(x):
        '''Is this word a 5-digit drug code?'''
        return re.match('^[acdn]\d{5}$', x) is not None

def argmin(xs, f):
    return [x for x in xs if f(x) == min([f(x) for x in xs])]

assert argmin([2, 9, 11, 14], lambda x: x % 10) == [11]

class Page:
    def __init__(self, number, words):
        self.number = number
        self.words = words
        self.code_desc = self._group_code_desc(self.words)

    @classmethod
    def _group_code_desc(cls, words):
        cells = cls._tesselate(words)
        return [(c[0].content, ' '.join([w.content for w in c[1]])) for c in cells]

    @staticmethod
    def _tesselate(words):
        cells = []
        for word in words:
            if word.code:
                # start a new cell with this code
                cells.append([word, []])
            else:
                # assign this word to an existing cell
                codes = [c[0] for c in cells]

                # go right and find codes that match
                cols = [c.char_column for c in codes]
                assert len(cols) > 0
                col = max([c for c in cols if c <= word.char_column])
                candidates = [c for c in codes if c.char_column == col]

                # take the one closest above
                l = max([c.line for c in candidates if c.line <= word.line])

                # assert there's one best match
                matches = [c for c in codes if c.char_column == col and c.line == l]
                assert len(matches) == 1

                # get the cell corresponding to that code.
                # there should be only one.
                cell = [c for c in cells if c[0] is matches[0]]
                assert len(cell) == 1

                # add this word to that cell
                cell[0][1].append(word)

        return cells

def mark_preamble(lines):
    '''
    Mark the preamble, which always starts with 'APPENDIX III' and ends with
    a line with 'semi-colons'. Yield (line_i, in preamble?, line) pairs
    '''
    state = 'before'
    for line in lines:
        if state == 'before' and line.lstrip().startswith('APPENDIX III'):
            state = 'in'
        elif state == 'in' and 'semi-colon' in line:
            state = 'last'
        elif state == 'last':
            state = 'after'
        else:
            pass

        yield (state in ['in', 'last'], line)

def extract_page_number(x):
    m = re.search('PAGE\s+(\d+)', x)
    page = m.groups()[0]
    return page

def parse_lines(lines):
    page_number = None
    line_no = 0
    for in_preamble, line in mark_preamble(lines):
        if not in_preamble:
            if 'PAGE' in line:
                line_no = 1
                page_number = extract_page_number(line)

            yield (page_number, line_no, line)

        line_no += 1

def parse_pages(lines):
    '''Parse the lines into Page objects'''
    previous_page_number = None
    pages = []
    words = None

    for page_number, line_i, line in parse_lines(lines):
        if previous_page_number is None and page_number is None:
            # top of the first page. do nothing.
            pass
        elif page_number != previous_page_number:
            # start a new page
            if words is not None:
                # make a page from the previous words
                pages.append(Page(previous_page_number, words))

            words = []
            previous_page_number = page_number
        else:
            # read the content of the line
            for m in re.finditer('(\S+)', line):
                words.append(Word(line_i, m.start(), m.group()))

    pages.append(Page(page_number, words))

    return pages

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('input', type=argparse.FileType('r'))
    args = p.parse_args()

    lines = [l.rstrip() for l in args.input]

    pages = parse_pages(lines)
    print('doc_page', 'code', 'desc', sep='\t')
    for page in pages:
        for code, desc in page.code_desc:
            print(page.number, code, desc, sep='\t')
