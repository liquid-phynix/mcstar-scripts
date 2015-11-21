import pickle
from numpy import loadtxt, fft
import gzip

def read_lowpass(fn):
    header, data = None, None
    with gzip.open(fn, 'r') as f:
        if f.readline().strip() != 'LOWPASS':
            raise ValueError('<%s> is not a valid LOWPASS file' % fn)
        picklelen = int(f.readline().strip())
        pickleload = f.read(picklelen)
        header = pickle.loads(pickleload)
        print(header)
        data = loadtxt(f)
    n0, n1 = int(header['n0']), int(header['n1'])
    print('nonzero elements %d amongst %d, %f%%' % (len(data), n0*n1, 100*float(len(data))/float(n0*n1)))
    n0c = n0//2+1
    indices = data[:,1].astype('int') * n0c + data[:,0].astype('int')
    data = data[:,2] + 1j * data[:,3] #.reshape((header['n1'], header['n0']))
    spectrum = zeros((n1, n0c), dtype='complex128')
    spectrum.ravel()[indices] = data.ravel()[:]
    return fft.irfft2(spectrum, s=(n1, n0))
