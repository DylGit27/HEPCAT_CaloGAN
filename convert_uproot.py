#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
file: convert.py
description: Convert GEANT4 root files into hdf5 files
author: Luke de Oliveira (lukedeo@manifold.ai)
"""

import ROOT
import pandas as pd
import numpy as np
from h5py import File as HDF5File
import uproot

### Supresses fragmentation warning from pandas ###
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


LAYER_SPECS = [(3, 96), (12, 12), (12, 6)]

LAYER_DIV = list(np.cumsum(list(map(np.prod, LAYER_SPECS))))
LAYER_DIV = zip([0] + LAYER_DIV, LAYER_DIV)

OVERFLOW_BINS = 3

def write_out_file(infile, outfile, tree=None):
    with uproot.open(infile) as f:
        T = f[tree]
        cells = list(filter(lambda x: x.startswith('cell'), T.keys()))

        assert len(list(cells)) == sum(map(np.prod, LAYER_SPECS)) + OVERFLOW_BINS

        X = T.arrays(cells, library='pd')
        E = T['TotalEnergy'].arrays(library='pd')

    with HDF5File(outfile, 'w') as h5:
        for layer, (sh, (l, u)) in enumerate(zip(LAYER_SPECS, LAYER_DIV)):
            h5['layer_{}'.format(layer)] = X.iloc[:, l:u].values.reshape((-1, ) + sh)
            
        h5['overflow'] = X.iloc[:, -OVERFLOW_BINS:].values
        h5['energy'] = E.values.reshape(-1, 1)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert GEANT4 output files into ML-able HDF5 files')

    parser.add_argument('--in-file', '-i', action="store", required=True,
                        help='input ROOT file')
    parser.add_argument('--out-file', '-o', action="store", required=True,
                        help='output HDF5 file')
    parser.add_argument('--tree', '-t', action="store", required=True,
                        help='input tree for the ROOT file')

    args = parser.parse_args()

    write_out_file(infile=args.in_file, outfile=args.out_file, tree=args.tree)

    
    

