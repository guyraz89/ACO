# -*- coding: utf-8 -*-

from ACO import AntforBinPacking as ACO
import numpy as np
import os
import sys
import time

if __name__ == "__main__" :
    
    """
    Build list of all groups from file.
    """
    dirname = ""
    fname = os.path.join(dirname, sys.argv[1])
    data = []
    with open(fname) as f :
        for line in f:   
            data.append(int(line.rstrip()))
    
    """
    Ant Colony params set and initialize.
    """
    Niter = 10**2
    Nant = 200
    bin_size = 150

    ant_colony = ACO(data, Nant, Niter, rho=0.95, alpha=1, beta=3, Bin_size=bin_size, seed=13)
    
    """
    Start ant exploring.
    """
    start = time.time()
    best_packing = ant_colony.run()
    end = time.time()

    """
    Show results.
    """
    print("best group packing: " + str(best_packing[1]) + " Rows\n" +
          "Time to calculate: " + str(end-start) + " secs\n")