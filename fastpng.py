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

def init(d, fl, min, max):
    global tdir, fmtlen, dmin, dmax
    tdir, fmtlen, dmin, dmax = d, fl, min, max
    import png

def worker(tpl):
    it, fn = tpl
    data = load(fn)
    if len(data.shape) == 3:
        data = data[0,:,:]
    data = (data - dmin) / (dmax - dmin)
    shape = data.shape
    data = cmap(data, bytes=True)[:,:,:3].reshape((shape[0], shape[1] * 3))
    png.from_array(data, 'RGB;8').save(('%s/out_%0'+str(fmtlen)+'d.png') % (tdir,it))

def main(here):
    if here: del sys.argv[0]
    min, max = float(sys.argv[0]), float(sys.argv[1])
    files = sort_files(filter_npy(sys.argv[2:]))
    if not files: return
    data = load(files[-1][1])
    if len(data.shape) == 3:
        data = data[0,:,:]
    height, width = data.shape
    #min, max = data.min(), data.max()
    #min, max = -0.35, 0.35
    del data
#    p = png.Writer(width=width, height=height)

    with tempfile.TemporaryDirectory(dir = os.getcwd() if here else None) as tmpdir:
        pool = mp.Pool(processes = mp.cpu_count(), initializer=init,
                       initargs=(tmpdir, ceil(log10(len(files))), min, max))
        pool.map(worker, files)
        print('images generated')
        os.system('mencoder "mf://%s/out*.png" -o seq.mp4 -of lavf -lavfopts format=mp4 -ss 0 -ovc x264 -x264encopts bframes=1:crf=20.0:nocabac:level_idc=30:global_header:threads=4 -fps 25' % tmpdir)
        print('movie saved')

if __name__ == '__main__':
    import sys, re, png, tempfile, os
    import multiprocessing as mp
    from matplotlib.cm import hot, RdYlBu, RdYlGn, gnuplot, gnuplot2, jet
    cmap = gnuplot
    from numpy import load, ceil, log10
    del sys.argv[0]
    main(sys.argv[0] == '-h')

	# pool = multiprocessing.Pool(processes=4)
	# results = []
	# r = pool.map_async(plot_exec, pltfiles, callback=results.append)
	# r.wait()
