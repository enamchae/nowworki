import sqlite3 as sql
import hashlib
from datetime import datetime

# inserts a user with the corresponding password to the database
def insert_user(name,uid, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO user (name, uid, password) VALUES (?,?,?);', (name, uid, hashPassword))
    connection.commit()


# Returns if an uid and password is valid
def is_valid_password(uid, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT password FROM user WHERE uid=(?);', (uid,))

    try:
        return cursor.fetchall()[0][0]==hashPassword
    except:
        False
#Gives the type of the user
def get_user_type(uid):
    pass

# Returns if an uid is a user
def is_user(uid):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT password FROM user WHERE uid=(?);', (uid,))

    return len(cursor.fetchall())>0

#Get Posts of a category
def get_posts(category, fulltime=False):
    type= int(fulltime)
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT User.name as firstname, post.name as Title,Post.pid as pid, time '
                                'FROM Post,User '
                                'WHERE Post.UID=User.UID AND Category = (?) AND FullTime= (?)'
                                'ORDER BY time desc;', (category, type))

    return cursor.fetchall()

#Implementation to get the post text
def get_post(pid):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT User.name as firstname, post.name as Title, text, time '
                                'FROM Post,User '
                                'WHERE Post.UID=User.UID AND post.PID=(?)'
                                'ORDER BY time desc;', (pid,))

    return cursor.fetchall()
#Implement the getting the replys
def get_postRep(pid):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT RID, PostRep.name as Title, USER.name as firstname, text, time '
                                'FROM PostRep,User '
                                'WHERE PostRep.UID=User.name AND PID = (?) '
                                'ORDER BY RID asc;', (pid,))

    return cursor.fetchall()
#Allows the creation of posts for the user
def insert_post(uid, category,text,PID,Fulltime,time):
    unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    connection = sql.connect('database.db')
    cursor = connection.execute('INSERT INTO post (uid, category,text,PID,Fulltime,time) VALUES (?,?,?,?,?,?);', (uid, category,text,PID,Fulltime,unix_timestamp))
    return cursor.fetchall()

def insert_postrep(uid, text, pid, rid, time):
    unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    connection = sql.connect('database.db')
    cursor = connection.execute('INSERT INTO PostRep (uid,text,pid,rid,time) VALUES (?,?,?,?,?);',
                                (uid, text, pid, rid, unix_timestamp))
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
