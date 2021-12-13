from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/*": {"origins": "*"}})

def get_connection():
    con = sqlite3.connect('test.sqlite3')
    return con

def get_users():
    users = []
    try:
        con = get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from emp')
        rows = cur.fetchall()

        for row in rows:
            user = {}
            user['id'] = row['id']
            user['personalNo'] = row['empno']
            user['firstName'] = row['first_name']
            user['lastName'] = row['last_name']
            user['departmentId'] = row['dept_id']
            users.append(user)
    except:
        users = []
    finally:
        con.close()

    return users

def get_id():
    id = -1
    try:
        con = get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select max(id) id from emp')
        row = cur.fetchone()

        id = row['id'] + 1
    except:
        id = -1
    finally:
        con.close()

    return id 

def add_user(user):
    id = get_id()
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('insert into emp (id, empno, first_name, last_name, dept_id) values (?, ?, ?, ?, ?)',
            (id, user['empno'], user['firstName'], user['lastName'], user['departmentId']))
        con.commit()
    except:
        con().rollback()
    finally:
        con.close()

    return get_user_by_id(id)
    #return user

def get_user_by_id(user_id):
    user = {}
    try:
        con = get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from emp where id=?', (str(user_id)))
        row = cur.fetchone()

        user['id'] = row['id']
        user['personalNo'] = row['empno']
        user['firstName'] = row['first_name']
        user['lastName'] = row['last_name']
        user['departmentId'] = row['dept_id']
    except:
        user = {}
    finally:
        con.close()

    return user

@app.route("/")
def hello():
   return "Test application is ready to be tested on <b>/api/users</b> URL !"

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(add_user(user))

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

if __name__ == "__main__":
   #app.run(debug=True)
   app.run(host='0.0.0.0', debug=True)
