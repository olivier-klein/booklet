#!/usr/bin/python
import subprocess
import os
import parse_schedule as parse

ScheduleName='program'
parse.txt_2_tex(ScheduleName)
subprocess.Popen(['pdflatex','schedule.tex'],shell=False)
