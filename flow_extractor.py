import os
import time
import pickle
import argparse
import subprocess as sp
import multiprocessing as mp

_GPU_ID = 0
_BUILD_DIR = "/data2/hsyn/LSMDC/dense_flow/build"
_SAV_DIR = "/data2/hsyn/LSMDC_shared/features/flow"


def extract_flow(fn):
    tick = time.time()
    sdir = os.path.join(_SAV_DIR,fn.split('/')[-2],fn.split('/')[-1])
    sp.call("mkdir -p {}".format(sdir), shell=True)
    command = "{}/extract_gpu -f={} -x={}/x -y={}/y -i={}/image -b=20 -t=1 -d={} -s=1 -w=960 -h=540 -o=dir".format(_BUILD_DIR,fn,sdir,sdir,sdir,_GPU_ID)
    sp.call(command, shell=True)
    print("{} - {} sec.".format(fn,time.time()-tick))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optical flow extractor')
    parser.add_argument('-g', '--gpu_id', type=int, help='GPU id', default=0)
    parser.add_argument('-d', '--directory', type=str, help='Directory list file', 
            default="/data2/hsyn/LSMDC_shared/features/image/0001_American_Beauty")
    parser.add_argument('-b', '--build_dir', type=str, help='Directory with built extractor',
            default="/data2/hsyn/LSMDC/flow_extractor/build")
    parser.add_argument('-s', '--save_dir', type=str, help='Directory to save flow',
            default="/data2/hsyn/LSMDC_shared/features/flow")
    parser.add_argument('-w', '--workers', type=int, help='Number of GPU processes',
            default=2)
    args = parser.parse_args()

    flist = pickle.load(open(args.directory,'rb'))
    _GPU_ID = args.gpu_id
    _BUILD_DIR = args.build_dir
    _SAV_DIR = args.save_dir
    
    for dd in flist:
        sp.call("mkdir -p {}".format(os.path.join(_SAV_DIR,dd.split('/')[-1])), shell=True)
        cliplist = [os.path.join(dd,r) for r in os.listdir(dd)]
        with mp.Pool(args.workers) as p:
            p.map(extract_flow, cliplist)

    # For slack notification
    sp.call("sh ./noti.sh {}".format(_GPU_ID), shell=True)
