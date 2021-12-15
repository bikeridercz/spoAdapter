from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/*": {"origins": "*"}})

def get_connection():
    con = sqlite3.connect('orders.sqlite3')
    con.row_factory = sqlite3.Row
    return con

def get_order(order_id):
    order = {}
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('select * from b2b_order where id=?', (str(order_id)))
        row = cur.fetchone()
        order['id'] = row['id']
        order['consumerOrderId'] = row['consumer_order_id']
        order['note'] = row['note']
    except:
        order = {}
    finally:
        con.close()
    return order

def get_orders():
    orders = []
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('select * from b2b_order order by id')
        rows = cur.fetchall()
        for row in rows:
            order = {}
            order['id'] = row['id']
            order['consumerOrderId'] = row['consumer_order_id']
            order['note'] = row['note']
            orders.append(order)
    except:
        orders = []
    finally:
        con.close()
    return orders

def get_new_order_id():
    id = -1
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('select max(id) id from b2b_order')
        row = cur.fetchone()
        id = row['id'] + 1
    except:
        id = -1
    finally:
        con.close()
    return id 

def add_order(order):
    id = get_new_order_id()
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('insert into b2b_order (id, consumer_order_id, note) values (?, ?, ?)',
            (id, order['consumerOrderId'], order['note']))
        con.commit()
    except:
        con().rollback()
    finally:
        con.close()
    return get_order(id)

def update_order(order):
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('update b2b_order set consumer_order_id=?, note=? where id=?',
            (order['consumerOrderId'], order['note'], order['id']))
        con.commit()
    except:
        con().rollback()
    finally:
        con.close()
    return get_order(order['id'])

def delete_order(order_id):
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute('delete from b2b_order where id=?', (order_id))
        con.commit()
    except:
        con().rollback()
    finally:
        con.close()
    return order_id

@app.route('/')
def hello():
   return 'Test application is ready to be tested on <b>/api/orders</b> URL !'

@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    #return jsonify(get_orders())
    return {'body': get_orders(), 'message': 'This endpoint returns a list of all Orders', 'method': request.method}

@app.route('/api/orders/<order_id>', methods=['GET'])
def api_get_order(order_id):
    #return jsonify(get_order(order_id))
    return {'body': get_order(order_id), 'message': 'This endpoint returns details of the Order[orderId:{}]'.format(order_id), 'method': request.method}

@app.route('/api/orders/add', methods=['POST'])
def api_add_order():
    order = request.get_json()
    new_order = add_order(order)
    #return jsonify(add_order(order))
    return {'body': new_order, 'message': 'This endpoint creates the new Order[orderId:{}]'.format(new_order['id']), 'method': request.method}

@app.route('/api/orders/update', methods=['PUT'])
def api_update_order():
    order = request.get_json()
    updated_order = update_order(order)
    return {'body': updated_order, 'message': 'This endpoint updates existing Order[orderId:{}]'.format(updated_order['id']), 'method': request.method}

@app.route('/api/orders/delete/<order_id>', methods=['DELETE'])
def api_delete_order(order_id):
    removed_order_id = delete_order(order_id)
    return {'body': removed_order_id, 'message': 'This endpoint removes existing Order[orderId:{}]'.format(removed_order_id), 'method': request.method}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
