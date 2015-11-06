#!/usr/bin/env python3
import tempfile
import sys
from os import getcwd, path
from os.path import basename
from numpy import loadtxt
from subprocess import check_call

povstrings = ["""
#include "colors.inc"
camera{ location <-300,300,-350> look_at <0,-25,0> }
""".encode(),"""
light_source { <-200,300,-350> color White }
background {Black}
""".encode()
]

def sphere(*args):
    return 'sphere{ <%e, %e, %e>, 4  pigment { rgb <%e, %e, %e> } finish { phong 0.7 phong_size 20 } }' % args

# Kawasaki & Tanaka
def coloring_1(d, f, vars):
    x,y,z = vars[d['x']], vars[d['y']], vars[d['z']]
    q6b = vars[d['q6b']]
    if 0.27 < q6b < 0.4:
        f.write(sphere(x, y, z, 1, 0, 0).encode())
    elif 0.4 <= q6b:
        f.write(sphere(x, y, z, 0, 1, 0).encode())

# Tan, Xu, Xu
def coloring_2(d, f, vars):
    x,y,z = vars[d['x']], vars[d['y']], vars[d['z']]
    xi = vars[d['xi']]
    q6b = vars[d['q6b']]
    if xi < 7 and q6b >= 0.27:    f.write(sphere(x,y,z, 1, 0, 0).encode())
    elif xi >= 7 and q6b >= 0.27: f.write(sphere(x,y,z, 0, 1, 0).encode())
    else:                         f.write(sphere(x,y,z, 1, 1, 1).encode())

# Tanaka
def coloring_3(d, f, vars):
    x,y,z = vars[d['x']], vars[d['y']], vars[d['z']]
    q6b = vars[d['q6b']]
    if q6b <= 0.28:         f.write(sphere(x, y, z, 0.5, 0.5, 0.5).encode())
    elif 0.28 < q6b < 0.4:  f.write(sphere(x, y, z, 1, 0, 0).encode())
    elif 0.4 <= q6b:        f.write(sphere(x, y, z, 0, 1, 0).encode())

# PRL2011
def coloring_4(d, f, vars):
    x,y,z = vars[d['x']], vars[d['y']], vars[d['z']]
    xi = vars[d['xi']]
    q4 = vars[d['q4']]
    q6 = vars[d['q6']]
    if (0.02 < q4 < 0.07) and (0.48 < q6 < 0.52):
        f.write(sphere(x,y,z, 1, 0, 0).encode())
    else:
        f.write(sphere(x,y,z, 0.5, 0.5, 0.5).encode())

def name2col(f):
    comment = f.readline().strip()
    return dict([(name,col) for col, name in enumerate(comment.split(' ')[1:])])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s <bond order files...>')
        sys.exit(1)
    coloring = coloring_3
    print('using %s for criteria' % coloring.__name__)
    with tempfile.NamedTemporaryFile() as tfile:
        for infn in sys.argv[1:]:
            data, assoc = None, None
            with open(infn, 'r') as inf:
                assoc = name2col(inf)
                data=loadtxt(inf)

            tfile.file.truncate(0)
            tfile.write(povstrings[0])
            for row in data:
                coloring(assoc, tfile, row)
            tfile.write(povstrings[1])
            tfile.file.flush()
            resultfn = '.'.join(basename(infn).split('.')[:-1])
            check_call(('povray +W640 +H480 +I%s +O%s.png' % (tfile.name, resultfn)).split(' '))
            print('%s => %s.png' % (infn, resultfn))


# PRL2011
# kek
#                elif 0.4 <= q6b < 0.55: tmp.write(sphere(row[0], row[1], row[2], 0, 1, 0).encode())
#                elif 0.55 <= q6b:       tmp.write(sphere(row[0], row[1], row[2], 0, 0, 1).encode())
