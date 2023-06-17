from flask import jsonify
from flask_mysqldb import MySQL

def init(app):

    
    app.config['MYSQL_HOST'] = '35.232.13.66'
    #app.config['MYSQL_UNIX_SOCKET'] = '/mysql/bissmillah-390010:us-central1:mydatabase'
    app.config['MYSQL_USER'] = 'username'
    app.config['MYSQL_PASSWORD'] = '12345678'
    app.config['MYSQL_DB'] = 'c23-ps067'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    return MySQL(app)

def getalluser(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    user = cur.fetchall()
    cur.close()
    return user

def registerdb(mysql,username,email, pwd):
    cur = mysql.connection.cursor()
    user = cur.execute("SELECT * FROM user WHERE email=(%s)",(email,))
    if user > 0:
        return jsonify({"msg":"Email already exist"}),401
    cur.execute("INSERT INTO user(username, email, password) VALUES (%s, %s, %s)", (username,email, pwd))
    mysql.connection.commit()
    id = cur.lastrowid
    cur.execute("SELECT * FROM user where id=(%s)",(id,))
    userdetail = cur.fetchall()
    cur.close()
    return jsonify({
        "msg":"Registration successfull",
        "data":userdetail
    })

def logindb(mysql,email,password):
    cur = mysql.connection.cursor()
    user = cur.execute("SELECT username,email FROM user where email= (%s) and password=(%s)",(email,password))
    if user > 0:
            login = cur.fetchall()
            cur.close()
            return login
    cur.close()
    return ""
