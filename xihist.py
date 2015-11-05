#!/usr/bin/python
import matplotlib
matplotlib.use('agg')

from numpy import loadtxt, array
from matplotlib.pyplot import subplot, hist, clf, savefig

import matplotlib.pyplot as p
import matplotlib.patches as pa
from matplotlib.pyplot import cm

def legend(dist):
    w,h = 0.06,0.4
    fig=p.figure(figsize=(10,0.7), dpi=300)
#    fig=p.figure(dpi=300)
    ax=fig.add_axes([0.005,0,1,1], frameon=False, xticks=[], yticks=[])

    ax.text(w/4., 0.5/2, '$\\xi$', name='Monospace', size=18, ha="center", va="center")
    ax.add_patch(pa.Rectangle((0,0.5/2+h/2.), w/2, h, fc= 'white'))
    ax.text(w/4., 0.5/2+h, '%', name='Monospace', size=18, ha="center", va="center")
    ax.add_patch(pa.Rectangle((0,0.5/2-h/2.), w/2, h, fc = 'white'))

    for y in range(16):
        c = cm.RdYlBu(y/16.)
        yy = y * w

        ax.text(yy+w/2. + w/2, 0.5/2, str(y), name='Monospace', size=18, ha="center", va="center")
        ax.add_patch(pa.Rectangle((yy+w/2.,0.5/2-h/2.), w, h, fc=c))
        
        ax.text(yy+w/2. + w/2, 0.5/2+h, '%.1f' % dist[y], name='Monospace', size=18, ha="center", va="center")
        ax.add_patch(pa.Rectangle((yy+w/2.,0.5/2+h/2.), w, h, fc=c))

#    ax.text(16.5*w/2., 0.2, '$ \\xi $', name='Monospace', size=22, ha="center", va="center")

import sys
from os import path

if __name__=='__main__':
    for pth in sys.argv[1:]:
        _, fn = path.split(pth)
        data=loadtxt(pth, skiprows=1, usecols=(4,))
        # xi \el [0, 15]
        dist = array([sum(data == s) for s in range(16)])
        s = sum(dist)
        dist = 100 * dist / float(s)
        legend(dist)
        savefig('xihist_%s.png'% fn)
        print(fn + ' processed')
