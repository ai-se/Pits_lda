from __future__ import print_function, division

__author__ = 'amrit'
import copy
import numpy as np
import matplotlib.pyplot as plt

def calculate(topics=[], lis=[], count1=0):
    count=0
    for i in topics:
        if i in lis:
            count+=1
    if count>=count1:
        return count
    else:
        return 0

def recursion(topic=[], index=0, count1=0):
    count=0
    global data
    #print(data)
    #print(topics)
    d=copy.deepcopy(data)
    d.pop(index)
    for l,m in enumerate(d):
        #print(m)
        for x,y in enumerate(m):
            if calculate(topics=topic,lis=y,count1=count1) !=0 :
                count+=1
                break
                #data[index+l+1].pop(x)
    return count


if __name__ == '__main__':
    fileB = ['101pitsA_2.txt', '101pitsB_2.txt', '101pitsC_2.txt','101pitsD_2.txt','101pitsE_2.txt','101pitsF_2.txt']
    l = []
    labels=[5,6,7,8,9]

    file_data={}
    for file1 in fileB:
        l = []
        data=[]
        with open("../../results/04-11/"+file1, 'r') as f:
            for doc in f.readlines():
                l.append(doc.split())
            # print(len(l))
            for i in range(len(l)-11,-1,-11):
                 l.pop(i)
        for i in range (0,len(l),10):
            l1=[]
            for j in range(10):
                l1.append(l[i+j])
            data.append(l1)
        dic={}
        print(len(data))
        for x in labels:
            j_score=[]
            for i,j in enumerate(data):
                for l,m in enumerate(j):
                    sum=recursion(topic=m, index=i,count1=x)
                    if sum !=0:
                        j_score.append(sum/float(10))
                    '''for m,n in enumerate(l):
                        if n in j[]'''
            dic[x]=j_score
            if len(dic[x])==0:
                dic[x]=[0]
        file_data[file1]=dic
    #print(file_data)
    X=range(len(labels))
    plt.figure(num=0,figsize=(25,15))
    plt.subplot(121)
    for file1 in fileB:
        Y_median=[]
        Y_iqr=[]
        for feature in labels:
            Y=file_data[file1][feature]
            Y_median.append(np.median(Y))
            Y_iqr.append(np.percentile(Y,75)-np.percentile(Y,25))
        line,=plt.plot(X,Y_median,label="median_"+file1)
        plt.plot(X,Y_iqr,"-.",color=line.get_color(),label="iqr_"+file1)
    plt.xticks(X, labels,rotation=30)
    plt.ylabel("J score")
    plt.xlabel("Labels")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0.)
    plt.savefig("Combined"+".png")
