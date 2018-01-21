#!/usr/bin/python
# coding: utf-8

import sys, getopt
import csv
import arxiv2bib as a2b

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

N=int(sys.argv[1:][0])
# N=7

filename='database.csv'
my_db_file = open(filename,"rb")
my_db = csv.reader(my_db_file, delimiter=',',skipinitialspace=True)
my_db.next()

for i in range(N):
    my_db.next()

row=my_db.next()

title     = row[ 1]
contrib   = row[ 2]
caption   = row[ 5]
lastname  = row[ 6]
name=lastname.replace(' ','_'); name = name.replace('é','e')
firstname = row[ 7]
email     = row[ 8]
instit    = row[ 9]
address   = row[10]
country   = row[11]
coauth1   = row[13]; strs=coauth1
count=strs.count(" and ")-1; strs=strs.replace(' and ',', ',count)
coauth1 = strs
affil1    = row[14]
coauth2   = row[15]; strs=coauth2
count=strs.count(" and ")-1; strs=strs.replace(' and ',', ',count)
coauth3 = strs
affil2    = row[16]
coauth3   = row[17]; strs=coauth3
count=strs.count(" and ")-1; strs=strs.replace(' and ',', ',count)
coauth3 = strs
affil3    = row[18]

Abstract = '''\\begin{conf-abstract}[\\input{stamps/%(Name)s}]
{%(Title)s}
{\\color{blue} %(FullName)s}
{%(Email)s}
{%(Address)s}
{%(Collabo)s}
\indexauthors{%(LastName)s!%(FirstName)s}

\\input{abstracts/body/%(Name)s}

\\input{figs/%(Name)s}

\\printbibliography[heading=none]

\\end{conf-abstract}
'''

Figure = '''\\setcounter{figure}{0}
\\begin{figure}[h]
  \\centering
  \\includegraphics[height=5.5cm,width=0.95 \\textwidth,keepaspectratio]{figs/%(Name)s}
  \\caption{(Color online) %(Caption)s}
\\end{figure}
'''

Stamp = '''%(Contrib)s\\\ \nDay \\\ \nXX:XX am'''

fullname = firstname+' '+lastname
affiliat = instit+', '+address+', '+country
collabo=''
if coauth1 != '':
    collabo='{\\color{blue}'+coauth1+'}\\\ \\textit{'+affil1+'}\\\ \n'
    if coauth2 != '':
        collabo=collabo+'{\\color{blue}'+coauth2+'}\\\ \\textit{ '+affil2+'}\\\ \n'
        if coauth3 != '':
            collabo=collabo+'{\\color{blue}'+coauth3+'}\\\ \\textit{'+affil3+'}\\\ \n'
collabo=collabo+'\\decofourleft \\decofourright'


texfile=open('../abstracts/'+name+'.tex','w')
texfile.write(Abstract %{"Name" : name, "FullName" : fullname,
                         "FirstName": firstname, "LastName": lastname,
                         "Title" : title, "Email" : email,
                         "Address" : affiliat, "Collabo" : collabo
                     })
texfile.close()

texfile=open('../figs/'+name+'.tex','w')
if caption != '':
    texfile.write(Figure %{"Name" : name, "Caption" : caption})
else:
    texfile.write('')
texfile.close()

# add stamp
contrib_short=['Tutor','Invit','Contr','Poste','Atten','Waiti']
contrib_type=['Tutorial','Invited Talk','Pending','Poster','Attendee','']
contrib_stamp=contrib_type[contrib_short.index(row[2][:5])]
texfile=open('../stamps/'+name+'.tex','w')
texfile.write(Stamp %{"Contrib" : contrib_stamp})
texfile.close()

###### add biblio
# texfile=open('../addbiblio.tex','a')
# texfile.write('\\addbibresource{biblio/'+name+'.bib} %'+str(N)+'\n')
# texfile.close()

# for i in range(N):
#     row=my_db.next()
#     # print row[2]
#     print contrib_type[contrib_short.index(row[2][:5])]
