import mysql.connector
import pymysql
mydb = pymysql.connect(host='localhost', user='root', passwd='mypassword')
#mydb = mysql.connector.connect(host='localhost',user='root',passwd='mypassword')
my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE Ourusers")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)