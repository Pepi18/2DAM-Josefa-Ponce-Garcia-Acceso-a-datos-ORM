import tkinter as tk
import random
import math
import json

personas= []
numeropersonas = 5

class Persona:

    def __init__(self):
        self.posx = random.randint(0,800)
        self.posy = random.randint(0,800)
        self.radio=30
        self.direccion = random.randint(0, 360)
        self.color = "blue"
        self.entidad = ""
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill =self.color)
    def mueve(self):
        self.colisiona()
        lienzo.move(
            self.entidad,
            math.cos(self.direccion),
            math.sin(self.direccion))
        self.posx += math.cos(self.direccion)
        self.posy +=math.sin(self.direccion)
    def colisiona(self):
        if self.posx < 0 or self.posx > 800 or self.posy < 0 or self.posy > 800:
            self.direccion += math.pi
            
def guardarPersonas():
    print("Guardo a los jugadores")
    cadena = json.dumps([vars(persona) for persona in personas])
    print(cadena)
    archivo=open("jugadores.json",'w')
    archivo.write(cadena)
    


#Creo una ventana
raiz = tk.Tk()

#En la ventana creo un lienzo
lienzo = tk.Canvas(raiz, width=800, height=800)
lienzo.pack()

#Botón guardar
boton = tk.Button(raiz, text = "Guardar", command = guardarPersonas)
boton.pack()

#Cargar personas desde el disco duro
carga = open("jugadores.json",'r')
cargado = carga.read()
cargadolista = json.loads(cargado)
print("es:" + cargado)
numeropersonas= len (cargadolista)
print(numeropersonas)
for elemento in cargadolista:
    print(elemento)
    

#En la colección introduzco instancias de persoans
if len(personas) == 0:
    numeropersonas = len(personas)
    for i in range(0, numeropersonas):
        personas.append(Persona())

## Pinto en la interfaz a cada persona de la colección
for persona in personas:
    persona.dibuja()

#Creo un bucle repetitivo
def bucle():
    #Muevo cada persona de la colección
    for persona in personas:
        persona.mueve()
    raiz.after(10,bucle)

#Ejecuto el bucle
bucle()




raiz.mainloop()




