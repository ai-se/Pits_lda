import os
import re
import sys, traceback
from Preprocess import *
import Preprocess

path = '/media/amrit/Ddrive/Manny Dataset/trunkx'

fo = open('/home/amrit/GITHUB/Pits_lda/dataset/dataset_SO.txt', 'a+')
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        a = os.path.join(root, name)
        ##manual change needed
        reg = a.split('/')[5]
        print a
        # pdb.set_trace()
        if (reg):
            with open(a, 'r') as content_file:
                for doc in content_file.readlines():
                    line = process(doc, string_lower, email_urls, unicode_normalisation, punctuate_preproc,
                                   numeric_isolation, stopwords, stemming, word_len_less, str_len_less)
                    if len(line) > 1:
                        fo.write(line)
                        fo.write('\n')
fo.close()