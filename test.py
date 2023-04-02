#Test file for adding and removing from database with database manager
import dbManager as dbm
import MySQLdb


# Function for connecting to MySQL database
info = "sql9.freemysqlhosting.net","sql9610407","d8zViT6lIW","sql9610407",3306
def mysqlconnect():
    db_connection= MySQLdb.connect(*info)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User;")
    m = cursor.fetchone()
    print("Today's Date Is ",m)
    db_connection.close()


# Function Call For Connecting To Our Database
mysqlconnect()
dbm.insert_user("Dr. Halla","Funtimesboy","Funtimesboy")