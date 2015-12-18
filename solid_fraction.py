#!/usr/bin/env python3

from numpy import array, fft, ones, real, prod
from scipy.ndimage import fourier_gaussian
from pandas import read_csv

def blur(arr):
    a1 = roll(arr, 1, axis=0)
    a2 = roll(arr, -1, axis=0)
    a3 = roll(arr, 1, axis=1)
    a4 = roll(arr, -1, axis=1)
    return 0.2 * (arr + a1 + a2 + a3 + a4)

def apply_kernel(d, k):
    return real(fft.ifft2(k * fft.fft2(d)))

if __name__ == '__main__':
    import sys
    shape = (4096, 4096)
    lpkernel = fourier_gaussian(ones(shape), 12)
    hpkernel = 1.-lpkernel
    for fn in sys.argv[1:]:
        data = array(read_csv(fn, sep = ' ', header = None, usecols = (2, )))
        data = data.reshape(shape)
        data = apply_kernel(data, hpkernel)
        data[:] **= 2
        data = apply_kernel(data, lpkernel)
        #print('max=%f' % data.max())
        data[:] /= 15.7
        data = data >= 0.5
        solid_fr = data.sum() / prod(shape)
        time = int(fn.split('_')[1].split('.')[0])
        print('%f\t%f' % (time, solid_fr))

