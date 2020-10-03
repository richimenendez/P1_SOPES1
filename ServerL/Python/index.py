from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo 
from time import time
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://192.168.1.18:27017/proyecto'
mongo = PyMongo(app)



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/crearNota", methods=["POST"])
def crearNota():
    autor = request.json['autor']
    nota = request.json['nota']
    tmstmp = time()
    idN = ""
    if( autor and nota and tmstmp):
        idN = mongo.db.notas.insert_one(
            {'autor':autor, 'nota':nota, 'tmstmp':tmstmp}
        )
    else:
        return {"message":"Faltan datos!!"}
    return {"message":"Nota Creada con id!"} 


@app.route("/verNotas",  methods=["GET"])
def verNota():
    users = mongo.db.notas.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
