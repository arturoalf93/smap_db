#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:08:23 2019

@author: arodriguez
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:06:11 2018

@author: Arturo
"""
# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST

import pandas as pd
import os

encoding = 'utf-8' #Mac
#encoding = 'cp1252' #Windows

SourceFolder = 'Finished tables'
DestinationFolder = 'insertSQLstatements'


def rowList(row, cols):
    rowList = []
    for c in cols:
        if pd.isnull(row[c]): rowList += ['NULL']
        elif type(row[c]) == int: rowList += ['"' + str(row[c]) + '"']
        elif type(row[c]) == float:
            if row[c].is_integer(): rowList += ['"' + str(int(row[c])) + '"']
            else: rowList += ['"' + str(row[c]) + '"']
        else: rowList += ['"' + str(row[c]).replace('"', '\\"').replace("'", "\\'").strip('\n') + '"']
    return rowList

test_data_path = os.path.join(os.getcwd(), SourceFolder)
sql_path = os.path.join(os.getcwd(), DestinationFolder)
files = os.listdir(test_data_path)

for f in files:
    #try:
    if f[0:4] == 'Icon': continue
    filename, ext = f.split('.')[0], f.split('.')[1]
    if ext != 'csv': print(f, 'NOT CSV FILE-----------')
    else:
        df = pd.read_csv(os.path.join(test_data_path, f), encoding=encoding)
        df = df.dropna(axis=0, how='all')
        if len(df.index) == 0: print(f, 'EMPTY------------')
        else:
            cols = list(df.columns)
            sql = 'INSERT IGNORE INTO ' + filename + ' (' + ', '.join(cols) + ') VALUES '
            for index, row in df.iterrows():
                sql += '(' + ', '.join(rowList(row, cols)) + '), '
            sql = sql[:-2]+';'
            fi = open(os.path.join(sql_path, filename + '.txt'),'w')
            fi.write(sql)
            fi.close()
            print(f + ' CREATED')
   # except: print(f + '!!!!! SPECIAL FILE--------------------')


#CREATE FILE WITH ALL THE INSERTS TOGETHER
#We need still need to define insert order
try: os.remove(os.path.join(sql_path, '0ALL_test.txt'))
except: pass

ordered = [ 'triggers_disabled_c',
            'current_quarteryear_c', 'rfi_participation_status', 'user_roles', 'log_codes',
           'vendors_c', 'users_c', 'users_h', 'current_quarteryear_h',
           'vendors_h', 'log_trail', 'modules_c', 'modules_h',
           'parent_categories_c', 'parent_categories_h', 'categories_c', 'categories_h', 'subcategories_c', 
           'subcategories_h', 'elements_c', 'elements_h', 'module_elements_c', 'module_elements_h',
           'rfi_vendors_analysts_h',
           'triggers_disabled_h' ]

""" LAST ORDER BEFORE Q2 19
ordered = ['suites', 'category_names', 'element_names',
           'suitemodules', 'suitemodcat', 'elementvariants', 'suitemodcatelem',
           'parentvendors', 'vendors', 'personas', 'users', 'rfi',
           'rfielements_providers', 'rfielements_analysts', 'vendors_rfi', 'current_quarteryear',
           'survey_references', 'refs_suitemods']

"""

""" LAST ORDER ALVARO DID
ordered = ['Suites', 'Categories', 'Subcategories', 'Elements', 'SuiteCategory',
           'SuiteCatSub', 'ElementVariants', 'SuiteCatSubElem', 'SuiteCatSubElem_version',
           'ParentVendors', 'Vendors', 'Personas', 'UserTypes', 'UserLogin', 'RFI',
           'RFIelements', 'Weights' ,'SMscores', 'Surveys', 'SurveyReferences',
           'SurveyQuestions', 'SurveyScores', 'SurveyRefSuiteCat', 'SurveyWeights']
"""
with open(os.path.join(sql_path, '0ALL_test.txt'),'w') as outfile:
    for fname in ordered:
        with open(os.path.join(sql_path, fname + '.txt')) as infile:
            outfile.write(infile.read() + '\n')
            print(fname, 'ADDED')
