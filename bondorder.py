#!/usr/bin/python
import matplotlib
matplotlib.use('agg')
#matplotlib.rc('text', usetex = True)

matplotlib.rcParams.update({'font.size': 25})

from numpy import loadtxt, ones
from matplotlib.pyplot import cm, hold, hexbin, axis, colorbar, clf, subplot, plot, figure, savefig, tight_layout, xlim, ylim, hist2d, imshow
from matplotlib.path import Path

columns = dict((v,k+5) for k,v in enumerate(['q4','q6','q8','w4','q4bar','q6bar','q8bar','w4bar']))

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

ranges={ 'q4':[0, 0.25],
         'q6':[0, 0.7],
         'q8':[0, 0.5],
         'w4':[-0.2, 0.2],
         'q4bar':[0, 0.2],
         'q6bar':[0, 0.6],
         'q8bar':[0, 0.5],
         'w4bar':[-0.2, 0.2] }

# ranges={ 'q4':[0, 0.25],
#          'q6':[0, 0.7],
#          'q8':[0, 0.5],
#          'w4':[-0.2, 0.2],
#          'q4bar':[0, 0.25],
#          'q6bar':[0, 0.7],
#          'q8bar':[0, 0.5],
#          'w4bar':[-0.2, 0.2] }

pretty={ 'q4':r'q_4',
         'q6':r'q_6',
         'q8':r'q_8',
         'w4':r'w_4',
         'q4bar':r'\overline{q}_4',
         'q6bar':r'\overline{q}_6',
         'q8bar':r'\overline{q}_8',
         'w4bar':r'\overline{w}_4', }

yoffsets={ 'q4':-20,
           'q6':-20,
           'q8':-20,
           'w4':-60,
           'q4bar':-20,
           'q6bar':-20,
           'q8bar':-20,
           'w4bar':-60 }


def myhist(data, frame, k1, k2, ths=None, cmap=cm.gnuplot):
    data = data[frame]
    # if data.shape[1]==9:
    #     data=data[:,1:]
    hold(True)
    clf()
    fig=figure()
#    fig.suptitle(r'$%s vs.\ %s$' % (pretty[k2], pretty[k1]), fontsize=35) #, {'color'    : 'black', 'fontsize'   : 30 })
    ax=fig.add_subplot(111, axisbg=cmap(0))

    ax.set_xlabel(r'$%s$' % pretty[k1], fontsize=35)
    ax.set_ylabel(r'$%s$' % pretty[k2], fontsize=35, rotation='horizontal')
    ax.xaxis.labelpad=-13
    ax.yaxis.labelpad=yoffsets[k2]

    
#    ax.text(0.125, 0.55, r'$%s vs.\ %s$' % (pretty[k2], pretty[k1]))  

    # if ths is None:
    #     ax.set_title('frame: %d' % frame)
    # else:
    #     ax.set_title('max: %d, frame: %d' % (ths, frame))

    # normal
    select = ones(len(data), dtype = 'bool')
#    nuclei - xi >= 7
#    select = data[:,4] >= 7
#    precursor xi < 7 && q6bar >= 0.27
    select = (data[:,4] < 7) * (data[:,10] > 0.27)

    # square bin
    hist2d(data[select,columns[k1]], data[select,columns[k2]], cmin=0, cmax=ths, range=[ranges[k1] , ranges[k2]], bins=100)
#    ax.imshow(h[0], cmap=cmap)

    # hexbin
    # hexbin(data[select,columns[k1]], data[select,columns[k2]],
    #        gridsize=100,
    #        cmap=cmap,
    #        vmin=0,
    #        vmax=ths,
    #        extent=ranges[k1] + ranges[k2])
    epilog(k1, k2)

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
from os import path

if __name__=='__main__':
    if sys.argv[1]=='noths':
        hasths=False
        files = sys.argv[2:]
    else:
        hasths=True
        files = sys.argv[1:]

#    prefix=os.getcwd()

    files.sort()
    print('working on %d files' % len(files))

    pairs = [('q4','q6'),('q4','q8'),('q6','q8'),('q4','w4'),('q6','w4'),
             ('q4bar','q6bar'),('q4bar','q8bar'),('q6bar','q8bar'),('q4bar','w4bar'),('q6bar','w4bar')]

    # test sor
#    ths=[200, 200, 100, 100, 75, 200, 200, 60, 150, 30]
# newsandviews
    ths=[200, 200, 100, 10, 75, 50, 200, 60, 150, 30]
    # prl2011 90-es frame
    # ths=[45, 45, 45, 20, 25, 60, 60, 60, 40, 20]

    data = [loadtxt(fn, skiprows=1) for fn in files]

    print('data read into memory')
    #    tight_layout()
    for frame in range(len(data)):
#        suffix = '%05d.png' % frame
        for i,(k1,k2) in enumerate(pairs):
            myhist(data, frame, k1, k2, ths = (ths[i] if hasths else None), cmap = cm.spectral)
            savefig('%s_%s_%s.png'%(k1,k2,path.split(files[frame])[1]))
#            savefig('%s/%s_%s_%s._%s'%(prefix,fn,k1,k2,suffix))
        print('frame %d done' % frame)
