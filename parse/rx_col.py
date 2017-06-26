#!/usr/bin/env python3

start_dat = {2011: 173, 2014: 466}

start = start_dat[2011]

for rx_i in range(8):
    n = '{:d}'.format(rx_i + 1)
    n0 = '{:02d}'.format(rx_i + 1)

    def printf(offset, col, var, typ):
        print(start + 20 * rx_i + offset, col.format(n), var.format(n0), typ, sep='\t')

    printf(0, 'drugid{}', 'rx{}_id', 'c')
    printf(1, 'prescr{}', 'rx{}_prescription', 'i')
    printf(4, 'rx{}cat1', 'rx{}_cat1', 'c')
    printf(5, 'rx{}cat2', 'rx{}_cat2', 'c')
    printf(6, 'rx{}cat3', 'rx{}_cat3', 'c')
    printf(7, 'rx{}cat4', 'rx{}_cat4', 'c')
