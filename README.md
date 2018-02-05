# Automatically manage a conference booklet using pyhton and LaTeX

This repository contains a tool suites in python / latex to manage a scientific conference automatically. It has been used to generate the booklet of the spin mechanics & nano-MRI workshop held at the École de Physique des Houches in Feb, 2018. 
http://houches.2018.neel.cnrs.fr/

The concept is as simple as  in one hand, 1) asking the participants to fill up themselves a database (file 'database.csv' managed by a google webform) containing all the informations concerning the speaker (name, affilitation etc..) and hist talk (tile, collaborators, figures etc.. even the bibliography is managed automatically through the exploitation of DOI), ii) while on the other hand, 2) the organizer manages solely the schedule through a timetable file (file 'program.txt').

The booklet compiles automatically, builds each abstracts, ranks them chronologically according to the timetable, creates different index tables.

