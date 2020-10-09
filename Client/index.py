from faker import Faker 
import requests

data = list()
faker = Faker()
url = "http://localhost:5001/"
def load_file():
    ruta_archivo = raw_input()
    print(ruta_archivo)
    try:
        archivo = open(ruta_archivo,"r")
        texto = archivo.read().splitlines()
        archivo.close()
        global data 
        data = []
        for x in texto:
            data.append({"autor":str(faker.name()),"nota":x})
    except Exception as e:
        print(e)
    return 0

def show_data():
    global data
    for x in data:
        print("Name: " + x["autor"]+ "  ,  Nota: "+x["nota"])
    return 0

def send_data():
    global url
    global data  
    uri = url +"crearNota"
    for x in data:
        req = requests.post(url=uri,json=x)
        print(req.json())

    return 0

def main():
    opcion = 0
    while opcion!=4:
        print("Ingrese una opcion:\n1. Abrir Archivo.\n2. Mostrar Datos.\n3. Enviar Datos.\n4. Salir!")
        try:
            opcion = int(input("Ingrese su opcion:"))
        except:
            opcion = 0
        if opcion == 1:
            load_file()
        if opcion == 2:
            show_data()
        if opcion == 3:
            send_data()

main()