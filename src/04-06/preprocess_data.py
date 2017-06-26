import pandas as pd

from Preprocess import *
from demos import cmd


def _test(res=''):
    # print res
    path = '/share/aagrawa8/Data/Pits/' + res
    path1 = '/share/aagrawa8/Data/process/'
    fo = open(path1 + res.split('.')[0]+'.txt', 'w')
    data = pd.read_csv(path)
    data['Description'] = data['Description'].apply(lambda x: str(x) + ' ')
    data['text'] = data['Description'] + data['Subject']
    li = data['text'].tolist()
    for doc in li:
        line = process(doc, string_lower, unicode_normalisation, punctuate_preproc,
                       numeric_isolation, stopwords, stemming, word_len_less)
        if len(line) > 1:
            fo.write(line)
            fo.write('\n')
    fo.close()


if __name__ == '__main__':
    eval(cmd())
