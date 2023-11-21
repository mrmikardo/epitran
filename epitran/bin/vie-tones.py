#!/usr/bin/env python3

import csv
import os.path
import re
import sys
import unicodedata

tones = {
    '\u00b4': '˧˥', # acute = sac
    '\u0060': '˨˩', # grave = huyen
    '\u0303': '˧˥', # tilde = nga
    '\u0309': '˧˩˧', # hook above = hoi
    '\u0323': '˧˩', # dot below = nang
}


def shuffle_tone(orth, phon):
    orth = unicodedata.normalize('NFD', orth)
    if re.search('[aeiouơư]', orth):
        for tone in tones:
            if tone in orth:
                phon += tones[tone]
        if not re.search('[˩˨˧˦˥]', phon):
            phon += '˧'
    return phon


def main():
    fnin = sys.argv[1]
    fnout = os.path.basename(fnin)
    with open(fnin) as fin, open(fnout, 'w') as fout:
        writer = csv.writer(fout)
        reader = csv.reader(fin)
        header = next(reader)
        writer.writerow(header)
        for orth, phon in reader:
            phon = shuffle_tone(orth, phon)
            writer.writerow([orth, phon])


if __name__ == '__main__':
    main()