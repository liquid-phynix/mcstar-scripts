#!/usr/bin/env python2

import StringIO
from numpy import *

def blur2d(arr):
    a1 = roll(arr, 1, axis=0)
    a2 = roll(arr, -1, axis=0)
    a3 = roll(arr, 1, axis=1)
    a4 = roll(arr, -1, axis=1)
    return (arr + a1 + a2 + a3 + a4) / 5.

def blur3d(arr):
    a1 = roll(arr, 1, axis=0)
    a2 = roll(arr, -1, axis=0)
    a3 = roll(arr, 1, axis=1)
    a4 = roll(arr, -1, axis=1)
    a5 = roll(arr, 1, axis=2)
    a6 = roll(arr, -1, axis=2)
    return (arr + a1 + a2 + a3 + a4 + a5 + a6) / 7.

def peakfilter2d(arr, mx=None):
    if mx is None:
        mx = arr.min()
    a1=roll(arr, 1, axis=0)
    a2=roll(arr, -1, axis=0)
    a3=roll(arr, 1, axis=1)
    a4=roll(arr, -1, axis=1)
    localmax =  arr > mx
    localmax *= arr > a1
    localmax *= arr > a2
    localmax *= arr > a3
    localmax *= arr > a4
    localmax *= arr > roll(a1, 1, axis=1)
    localmax *= arr > roll(a1, -1, axis=1)
    localmax *= arr > roll(a2, -1, axis=1)
    localmax *= arr > roll(a2, 1, axis=1)
    y,x = where(localmax)
    return vstack((x,y)).transpose()

def peakfilter3d(arr, mx=None):
    if mx is None:
        mx = arr.min()
    a1=roll(arr, 1, axis=0)
    a2=roll(arr, -1, axis=0)
    a3=roll(arr, 1, axis=1)
    a4=roll(arr, -1, axis=1)
    a5=roll(arr, 1, axis=2)
    a6=roll(arr, -1, axis=2)
    localmax =  arr > mx
    localmax *= arr > a1
    localmax *= arr > a2
    localmax *= arr > a3
    localmax *= arr > a4
    localmax *= arr > a5
    localmax *= arr > a6
    #localmax *= arr > roll(a1, 1, axis=1)
    #localmax *= arr > roll(a1, -1, axis=1)
    #localmax *= arr > roll(a2, -1, axis=1)
    #localmax *= arr > roll(a2, 1, axis=1)
    z,y,x = where(localmax)
    return vstack((x,y,z)).transpose()

if __name__ == '__main__':
#if True:
    import sys
    if len(sys.argv) != 3:
        print('usage: %s <ths> <file to filter>' % sys.argv[0])
        exit(-1)
    ths = float(sys.argv[1])
    fn = sys.argv[2]
    data = load(fn)
    if len(data.shape) == 3:
        data = blur3d(data)
        peaks = peakfilter3d(data, ths)
    elif len(data.shape) == 2:
        data = blur2d(data)
        peaks = peakfilter2d(data, ths)
        hstack((peaks, matrix([0 for _ in range(len(peaks))]).transpose()))
    else: raise ValueError('wtf')
    s = StringIO.StringIO()
    s.write('%d\ncomment\n' % len(peaks))
    for row in peaks:
        row=tuple(row)
        s.write('A\t%f\t%f\t%f\n' % row)
    with open('out.xyz', 'w') as f:
    #with open(fn + '.xyz', 'w') as f:
        f.write(s.getvalue())
