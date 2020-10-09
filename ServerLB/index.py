from flask import Flask, request, jsonify, Response
from time import time
from bson import json_util
import urllib
import requests

URL = "http://3.138.60.59:5000/"
URL2 = "http://3.22.221.7:5000/"

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/crearNota",methods=["POST"])
def crearNota():
    s1 = testConnection(URL)
    s2 = testConnection(URL2)
    server = False
    if(s1==False):
        server = False 
    if(s2 == False):
        server = True
    if(s1 and s2):
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
        cap1 = int(data1["SIZE"])
        cap2 = int(data2["SIZE"])
        msg = "none"

        if cap1 > cap2: 
            server = True
            msg = "Servidor 2 tiene menos elementos"
        elif cap2 > cap1: 
            server = False
            msg = "Servidor 1 tiene menos elementos"
        elif ram1>ram2:
            server = True
            msg = "Servidor 2 tiene mas RAM disponible"
        elif ram2>ram1:
            server = False
            msg = "Servidor 1 tiene mas RAM disponible"
        elif(cpu1>cpu2): 
            server = True
            msg = "Servidor 2 tiene mas CPU disponible"
        elif cpu2>cpu1:
            server = False
            msg = "Servidor 1 tiene mas CPU disponible"
    elif s1 and not s2:
        server = False
        msg = "Servidor 1 esta disponible, pq el 2 no esta ):"
    elif s2 and not s1:
        server = True
        msg = "Servidor 2 esta disponible, pq el 1 no esta ):"
    elif not s2 and not s1:
        msg = "No hay servidores disponibles"
        response = "ERROR"
        return {"res":response,"data":msg}


    if(not server):
        response = "Reenviando a Servidor 1"
        requests.post(URL+"/crearNota",json = request.json)
    else:
        requests.post(URL2+"/crearNota",json = request.json)
        response = "Reenviando a Servidor 2"
    #response = str(ram1) + "  -  "+str(ram2) + "  -  "+str(cpu1) + "  -  "+str(cpu2) + "  -  " 
    return {"res":response,"data":msg}

def testConnection(url):
    try:
        urllib.request.urlopen(url,timeout=1)
        return True 
    except urllib.error.URLError as err:
        print(err)
        return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5001"), debug=True)
