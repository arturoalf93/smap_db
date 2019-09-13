#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:09:41 2018

@author: arodriguez
"""

import mysql.connector
from mysql.connector import errorcode
import getpass

#pswd = getpass.getpass('Introduce Password:')

try:
  cnx = mysql.connector.connect(user='root', password='nomagichere',
                              host='127.0.0.1',
                              database='SolutionMaps')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    print("Successfully connected")
  #cnx.close()

cursor = cnx.cursor()

query = ("SELECT * FROM rfielements \
         ")

cursor.execute(query)

for (a, b, c, d ,e, f, g, h, i, j ,k ,l) in cursor:
    print(a,b,c,d,e,f,g)

cursor.close()
cnx.close()