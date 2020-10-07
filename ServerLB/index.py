from flask import Flask, request, jsonify, Response
from time import time
from bson import json_util
import requests

URL = "http://3.138.60.59:5000/"
URL2 = "http://localhost:5000/"

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/crearNota",methods=["POST"])
def crearNota():
    url_ = URL + "verSTAT"
    r1 = requests.get(str(url_))
    data1 = r1.json() 
    url2_ = URL2 + "verSTAT"
    r2 = requests.get(str(url2_))
    data2 = r2.json() 
    ram1 = int(data1["RAML"])/int(data1["RAMT"])
    ram2 = int(data2["RAML"])/int(data2["RAMT"])
    cpu1 = int(data1["CPU"])
    cpu2 = int(data2["CPU"])
    ,llcap1 = data1["SIZE"]
    cap2 = data2["SIZE"]

    server = False

    if cap1 > cap2: 
        server = True
    elif cap2 > cap1: 
        server = False
    if ram1>ram2:
        server = True
    elif ram2>ram1:
        server = False
    elif(cpu1>cpu2): 
        server = True
    elif cpu2>cpu1:
        server = False

    if(not server):
        response = "Reenviando a Servidor 1"
        requests.post(URL+"/crearNota",request.json)
    else:
        response = "Reenviando a Servidor 2"
    #response = str(ram1) + "  -  "+str(ram2) + "  -  "+str(cpu1) + "  -  "+str(cpu2) + "  -  " 
    return {"res":response,"data":data1}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5001"), debug=True)
