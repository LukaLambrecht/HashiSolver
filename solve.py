#!/usr/bin/env python3

import os
import sys

sys.path.append('./src')
from hashi import Hashi
sys.path.append('./solver')
import hashisolver


if __name__=='__main__':

    # read input file
    inputfile = sys.argv[1]
    h = None

    # handle case where txt input file is provided
    if inputfile.endswith('.txt'):
        h = Hashi.from_txt(inputfile)
    # handle case where image is provided
    elif inputfile.endswith('.png') or inputfile.endswith('.jpg'):
        sys.path.append('./reader')
        from reader import HashiImageReader
        HIR = HashiImageReader()
        HIR.loadimage(inputfile)
        vertices = HIR.hashidict(verbose=False)
        h = Hashi.from_dict(vertices)
    else:
        msg = 'ERROR: type of input file not recognized;'
        msg += ' only .txt, .png and .jpg files are supported (for now).'
        raise Exception(msg)

    # print the hashi
    h.print()

    # solve the hashi
    hashisolver.solve(h)
    h.print()
    print('Complete: {}'.format(h.complete))
