#!/usr/bin/env python3
import tempfile
import sys
from os import getcwd, path
from os.path import basename
from numpy import loadtxt, zeros, array

# kinds of atoms
AMOR = 1
MRCO = 2
CRYS = 3

# Kawasaki & Tanaka
def coloring_1(asc, d):
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[(0.27 < q6b) * (q6b < 0.4)] = MRCO
    ret[0.4 <= q6b] = CRYS
    return ret

# Tan, Xu, Xu
def coloring_2(asc, d):
    xi = d[:,asc['xi']]
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[:] = AMOR
    ret[(xi < 7) * (q6b >= 0.27)] = MRCO
    ret[(xi >= 7) * (q6b >= 0.27)] = CRYS
    return ret

# Tanaka
def coloring_3(asc, d):
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[q6b <= 0.28] = AMOR
    ret[(0.28 < q6b)  * (q6b < 0.4)] = MRCO
    ret[0.4 <= q6b] = CRYS
    return ret

# PRL2011
def coloring_4(asc, d):
    xi = d[:,asc['xi']]
    q4b = d[:,asc['q4b']]
    q6b = d[:,asc['q6b']]
    ret=zeros(len(d))
    ret[:] = AMOR
    ret[((0.02 < q4) * (q4 < 0.07)) * ((0.48 < q6) * (q6 < 0.52))] = MRCO
    return ret

def name2col(f):
    comment = f.readline().strip()
    return dict([(name,col) for col, name in enumerate(comment.split(' ')[1:])])

def write_xyz(data, fn, pdes='A', comment=''):
    with open(fn + '.xyz', 'w') as f:
        f.write('%d\n%s\n' % (len(data), comment))
        for row in data:
            f.write('%s %f %f %f\n' % (pdes, row[0], row[1], row[2]))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s <bond order files...>' % sys.argv[0])
        sys.exit(1)
    coloring = coloring_2
    print('using %s for criteria' % coloring.__name__)
    for infn in sys.argv[1:]:
        num = int(infn.split('_')[-1].split('.')[0])
        data, assoc = None, None
        with open(infn, 'r') as inf:
            assoc = name2col(inf)
            data=loadtxt(inf)
        sep = coloring(assoc, data)
        bname = '.'.join(basename(infn).split('.')[:-1])
        write_xyz(data[sep == AMOR], bname + '_amor', pdes='A', comment='AMOR')
        write_xyz(data[sep == MRCO], bname + '_mrco', pdes='B', comment='MRCO')
        write_xyz(data[sep == CRYS], bname + '_crys', pdes='C', comment='CRYS')


# PRL2011
# kek
#                elif 0.4 <= q6b < 0.55: tmp.write(sphere(row[0], row[1], row[2], 0, 1, 0).encode())
#                elif 0.55 <= q6b:       tmp.write(sphere(row[0], row[1], row[2], 0, 0, 1).encode())
