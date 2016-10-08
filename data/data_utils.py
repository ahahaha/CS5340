import os
import cv2
import lmdb
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('/home/dy/caffe-master/python/')
import caffe

from random import shuffle

def insertDB(items, db):
    env = lmdb.open(db, map_size=1024**4)
    with env.begin(write=True) as txn:
        idx = env.stat()["entries"] + 1
        for img, lbl in items:
            datum = caffe.proto.caffe_pb2.Datum()
            datum.height = img.shape[0]
            datum.width = img.shape[1]
            if 2 == len(img.shape):
                datum.channels = 1
            else:
                datum.channels = img.shape[2]
            datum.data = img.tobytes()  
            datum.label = int(lbl)
            str_id = '{:08}'.format(idx)
            txn.put(str_id, datum.SerializeToString())
            idx += 1
    env.close()
    
def testDB(db):
    env = lmdb.open(db, readonly=True)
    print env.stat()["entries"]


def test():
    testDB('./data/train')
    testDB('./data/test')
    cnt = 0
    lbl_cnt = {}
    for key in label.iterkeys():
        lbl_cnt[key] = 0
    for folder in os.listdir('.'):
        if folder.endswith('depth'):
            dbPath = './data/'
            if cnt > train_num:
                break
            path = os.getcwd() + '/' + folder + '/'
            for f in os.listdir(path):
                if f.endswith(img_format):
                    lbl = f.split('_')[0]
                    lbl_cnt[lbl] += 1
                    cnt += 1
                else:
                    print path + f
    for key in lbl_cnt.iterkeys():
        print key, lbl_cnt[key] / float(train_num)

mkdir data

tot_img = 0
label = set()
img_format = '.jpg'
for folder in os.listdir('.'):
    if folder.endswith('depth'):
        path = os.getcwd() + '/' + folder + '/'
        for f in os.listdir(path):
            if f.endswith(img_format):
                tot_img += 1
                lbl = f.split('_')[0]
                label.add(lbl)

label_map = {}
idx = 1
for x in sorted(label):
    label_map[x] = idx
    idx += 1

percent = 0.85
train_num = tot_img * percent

cnt = 0
for folder in os.listdir('.'):
    if folder.endswith('depth'):
        dbPath = './data/'
        if cnt > train_num:
            print folder + ' : test'
            dbPath += 'test'
        else:
            print folder + ' : train'
            dbPath += 'train'
        path = os.getcwd() + '/' + folder + '/'
        items = []
        for f in os.listdir(path):
            if f.endswith(img_format):
                lbl = label[f.split('_')[0]]
                # single channel
                img = cv2.imread(path + f, 0)
                img1 = cv2.resize(img, (80, 80))
                items.append((img1[5:-5,5:-5], lbl))
            else:
                print path + f
        insertDB(items, dbPath)
        cnt += len(items)



