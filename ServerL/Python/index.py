from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo 
from time import time
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mng-db:27017/proyecto'
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


@app.route("/verRAM",  methods=["GET"])
def verRAM():
    archivo = open("/proc/ram-module","r")
    ram = str(archivo.read()).split(";")
    response = json_util.dumps({'RAM':100-int(100*(int(ram[1])/int(ram[0])))})
    archivo.close()
    return Response(response, mimetype='application/json')


@app.route("/verCPU",  methods=["GET"])
def verCPU():
    archivo = open("/proc/cpu-module","r")
    cpu = int(str(archivo.read()))
    if(cpu<100):
        cpu = cpu
    elif cpu < 1000 :
        cpu = cpu/10 
    elif cpu < 10000:
        cpu = cpu /100
    response = json_util.dumps({'CPU':int(cpu)})
    archivo.close()
    return Response(response, mimetype='application/json')


@app.route("/verSTAT",  methods=["GET"])
def verSTAT():
    archivo = open("/proc/cpu-module","r")
    archivo2 = open("/proc/ram-module","r")
    elementos = mongo.db.notas.count()
    ram = str(archivo2.read()).split(";")
    cpu = int(str(archivo.read()))
    if(cpu<100):
        cpu = cpu
    elif cpu < 1000 :
        cpu = cpu/10 
    elif cpu < 10000:
        cpu = cpu /100

    response = json_util.dumps({'CPU':cpu,'RAMT':ram[0], 'RAML':ram[1],'SIZE':elementos, 'RAMP':100-int(100*(int(ram[1])/int(ram[0]))), 'CPUP':int(cpu)})
    archivo.close()
    archivo2.close()
    return Response(response, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
