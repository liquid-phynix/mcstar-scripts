#!/usr/bin/env python3
import matplotlib
matplotlib.use('agg')
#matplotlib.rc('text', usetex = True)

matplotlib.rcParams.update({'font.size': 25})

from numpy import loadtxt, ones, array, vstack, save
from matplotlib.pyplot import cm, hold, hexbin, axis, colorbar, clf, subplot, plot, figure, savefig, tight_layout, xlim, ylim, hist2d, imshow, draw
from matplotlib.path import Path
import warnings

# associate name with input columns
header = ['q4','q6','q8','w4','q4bar','q6bar','q8bar','w4bar']
columns = dict((v,k+5) for k,v in enumerate(header))

_epilog = {
    'bcc':{
        'coords':[0.036369648372665396,0.5106882308569509,0.42932247292248493,0.15931737313308109,0.038967480399284354,0.5471659616324475,0.4599883638455196,0.15931737313308109],
        'color':'black'},
    'fcc':{
        'coords':[0.19094065395649334,0.5745242597140698,0.40391456108470514,-0.15931737313308109,0.20685237511953444,0.622401281356909,0.43757410784176387,-0.15931737313308109],
        'color':'red'},
    'hcp':{
        'coords':[0.09722222222222222,0.48476168522368324,0.3169924482374672,0.13409704688030225,0.10532407407407407,0.5251584923256568,0.3434084855905895,0.13409704688030227],
        'color':'green'},
    'sc':{
        'coords':[0.7637626158259734,0.35355339059327373,0.7180703308172536,0.15931737313308109,0.8910563851303024,0.4124789556921527,0.8377487192867958,0.15931737313308109],
        'color':'blue'},
    'ico':{
        'coords':[0,0.6633249580710799,0,0,0,0,0,0],
        'color':'orange'}}

def epilog(k1, k2):
    marker = Path.unit_circle()
    for d in _epilog.values():
        plot(d['coords'][columns[k1]-5], d['coords'][columns[k2]-5],
             marker=marker,
             markersize=7,
             markeredgecolor='white',
             markeredgewidth=2,
             markerfacecolor=d['color'])

# relevant ranges of different order parameters
ranges={ 'q4':[0, 0.25],
         'q6':[0, 0.7],
         'q8':[0, 0.5],
         'w4':[-0.2, 0.2],
         'q4bar':[0, 0.2],
         'q6bar':[0, 0.6],
         'q8bar':[0, 0.5],
         'w4bar':[-0.2, 0.2] }

#pretty={ 'q4':r'q_4',
         #'q6':r'q_6',
         #'q8':r'q_8',
         #'w4':r'w_4',
         #'q4bar':r'\overline{q}_4',
         #'q6bar':r'\overline{q}_6',
         #'q8bar':r'\overline{q}_8',
         #'w4bar':r'\overline{w}_4', }

pretty={ 'q4':r'q4',
         'q6':r'q6',
         'q8':r'q8',
         'w4':r'w4',
         'q4bar':r'q4b',
         'q6bar':r'q6b',
         'q8bar':r'q8b',
         'w4bar':r'w4b', }

yoffsets={ 'q4':-20,
           'q6':-20,
           'q8':-20,
           'w4':-60,
           'q4bar':-20,
           'q6bar':-20,
           'q8bar':-20,
           'w4bar':-60 }


def myhist_interactive(data, frame, k1, k2, ths=None, cmap=cm.gnuplot):
    fig=figure()
    ax=fig.add_subplot(111, axisbg=cmap(0))
    #ax.set_xlabel(r'$%s$' % pretty[k1], fontsize=35)
    #ax.set_ylabel(r'$%s$' % pretty[k2], fontsize=35, rotation='horizontal')
    ax.set_xlabel(r'%s' % pretty[k1], fontsize=35)
    ax.set_ylabel(r'%s' % pretty[k2], fontsize=35, rotation='horizontal')
    ax.xaxis.labelpad=-13
    ax.yaxis.labelpad=yoffsets[k2]
    hist2d(data[:,columns[k1]], data[:,columns[k2]], cmin=0, bins=100)
    draw()

def myhist(data, frame, k1, k2, ths=None, cmap=cm.gnuplot):
    hold(True)
    clf()
    fig=figure()
#    fig.suptitle(r'$%s vs.\ %s$' % (pretty[k2], pretty[k1]), fontsize=35) #, {'color'    : 'black', 'fontsize'   : 30 })
    ax=fig.add_subplot(111, axisbg=cmap(0))

    #ax.set_xlabel(r'$%s$' % pretty[k1], fontsize=35)
    #ax.set_ylabel(r'$%s$' % pretty[k2], fontsize=35, rotation='horizontal')
    ax.set_xlabel(r'%s' % pretty[k1], fontsize=35)
    ax.set_ylabel(r'%s' % pretty[k2], fontsize=35, rotation='horizontal')
    ax.xaxis.labelpad=-13
    ax.yaxis.labelpad=yoffsets[k2]


