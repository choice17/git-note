# -*- coding: utf-8 -*-

import os
import sqlite3

#%%
conn = sqlite3.connect('test.db')
conn.execute('''CREATE TABLE COMPANY
             (ID INT PRIMARY KEY   NOT NULL,
             NAME            TEXT  NOT NULL,
             AGE             INT   NOT NULL,
             ADDRESS         CHAR(50),
             SALARY          REAL);''')
print("table  created successfully")
conn.close()

#%%
conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
     
conn.commit()
print("Records created successfully")
conn.close()
#%%
conn = sqlite3.connect('test.db')
conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS) \
      VALUES (5, 'Ann', 32, 'California' )");
conn.commit()
conn.close()
#%%
conn = sqlite3.connect('test.db')
print("Opened database successfully")

cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
for row in cursor:
   print("ID = ", row[0])
   print( "NAME = ", row[1])
   print( "ADDRESS = ", row[2])
   print( "SALARY = ", row[3], "\n")

print("Operation done successfully")
conn.close()

#%%
conn = sqlite3.connect('test.db')
exe_command = "CREATE TABLE DEPARTMENT( \
   ID INT PRIMARY KEY      NOT NULL, \
   DEPT           CHAR(50) NOT NULL, \
   EMP_ID         INT      NOT NULL \
)"
conn.execute(exe_command)
conn.execute( " \
INSERT INTO DEPARTMENT (ID, DEPT, EMP_ID) \
VALUES (1, 'IT Billing', 1 );")

conn.execute( " \
INSERT INTO DEPARTMENT (ID, DEPT, EMP_ID) \
VALUES (2, 'Engineering', 2 );")

conn.execute( " \
INSERT INTO DEPARTMENT (ID, DEPT, EMP_ID) \
VALUES (3, 'Finance', 7 );")

conn.commit()
conn.close()
#%% cross join
conn = sqlite3.connect('test.db')
cursor = conn.execute("SELECT EMP_ID, NAME, DEPT FROM COMPANY CROSS JOIN DEPARTMENT;")
for row in cursor:
    print(row)

conn.close()
#%% inner join
conn = sqlite3.connect('test.db')
cursor = conn.execute("SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT ON COMPANY.ID = DEPARTMENT.EMP_ID;")
for row in cursor:
    print(row)
conn.close()
#%% Outer join
conn = sqlite3.connect('test.db')
cursor = conn.execute("SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT \
        ON COMPANY.ID = DEPARTMENT.EMP_ID;")
for row in cursor:
    print(row)
conn.close()
#%% list tables
conn = sqlite3.connect('test.db')
cursor = conn.execute("select name from sqlite_master where type = 'table';")
for row in cursor:
    print(row)
conn.close()
#%% check table definition
conn = sqlite3.connect('test.db')
cursor = conn.execute("# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name1, nf=new_field, ft=field_type))

#%% Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("select name from sqlite_master where type = 'table';")
list_table = c.fetchall()
print(list_table)
c.execute('PRAGMA TABLE_INFO({})'.format(list_table[1][0]))
#for row in cursor:
#    print(row)
print([(tup[1],tup[2]) for tup in c.fetchall()])
conn.close()
#%%

