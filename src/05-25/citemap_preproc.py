import os
import re
import sys, traceback
from Preprocess import *
import Preprocess
import csv

path = '/media/amrit/Ddrive/Manny Dataset/trunkx'

fo = open('/Users/amrit/GITHUB/Pits_lda/dataset/nostem_citemap_v3.txt', 'a+')
with open('/Users/amrit/GITHUB/Pits_lda/dataset/citemap_v3.csv', 'r') as csvinput:
    reader = csv.DictReader(csvinput, delimiter='|')
    for row in reader:
        x= row['$Abstract'].split('$')[1]
        if x=='None':
            str= row['$Title$'].split('$')[1]
        else:
            str=x
        line = process(str, string_lower, email_urls, punctuate_preproc,
                                   numeric_isolation, stopwords, word_len_less, str_len_less)
        if len(line) > 1:
            fo.write(line)
            fo.write('\n')
fo.close()
