#!/usr/bin/env python3
import tempfile
import sys
from os import getcwd, path
from os.path import basename
from numpy import loadtxt, zeros

# kinds of atoms
AMOR = 1
MRCO = 2
CRYS = 3

# Kawasaki & Tanaka
def coloring_1(asc, d):
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[0.27 < q6b < 0.4] = MRCO
    ret[0.4 <= q6b] = CRYS
    return ret

# Tan, Xu, Xu
def coloring_2(asc, d):
    xi = d[:,asc['xi']]
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[:] = AMOR
    ret[xi < 7 and q6b >= 0.27] = MRCO
    ret[xi >= 7 and q6b >= 0.27] = CRYS
    return ret

# Tanaka
def coloring_3(asc, d):
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[q6b <= 0.28] = AMOR
    ret[0.28 < q6b < 0.4] = MRCO
    ret[0.4 <= q6b] = CRYS
    return ret

# PRL2011
def coloring_4(asc, d):
    xi = d[:,asc['xi']]
    q4b = d[:,asc['q4b']]
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[:] = AMOR
    ret[(0.02 < q4 < 0.07) and (0.48 < q6 < 0.52)] = MRCO
    return ret

def name2col(f):
    comment = f.readline().strip()
    return dict([(name,col) for col, name in enumerate(comment.split(' ')[1:])])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s <bond order files...>')
        sys.exit(1)
    coloring = coloring_3
    print('using %s for criteria' % coloring.__name__)
    timeseries = []
    for infn in sys.argv[1:]:
        num = int(infn.split('_')[-1].split('.')[0])
        data, assoc = None, None
        with open(infn, 'r') as inf:
            assoc = name2col(inf)
            data=loadtxt(inf)
        sep = coloring_3(assoc, data)
        timeseries.append((num, sum(sep==AMOR), sum(sep==MRCO), sum(sep==CRYS)))
    ts = array(timeseries)
    t,amor,mrco,crys = ts[:,0], ts[:,1], ts[:,2], ts[:,3]
    plot(t, amor)
    plot(t, mrco)
    plot(t, crys)
    draw()


# PRL2011
# kek
#                elif 0.4 <= q6b < 0.55: tmp.write(sphere(row[0], row[1], row[2], 0, 1, 0).encode())
#                elif 0.55 <= q6b:       tmp.write(sphere(row[0], row[1], row[2], 0, 0, 1).encode())
