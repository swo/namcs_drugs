#!/usr/bin/env python3

'''
Convert column specs between years. Use an existing column specs file to look up
the desired names, types, etc. Use a csv file to look at the names and item
numbers.
'''


import argparse, csv

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('column_specs', type=argparse.FileType('r'))
    p.add_argument('data', type=argparse.FileType('r'))
    args = p.parse_args()

    r = csv.reader(args.data)
    known_cols = next(r)

    dat = []
    for line_i, line in enumerate(args.column_specs):
        line = line.rstrip()
        if line_i == 0:
            print(line)
        else:
            old_item_no, col_name, var_name, col_type = line.split('\t')

            # I made a hack for this, since it changes name between 2011 and 2012
            if col_name not in known_cols:
                assert col_name == 'REGION'
                col_name = 'REGIONOFF'

            new_item_no = known_cols.index(col_name) + 1
            dat.append([new_item_no, col_name, var_name, col_type])

    for fields in sorted(dat):
        print(*fields, sep='\t')
