import os, re


os.getcwd()
os.chdir()
file=open('mbox.txt')
for line in file:
    line=line.rstrip()
    if re.search('^From:',line):
        print(line)