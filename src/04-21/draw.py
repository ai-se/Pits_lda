__author__ = 'amrit'

import matplotlib.pyplot as plt

#https://docs.google.com/a/ncsu.edu/spreadsheets/d/1kLAHoSQzf4QGEhlGBcpmkukMWpaTPsEeNSMl1kVIj2I/edit?usp=sharing

if __name__ == '__main__':
    fileB = ['101pitsA_2.txt', '101pitsB_2.txt', '101pitsC_2.txt', '101pitsD_2.txt', '101pitsE_2.txt', '101pitsF_2.txt']
    l = []
    file_data={'101pitsA_2.txt':{"tuned":[0.9, 0.6, 0.7, 0.4, 0.3],"untuned":[0.8,0.7,0.5,0.4,0.2] }, '101pitsB_2.txt':{"tuned":[0.9,0.9,0.8,0.8,0.55],"untuned":[0.7,0.7,0.6,0.6,0.4] },'101pitsC_2.txt':{"tuned":[0.9,0.9,0.9,0.9,0.9],"untuned":[0.9,0.7,0.6,0.5,0.4]},
               '101pitsD_2.txt':{"tuned":[1.0,0.9,0.9,0.9,0.8],"untuned":[0.9,0.8,0.8,0.8,0.7] },'101pitsE_2.txt':{"tuned":[0.9,0.9,0.7,0.5,0.65],"untuned":[0.8,0.8,0.7,0.5,0.4] },'101pitsF_2.txt':{"tuned":[0.9,0.9,0.6,0.6,0.5],"untuned":[0.8,0.8,0.7,0.55,0.4]}  }
    labels = [5, 6, 7, 8, 9]
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)
    X = range(len(labels))
    plt.figure(num=0, figsize=(25, 15))
    #plt.subplot(121)
    for file1 in fileB:
        Y_tuned=file_data[file1]["tuned"]
        Y_untuned=file_data[file1]["untuned"]
        line, = plt.plot(X, Y_tuned, marker='o', markersize=16, label="tuned_" + file1)
        plt.plot(X, Y_untuned, linestyle="-.", color=line.get_color(), marker='*', markersize=16, label="untuned_" + file1)
    plt.xticks(X, labels)
    plt.ylabel("Stable Measure")
    plt.xlabel("No of terms overlap")
    plt.legend(bbox_to_anchor=(0.95, 0.5), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("DE_tuned" + ".png")
