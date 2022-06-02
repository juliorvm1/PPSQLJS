from flask import Flask, request
from psycopg2 import connect

app = Flask(__name__)

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
    return('getting users')

#endponit para insertar un usuario a la base de datos obtenidos desde el cliente metodo post
@app.post('/api/users')
def create_users():
    # print(request.get_json())
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = new_user['password']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username,email,password) VALUES (%s,%s,%s)',
                (username, email, password))
    conn.commit()
    cur.close()
    conn.close()


    # print(username,email,password)
    return('creating users')

#endponit para borrar un usuario a la base de datos obtenidos desde el cliente metodo delete y un id de referencia
@app.delete('/api/users/1')
def delete_users():
    return('deleting users')

#endponit para actualizar un usuario a la base de datos obtenidos desde el cliente metodo put y un id de referencia
@app.put('/api/users/1')
def update_users():
    return('updating users')

#endponit para obtener la información de un solo usuario usando el metodo get y un id de referencia
@app.get('/api/users/1')
def getting_user():
    return('getting user 1')


if __name__ == '__main__':
    app.run(debug=True)
