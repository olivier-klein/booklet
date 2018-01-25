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


ScheduleName='program'
my_db_file = open(ScheduleName+'.txt','rb')
my_db = csv.reader(my_db_file, delimiter='\t',skipinitialspace=True)
my_db.next()

code     = empty([N],dtype=object)
talk     = empty([N],dtype=object)
days     = empty([N],dtype=object)
begin    = empty([N],dtype=object)
end      = empty([N],dtype=object)
label    = empty([N],dtype=object)
speaker  = empty([N],dtype=object)

i=0
for row in my_db :
    if len(row) > 0:
        code[i]     = str(row[0])
        talk[i]     = str(row[1])
        days[i]     = str(row[2])
        begin[i]    = str(row[3])
        end[i]      = str(row[4])
        label[i]    = str(row[5])
        speaker[i]  ='_'.join(label[i].rsplit()[1:])
        i+=1

# days     = days.astype(int)
N=70  # number of talks
# N=42  # number of talks
code     = code[:N]
talk     = talk[:N]
days     = days[:N].astype(int)
begin    = begin[:N]
end      = end[:N]
label    = label[:N]
speaker  = speaker[:N]

Talk='''\\begin{talk}
{%(Begin)s}
{%(End)s}
{%(Code)s}
{%(Contrib)s}
{%(Title)s}
{%(FullName)s}
{%(Address)s}
\\end{talk}

'''
Break='''\\begin{confbreak}
{%(Begin)s}
{%(End)s}
{%(Contrib)s}
\\end{confbreak}

'''

# Stamp = '''%(Contrib)s \\\ \n%(Day)s \\\ \n%(Begin)s-%(End)s '''
Stamp = '''%(Contrib)s. %(Code)s \\\ \n%(Day)s \\\ \n%(Begin)s'''

Abstract = '''\\begin{refsection}
\\input{abstracts/%(Name)s}
\\end{refsection}
'''

week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

# for day in range(5):

absfilename='talks_abstract.tex'
try:
    os.remove(absfilename)
except OSError:
    pass
abslist=open(absfilename,'a')

for day in range(5):
    cut = (days==day+2)
    index=begin[cut].argsort()
    filename=week[day]+'.tex'
    absfilename='talks_abstract.tex'
    print filename
    try:
        os.remove(filename)
    except OSError:
        pass
    texfile=open(filename,'a')
    for i in index:
        talk_beg  = begin[cut][i]; start=talk_beg[:2]+':'+talk_beg[-2:]
        talk_end  = end[cut][i]  ; finsh=talk_end[:2]+':'+talk_end[-2:]
        talkcode  = code[cut][i]
        talktype  = talk[cut][i]
        flag = 0
        if talktype == 'tut':
            talktype = 'Tutorial'; flag=1
        elif talktype == 'invited':
            talktype = 'Invited Talk'; flag=1
        elif talktype == 'break':
            talktype = 'Nutrition Break'
        else:
            talktype = label[cut][i]
        if flag :
            if start == '08:30':
                texfile.write('\\input{schedule/titles/'+week[day]+'1} \n\n')
            elif start == '17:15':
                texfile.write('\\input{schedule/titles/'+week[day]+'2} \n\n')
            elif start == '20:00':
                texfile.write('\\input{schedule/titles/'+week[day]+'3} \n\n')
            pointer   =  where(name==speaker[cut][i])[0][0]
            thetitle  = title[pointer]
            fullname  = firstname[pointer]+' '+lastname[pointer]
            fulladdr  = instit[pointer]+', '+address[pointer]+\
                        ', '+country[pointer]
            texfile.write(Talk %{"Begin" : start, "End" : finsh,
                                 "Code": talkcode, "Contrib": talktype,
                                 "Title" : thetitle, "FullName" : fullname,
                                 "Address" : fulladdr
                             })
            abslist.write(Abstract %{"Name" : speaker[cut][i]})
            stampfile='../stamps/'+speaker[cut][i]+'.tex'
            stamp =  open(stampfile,'w')
            stamp.write(Stamp %{ "Contrib": talktype[:3],"Code": talkcode,
                                 "Day": week[day],
                                 "Begin" : start, "End" : finsh})
            stamp.close()
        else:
            texfile.write(Break %{"Begin" : start, "End" : finsh,
                                 "Contrib": talktype
                             })
    texfile.close()

abslist.close()
