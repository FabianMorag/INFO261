import flask
import json
from flask import request, jsonify
import mysql.connector

# Creación de una nueva aplicación web
app = flask.Flask(__name__)

# Conexión al SGBD
  ## reemplazar 'root' por el password del usuario administrador de MySQL
conn = mysql.connector.connect(user="root",host="localhost",password="")
cursor = conn.cursor()
cursor.execute("USE smartvaldivia")

# Definición de las rutas

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to SmartValdvia API</h1>
<p>Un prototipo de API para la base de datos SmartValdivia.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api_smartvaldivia/v1/package/sectores/all', methods=['GET'])
def sectores_all():
    ## Consultar MySQL para obtener datos sobre los sectores
    result=cursor.execute('SELECT id_sector, nombre_sector, radio FROM sectores;')
    all_films =cursor.fetchall()
    ## Conservar el nombre de los atributos
    row_headers=[x[0] for x in cursor.description]
    ## Transformar resultados en datos JSON
    json_data=[]
    for result in all_films:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

@app.route('/api_smartvaldivia/v1/package/choferes/all', methods=['GET'])
def choferes_all():
    ## Consultar MySQL para obtener datos sobre los choferes
    result=cursor.execute('SELECT * FROM choferes;')
    all_films =cursor.fetchall()
    ## Conservar el nombre de los atributos
    row_headers=[x[0] for x in cursor.description]
    ## Transformar resultados en datos JSON
    json_data=[]
    for result in all_films:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

@app.route('/api_smartvaldivia/v1/package/camionsector', methods=['GET'])
def camiones_sectores_filter():
    ## Definir parametros posibles
    query_parameters = request.args

    nombre_sector = query_parameters.get('nombre_sector')
    
    ##Construir la consulta SQL según parametros
    query = "SELECT nombre_sector, patente_camion, fecha FROM limpieza"
    to_filter = []

    query += ' INNER JOIN camiones ON limpieza.id_camion=camiones.id_camion \
    INNER JOIN sectores ON limpieza.id_sector=sectores.id_sector WHERE'

    if nombre_sector:
        query += ' nombre_sector=%s;'
        to_filter.append(nombre_sector)
    if not (nombre_sector):
        return page_not_found(404)
    
    print(query)
    print(to_filter)
    
    ## Consultar
    results=cursor.execute(query,to_filter)
    some_films =cursor.fetchall()
    ## Conservar el nombre de los atributos
    row_headers=[x[0] for x in cursor.description]
    ## Transformar resultados en datos JSON
    json_data=[]
    for result in some_films:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

app.run(debug=True,port=1234)