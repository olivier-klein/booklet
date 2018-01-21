#!/usr/bin/python
# coding: utf-8

import sys, getopt
import csv
import arxiv2bib as a2b
from numpy import *
import sys
import string
from urllib2 import HTTPError
import codecs

# http://bibtexparser.readthedocs.io/en/v0.6.2/tutorial.html
N=int(sys.argv[1:][0])
# N=7

alphabet=list(string.ascii_lowercase)

def doi2bib(doi):
    # https://github.com/fxcoudert/citedoi/blob/master/doihelper.py
    import requests
    """
    Return a bibTeX string of metadata for a given DOI.
    """
    url = "http://dx.doi.org/" + doi
    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers = headers)
    return r.text

# parse biblio
# 0  Horodateur,
# 1  "Abstract title",
# 2  Contribution,
# 3  "Abstract text",
# 4  "Abstract bibliography",
# 5  Figure,
# 6  "Presenting author:  Family name",
# 7  "Presenting author: First name",
# 8  "Presenting author: E-mail",
# 9  "Presenting author: Institution",
# 10 "Presenting author: Address",
# 11 "Presenting author: Country",
# 12 "Dietary Restrictions",
# 13 "Co-authors 1 list with common affiliation.",
# 14 "Affiliation 1: institution, address, country",
# 15 "Co-authors 2 list with common affiliation.",
# 16 "Affiliation 2: institution,  address, country",
# 17 "Co-authors list with common affiliation.",
# 18 "Affiliation 3: institution, address, country"

# bibtex parser


filename='database.csv'
my_db_file = open(filename,"rb")
my_db = csv.reader(my_db_file, delimiter=',',skipinitialspace=True)
my_db.next()

for i in range(N):
    my_db.next()

row=my_db.next()

name = row[6]; name=name.replace(' ','_'); name = name.replace('é','e')
abstract = row[3]
abstract=abstract.replace('‘',"'")
abstract=abstract.replace('’',"'")
abstract=abstract.replace('–',"$-$")
abstract=abstract.replace('µ',"$\mu$")

texfile=open('../abstracts/body/'+name+'.tex','w')
texfile.write(abstract)
texfile.close()

bib=row[4]

biblist=bib.split('\n')
for i,j in enumerate(biblist):
    j=j.rstrip()
    j=j.lstrip()
    biblist[i]=j
old_bibkey=ones_like(biblist)
new_bibkey=ones_like(biblist); new_bibkey=list(new_bibkey)
doi       =ones_like(biblist)
print bib
j=0
bibfile=codecs.open('../biblio/'+name+'.bib','w','utf-8')
if len(bib)==0:
    bibfile.close()
# bibfile=open('../biblio/'+name+'.bib','w')
for i,ref in enumerate(biblist):
    old_bibkey[i]=ref[ref.find("[")+1:ref.find("]")]
    doi[i]=ref.split(' ')[-1]
    doi[i]=doi[i].replace('https://doi.org/', '')
    doi[i]=doi[i].replace('https://journals.aps.org/prb/abstract/', '')
    if doi[i][:5]=='arXiv':
        try:
            out=a2b.arxiv2bib([doi[i].split(':')[-1]])
            bibitem=out[0].bibtex()
        except urllib2.HTTPError:
            bibitem=''
    else:
        try:
            print 'searching DOI:',doi[i]
            bibitem=doi2bib(doi[i])
        except urllib2.HTTPError:
            bibitem=''
    y, z = bibitem.split(",", 1)
    x, key = y.split("{", 1)
    if key in new_bibkey:
        new_bibkey[i]=key+alphabet[j]
        j+=1
        bibitem=bibitem.replace(key,new_bibkey[i])
    else:
        new_bibkey[i]=key
    print 'bibkey=', new_bibkey[i]
    bibfile.write(bibitem)
    bibfile.write('\n')
bibfile.close()

i=0
bibkeys=[]
Nbrs=abstract.count('\cite')
for j in range(Nbrs):
    i=abstract.find("\cite{",i)
    k=abstract.find("}",i)
    cite=abstract[i+6:k]
    bibkeys.append(cite)
    i=k+2
    # print abstract[k-6:k+1]

new_bibkeys=list(ones_like(bibkeys))
old_bibkey=list(old_bibkey)
for i,keys in enumerate(bibkeys):
    key=keys.split(',')
    for j,k in enumerate(key):
        key[j]=new_bibkey[old_bibkey.index(k)]
        # print key[j]
    new_bibkeys[i]=','.join(key)

for i in range(Nbrs):
    old_quote='\cite{'+bibkeys[i]+'}'
    new_quote='\cite{'+new_bibkeys[i]+'}'
    abstract=abstract.replace(old_quote,new_quote)

texfile=open('../abstracts/body/'+name+'.tex','w')
texfile.write(abstract)
texfile.close()
