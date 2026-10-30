# LIBRERIAS A IMPORTAR/NECESITAMOS
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk,Label, Button, Entry, Frame, Toplevel
from io import BytesIO
from PIL import Image, ImageTk
import string
import os
import shutil
import re
# ================================================================================================
# VARIABLES GLOBALES
# ================================================================================================
indice_edicion = None
imagenes_cargadas = []
# ================================================================================================
# BASE DE DATOS 
# ================================================================================================
conexion = sqlite3.connect("Trabajo_FINAL_V4.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
# TABLA DE PERSONAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    foto BLOB
)""")

# TABLA DE IMAGENES
cursor.execute("""CREATE TABLE IF NOT EXISTS imagenes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
formato TEXT NOT NULL,
contenido BLOB NOT NULL,
id_empleado INTEGER)""")

# TABLA DE ENTREVISTAS (Saque el UNIQUE de DNI, porque una persona puede tener muchas entrevistas, POR LAS DUDAS LO DEJAMOS ASI)
cursor.execute("""CREATE TABLE IF NOT EXISTS entrevistas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
entrevista TEXT NOT NULL,
dni INTEGER NOT NULL,
nombre_profecional TEXT NOT NULL,
fecha TEXT NOT NULL)""")


conexion.commit()
# =================================================================================================================
# PALETA DE COLORES (VIEJA Y NUEVA) 
# ==================================================================================================================
ROJO = "#E3000F"
AMARILLO = "#FCAF17"
NEGRO = "#0a0a0a"
VERDE = "#00FF00"
GRIS = "#222222"
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_AZULADO = "#008080"
VERDE_TERMINAL = "#00FF00"
# NUEVOS COLORES, MODO CLARO , ASI LLAMA LA ATENCION Y DA BUENAS VIBRAS
#Fondo General (Ventana): 
GRIS_NIEBLA="#F4F7F6" #(Gris niebla, muy suave y descansa la vista). ---- FONDO
#Paneles/Tarjetas: 
BLANCO = "#FFFFFF" #(Blanco puro, para que resalte el contenido). ---- RECUADROS
#Textos Principales: 
GRIS_AZULADO = "#2C3E50" #(Gris azulado muy oscuro, más amigable que el negro). --- BANNER, Títulos, nombres de personas, etc
#Textos Secundarios:
GRIS_MEDIO ="#7F8C8D" #(Gris medio).
#Color de Acento (Botones):
AZUL_SERENO= "#4A90E2" #(Azul sereno).
#Color de Éxito/Progreso:
VERDE_AZULADO="#26A69A" #(Verde azulado/Teal).
# ==================================================================================================================
#                                                              VENTANA PRINCIPAL
# ===================================================================================================================
ventana = tk.Tk()
ventana.title("✚ MEDTRACK")
ventana.geometry("1000x700") 
ventana.config(bg=GRIS_NIEBLA) #FONDO DE PANTALLA PARA LA APP
# =====================================================================================================================================
#                                                           Banner para el titulo
# =====================================================================================================================================

banner = tk.Frame(ventana,bg=AZUL_SERENO, height=70) # FONDO PARA EL BANNER
banner.pack(side="bottom",fill="x") # SE EXPANDE EN X, EN EL ANCHO
banner.pack_propagate(False) # FALSO PARA QUE NO SE PROPAGUE
# GUARDE EL LABEL EN UNA VARIABLE ASI EL MODO OSCURO PUEDE CAMBIARLE EL COLOR
banner_label = tk.Label(banner, text="✚ MEDTRACK", bg=AZUL_SERENO, fg=BLANCO, font=("Arial", 20, "bold"))
banner_label.pack(pady=18) 

# =====================================================================================================================================
#                                                         FRAME PARA BOTONERA Y BOTONES  
# ======================================================================================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn.pack(side="top", fill="x", padx=15, pady=10) 
tk.Button(frame_btn, text="Agregar",bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar", bg=VERDE_AZULADO, fg="white", width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar", bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
# ======================================================================================================================================
#                                                               FORMULARIO
# ======================================================================================================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top",fill="x", padx=15, pady=10)
# GUARDE LOS LABELS EN VARIABLES PARA QUE EL MODO OSCURO LES CAMBIE EL COLOR
label_nombre = tk.Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA,fg=GRIS_AZULADO)
label_nombre.grid(row=0, column=0, sticky="e", padx=5)
entry_nombre = tk.Entry(frame_form, width=22)
entry_nombre.grid(row=0, column=1, padx=5, pady=3)

label_apellido = tk.Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA,fg =GRIS_AZULADO)
label_apellido.grid(row=0, column=2, sticky="e", padx=5)
entry_apellido = tk.Entry(frame_form, width=22)
entry_apellido.grid(row=0, column=3, padx=5, pady=3)

label_dni = tk.Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO)
label_dni.grid(row=0, column=4, sticky="e", padx=5)
entry_dni = tk.Entry(frame_form, width=15)
entry_dni.grid(row=0, column=5, padx=5, pady=3)
# ======================================================================================================================================
#                                                        Cuerpo principal (PANTALLA PRINCIPAL)
# ======================================================================================================================================

cuerpo = tk.Frame(ventana,bg = GRIS_NIEBLA) # este FRAME es para el cuerpo, es decir con esto puedo poner la listbox y foto para que funcione, por desgracia al usar pack hay que usar Frame
cuerpo.pack(fill="both", expand=True, padx=15, pady=10)
# ======================================================================================================================================
#                                                               VISOR DE FOTOS 
# ======================================================================================================================================
frame_foto = tk.Frame(cuerpo, bg=BLANCO, relief="solid", bd=1) #BORDEADO PARA QUE QUEDE MAS PROFESIONAL
frame_foto.pack(side="left", fill="both", expand=True, padx=(0, 15))
frame_foto.pack_propagate(False) # NO SE PROPAGA
visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Arial", 14))
visor_foto.pack(expand=True, fill="both")
# ======================================================================================================================================
#                                                   LISTBOX PARA QUE SE PUEDA VER A LA PERSONA
# ======================================================================================================================================
frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO,relief="solid", bd=1)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)
# GUARDE EL TITULO EN UNA VARIABLE ASI EL MODO OSCURO LE CAMBIA EL COLOR
titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Arial", 12, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)

scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")

# GUARDE LA LISTA EN UNA VARIABLE PARA APLICARLE EL TEMA (antes no existia la variable)
lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set, font=("Arial", 11), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
lista_personas.pack(side="left", fill="both", expand=True)
scroll.config(command=lista_personas.yview)

# =======================================================================================================================================
#                                                              MODO OSCURO
# =======================================================================================================================================

tema_oscuro = False

def aplicar_tema():
    global tema_oscuro
    tema_oscuro = not tema_oscuro # Cambia el estado (si es True lo hace False, y viceversa)

    if tema_oscuro:
        # COLORES DEL MODO OSCURO
        fondo_general = "#111111"
        panel = "#1B1B1B"
        panel_2 = "#202020"
        texto = "#F5F5F5"
        texto_secundario = "#D9D9D9"
        fondo_banner = "#0D0D0D"
        boton_accion = "#1A1A1A"
        boton_fill = "#FFFFFF"   # Fondo del boton de la luna
        boton_text = "#000000"   # Color de la luna
        active_bg = "#EAEAEA"
        active_fg = "#000000"
        lista_bg = "#1B1B1B"
        lista_fg = "#F5F5F5"
    else:
        # COLORES DEL MODO CLARO
        fondo_general = GRIS_NIEBLA
        panel = BLANCO
        panel_2 = GRIS_AZULADO
        texto = GRIS_AZULADO
        texto_secundario = GRIS_MEDIO
        fondo_banner = AZUL_SERENO
        boton_accion = VERDE_AZULADO
        boton_fill = "#111111"
        boton_text = "#FFFFFF"
        active_bg = "#333333"
        active_fg = "#FFFFFF"
        lista_bg = BLANCO
        lista_fg = GRIS_AZULADO

    # Aplicamos los colores a los contenedores grandes
    ventana.config(bg=fondo_general)
    banner.config(bg=fondo_banner)
    frame_btn.config(bg=fondo_general)
    frame_form.config(bg=fondo_general)
    cuerpo.config(bg=fondo_general)
    
    # Aplicamos a las tarjetas y textos
    frame_foto.config(bg=panel)
    visor_foto.config(bg=panel, fg=texto_secundario)
    
    frame_lista.config(bg=panel_2)
    titulo_lista.config(bg=panel_2, fg="white" if tema_oscuro else BLANCO)
    lista_personas.config(bg=lista_bg, fg=lista_fg, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    
    banner_label.config(bg=fondo_banner, fg="white")

    # Aplicamos a los Labels del formulario
    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=fondo_general, fg=texto)
            
    # Aplicamos a los Entry del formulario
    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(bg=lista_bg, fg=lista_fg, insertbackground=lista_fg)

    # Aplicamos a los botones
    for widget in frame_btn.winfo_children():
        if isinstance(widget, tk.Button) and widget is not btn_tema:
            widget.config(
                bg=boton_accion,
                fg="white",
                activebackground=VERDE_TERMINAL if not tema_oscuro else "#444444",
                activeforeground="white"
            )

    # Aplicamos al boton de la luna
    btn_tema.config(
        bg=boton_fill,
        fg=boton_text,
        activebackground=active_bg,
        activeforeground=active_fg
    )

# Creamos el botón de la luna (Movido ANTES de aplicar_tema para que no de error)
btn_tema = tk.Button(
    frame_btn,
    text="☾",
    command=aplicar_tema,
    bg="#111111",
    fg="#FFFFFF",
    font=("Arial", 18, "bold"),
    width=3,
    height=1,
    relief="flat",
    bd=0,
    cursor="hand2"
)
btn_tema.pack(side="right", padx=5)
# =======================================================================================================================================
#                                                       # FUNCIONES AUXILIARES
# ======================================================================================================================================

def comprobar(i_del_for,entry_,orden):
    variable=entry_.get()
    if variable=="":
        return i_del_for[orden]
    else:
        return variable

def comprobar_fecha(entry_fecha):
    fecha=entry_fecha.get()
    for i in string.punctuation:
        fecha=fecha.replace(i,"/")
    return str(fecha)
# ======================================================================================================================================
#                                                          VENTANA PARA ENTREVISTAS
# ======================================================================================================================================

def new_entrevista():
    entrevista=text_entrevista.get("1.0",tk.END)
    dni=entry_dni.get()
    nom_profecional=entry_nombre_profecional.get()
    fecha=comprobar_fecha(entry_fecha)
    cursor.execute("INSERT INTO entrevistas (entrevista,dni,nombre_profecional,fecha) VALUES (?,?,?,?)",(entrevista,dni,nom_profecional,fecha))
    conexion.commit()
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
        dato=f"ID: {i[0]} // Fecha: {i[4]} // DNI: {i[2]} // Profecional: {i[3]} // Entrevista: {i[1]}"
        lista_entrevistas.insert(tk.END, dato)

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


def abrir_ventana_entrevistas():
    # ACA CREO LA VENTANA EMERGENTE PARA ENTREVISTAS
    ventana_entrevistas = tk.Toplevel(ventana) 
    ventana_entrevistas.title("Entrevistas")
    ventana_entrevistas.geometry("1000x700")
    #tuve problemas con un par de variables asi que las defino global para enparcharlo
    global lista_entrevistas, text_entrevista, entry_dni, entry_nombre_profecional, entry_fecha









# Esto abre entrevistas
tk.Button(frame_btn, text="Entrevistas",command=abrir_ventana_entrevistas,bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)
ventana.mainloop()
