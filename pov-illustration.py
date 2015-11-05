#!/usr/bin/env python3
import tempfile
from sys import argv
from os import getcwd, path
from numpy import loadtxt
from subprocess import check_call

povstrings = ["""
#include "colors.inc";
camera{ location <-300,300,-350> look_at <0,-25,0> };
""".encode(),"""
light_source { <-200,300,-350> color White };
background {White};
""".encode()
]

def sphere(*args):
    return 'sphere{ <%e, %e, %e>, 4  pigment { rgb <%e, %e, %e> } finish { phong 0.7 phong_size 20 } }' % args

if __name__ == '__main__':
    with tempfile.NamedTemporaryFile() as tmp:
        white_fn = argv[1]
        # , purple_fn, red_fn, blue_fn = argv[1:]
        # tmp.file.truncate(0)
        # tmp.write(povstrings[0])
        white_data = loadtxt(white_fn)
        # purple_data = loadtxt(purple_fn)
        # red_data = loadtxt(red_fn)
        # blue_data = loadtxt(blue_fn)

        for row in white_data:
            tmp.write(sphere(row[0], row[1], row[2], 1, 1, 1).encode())
        # for row in purple_data:
        #     tmp.write(sphere(row[0], row[1], row[2], 0.5, 0, 0.5).encode())
        # for row in red_data:
        #     tmp.write(sphere(row[0], row[1], row[2], 1, 0, 0).encode())
        # for row in blue_data:
        #     tmp.write(sphere(row[0], row[1], row[2], 0, 0, 1).encode())

        tmp.write(povstrings[1])
        tmp.file.flush()
        check_call(('povray +L/home/mcstar/bin/ +W640 +H480 +I%s +O%s.png' % (tmp.name, 'illustration')), shell=True)
        print(fn + ' processed')

