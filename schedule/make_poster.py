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
import os as os

filename='database.csv'
my_db_file = open(filename,"rb")
my_db = csv.reader(my_db_file, delimiter=',',skipinitialspace=True)
my_db.next()

N=73 # number of participants

title     = empty([N],dtype=object)
contrib   = empty([N],dtype=object)
caption   = empty([N],dtype=object)
lastname  = empty([N],dtype=object)
name      = empty([N],dtype=object)
firstname = empty([N],dtype=object)
email     = empty([N],dtype=object)
instit    = empty([N],dtype=object)
address   = empty([N],dtype=object)
country   = empty([N],dtype=object)

for i in range(N):
    row=my_db.next()
    title[i]     = row[ 1]
    contrib[i]   = row[ 2]
    caption[i]   = row[ 5]
    lastname[i]  = row[ 6]
    name[i]=lastname[i].replace(' ','_'); name[i] = name[i].replace('é','e')
    firstname[i] = row[ 7]
    email[i]     = row[ 8]
    instit[i]    = row[ 9]
    address[i]   = row[10]
    country[i]   = row[11]


cut = (contrib=="Poster") + (contrib == "Contributed talk (20')")

# Stamp = '''%(Contrib)s \\\ \n%(Day)s \\\ \n%(Begin)s-%(End)s '''
Stamp = '''%(Contrib)s \\\ \n%(Day)s \\\ \n%(Begin)s'''

Abstract = '''\\begin{refsection}
\\input{abstracts/%(Name)s}
\\end{refsection}
'''

week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

# for day in range(5):

absfilename='posters_abstract.tex'
try:
    os.remove(absfilename)
except OSError:
    pass
abslist=open(absfilename,'a')

N=sum(cut)

for i,pointer in enumerate(where(cut==True)[0]):
    if i < sum(cut)/2:
        day=0
        talktype = 'Post 1'
    else:
        day=1
        talktype = 'Post 2'
    start='20:00'; finsh='22:00'
    abslist.write(Abstract %{"Name" : name[cut][i]})
    stampfile='../stamps/'+name[cut][i]+'.tex'
    stamp =  open(stampfile,'w')
    stamp.write(Stamp %{ "Contrib": talktype,
                         "Day": week[day],
                         "Begin" : start, "End" : finsh})
    stamp.close()

abslist.close()
