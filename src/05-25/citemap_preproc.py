import os
import re
import sys, traceback
from Preprocess import *
import Preprocess
import csv

path = '/media/amrit/Ddrive/Manny Dataset/trunkx'

fo = open('/home/amrit/GITHUB/Pits_lda/dataset/processed_citemap.txt', 'a+')
with open('/home/amrit/GITHUB/Pits_lda/dataset/citemap.csv', 'r') as csvinput:
    reader = csv.DictReader(csvinput, delimiter='|')
    for row in reader:
        str= row['$Title$'] + row['$Abstract']
        line = process(str, string_lower, email_urls, unicode_normalisation, punctuate_preproc,
                                   numeric_isolation, stopwords, stemming, word_len_less, str_len_less)
        if len(line) > 1:
            fo.write(line)
            fo.write('\n')
fo.close()
