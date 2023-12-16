import tkinter as tk
import random
import math
import json
import sqlite3

#Declaración de variables globales
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
        self.velocidad = 2
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
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadroes.sqlite3")
    cursor = conexion.cursor()
    for persona in personas:
        cursor.execute('''
        INSERT INTO jugadores
        VALUES(
            NULL,
            '''+str(persona.posx)+''',
            '''+str(persona.posy)+''',
            '''+str(persona.radio)+''',
            '''+str(persona.direccion)+''',
            "'''+str(persona.color)+'''",
            "'''+str(persona.entidad)+'''",
            '''+str(persona.velocidad)+'''
        )
        ''')
    
    conexion.commit()
    conexion.close()
    

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
#Cargar personas desde SQL    
conexion = sqlite3.connect("jugadroes.sqlite3")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM jugadores")
while True:
    fila = cursor.fetchone()
    if fila is None:
        break
    print(fila)
    


conexion.close()   

#En la colección introduzco instancias de persoans
if len(personas) == 0:
    numeropersonas = 300
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




