import sqlite3 as sql
import MySQLdb
import hashlib
from datetime import datetime
import mysql.connector
info = {'host':"sql9.freemysqlhosting.net",'user':"sql9610407",'password':"d8zViT6lIW",'database':"sql9610407",'port':3306}



local = False;
if not local:
    connector = MySQLdb.connect(
        host="sql9.freemysqlhosting.net",

        user="sql9610407",
        passwd="d8zViT6lIW",
        db="sql9610407", port=3306
    )
    cursor = connector.cursor()
    cursor.execute("select database();")
    db = cursor.fetchone()
    print("You're connected to dtabase: ", db)
    db = cursor.fetchall()
    connector.close()
# inserts a user with the corresponding password to the database
def insert_user(name,uid, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    if local:
        connection = sql.connect('database.db')
        connection.execute('INSERT INTO user (name, uid, password) VALUES (?,?,?);', (name, uid, hashPassword))
        connection.commit()
    else:

        print("Inserting User")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor()
        querry = "INSERT INTO User (name, UID, password) VALUES (%s,%s,%s);"
        print((name,uid,hashPassword))
        cursor.execute(querry,(name,uid,hashPassword))
        db_connection.commit()
        db_connection.close()


# Returns if an uid and password is valid
def is_valid_password(uid, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    if local:
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT password FROM user WHERE uid=(?);', (uid,))

        try:
            return cursor.fetchall()[0][0]==hashPassword
        except:
            False
    else:
        print("Testing if valid password")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor()
        querry = "('SELECT password FROM User WHERE UID=(%s);"
        cursor.execute(querry, (uid,))
        db_connection.commit()
        try:
            return cursor.fetchall()[0][0]==hashPassword
        except:
            return False
#Gives the type of the user
def get_user_type(uid):
    pass

# Returns if an uid is a user
def is_user(uid):
    if local:
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT password FROM user WHERE uid=(?);', (uid,))

        return len(cursor.fetchall())>0
    else:
        print("Testing if is an user")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor()
        querry = "('SELECT password FROM User WHERE UID=(%s);"
        cursor.execute(querry, (uid,))
        db_connection.commit()

        return len(cursor.fetchall()) > 0

#Get Posts of a category
def get_posts(category, fulltime=False):
    if local:
        type= int(fulltime)
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT User.name as firstname, post.name as Title,Post.pid as pid, time '
                                    'FROM Post,User '
                                    'WHERE Post.UID=User.UID AND Category = (?) AND FullTime= (?)'
                                    'ORDER BY time desc;', (category, type))

        return cursor.fetchall()
    else:
        print("Getting the posts")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor(buffered=True)
        fun = 'SELECT User.name as firstname, Post.Title as Title,Post.PID as pid, entrytime FROM Post,User WHERE Post.UID=User.UID AND Category = (%s) AND FullTime= (%s) ORDER BY entrytime desc;'
        cursor.execute(fun, (category, fulltime))
        db_connection.commit()
        return cursor.fetchall()

#Implementation to get the post text
def get_post(pid):
    if local:
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT User.name as firstname, post.name as Title, text, time '
                                    'FROM Post,User '
                                    'WHERE Post.UID=User.UID AND post.PID=(?)'
                                    'ORDER BY time desc;', (pid,))

        return cursor.fetchall()
    else:
        print("Getting a post value")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor(buffered=True)
        cursor.execute('SELECT User.name as firstname, Title, text, entrytime '
                                    'FROM Post,User '
                                    'WHERE Post.UID=User.UID AND post.PID=(%s)'
                                    'ORDER BY time desc;', (pid,))
        db_connection.commit()
        return cursor.fetchall()
#Implement the getting the replys
def get_postRep(pid):
    if local:
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT RID, PostRep.name as Title, USER.name as firstname, text, entrytime '
                                    'FROM PostRep,User '
                                    'WHERE PostRep.UID=User.name AND PID = (?) '
                                    'ORDER BY RID asc;', (pid,))
        return cursor.fetchall()
    else:
        print("Getting the post replys")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor()
        cursor.execute('SELECT RID, PostRep.name as Title, USER.name as firstname, text, entrytime '
                                    'FROM PostRep,User '
                                    'WHERE PostRep.UID=User.name AND PID = (?) '
                                    'ORDER BY RID asc;', (pid,))
        db_connection.commit()
        return cursor.fetchall()

#Allows the creation of posts for the user
def insert_post(uid, category,text,Fulltime,time):
    if local:
        PID=12312
        unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
        connection = sql.connect('database.db')
        cursor = connection.execute('INSERT INTO post (uid, category,text,PID,Fulltime,time) VALUES (?,?,?,?,?,?);', (uid, category,text,PID,Fulltime,unix_timestamp))
        return cursor.fetchall()
    else:
        unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
        print("Inserting Post")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor()
        cursor.execute('INSERT INTO post (uid, category,text,Fulltime) VALUES (?,?,?,?,?);', (uid, category,text,Fulltime))
        db_connection.commit()
        return cursor.fetchall()

def insert_postrep(uid, text, pid, rid, time):
    if local:
        unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
        connection = sql.connect('database.db')
        cursor = connection.execute('INSERT INTO PostRep (uid,text,pid,rid,time) VALUES (?,?,?,?,?);',
                                    (uid, text, pid, rid, unix_timestamp))
        return cursor.fetchall()
    else:
        unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
        print("Inserting post reply")
        db_connection = mysql.connector.connect(**info)
        cursor = db_connection.cursor()
        cursor.execute('INSERT INTO PostRep (uid,text,pid,rid) VALUES (?,?,?,?);',
                                    (uid, text, pid, rid))
        db_connection.commit()
        return cursor.fetchall()
'''
def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()
'''
