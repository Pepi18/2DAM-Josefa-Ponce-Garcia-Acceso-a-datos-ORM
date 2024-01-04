import tkinter as tk
import random
import math
import json
import sqlite3

#Declaración de variables globales
personas= []
numeropersonas = 200

class Recogible():
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        colores = ["turquoise", "SteelBlue", "LightGreen", "sky blue", "aquamarine", "DeepPink", "pink", "violet"]
        self.color = random.choice (colores)
    def serializar(self):
        recogible_serializado ={
            "posx":self.posx,
            "posy":self.posy,
            "color":self.color,
            }
        return recogible_serializado
class Recogible2():
    def __init__(self):
        self.direccion = random.randint(0,360)
        self.velocidad = 0.6                
    def serializar(self):
        recogible_serializado ={
            "direccion":self.direccion,
            "velocidad": self.velocidad
            }
        return recogible_serializado
            
class Persona():
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
        #Añado experiencia
        self.experiencia = 0
        self.entidadexperiencia = ""
        #Añado velocidad
        self.velocidad = 0.6
        self.inventario = []
        for i in range(0,10):
            self.inventario.append(Recogible())
        self.inventario2 = []
        for i in range(0,5):
            self.inventario2.append(Recogible2())

        
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill =self.color
            )
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-16,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill ="green yellow"
            )
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-10,
            self.posx+self.radio/2,
            self.posy-self.radio/2-8,
            fill ="blue2"
            )
        self.entidadexperiencia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-22,
            self.posx+self.radio/2,
            self.posy-self.radio/2-20,
            fill ="mediumorchid1"
            )
                
    def mueve(self):
        if self.energia > 0:
            self.energia -= 0.1
        if self.descanso > 0:
            self.descanso -= 0.1
        
        if self.experiencia < 100:
            self.experiencia +=0.1
            self.nivelexperiencia = 1
        elif self.experiencia >= 100:
            self.nivelexperiencia = 2
        self.colisiona()
        
        lienzo.move(
            self.entidad,
            math.cos(self.direccion) * self.velocidad,
            math.sin(self.direccion)* self.velocidad)

        
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(
            self.entidadenergia,
            self.posx - self.radio/2,
            self.posy - self.radio/2-16,
            self.posx - self.radio/2 + anchuraenergia,
            self.posy - self.radio/2-14
        )
        anchuradescanso = (self.descanso/100)*self.radio
        lienzo.coords(
            self.entidaddescanso,
            self.posx - self.radio/2,
            self.posy - self.radio/2-10,
            self.posx - self.radio/2 + anchuradescanso,
            self.posy - self.radio/2-8
        )

        anchuraexperiencia = (self.experiencia/100)*self.radio
        lienzo.coords(
            self.entidadexperiencia,
            self.posx - self.radio/2,
            self.posy - self.radio/2-22,
            self.posx - self.radio/2 + anchuraexperiencia,
            self.posy - self.radio/2-20,
        )
       
        
        self.posx += math.cos(self.direccion)* self.velocidad
        self.posy +=math.sin(self.direccion)* self.velocidad
 
        
    def colisiona(self):
        if self.posx < 0 or self.posx > 1024 or self.posy < 0 or self.posy > 1024:
            self.direccion += math.pi
    def serializar(self):
        persona_serializada ={
            "posx":self.posx,
            "posy":self.posy,
            "radio":self.radio,
            "direccion":self.direccion,
            "color":self.color,
            "entidad":self.entidad,
            "velocidad":self.velocidad,
            "energia":self.energia,
            "descanso":self.descanso,
            "experiencia":self.experiencia,
            "inventario":[item.serializar() for item in self.inventario],
            "inventario2":[item.serializar() for item in self.inventario2],
            }
        return persona_serializada
    
def guardarPersonas():
    print("Guardo a los jugadores")
    
    #También guardo en json con fines demostrativos
    personas_serializadas =[persona.serializar() for persona in personas]
##    cadena = json.dumps(personas_serializadas)
##    archivo = open("jugadores.json",'w')
##    archivo.write(cadena)
    with open("jugadores.json",'w') as archivo:
        json.dump(personas_serializadas,archivo,indent=4)
    
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            DELETE FROM jugadores
            ''')
    cursor.execute('''
            DELETE FROM recogible
            ''')
    cursor.execute('''
            DELETE FROM recogible2
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
                '''+str(persona.velocidad)+''',
                '''+str(persona.energia)+''',
                '''+str(persona.descanso)+''',
                "'''+str(persona.entidadenergia)+'''",
                "'''+str(persona.entidaddescanso)+'''",
                '''+str(persona.experiencia)+''',
                "'''+str(persona.entidadexperiencia)+'''",
                "'''+str(persona.inventario)+'''",
                "'''+str(persona.inventario2)+'''"
                )
        ''')
        for recogible in persona.inventario:
            peticion = '''
            INSERT INTO recogible
            VALUES(
                NULL,
                '''+str(persona.entidad)+''',
                "'''+str(recogible.posx)+'''",
                "'''+str(recogible.posy)+'''",
                "'''+str(recogible.color)+'''"
            )
            '''
        

            cursor.execute(peticion)
            
        for recogible2 in persona.inventario2:
            peticion2 = '''
            INSERT INTO recogible2
            VALUES(
                NULL,
                '''+str(persona.entidad)+''',
                '''+str(persona.direccion)+''',
                '''+str(persona.velocidad)+'''
            )
            '''
        

            cursor.execute(peticion2)
    
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

    cursor.execute('''
            SELECT *
            FROM jugadores
            ''')
    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        #print(fila)
        persona= Persona()
        persona.posx = fila[1]
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad= fila[6]
        persona.velocidad = fila[7]
        persona.energia = fila[8]
        persona.descanso = fila[9]
        persona.entidadenergia= fila[10]
        persona.entidaddescanso = fila[11]
        persona.experiencia = fila[12]
        persona.entidadexperiencia = fila[13]
        persona.nivelexperiencia = fila [14]

        cursor2 = conexion.cursor()
        nuevapeticion = '''
            SELECT *
            FROM recogible
            WHERE persona = '''+persona.entidad+'''
            '''
        
        cursor2.execute(nuevapeticion)
        while True:
            fila2 = cursor2.fetchone()
            if fila2 is None:
                break
            nuevorecogible = Recogible()
            nuevorecogible.posx = fila2[2]
            nuevorecogible.posy = fila2[3]
            nuevorecogible.color = fila2[4]
            persona.inventario.append(nuevorecogible)

        cursor3 = conexion.cursor()
        nuevapeticion = '''
            SELECT *
            FROM recogible2
            WHERE persona = '''+persona.entidad+'''
            '''
        
        cursor3.execute(nuevapeticion)
        while True:
            fila3 = cursor3.fetchone()
            if fila2 is None:
                break
            nuevorecogible2 = Recogible2()
            nuevorecogible2.direccion = fila3[2]
            nuevorecogible2.velocidad = fila3[3]
            persona.inventario.append(nuevorecogible2)    
        personas.append(persona)
    conexion.close()   
except sqlite3.Error as error:
    print("error al leer base de datos", error)
#En la colección introduzco instancias de personas
    print(len(personas))
if len(personas) == 0:
    numeropersonas = 200
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




