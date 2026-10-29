#cargar entrevistas
#
import string
#
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO
#from PIL import Image, ImageTk
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
        return i_del_for[orden]
    else:
        return variable

def comprobar_fecha():
    fecha=entry_fecha.get()
    for i in string.punctuation:
        fecha=fecha.replace(i,"/")
    return str(fecha)
####################################
#CRUD entrevistas
def new_entrevista():
    entrevista=text_entrevista.get("1.0",tk.END)
    dni=entry_dni.get()
    nom_profecional=entry_nombre_profecional.get()
    fecha=comprobar_fecha()
    cursor.execute("INSERT INTO entrevistas (entrevista,dni,nombre_profecional,fecha) VALUES (?,?,?,?)",(entrevista,dni,nom_profecional,fecha))
    conexion.commit()
    ver_list_entrevist()
    
def pantalla_edit_entrevista():
#voy a editar por ID porque es el unico numero que permanece inmutable
#se va a editar en un toplevel, en donde se pida el ID de la persona a la que se quiera editar
    ventana_editar=tk.Toplevel(ventana)
    ventana_editar.title("edit_entrevista")
    ventana_editar.geometry("300x200")
    label_id=tk.Label(ventana_editar,text="ingrese el ID de la entrevista que desea editar")
    label_id.pack()
    entry_id=tk.Entry(ventana_editar)
    entry_id.pack()

    label_entrevista=tk.Label(ventana_editar, text="entrevista")
    label_entrevista.pack()
    text_entrevista=tk.Text(ventana_editar)
    text_entrevista.pack()

    label_dni=tk.Label(ventana_editar, text="dni")
    label_dni.pack()
    entry_dni=tk.Entry(ventana_editar)
    entry_dni.pack()

    label_nombre_profecional=tk.Label(ventana_editar, text="nombre_profecional")
    label_nombre_profecional.pack()
    entry_nombre_profecional=tk.Entry(ventana_editar)
    entry_nombre_profecional.pack()

    label_fecha=tk.Label(ventana_editar, text="fecha")
    label_fecha.pack()
    entry_fecha=tk.Entry(ventana_editar)
    entry_fecha.pack()

    boton_edit_entrevista=tk.Button(ventana_editar,text="editar_entrevista",command=edit_entrevista)
    boton_edit_entrevista.pack()

    def edit_entrevista():
        p_id=entry_id.get()
        cursor.execute("SELECT * FROM entrevistas")
        entrevistas=cursor.fetchall()
        for entrevista in entrevistas:
            if int(p_id)==entrevista[0]:
                entrevist=comprobar(entrevista,text_entrevista,1)
                dni=comprobar(entrevista,entry_dni,2)
                nom_profecional=comprobar(entrevista,entry_nombre_profecional,3)
                fecha=entry_fecha.get()
                if fecha=="":
                    fecha=entrevista[4]
                else:
                    fecha=comprobar_fecha()
                conexion.execute("UPDATE entrevistas SET entrevista = ?, dni = ?, nombre_profecional = ?, fecha = ? WHERE dni = ?",(entrevist,dni,nom_profecional,fecha,p_id))
                conexion.commit()
                break
        ver_list_entrevist()
    
def eliminar_entrevista():
    p_dni=entry_dni.get()
    cursor.execute("DELETE FROM entrevistas WHERE dni = ?",(p_dni,))
    conexion.commit()
    ver_list_entrevist()

def ver_list_entrevist():
    lista_entrevistas.delete(0, tk.END)
    cursor.execute("SELECT * FROM entrevistas")
    for i in cursor.fetchall():
        dato=f"ID: {i[0]} // fecha: {i[4]} // DNI: {i[2]} // profecional: {i[3]} // entrevista: {i[1]}"
        lista_entrevistas.insert(tk.END, dato)
#############

def detalles_entrevsit(event=None):
    seleccion=lista_entrevistas.curselection()
    if seleccion:
        dato=lista_entrevistas.get(seleccion)
        datos=dato.split("//")

        ventana_entrevista=tk.Toplevel(ventana)
        ventana_entrevista.title("entrevista")
        ventana_entrevista.geometry("300x200")

        label_dato_fecha=tk.Label(ventana_entrevista,text=datos[1])
        label_dato_fecha.pack()
        label_dato_dni=tk.Label(ventana_entrevista,text=datos[2])
        label_dato_dni.pack()
        label_dato_profecional=tk.Label(ventana_entrevista,text=datos[3])
        label_dato_profecional.pack()

        text_dato_entrevista=tk.Text(ventana_entrevista)
        text_dato_entrevista.pack()
        text_dato_entrevista.insert("1.0",datos[4])
        text_dato_entrevista.config(state=tk.DISABLED)


#############
ventana = tk.Tk()
ventana.title("Prueba Multiprocessing")
ventana.geometry("400x650")

lista_entrevistas=tk.Listbox(ventana)
lista_entrevistas.pack()

lista_entrevistas.bind("<<ListboxSelect>>",detalles_entrevsit)

ver_list_entrevist()

label_entrevista=tk.Label(ventana, text="entrevista")
label_entrevista.pack()
text_entrevista=tk.Text(ventana)
text_entrevista.pack()

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

boton_new_entrevista=tk.Button(ventana,text="new_entrevista",command=new_entrevista)
boton_new_entrevista.pack()

boton_ventana_edit_entrevista=tk.Button(ventana,text="pantalla_edit_entrevista",command=pantalla_edit_entrevista)
boton_ventana_edit_entrevista.pack()

boton_eliminar_entrevista=tk.Button(ventana,text="eliminar_entrevista",command=eliminar_entrevista)
boton_eliminar_entrevista.pack()

ventana.mainloop()