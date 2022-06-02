from flask import Flask, request, jsonify
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

app = Flask(__name__)
key=Fernet.generate_key()


#datos de conexión a la base de datos postgres
host = 'localhost'
port = 5432
dbname = 'userdb'
user = 'superu'
password = 'mipassword'


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

#endponit para obtener la lista de usuarios
@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor) #para convertirlo en diccionario
    cur.execute('SELECT * FROM users')
    list_users=cur.fetchall()    
    cur.close()
    conn.close()
    return jsonify(list_users)
    #return('getting users')

#endponit para insertar un usuario a la base de datos obtenidos desde el cliente metodo post 
#Commit en git para identificar la creacion de usuarios
@app.post('/api/users')
def create_users():
    # print(request.get_json())
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password=Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    #password = new_user['password']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username,email,password) VALUES (%s,%s,%s) RETURNING *',
                (username, email, password))
    new_created_user=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_created_user)
   # print(username,email,password)
   # return('creating users')
   


#endponit para borrar un usuario a la base de datos obtenidos desde el cliente metodo delete y un id de referencia
@app.delete('/api/users/1')
def delete_users():
    return('deleting users')

#endponit para actualizar un usuario a la base de datos obtenidos desde el cliente metodo put y un id de referencia
@app.put('/api/users/1')
def update_users():
    return('updating users')

#endponit para obtener la información de un solo usuario usando el metodo get y un id de referencia
@app.get('/api/users/<id>')
def getting_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor) #para convertirlo en diccionario
    cur.execute('SELECT * FROM users WHERE id=%s', (id,))
    user=cur.fetchone()    
    cur.close()
    conn.close()
    return jsonify(user)
    return('getting user 1')


if __name__ == '__main__':
    app.run(debug=True)
