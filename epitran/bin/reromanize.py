#!/usr/bin/env python2



import argparse
import sys

import epitran.reromanize


def main(code, table):
    rr = epitran.reromanize.ReRomanizer(code, table)
    for line in sys.stdin:
        line = line.decode('utf-8')
        tokens = line.strip().split('\t')
        tokens = [rr.reromanize(x) for x in tokens]
        print('\t'.join(tokens).encode('utf-8'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--code', default='ori-Orya', type=str, help='Languagee and script code')
    parser.add_argument('-t', '--table', default='anglocentric', type=str, help='Romanization table')
    args = parser.parse_args()
    main(args.code, args.table)
