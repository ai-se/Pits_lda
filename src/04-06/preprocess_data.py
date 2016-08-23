import glob, os
import re
import pdb
import sys, traceback
from Preprocess import *
import Preprocess
from demos import atom
from demos import cmd


def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def _test(res=''):
    path = 'share/aagrawa8/Data/SO/'
    path1 = 'share/aagrawa8/Data/process/'
    for root, dirs, files in os.walk(path+str(res)+'/', topdown=False):
        for name in files:
            a = os.path.join(root, name)
        ##manual change needed
            reg = a.split('/')[5]
            print a
            # pdb.set_trace()
            fo=open(path1+reg,'a+')
            if (reg):
                # waste='Results/Enron/Without_Stem/'+file1+'.txt

                with open(a, 'r') as content_file:
                    for doc in content_file.readlines():
                        line = process(doc, string_lower, email_urls, unicode_normalisation, punctuate_preproc,
                                       numeric_isolation, stopwords, stemming, word_len_less)
                        if len(line) > 1:
                            fo.write(line)
                            fo.write('\n')
            fo.close()


if __name__ == '__main__':
    eval(cmd())
