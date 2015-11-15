#!/usr/bin/python3

def filter_npy(files):
    numbered_npy = re.compile(r'\S+?([0-9]+)\.npy$')
    def g(fns):
        for fn in fns:
            m = numbered_npy.match(fn)
            if m: yield int(m.group(1)), fn
    return g(files)

def sort_files(g):
    lst = list(g)
    lst.sort(key = lambda tpl: tpl[0])
    return [(i,fn) for (i,(_,fn)) in enumerate(lst)]

def init(d, fl, _rmin, _rmax, _cmin, _cmax, _fmin, _fmax):
    global tdir, fmtlen, rmin, rmax, cmin, cmax, fmin, fmax
    tdir, fmtlen, fmin, fmax = d, fl, _fmin, _fmax
    rmin, rmax, cmin, cmax = _rmin, _rmax, _cmin, _cmax
    import png

def worker(tpl):
    it, fn = tpl
    data = load(fn)
    if len(data.shape) == 3:
        data = data[0,:,:]
    data = (data - fmin) / (fmax - fmin)
    if (rmin != None) and (rmax != None) and (cmin != None) and (cmax != None):
        data = data[rmin:rmax, cmin:cmax]
    shape = data.shape
    data = cmap(data, bytes=True)[:,:,:3].reshape((shape[0], shape[1] * 3))
    png.from_array(data, 'RGB;8').save(('%s/out_%0'+str(fmtlen)+'d.png') % (tdir,it))

def main(here, rmin, rmax, cmin, cmax, fmin, fmax):
    files = sort_files(filter_npy(sys.argv[2:]))
    if not files: return
    data = load(files[-1][1])
    if len(data.shape) == 3:
        data = data[0,:,:]
    #height, width = data.shape
    #min, max = data.min(), data.max()
    #min, max = -0.35, 0.35
    del data
#    p = png.Writer(width=width, height=height)

    with tempfile.TemporaryDirectory(dir = os.getcwd() if here else None) as tmpdir:
        pool = mp.Pool(processes = mp.cpu_count(), initializer=init,
                       initargs=(tmpdir, ceil(log10(len(files))), rmin, rmax, cmin, cmax, fmin, fmax))
        pool.map(worker, files)
        print('images generated')
        os.system('mencoder "mf://%s/out*.png" -o seq.mp4 -of lavf -lavfopts format=mp4 -ss 0 -ovc x264 -x264encopts bframes=1:crf=20.0:nocabac:level_idc=30:global_header:threads=4 -fps 25' % tmpdir)
        if here:
            os.system('mkdir images')
            os.system('mv %s/*.png images/' % tmpdir)
        print('movie saved')

if __name__ == '__main__':
    import sys, re, png, tempfile, os
    import multiprocessing as mp
    from matplotlib.cm import hot, RdYlBu, RdYlGn, gnuplot, gnuplot2, jet
    cmap = gnuplot
    from numpy import load, ceil, log10
    rmin,rmax,cmin,cmax,fmin,fmax = None,None,None,None,None,None
    args = sys.argv[1:]
    here = False
    if args[0] == '-h':
        here = True
        del args[0]
    if args[0] == '-range':
        rmin = int(args[1])
        rmax = int(args[2])
        cmin = int(args[3])
        cmax = int(args[4])
        fmin = float(args[5])
        fmax = float(args[6])
    else:
        fmin = float(args[0])
        fmax = float(args[1])
    main(here, rmin, rmax, cmin, cmax, fmin, fmax)
    #main(sys.argv[0] == '-h')

	# pool = multiprocessing.Pool(processes=4)
	# results = []
	# r = pool.map_async(plot_exec, pltfiles, callback=results.append)
	# r.wait()
