# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 13:58:14 2018

@author: Arturo
"""

import pandas as pd
import os
import numpy as np
df = pd.read_excel(os.getcwd() + '\elements_copy.xlsm', sheet_name = 'SuiteCatSubElem_Version')
print(df.head(10))

df.shape
df.dtypes

for i in df.dtypes: print(i)
df.columns

df = df[np.isfinite(df['ElementID'])]

for col in df.columns:
    if df[col].dtype == 'float64':
        try:
            df[col] = df[col].fillna(-1).astype(int)
        except: continue
    elif df[col].dtype == 'object': 
        try:
            df[col] = df[col].fillna('')
        except: continue
df.dtypes

varSpec = {}
equals = []
diffs = {}
for index, row in df.iterrows():
    if row['VariantID'] in varSpec:
        if row['Specification'] == varSpec[row['VariantID']]['Specification'] and \
            row['ExampleScoring'] == varSpec[row['VariantID']]['ExampleScoring']:
            equals += [row['scseID']]
        else:
            diffs[row['scseID']] = {}
            diffs[row['scseID']]['Spec'] = row['Specification']
            diffs[row['scseID']]['OldSpec'] = varSpec[row['VariantID']]['Specification']
            diffs[row['scseID']]['Scoring'] = row['Specification']
            diffs[row['scseID']]['OldScoring'] = varSpec[row['VariantID']]['ExampleScoring']
            diffs[row['scseID']]['VariantID'] = row['VariantID']
    else:
        varSpec[row['VariantID']] = {}
        varSpec[row['VariantID']]['Specification'] = row['Specification']
        varSpec[row['VariantID']]['ExampleScoring'] = row['ExampleScoring']

print(diffs.keys())