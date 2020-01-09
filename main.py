import pymysql
import json
from db_config import conn
from app import app

from flask import jsonify, request





@app.route('/peliculas')
def getAll():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("select * from pelicula")
        jsonObjects = []
        rows = cursor.fetchall()
        for object in rows:
            pelicula = {"titulo": object[0], "director": object[1], "fecha": object[2]}
            jsonObjects.append(pelicula)
        resp = json.dumps(jsonObjects)
        return resp

    except Exception as e:
        print("Error " + e)
    finally:
        cursor.close()

@app.route('/peliculas/<string:titulo>')
def getPeliculaByTitulo(titulo):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("select * from pelicula where titulo =%s", [titulo])
        jsonObjects = []
        rows = cursor.fetchall()
        for object in rows:
            pelicula = {"titulo": object[0], "director": object[1], "fecha": object[2]}
            jsonObjects.append(pelicula)
        resp = json.dumps(jsonObjects)
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()


@app.route('/listadoPeliculas/<string:director>')
def getPeliculaByDirector(director):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("select * from pelicula where director =%s", [director])
        rows = cursor.fetchall()
        jsonObjects = []
        for object in rows:
            pelicula = {"titulo": object[0], "director": object[1], "fecha": object[2]}
            jsonObjects.append(pelicula)
        resp = json.dumps(jsonObjects)
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()



@app.route('/login/<string:usuario>')
def getUser(usuario):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("select * from login where usuario =%s", [usuario])
        jsonObjects = []
        rows = cursor.fetchall()
        for object in rows:
            login = {"usuario": object[0], "password": object[1]}
            jsonObjects.append(login)
        resp = json.dumps(jsonObjects)
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def addUser():
    cursor = conn.cursor()
    try:
        _json = request.json
        _username = _json['usuario']
        _password = _json['password']

        #validamos si se han recivido
        if _username and _password and request.method == 'POST':
            sql = "insert into login(usuario, password) values(%s, %s)"
            data = (_username, _password)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("Usuario añadido correctamente")
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/peliculas', methods=['POST'])
def createPeliculas():
    cursor = conn.cursor()
    try:

        _json = request.json
        _titulo = _json['titulo']
        _director = _json['director']
        _fecha = _json['fecha']

        if _titulo and _director and _fecha and request.method == 'POST':
            sql = "insert into pelicula(titulo, director, fecha) values(%s, %s, %s)"
            data = (_titulo, _director, _fecha)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("Pelicula añadida correctamente")
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/peliculas/<string:titulo>', methods=['DELETE'])
def deletePelicula(titulo):
    cursor = conn.cursor()
    try:
        cursor.execute("delete from pelicula where titulo =%s", [titulo])
        conn.commit()
        resp = jsonify("Pelicula borrada correctamente")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/update', methods=['POST'])
def updatePelicula():
    cursor = conn.cursor()
    try:
        _json = request.json
        _titulo = _json['titulo']
        _director = _json['director']
        _fecha = _json['fecha']

        if _titulo and _director and _fecha and request.method == 'POST':
            sql = "update pelicula set director = %s, fecha = %s where titulo =%s"
            data = (_director, _fecha, _titulo)
            cursor.execute(sql, data)
            conn.commit()
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()