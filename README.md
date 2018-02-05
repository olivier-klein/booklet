# Tools suite to manage automatically a conference booklet with pyhton and LaTeX

This repository contains a tool suite in python / latex to manage a scientific conference automatically. It has been used to generate the booklet of the "spin mechanics & nano-MRI workshop" held at the École de Physique des Houches in Feb, 2018. 
http://houches.2018.neel.cnrs.fr/

The concept is as simple as  1) on one hand, asking the participants to fill up themselves a  database (file 'database.csv', a coma separated value file managed by google webform) containing all the informations concerning the speaker (name, affilitation etc..) and hist talk (tile, collaborators, abstract, figures etc.. even the bibliography is managed automatically through the exploitation of DOI), while 2) on the other hand, the organizer fills up the program through a timetable file (file 'program.txt').

The booklet compiles automatically, creates a timetable, builds the abstracts, ranks them chronologically according to the schedule, creates different index tables. The solution offers great flexibility in the management of the event.

Objective of the next release: provides automatic feedback about the compilation of the abstract. 
