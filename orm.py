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
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.radio=30
        self.direccion = random.randint(0,360)
        #Los colores se cogen aleatoriamente de varios colores posibles
        colores = ["turquoise", "SteelBlue", "LightGreen", "sky blue", "aquamarine", "DeepPink", "pink", "violet"]
        self.color = random.choice (colores)
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso= "" 
        
        #Añado velocidad
        self.velocidad = 1
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill =self.color)
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-16,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill ="green"
            )
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-10,
            self.posx+self.radio/2,
            self.posy-self.radio/2-8,
            fill ="blue"
            )

            
        
    def mueve(self):
        self.colisiona()
        lienzo.move(
            self.entidad,
            math.cos(self.direccion) * self.velocidad,
            math.sin(self.direccion)* self.velocidad)
        lienzo.move(
            self.entidadenergia,
            math.cos(self.direccion) * self.velocidad,
            math.sin(self.direccion)* self.velocidad)
        lienzo.move(
            self.entidaddescanso,
            math.cos(self.direccion) * self.velocidad,
            math.sin(self.direccion)* self.velocidad)
        self.posx += math.cos(self.direccion)
        self.posy +=math.sin(self.direccion)
    def colisiona(self):
        if self.posx < 0 or self.posx > 1024 or self.posy < 0 or self.posy > 1024:
            self.direccion += math.pi
            
def guardarPersonas():
    print("Guardo a los jugadores")
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            DELETE FROM jugadores
            ''')
    conexion.commit()
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
lienzo = tk.Canvas(raiz, width=1024, height=924)
lienzo.pack()

#Botón guardar
boton = tk.Button(raiz, text = "Guardar", command = guardarPersonas)
boton.pack()

#Cargar personas desde SQL
try:
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''SELECT *
                      FROM jugadores
                                     
                      ''')
    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        #print(fila)
        persona= Persona()
        persona.pox = fila[1]
        persona.poy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad= fila[6]
        persona.velocidad = fila[7]
        personas.append(persona)
        
    conexion.close()   
except:
    print("error al leer base de datos")
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




