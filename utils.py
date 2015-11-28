import pickle
from numpy import loadtxt, fft
import gzip
import glob
from os.path import basename
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
    if d[-1] != '/': d = d + '/'
    fn_avg = d + 'avg_%d.lowpass' % num
    fn_amp = d + 'amp_%d.lowpass' % num
    fn_peaks = d + 'peaks_%d.txt' % num
    fn_ifaces = glob.glob(d + 'iface_*_%d.txt' % num)
    fig,ax=subplots()
    h0, h1 = 1., 1.
    try:
        #avg,header = read_lowpass(fn_amp)
        avg,header = read_lowpass(fn_avg)
        imshow(avg)
        h0 = header['l0']/float(header['n0'])
        h1 = header['l1']/float(header['n1'])
        axi=ax.imshow(avg,cmap=cm.gnuplot)
        fig.colorbar(axi)
    except None: pass
    #except IOError: pass
    try:
        peaks = loadtxt(fn_peaks, usecols=(0,1,3))
        if len(peaks) > 0:
            vals = peaks[:,2]
            peaks[:,2] = 7 * (vals - vals.min())/(vals.max() - vals.min())
            #if len(peaks)>0: ax.plot(peaks[:,0]/h0, peaks[:,1]/h1,'wo')
            #val =         #if len(val)>0: ax.scatter(i0/h0, i1/h1, c='black', s=val, edgecolors='none')
            ps = [patches.Circle((i0/h0,i1/h1), v) for i0,i1,v in peaks]
            ax.add_collection(PatchCollection(ps, edgecolor='none', facecolor='black'))
    except None: pass
    #except IOError: pass
    try:
        for iface in (loadtxt(fn_iface) for fn_iface in fn_ifaces):
            if len(iface)>0: ax.plot(iface[:,0]/h0, iface[:,1]/h1,'w-')
    except None: pass
    #except IOError: pass
    fig.tight_layout()

def grep(fn, what):
    def _g():
        with open(fn, 'r') as f:
            for line in f.readlines():
                if line.find(what) != -1:
                    yield line
    return list(_g())

#from collections import defaultdict
#def process_dirs(ds):
    #res = defaultdict(defaultdict(dict))
    #res = {}
    #for d in ds:
        #print(d)
        #misfit = grep(d + '/log', 'misfit')[0].split('=')[-1].strip()
        #layers = grep(d + '/log', 'layers')[0].split('=')[-1].strip()
        #head = res
        #for kv in d.split('_'):
            #k,v=kv.split('=')
            #key = (k,int(v))
            #if key not in head:
                #head[key] = {}
            #head = head[key]
        #head.update(misfit=misfit, layers=layers)
    #return res

#def query(d, ):
    #pass

from tinydb import TinyDB, Query

def process_dirs(ds):
    db = TinyDB('./results.json')
    for d in ds:
        d=d.strip('/')
        print(d)
        misfit = grep(d + '/log', 'misfit')
        layers = grep(d + '/log', 'layers')
        if len(misfit)==0 or len(layers)==0: continue
        misfit = misfit[0].split('=')[-1].strip()
        layers = layers[0].split('=')[-1].strip()
        key = {}
        for kv in basename(d).split('_'):
            k,v=kv.split('=')
            key[k] = int(v)
        key['misfit'] = misfit
        key['layers'] = layers
        db.insert(key)
    return db

#def print_db(db, **args):
    #rec = Query()
    #query = rec
    #for res in db.search((rec.stress==-1) & (rec.nn==20)):
            #print '{layers},'.format(**res)
    #pass

def pretty_1(tdb, stress=None, nn=None):
    rec=Query()
    print '{ %d, ' % nn,
    for res in tdb.search((rec.stress==stress) & (rec.nn==nn)):
        print '{layers},'.format(**res),
    print '}'

#import dataset

#def process_dirs(ds):
    #db = dataset.connect('sqlite:///results.db')
    #table = db['results']
    #for d in ds:
        #print(d)
        #misfit = grep(d + '/log', 'misfit')[0].split('=')[-1].strip()
        #layers = grep(d + '/log', 'layers')[0].split('=')[-1].strip()
        #key = {}
        #for kv in d.split('_'):
            #k,v=kv.split('=')
            #key[k] = int(v)
        #key['misfit'] = misfit
        #key['layers'] = layers
        #table.insert(key)
    #return db
def nn2misfit(stress, nn): return float(nn)/float(nn-stress)-1

def plot_hc_vs_f(db, op=np.min, fig=None, label=None):
    r=Query()
    nnlist = set(int(db.get(eid=i)['nn']) for i in range(1, len(db)+1))
    nnlist = sorted(list(nnlist))
    #print nnlist
    conv = {}
    for stress in [-1,1]:
        conv[stress] = [array([float(rec['layers']) for rec in db.search((r.stress==stress) & (r.nn==nn))]) for nn in nnlist]
    if fig is None:
        fig=figure()
        if len(fig.get_axes()) == 0:
            fig.add_subplot(111)
    ax = fig.get_axes()[0]
    for s,lst in conv.iteritems():
        toplot=array([(nn2misfit(s, nn), op(arr)) for nn,arr in zip(nnlist, lst)])
        ax.plot(toplot[:,0], toplot[:,1],'-x',label=label)
    draw()
    return fig


