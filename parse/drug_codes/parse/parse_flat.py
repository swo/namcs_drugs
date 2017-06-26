#!/usr/bin/env python3

import argparse, re

def extract_page_number(x):
    m = re.search('PAGE\s+(\d+)', x)
    page = m.groups()[0]
    return page

def is_code(x):
    '''Is this word a 5-digit drug code?'''
    return re.match('^[acdn]\d{5}$', x) is not None

def contains_code(x):
    return re.search('[acdn]\d{5}', x) is not None

def smart_join(words):
    out = ''
    for word in words:
        if out != '' and not out.endswith('-'):
            out += ' '

        out += word

    return out

def parse_lines(lines):
    header = True
    page = None

    for line in lines:
        line = line.rstrip()
        words = line.rstrip().split()
        if 'APPENDIX' in line or len(words) == 0:
            continue

        if 'PAGE' in line:
            page = extract_page_number(line)

        if header:
            if is_code(words[0]):
                header = False
                code = words[0]
                desc_words = words[1:]
            else:
                pass
        else:
            if is_code(words[0]):
                if len(desc_words) == 0 or any([contains_code(w) for w in desc_words]):
                    raise RuntimeError("bad desc words '{}' with code '{}' on page {}".format(desc_words, code, page))

                yield (page, code, smart_join(desc_words))
                code = words[0]
                desc_words = words[1:]
            else:
                desc_words += words

    yield (page, code, smart_join(desc_words))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('input', type=argparse.FileType('r'))
    args = p.parse_args()

    print('doc_page', 'code', 'desc', sep='\t')
    for fields in parse_lines(args.input):
        print(*fields, sep='\t')
