#!/usr/bin/env python2
import sys, StringIO
import numpy as np
from os.path import basename

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: %s <ths> <files to filter and concatenate>' % sys.argv[0])
        exit(-1)
    ths = float(sys.argv[1])
    for fn in sys.argv[2:]:
        d = np.loadtxt(fn,skiprows=1)
        d = d[d[:,3] > ths, :3]
        if len(d) < 1: continue
        s = StringIO.StringIO()
        s.write('%d\ncomment\n' % len(d))
        for row in d:
            s.write('A\t%f\t%f\t%f\n' % tuple(row))
        with open(basename(fn).split('.')[0] + '.xyz', 'w') as outf:
            outf.write(s.getvalue())

#if __name__ == '__main__':
    #if len(sys.argv) < 3:
        #print('usage: %s <ths> <files to filter and concatenate>' % sys.argv[0])
        #exit(-1)
    #ths = float(sys.argv[1])
    #with open('out.xyz', 'w') as outf:
        #for fn in sys.argv[2:]:
            #d = np.loadtxt(fn,skiprows=1)
            #d = d[d[:,3] > ths, :3]
            #s = StringIO.StringIO()
            #s.write('%d\ncomment\n' % len(d))
            #for row in d:
                #s.write('A\t%f\t%f\t%f\n' % tuple(row))
                #outf.write(s.getvalue())
