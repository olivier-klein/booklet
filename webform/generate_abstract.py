#!/usr/bin/python
# coding: utf-8

import os

for i in range(71):
    print i
    os.popen("./make_abstract.py "+str(i))
    # subprocess.Popen("./make_biblio.py "+str(i))
