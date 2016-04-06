import glob, os
import re, unicodedata
#import spell
import nltk.corpus
from nltk.stem import PorterStemmer

#numeric isolation
def numeric_isolation(x):
	return re.sub("[-+]?\d+[\.]?\d*",'',x)

#for words like don't, Adam's (Adam is)// We won't need is/not and would like to remove them
def special_case(x):
	x=re.sub(r"n't",' not',x)
        return re.sub(r"'",'',x)

#all punctuation marks removal
def punctuate_preproc(x):
	return re.sub(r"<(.*?)>|\n|(\\(.*?){)|}|[#!$%^&*()_+|~\^\-<>/={}\[\],:\";<>?,.\/\\]|[@]",' ', x)

#unicode normalisation
def unicode_normalisation(x):
	x = unicode(x, "utf-8")
	x = unicodedata.normalize('NFKD', x).encode('ascii','ignore')
	return x

#string lower
def string_lower(x):
	return x.lower()

#stemming
def stemming(x):
	port_stem = PorterStemmer()
	words=[]
	for word in x.split(' '):
		words.append(port_stem.stem(word))
	return ' '.join(words)

#stopwords
def stopwords(x):
	temp=[]
	stop=nltk.corpus.stopwords.words('english')
	x=re.findall(r"\b([a-zA-Z]+)\b", x)
	for i in x:
		if i not in stop:
			temp.append(i)
	return ' '.join(temp)

#will it be useful as it is more like a similarity check between the texts.
#def shingles(x):

#Spell Corrector. It works for each word, not whole text
'''def correct(x):
	line=re.findall(r"\b([a-zA-Z]+)\b", x)
	y=''
	for word in line:
		spell.correct(x)
		y=y+(spell.correct(word))+' '
	return y'''

def str_len_less(x):
	if len(x)<20:
		return ''
	else:
		return x

def word_len_less(x):
	line=re.findall(r"\b([a-zA-Z]+)\b", x)
	y=''
	for word in line:
		if len(word)<3:
			y=y+''
		else:
			y=y+word+' '
	return y

#only consider http and https not ftps			
def email_urls(x):
	x=re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b','',x)
	return re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:\'".,<>?]))', '', x)
	
#most steps need to be in specific order to achieve one
def process(x,*steps):
	for p in steps:
		x=p(x)
	return x
