import tkinter as tk
import random
import math
import json

personas= []
numeropersonas = 5

class Persona:

    def __init__(self):
        self.posx = random.randint(0,950)
        self.posy = random.randint(0,950)
        self.radio=30
        self.direccion = random.randint(0, 360)
        #Los colores se cogen aleatoriamente de varios colores posibles
        colores = ["turquoise", "SteelBlue", "LightGreen", "sky blue", "aquamarine", "DeepPink", "pink", "violet"]
        self.color = random.choice (colores)
        self.entidad = ""
        #Añado velocidad
        self.velocidad = 0.5
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
            math.cos(self.direccion) * self.velocidad,
            math.sin(self.direccion)* self.velocidad)
        self.posx += math.cos(self.direccion)
        self.posy +=math.sin(self.direccion)
    def colisiona(self):
        if self.posx < 0 or self.posx > 950 or self.posy < 0 or self.posy > 950:
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
lienzo = tk.Canvas(raiz, width=950, height=950)
lienzo.pack()

#Botón guardar
boton = tk.Button(raiz, text = "Guardar", command = guardarPersonas)
boton.pack()

#Cargar personas desde el disco duro
try:
    carga = open("jugadores.json",'r')
    cargado = carga.read()
    cargadolista = json.loads(cargado)
    for elemento in cargadolista:
        persona= Persona()
        persona.__dict__.update(elemento)
        personas.append(persona)
except:
    print("error")
    
    

#En la colección introduzco instancias de persoans
if len(personas) == 0:
    numeropersonas = 700
    for i in range(0, numeropersonas):
        personas.append(Persona())

## Pinto en la interfaz a cada persona de la colección
for persona in personas:
    persona.dibuja()

#Creo un bucle repetitivo
def bucle():
    #Muevo cada persona de la colección
    for Persona in personas:
        Persona.mueve()
    raiz.after(10,bucle)

#Ejecuto el bucle
bucle()




raiz.mainloop()




