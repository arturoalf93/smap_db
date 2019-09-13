# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 13:18:24 2018

@author: Alvaro
"""

workbenchHTMLfile = 'SMAPdictionary'
folderName = 'ImportData_to_generate'

import codecs,csv,os
from bs4 import BeautifulSoup

bs = BeautifulSoup(codecs.open(workbenchHTMLfile + ".html", 'r'))

SMAPschema = {}
for table in bs.find_all('table'):
    for caption in table.find_all('caption'):
        cap = caption.text
        SMAPschema[cap] = []
        print(caption.text)
        for column in table.find_all('td', {'class': 'field'}):
            print(column.text)
            SMAPschema[cap] += [column.text]
            
for table in SMAPschema:
    with open(str(os.getcwd() + '/' + folderName + '/' + table + '.csv'), 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(SMAPschema[table])
        print(table + '.csv CREATED')