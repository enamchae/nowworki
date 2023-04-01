import sqlite3 as sql
import hashlib


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


'''
def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()
'''
