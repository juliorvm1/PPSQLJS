from json import load
from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)
key = Fernet.generate_key()


# datos de conexión a la base de datos postgres
#comentario de prueba
"""host = 'localhost'
port = 5432
dbname = 'userdb'
user = 'superu'
password = 'mipassword'
"""

host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')



def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn


""" CODIGO PARA HACER UNA PRUEBA AL CONFIGURAR UNA BASE DE DATOS
@app.get('/')
def home():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT 1 + 1")
    result=cur.fetchone()
    print(result)

    return 'hello world' + str(result)"""

# endponit para obtener la lista de usuarios


@app.get('/api/users')
def get_users():
    conn = get_connection()
    # para convertirlo en diccionario
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users')
    list_users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list_users)
    # return('getting users')

# endponit para insertar un usuario a la base de datos obtenidos desde el cliente metodo post
# Commit en git para identificar la creacion de usuarios


@app.post('/api/users')
def create_users():
    # print(request.get_json())
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    #password = new_user['password']

    conn = get_connection()
    #cur = conn.cursor()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('INSERT INTO users (username,email,password) VALUES (%s,%s,%s) RETURNING *',
                (username, email, password))
    new_created_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_created_user)
    
   # print(username,email,password)
   # return('creating users')


# endponit para borrar un usuario a la base de datos obtenidos desde el cliente metodo delete y un id de referencia
@app.delete('/api/users/<id>')
def delete_users(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('DELETE FROM users WHERE id=%s RETURNING *', (id,))
    user_deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user_deleted is None:
        return jsonify({'message': 'user not found'}), 404
    return jsonify(user_deleted)
    # return('deleting users')

# endponit para actualizar un usuario a la base de datos obtenidos desde el cliente metodo put y un id de referencia


@app.put('/api/users/<id>')
def update_users(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    update_user = request.get_json()
    new_user_name = update_user['username']
    new_user_email = update_user['email']
    new_user_password = Fernet(key).encrypt(
        bytes(update_user['password'], 'utf-8'))
    cur.execute('UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s RETURNING *',
                (new_user_name, new_user_email, new_user_password, id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_user is None:
        return jsonify({'message': 'user not found'}, 404)
    return jsonify(updated_user)

    return('updating users')

# endponit para obtener la información de un solo usuario usando el metodo get y un id de referencia


@app.get('/api/users/<id>')
def getting_user(id):
    conn = get_connection()
    # para convertirlo en diccionario
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id=%s', (id,))
    user = cur.fetchone()
    if user is None:
        return jsonify({'message': 'user not found'}, 404)
    cur.close()
    conn.close()
    return jsonify(user)
    return('getting user 1')


@app.get('/')
def home():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(debug=True)
