import time
import glob
import pickle
import argparse
import subprocess as sp
import multiprocessing as mp

_GPU_ID = 0
_MAX_WORKER = 2
_BUILD_DIR = "/data1/yj/optflow/flow_extractor/build"
_SAV_DIR = "/data1/yj/optflow/flow"


def extract_flow(fn):
    tick = time.time()
    sdir = os.path.join(_SAV_DIR,fn.split('/')[-2],fn.split('/')[-1])
    sp.call("mkdir -p {}".format(sdir), shell=True)
    if(len(glob.glob(sdir+'/*')) == 2*(len(glob.glob(fn+'/*')) - 1)):
        #print("{}".format(fn))
        return
    command = "{}/extract_gpu -f={} -x={}/x -y={}/y -i={}/image -b=20 -t=1 -d={} -s=1 -o=dir".format(_BUILD_DIR,fn,sdir,sdir,sdir,_GPU_ID)
    sp.call(command, shell=True)
    #print("{} - {} sec.".format(fn,time.time()-tick))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optical flow extractor')
    parser.add_argument('-g', '--gpu_id', type=int, default='GPU id')
    parser.add_argument('-d', '--directory', type=str, default='Directory list file')
    args = parser.parse_args()

    flist = pickle.load(open(args.directory,'rb'))
    #dd = args.directory
    _GPU_ID = args.gpu_id

    for dd in flist:
        sp.call("mkdir -p {}".format(os.path.join(_SAV_DIR,dd.split('/')[-1])), shell=True)
        cliplist = [os.path.join(dd,r) for r in os.listdir(dd)]
        with mp.Pool(1) as p:
            p.map(extract_flow, cliplist)
        #sp.call("sh ./noti.sh {} {}".format(_GPU_ID, dd.split('/')[-1]), shell=True)

