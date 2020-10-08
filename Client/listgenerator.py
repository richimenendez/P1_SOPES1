from faker import Faker 
fake = Faker()

def main():
    archivo = open("lista.txt","w")
    for x in range(20):
        archivo.write(fake.sentence()+"\n")
    archivo.write(fake.sentence())
    archivo.close()

main()