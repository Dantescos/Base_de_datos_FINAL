#cargar entrevistas
#
import string
#
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import Label, Button, Entry, Frame, Toplevel

conexion = sqlite3.connect("Trabajo_FINAL.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""CREATE TABLE IF NOT EXISTS entrevistas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
entrevista TEXT NOT NULL,
dni INTEGER UNIQUE,
nombre_profecional TEXT NOT NULL,
fecha TEXT NOT NULL)""")
########################
def comprobar(i_del_for,entry_,orden):
    variable=entry_.get()
    if variable=="":
        print(i_del_for[orden])
        return i_del_for[orden]
    else:
        print(variable)
        return variable

def comprobar_fecha():
    fecha=entry_fecha.get()
    for i in string.punctuation:
        fecha=fecha.replace(i,"/")
    return str(fecha)
####################################
#CRUD entrevistas
def new_entrevista():
    entrevista=entry_entrevista.get()
    dni=entry_dni.get()
    nom_profecional=entry_nombre_profecional.get()
    fecha=comprobar_fecha()
    cursor.execute("INSERT INTO entrevistas (entrevista,dni,nombre_profecional,fecha) VALUES (?,?,?,?)",(entrevista,dni,nom_profecional,fecha))
    conexion.commit()
    
def edit_entrevista():
    p_dni=entry_dni.get()
    cursor.execute("SELECT * FROM entrevistas")
    entrevistas=cursor.fetchall()
    for entrevista in entrevistas:
        if p_dni in entrevista[2]:
            entrevist=comprobar(entrevista,entry_entrevista,1)
            dni=comprobar(entrevista,entry_dni,2)
            nom_profecional=comprobar(entrevista,entry_nombre_profecional,3)
            fecha=entry_fecha.get()
            if fecha=="":
                fecha=entrevista[4]
            else:
                fecha=comprobar_fecha()
            conexion.execute("UPDATE entrevistas SET entrevista = ?, dni = ?, nombre_profecional = ?, fecha = ? WHERE dni = ?",(entrevist,dni,nom_profecional,fecha,p_dni))
            conexion.commit()
            break
    
def eliminar_entrevista():
    p_dni=entry_dni.get()
    cursor.execute("DELETE FROM entrevistas WHERE dni = ?",(p_dni,))
    conexion.commit()

#############333
ventana = tk.Tk()
ventana.title("Prueba Multiprocessing")
ventana.geometry("400x650")

label_entrevista=tk.Label(ventana, text="entrevista")
label_entrevista.pack()
entry_entrevista=tk.Entry(ventana)
entry_entrevista.pack()

label_dni=tk.Label(ventana, text="dni")
label_dni.pack()
entry_dni=tk.Entry(ventana)
entry_dni.pack()

label_nombre_profecional=tk.Label(ventana, text="nombre_profecional")
label_nombre_profecional.pack()
entry_nombre_profecional=tk.Entry(ventana)
entry_nombre_profecional.pack()

label_fecha=tk.Label(ventana, text="fecha")
label_fecha.pack()
entry_fecha=tk.Entry(ventana)
entry_fecha.pack()

