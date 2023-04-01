import sqlite3 as sql
import hashlib


# inserts a user with the corresponding password to the database
def insert_user(email, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO users (email, password) VALUES (?,?);', (email, hashPassword))
    connection.commit()


# Returns if an email and password is valid
def is_valid_password(email, password):
    hashPassword = hashlib.md5(password.encode('utf-8')).hexdigest()
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT password FROM users WHERE email=(?);', (email,))

    try:
        return cursor.fetchall()[0][0]==hashPassword
    except:
        False
#Gives the type of the user
def get_user_type(email):
    pass

# Returns if an email is a user
def is_user(email):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT password FROM users WHERE email=(?);', (email,))

    return len(cursor.fetchall())>0



'''
def valid_name(first_name, last_name):
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users (firstname, lastname) VALUES (?,?);', (first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()
'''
