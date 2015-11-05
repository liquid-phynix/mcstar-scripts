#!/usr/bin/env ipython2

from subprocess import Popen
from multiprocessing import Process, Queue
import sys, os

EXE='/home/mcstar/src/pfc-codes/ver0/main'
COMMAND='{exe} -g {gpu} -i 30000 -e 100 -x 30 -y 30 -z 30 --namp {namp} --eps {eps} --psi0 -0.4 --tau 0.05 --sk 100 --taucorr {tau} --divs 9'

def job(hostname, gpu, params):
    BASEDIR=os.getcwd()
    TASKDIR='_'.join(['%s=%s' % kv for kv in params.iteritems()])
    DIR=BASEDIR+'/'+TASKDIR
    os.makedirs(DIR)
    params.update(exe=EXE, gpu=gpu)
    command = 'ssh %s \'%s\'' % (hostname, 'cd %s; %s' % (DIR, COMMAND.format(**params)))
    p = Popen(command, shell=True)
    p.wait()
    p = Popen('/home/mcstar/bin/fastpng.py -1 1 out*.npy', shell=True)
    p.wait()

GPUDICT={
    #'g11' : 4,
    'g14' : 4,
    'g24' : 2,
    'g25' : 2,
    'g26' : 2
}

def engine(wqueue, hostname, gpu):
    for d in iter(wqueue.get, None):
        job(hostname, gpu, d)


if __name__ == '__main__':
    #if len(sys.argv) <= 2:
        #print 'usage: %s <gpu_hostname0 ...>' % sys.argv[0]
        #sys.exit(1)

    work_queue = Queue()

    # prepare jobs
    jobparams = [dict(eps=eps, tau=tau, namp=namp) for namp in [1e-2, 5e-2] for eps in [0.3, 0.32, 0.34, 0.36] for tau in [0, 2, 8]]
    for j in jobparams:
        work_queue.put(j)

    # start engines
    num_of_engines = 0
    #for gpu_hostname in sys.argv[1:]:
    for gpu_hostname in GPUDICT.keys():
        for gpu in range(GPUDICT[gpu_hostname]):
            Process(target=engine, args=(work_queue, gpu_hostname, gpu)).start()
            num_of_engines += 1

    for _ in range(num_of_engines):
        work_queue.put(None)

