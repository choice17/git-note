# SQL on python

## sqlite3  

which is easy in python, for installation  
`pip install sqlite3`   
it helps, and take a look into experiment in [python sqlite example](./sqlite3_python.py)

for working in python environment, we can always do sql by calling `execute`
* command table  
connect/create database
```python
conn = sqlite3.connect('test.db') 
```
execute on sql bd
```python
conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");
```
commit    
```python
conn.commit()
```
close 
```python
conn.close()
```
cursor, fetch  to obtain data to numpy/tuple
```python
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
```

## SQL command  

* command menu table [sqlite tutorial](http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html)
```python
select (distinct) * <from> A where B in (select C from D) 
```
> from  
> where  
> and or not <>  
> order by  
> insert into  
> update  
> delete  
> top  
> min  
> max  
> count  
> avg  
> sum  
> like  
> [wildcards](#wildcards)



### wildcards  
```
_
%
[abc]
[a-d]
[!abc]
in
between
as
inner join xx on xx=xx
left join xx on xx=xx
full join xx on xx=xx
union
group by
concat(A,',',B,',',C) as address
having (congregate func)
where exists (cond)
where A = Any (cond)
where A = All (cond)
Select * into BB (IN 'abc.bd') create new db
Insert into A (Col1,col2,col3) select col1,col2,col3 from B
ifnull(A,0)
#comment


#database management
CREATE DATABASE A;
DROP DATABASE B;
CREATE TABLE C(
	c int,
	c2 varchar(255)
	);
DROP TABLE C;
ALTER TALBE D
ADD/drop/alter col_name datatype
```


