# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:42:03 2018

@author: Arturo
"""

import csv, os
import pandas as pd
    
# Take file WORKFILE and get a sorted list of UNIQUE ELEMENTS in the first row
# Folder: "ImportData work"

def sortedUnique(workfile):
    with open(os.getcwd() + "/ImportData work/" + workfile + ".csv") as myfile:
        reader = csv.reader(myfile)
        mylist = []
        for row in reader: mylist += [row[0]]
        uniquelist = sorted(list(set(mylist)))
        
    doc = "\n".join(uniquelist)
    with open(os.getcwd() + "/ImportData work/" + workfile + "Unique.csv", 'w') as myfile:
        myfile.write(doc)

sortedUnique('elements')





'''
data = pd.read_csv(os.getcwd() + "/ImportData work/" + workfile + '.csv', header = None)
with open(os.getcwd() + "/ImportData provisional/" + table + '.csv', mode='r') as infile:
    tablesDict[table] = {}
    reader = csv.reader(infile)
    columns = next(reader)  # gets the first line
    for row in reader:
        tablesDict[table]
    tablesDict[table] = {rows[0]:rows[1] for rows in reader}
    
    str_list = [l.split('-') for l in str.split('.')]
    
    '''