#    ax.text(0.125, 0.55, r'$%s vs.\ %s$' % (pretty[k2], pretty[k1]))

    # if ths is None:
    #     ax.set_title('frame: %d' % frame)
    # else:
    #     ax.set_title('max: %d, frame: %d' % (ths, frame))

    # normal
    #select = ones(len(data), dtype = 'bool')
#    nuclei - xi >= 7
#    select = data[:,4] >= 7
#    precursor xi < 7 && q6bar >= 0.27
    #select = (data[:,4] < 7) * (data[:,10] > 0.27)
    # square bin
    hist2d(data[:,columns[k1]], data[:,columns[k2]], cmin=0, bins=100)
    #hist2d(data[:,columns[k1]], data[:,columns[k2]], cmin=0, range=[ranges[k1] , ranges[k2]], bins=100)
    #hist2d(data[select,columns[k1]], data[select,columns[k2]], cmin=0, cmax=ths, range=[ranges[k1] , ranges[k2]], bins=100)
#    ax.imshow(h[0], cmap=cmap)
    # hexbin
    # hexbin(data[select,columns[k1]], data[select,columns[k2]],
    #        gridsize=100,
    #        cmap=cmap,
    #        vmin=0,
    #        vmax=ths,
    #        extent=ranges[k1] + ranges[k2])

    epilog(k1, k2)
    if False:
        ax.set_xlim(ranges[k1])
        ax.set_ylim(ranges[k2])

        # axis(ranges[k1] + ranges[k2])
        # print("k1: %s, k2: %s => %s" % (k1, k2, ranges[k1] + ranges[k2]))
        ax.set_xticks(ranges[k1])
        ax.set_yticks(ranges[k2])
        # ax.set_xticks(ax.get_xticks()[[0,-1]])
        # ax.set_yticks(ax.get_yticks()[[0,-1]])
        # ax.set_xticks(ax.get_xticks()[::2])
        # ax.set_yticks(ax.get_yticks()[::2])

    ax.tick_params(axis='both', which='major', color='white', length=10)

    colorbar()
    hold(False)

import sys
from re import compile as rec
from os import path

def filter_files(files, suffix):
    re = rec(r'\S+?([0-9]+)\.%s$' % suffix)
    def g(fns):
        for fn in fns:
            m = re.match(fn)
            if m: yield int(m.group(1)), fn
    return [tt[1] for tt in sorted(g(files), key=lambda t: t[0])]

def sort_files(g):
    lst = list(g)
    lst.sort(key = lambda tpl: tpl[0])
    return [(i,fn) for (i,(_,fn)) in enumerate(lst)]

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('usage: %s <bins> <filenames...>' % sys.argv[0])
    bins = 1
    files = sys.argv[2:]
    if sys.argv[1] == 'all':
        bins = len(files)
    else:
        bins = int(sys.argv[1])
    files = filter_files(files, 'txt')
    print('working on %d files' % len(files))

    #pairs = [('q4','q6'),('q4','q8'),('q6','q8'),('q4','w4'),('q6','w4'),
             #('q4bar','q6bar'),('q4bar','q8bar'),('q6bar','q8bar'),('q4bar','w4bar'),('q6bar','w4bar')]
    pairs = [(header[i],header[j]) for i in range(len(header)) for j in range(i+1, len(header))]

    binned_files = []
    for idx in range(len(files) // bins):
        l = [files[bins * idx + i] for i in range(bins)]
        binned_files.append(l)
    print('expected number of output files is %d' % len(binned_files))

    #    tight_layout()
    for fidx, files in enumerate(binned_files):
        data = None
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            data = []
            for fn in files:
                d = loadtxt(fn, skiprows=1)
                if len(d) < 1: continue
                # point should have at least 5 neigbors
                d = d[d[:,3] > 4]
                if len(d) < 1: continue
                data.append(d)
        data = vstack(data)
        save("egyben_%d" % fidx, data)
        #sys.exit(1)
        data0shape = data[0].shape
        #if len(data) < bins:
            #print fidx
            #continue
#        suffix = '%05d.png' % frame
        print ('idx=%d with %d points' % (fidx, len(data)))
        for i, (k1, k2) in enumerate(pairs):
            myhist(data, fidx, k1, k2, None, cmap = cm.gnuplot)
            #myhist_interactive(data, fidx, k1, k2, None, cmap = cm.gnuplot)
            savefig('bo_%s_%s_%d.png' % (k1, k2, fidx))
#            savefig('%s/%s_%s_%s._%s'%(prefix,fn,k1,k2,suffix))
        print('batch %d done' % fidx)

#for i in range(5, 13):
    #figure()
    #hist(d[:,i], bins=40)
    #title(str(i))

#figure();hist(d[:,3],bins=array(range(0,20))+0.5)
