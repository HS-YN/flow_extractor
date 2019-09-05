import os
import glob
import imghdr
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="give movie id")
    parser.add_argument('-i', '--id', type=str)
    args = parser.parse_args()
    dr = [v for v in os.listdir('/data1/yj/optflow/image2') if v[:4]==args.id]
    if(len(dr) != 1):
        print("ERROR")
    else:
        icnt = len(glob.glob('/data1/yj/optflow/image2/'+dr[0]+'/**/*'))
        dcnt = len(os.listdir('/data1/yj/optflow/image2/'+dr[0]))
        fcnt = len(glob.glob('/data1/yj/optflow/flow/'+dr[0]+'/**/*'))
        print("i {} d {} f {}".format(icnt, dcnt, fcnt))
        if(2*(icnt - dcnt) - fcnt == 0):
            print("TRUE")
        else:
            print("FALSE")
