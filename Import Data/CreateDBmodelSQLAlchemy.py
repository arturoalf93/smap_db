# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 17:38:24 2018

@author: Arturo
"""

'''
0: Data Type
1: PK
2: FK
3: NN
4: UQ
5: BIN
6: UN
7: ZF
8: AI
9: Default
10: Comment
11[] When the table.column is a TargetTable and TargetColumn
'''

import codecs, os
from bs4 import BeautifulSoup
import sys

def FindTableIndex(MyTable):
    for auxi in range(0,NumberOfTables):
        if MyTable == SMAPschema[auxi]:
            break
        elif auxi == NumberOfTables - 1:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: TableIndex not found')
    return auxi

def FindColumnIndex(MyTableIndex, MyColumn):
    for auxj in range(0, NumberOfColumns[MyTableIndex]):
        if MyColumn == SMAPschema[MyTableIndex,auxj]:
            break
        if auxj == NumberOfColumns[MyTableIndex] - 1:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: ColumnIndex not found')
    return auxj

workbenchHTMLfile = 'SMAPdictionary'
folderName = 'ImportData_to_generate'
model = ''
NumberOfTables = 0
NumberOfColumns = []
#bs = BeautifulSoup(codecs.open(workbenchHTMLfile + ".html", 'r')) #if we don't put 'lxml' to specify that HTML parser it gives a warning
bs = BeautifulSoup(codecs.open(workbenchHTMLfile + ".html",'r'), 'lxml')
i = 0
j = 0
k = 0
l = 0
flag = 0
aux = 0
aux2 = 1
            
#Retrive SMAPschema from SMAPdictionary.html  
'''
UNIQUE column is not working in the MySQLWorkbench Script
Improve things later, when it works, like using SQLAlchemy Dialect MySQL for specific Data Types
'''
SMAPschema = {}
for table in bs.find_all('table'):
    SMAPschema[i] = table.caption.get_text()
    for ColumnName in table.find_all('td', {'class': 'field'}):
        SMAPschema[i,j] = ColumnName.text
        j += 1
    j = 0
    for row in table.find_all('tr'):
        if aux >= 2:
            for atrr in row.find_all('td'):
                if aux2 >= 1:
                    SMAPschema[i,j,k] = atrr.text
                    k += 1
                aux2 += 1
            k = 0
            j += 1
        aux2 = 0
        aux += 1
    aux = 0
    NumberOfColumns.append(j)
    j = 0
    i += 1
    NumberOfTables = i
i = 0

#Change data types to what SQLAlchemy understands. 
#Also change PK from &#10004 (html code for a tick) to 1
for i in range(0,NumberOfTables):
    for j in range(0, NumberOfColumns[i]):
        #DataTypes
        if SMAPschema[i,j,0][:3] == 'INT':
            SMAPschema[i,j,0] = 'Integer'
        elif SMAPschema[i,j,0][:7] == 'VARCHAR':
            SMAPschema[i,j,0] = 'String' + SMAPschema[i,j,0][7:]
        elif SMAPschema[i,j,0] == 'DATETIME':
            SMAPschema[i,j,0] = 'DateTime'
        elif SMAPschema[i,j,0][:7] == 'DECIMAL':
            #scale = SMAPschema[i,j,0].split('('))[1].split(':')[0]
            #scale = re.search('((.*):')
            scale = SMAPschema[i,j,0][SMAPschema[i,j,0].find('(')+len('('):SMAPschema[i,j,0].find(',')]
            precision = SMAPschema[i,j,0][SMAPschema[i,j,0].find(',')+len(','):SMAPschema[i,j,0].find(')')]
            SMAPschema[i,j,0] = 'Numeric(' + scale + ',' + precision + ')' #CHECK IF THIS NEEDS THE DIALECT. IF NOT, WE CAN DO NUMERIC(SCALE = , PRECISION = )
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Data Type not found in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
        #Primary Key
        if SMAPschema[i,j,1] == '✔':
            SMAPschema[i,j,1] = 1
        elif SMAPschema[i,j,1] == u'\xa0': #this is the unicode for a &nbsp, which is html for a non-breaking space
            SMAPschema[i,j,1] = 0
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Something wrong with the Primary Key in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
         #Foreign Key
        if SMAPschema[i,j,2] == '✔':
            SMAPschema[i,j,2] = 1
            if SMAPschema[i,j,10][:3] == 'fk*':
                TargetTable = SMAPschema[i,j,10].split()[0][3:SMAPschema[i,j,10].split()[0].find('.')]
                TargetColumn = SMAPschema[i,j,10].split()[0][SMAPschema[i,j,10].split()[0].find('.')+len('.'):]
                TargetTableIndex = FindTableIndex(TargetTable)
                TargetColumnIndex = FindColumnIndex(TargetTableIndex,TargetColumn)
                print(TargetTableIndex, TargetColumnIndex)
                l = 0
                flag = 0
                while flag == 0:
                    try:
                        SMAPschema[TargetTableIndex,TargetColumnIndex,11,l]
                        if SMAPschema[TargetTableIndex,TargetColumnIndex,11,l] == SMAPschema[i]:
                            #sys.exit('CUSTOM ERROR DEINDED BY ARTURO: TargetTable already exists') this gave error when survey_references was referenced twice to vendors
                            print('WARNING : CUSTOM ERROR DEINDED BY ARTURO: TargetTable already exists')
                            break #NOT SURE IF THIS WORKS 100%. I PUT THIS IN ORDER TO SOLVE THE PROBLEM WHEN ONE TABLE HAD TWO FOREIGNS KEYS FOR THE SAME TABLE (SURVEY_REFERENCES TO VENDORS)
                        l += 1
                    except KeyError:
                        SMAPschema[TargetTableIndex,TargetColumnIndex,11,l] = SMAPschema[i]
                        flag = 1
                l = 0
                flag = 0          
        elif SMAPschema[i,j,2] == u'\xa0': #this is the unicode for a &nbsp, which is html for a non-breaking space
            SMAPschema[i,j,2] = 0
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Something wrong with the Foreign Key in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
        #Not Null
        if SMAPschema[i,j,3] == '✔':
            SMAPschema[i,j,3] = 1
        elif SMAPschema[i,j,3] == u'\xa0': #this is the unicode for a &nbsp, which is html for a non-breaking space
            SMAPschema[i,j,3] = 0
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Something wrong with the Not Null in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
        #Unique
        if SMAPschema[i,j,4] == '✔':
            SMAPschema[i,j,4] = 1
        elif SMAPschema[i,j,4] == u'\xa0': #this is the unicode for a &nbsp, which is html for a non-breaking space
            SMAPschema[i,j,4] = 0
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Something wrong with the UNIQUE in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
        #Auto Increment
        if SMAPschema[i,j,8] == '✔':
            SMAPschema[i,j,8] = 1
        elif SMAPschema[i,j,8] == u'\xa0': #this is the unicode for a &nbsp, which is html for a non-breaking space
            SMAPschema[i,j,8] = 0
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Something wrong with the AutoIncrement in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
        #Check Deault is either CURRENT_TIMESTAMP or Blank
        if SMAPschema[i,j,9] == 'CURRENT_TIMESTAMP' or SMAPschema[i,j,9] == '':
            pass
        else:
            sys.exit('CUSTOM ERROR DEFINED BY ARTURO: Something wrong with DEFAULT in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
        #__repr__ and onupdate
        if SMAPschema[i,j,10][:5] == 'repr*':
            SMAPschema[i,j,12] = 1
            print('repr* found in ' + SMAPschema[i])
        else:
            SMAPschema[i,j,12] = 0
        if SMAPschema[i,j,10][:9] == 'onupdate*':
            SMAPschema[i,j,13] = 1
            print('onupdate* found in ' + SMAPschema[i])
        else: SMAPschema[i,j,13] = 0
            

            
'''
http://docs.sqlalchemy.org/en/latest/core/type_basics.html

Note:
The Float type is designed to receive data from a database type that is explicitly 
known to be a floating point type (e.g. FLOAT, REAL, others) and not a decimal type 
(e.g. DECIMAL, NUMERIC, others). If the database column on the server is in fact a 
Numeric type, such as DECIMAL or NUMERIC, use the Numeric type or a subclass, 
otherwise numeric coercion between float/Decimal may or may not function as expected.

Note:
The Numeric type is designed to receive data from a database type that is explicitly
known to be a decimal type (e.g. DECIMAL, NUMERIC, others) and not a floating point
type (e.g. FLOAT, REAL, others). If the database column on the server is in fact a
floating-point type type, such as FLOAT or REAL, use the Float type or a subclass,
otherwise numeric coercion between float/Decimal may or may not function as expected.

class sqlalchemy.types.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True)¶
'''
        

        
#Create the text variable that contains the model
for i in range(0,NumberOfTables):
    if SMAPschema[i].lower() == SMAPschema[i]: #now, only lowercase tables from dictionary
        model += 'class ' + SMAPschema[i] + '(db.Model):\n'
        #for column in table.find_all('td', {'class': 'field'}):
        repr_flag = 0
        for j in range(0,NumberOfColumns[i]):
            model += '\t' + SMAPschema[i,j] + ' = db.Column(db.' + SMAPschema[i,j,0]
            if SMAPschema[i,j,2] == 1 and SMAPschema[i,j,10][:3] == 'fk*': #apparently the FK must be defined at the start, after the DataType
                model += ", db.ForeignKey('" + SMAPschema[i,j,10].split()[0][3:] + "')" #space as default delimiter, if we don't specify it
            if SMAPschema[i,j,1] == 1:
                model += ', primary_key = True'
            if SMAPschema[i,j,3] == 1:
                model += ', nullable = False' #It's the opposite. In the HTML dictionary and variable it is Not Null = 1, while in the ORM it is not nullable = False
            if SMAPschema[i,j,4] == 1:
                model += ', unique = True'
            if SMAPschema[i,j,8] == 1:
                model += ', autoincrement = True'
            elif SMAPschema[i,j,8] == 0:
                model += ', autoincrement = False'
            else:
                sys.exit('CUSTOM ERROR DEFINED BY ARTURO: AutoIncrement different than 0 and 1 in table: ' + SMAPschema[i] + ', column: ' + SMAPschema[i,j])
            if SMAPschema[i,j,9] == 'CURRENT_TIMESTAMP':
                model += ', default = datetime.datetime.now'
            if SMAPschema[i,j,13] == 1:
                model += ', onupdate = datetime.datetime.now'
            model += ')\n'
            flag = 0
            l = 0
            while flag == 0:
                try:
                    SMAPschema[i,j,11,l]
                    model += '\t' + SMAPschema[i,j,11,l] + " = db.relationship('" + SMAPschema[i,j,11,l] + "', backref = '" + SMAPschema[i] + "')\n"
                    l += 1
                except KeyError:
                    flag = 1
            l = 0
            flag = 0
            
            if SMAPschema[i,j,12] == 1:
                repr_flag = 1
                repr_column = SMAPschema[i,j]

        model += '\n'
        
        if repr_flag == 1:
            model += '\t' + 'def __repr__ (self):\n'
            model += '\t\t' + 'return self.' + repr_column + '\n'
            model += '\n'
        

try: os.remove('DBmodelSQLAlchemy.txt')
except: pass

fi = open(os.path.join(os.getcwd(),'DBmodelSQLAlchemy.txt'), 'w')
fi.write(model)
fi.close()



