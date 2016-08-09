__author__ = 'amrit'

import matplotlib.pyplot as plt
import os, pickle
import operator
import numpy as np
import csv

if __name__ == '__main__':

    fileB = ['citemap']#, 'pitsB', 'pitsC', 'pitsD', 'pitsE', 'pitsF','processed_citemap']
    result1={}
    current_dic1={}
    para_dict1={}
    time1={}
    path = '/home/amrit/GITHUB/Pits_lda/src/06-17/dump/spark/tuned/test/'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            with open(a, 'rb') as handle:
                result = pickle.load(handle)
                result1 = dict(result1.items() + result.items())
                #current_dic = pickle.load(handle)
                #current_dic1 = dict(current_dic1.items() + current_dic.items())
                para_dict = pickle.load(handle)
                para_dict1 = dict(para_dict1.items() + para_dict.items())
                #time = pickle.load(handle)
                #time1 = dict(time1.items() + time.items())
    #print(para_dict1)
    #print(result1)
    with open('parameters1.csv', 'a+') as csvinput:
        fileds = ['method', 'File', 'term', 'tuned','median/iqr (k)','median/iqr (a)','median/iqr (b)']
        writer = csv.DictWriter(csvinput, fieldnames=fileds)
        #writer.writeheader()
        labels = [1,2,3,4, 5, 6, 7, 8, 9]
        for file1 in fileB:
            for l in labels:
                x=max(para_dict1[file1][l].iteritems(), key=operator.itemgetter(0))[0]
                k=[]
                a=[]
                b=[]
                print(x)
                for i in para_dict1[file1][l][x]:
                    k.append(i[0])
                    a.append(i[1])
                    b.append(i[2])
                k_string="{0:.2f}".format(np.median(k))+' / '+"{0:.2f}".format(np.percentile(k,75)-np.percentile(k,25))
                a_string="{0:.2f}".format(np.median(a))+' / '+"{0:.2f}".format(np.percentile(a,75)-np.percentile(a,25))
                b_string="{0:.2f}".format(np.median(b))+' / '+"{0:.2f}".format(np.percentile(b,75)-np.percentile(b,25))

                writer.writerow({'method':'spark','File':file1, 'term':l, 'tuned':"{0:.2f}".format(x),'median/iqr (k)':k_string,'median/iqr (a)':a_string,'median/iqr (b)':b_string})#'Cust_id': k, 'Active_Customer': int(li[i])})
