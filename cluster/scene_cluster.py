import os
import json
import glob
import pickle
from operator import add

from sklearn.cluster import KMeans, Birch, DBSCAN, AffinityPropagation
from sklearn.cluster import AgglomerativeClustering as Agnes
from tqdm import tqdm
import numpy as np
import cv2


def pool_3x3(imgx, imgy):
    sh = imgx.shape
    ret = []
    for i in np.arange(0,sh[0],int(sh[0]/3)):
        for j in np.arange(0,sh[1],int(sh[1]/3)):
            ret.append((np.average(imgx[i:i+int(sh[0]/3),j:j+int(sh[1]/3)])-128)/2)
            ret.append((np.average(imgy[i:i+int(sh[0]/3),j:j+int(sh[1]/3)])-128)/2)
    return ret


def preprocess(dirlist):
    dataset = []
    for dd in dirlist:
        # Load scene transition file
        boundary = json.load(open(os.path.join('boundary',dd.split('/')[-1]+'.json')))
        for r,s,f in tqdm(os.walk(dd), total=len(os.listdir(dd))):
            if r.split('/')[-1] not in boundary.keys():
                continue
            if r.split('/')[-1][:4] != '1012':
                continue
            subshot = boundary[r.split('/')[-1]]
            former = 1
            print(">>>{}".format(r))
            print(">>>{} {}".format(subshot,len(glob.glob(r+'/*'))))
            for idx in subshot:
                if idx <= 2:
                    continue
                latter = idx-2
                fidx = former + (int)((latter-former)/4)
                lidx = latter - (int)((latter-former)/4)
                print("{} {}".format(fidx, lidx))
                ffeat = pool_3x3(
                    cv2.imread(os.path.join(r,"x_{:05d}.jpg".format(fidx)),0),
                    cv2.imread(os.path.join(r,"y_{:05d}.jpg".format(fidx)),0)
                )
                lfeat = pool_3x3(
                    cv2.imread(os.path.join(r,"x_{:05d}.jpg".format(lidx)),0),
                    cv2.imread(os.path.join(r,"y_{:05d}.jpg".format(lidx)),0)
                )
                dataset.append(list(map(add,ffeat,lfeat)))
                former = latter+1
        print("[LOG] {} complete".format(dd))
        pickle.dump(dataset, open('flow_cluster.pkl', 'wb'))
    return dataset


def main():
    dirlist = [os.path.join(os.getcwd(),'flow',d) for d in os.listdir('./flow') if
               d[:4] not in ['1018','3091','0028','3006']]
    #if(os.path.isfile('flow_cluster.pkl')):
    #    dataset = pickle.load(open('flow_cluster.pkl', 'rb'))
    #else:
    dataset = preprocess(dirlist)


if __name__ == '__main__':
    main()
