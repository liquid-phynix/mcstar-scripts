import pickle
from numpy import loadtxt, fft
import gzip
import glob
from matplotlib import patches
from matplotlib.collections import PatchCollection

def read_lowpass(fn):
    header, data = None, None
    with gzip.open(fn, 'r') as f:
        if f.readline().strip() != 'LOWPASS':
            raise ValueError('<%s> is not a valid LOWPASS file' % fn)
        picklelen = int(f.readline().strip())
        pickleload = f.read(picklelen)
        header = pickle.loads(pickleload)
        #print(header)
        data = loadtxt(f)
    n0, n1 = int(header['n0']), int(header['n1'])
    print('nonzero elements %d amongst %d, %f%%' % (len(data), n0*n1, 100*float(len(data))/float(n0*n1)))
    n0c = n0//2+1
    indices = data[:,1].astype('int') * n0c + data[:,0].astype('int')
    data = data[:,2] + 1j * data[:,3] #.reshape((header['n1'], header['n0']))
    spectrum = zeros((n1, n0c), dtype='complex128')
    spectrum.ravel()[indices] = data.ravel()[:]
    return fft.irfft2(spectrum, s=(n1, n0)), header


def plot_all(num, d='./'):
    fn_avg = d + 'avg_%d.lowpass' % num
    fn_amp = d + 'amp_%d.lowpass' % num
    fn_peaks = d + 'peaks_%d.txt' % num
    fn_ifaces = glob.glob(d + 'iface_*_%d.txt' % num)
    fig,ax=subplots()
    h0, h1 = 1., 1.
    try:
        #avg,header = read_lowpass(fn_amp)
        avg,header = read_lowpass(fn_avg)
        h0 = header['l0']/float(header['n0'])
        h1 = header['l1']/float(header['n1'])
        axi=ax.imshow(avg,cmap=cm.gnuplot)
        fig.colorbar(axi)
    except IOError: pass
    try:
        peaks = loadtxt(fn_peaks, usecols=(0,1,3))
        vals = peaks[:,2]
        peaks[:,2] = 7 * (vals - vals.min())/(vals.max() - vals.min())
        #if len(peaks)>0: ax.plot(peaks[:,0]/h0, peaks[:,1]/h1,'wo')
        #val =         #if len(val)>0: ax.scatter(i0/h0, i1/h1, c='black', s=val, edgecolors='none')
        ps = [patches.Circle((i0/h0,i1/h1), v) for i0,i1,v in peaks]
        ax.add_collection(PatchCollection(ps, edgecolor='none', facecolor='black'))
    except IOError: pass
    try:
        for iface in (loadtxt(fn_iface) for fn_iface in fn_ifaces):
            if len(iface)>0: ax.plot(iface[:,0]/h0, iface[:,1]/h1,'w-')
    except IOError: pass
    fig.tight_layout()

