#!/usr/bin/python
import matplotlib
matplotlib.use('agg')

from numpy import loadtxt
from matplotlib.pyplot import subplot, hist, clf, savefig

def nbhist(data):
    clf()
    ax=subplot(111)
    ax.axis([8,16,0, 20])
    ax.hist(data, bins=list(range(9,17)), align='left')

import sys
from os import path

if __name__=='__main__':
#    prefix=os.getcwd()
#    files.sort()
#    print('working on %d files' % len(files))
#    data = [loadtxt(fn) for fn in files]
    for pth in sys.argv[1:]:
        _, fn = path.split(pth)
        data=loadtxt(pth, skiprows=1, usecols=(3,))
        if len(data) < 1: continue
        nbhist(data)
        savefig('nbhist_%s.png'% fn)
        print(fn + ' processed')
