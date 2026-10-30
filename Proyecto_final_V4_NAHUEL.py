# LIBRERIAS A IMPORTAR/NECESITAMOS
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk,Label, Button, Entry, Frame, Toplevel
from io import BytesIO
from tkinter import Label, Button, Entry, Frame, Toplevel
from PIL import Image, ImageTk
import string
from PIL import Image, ImageTk
import os
import shutil
import re
# ================================================================================================
# BASE DE DATOS (3 TABLAS, 1) CREA LA PERSONA, 2) CREA PARA ENTREVISTAS, 3) CREAR PARA IMAGENES
# ================================================================================================
conexion = sqlite3.connect("Trabajo_FINAL_V4.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    foto BLOB
)""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni_persona INTEGER NOT NULL,
    entrevistador TEXT NOT NULL,
    fecha TEXT NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (dni_persona) REFERENCES personas(dni)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS imagenes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
formato TEXT NOT NULL,
contenido BLOB NOT NULL,
id_empleado INTEGER)""")

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
tk.Label(banner, text="✚ MEDTRACK", bg=AZUL_SERENO, fg=BLANCO, font=("Arial", 20, "bold")).pack(pady=18) # Puse fuente ariel(lo comun, cualquier cosa lo vemos)
# =====================================================================================================================================
#                                                         FRAME PARA BOTONERA Y BOTONES  
# ======================================================================================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn.pack(side="top", fill="x", padx=15, pady=10) 
tk.Button(frame_btn, text="Agregar",bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar", bg=VERDE_AZULADO, fg="white", width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar", bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)
#tk.Button(frame_btn, text="Entrevistas", command= ventana_entrevista,bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)
# ======================================================================================================================================
#                                                               FORMULARIO
# ======================================================================================================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top",fill="x", padx=15, pady=10)
tk.Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA,fg=GRIS_AZULADO).grid(row=0, column=0, sticky="e", padx=5)
entry_nombre = tk.Entry(frame_form, width=22)
entry_nombre.grid(row=0, column=1, padx=5, pady=3)
tk.Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA,fg =GRIS_AZULADO).grid(row=0, column=2, sticky="e", padx=5)
entry_apellido = tk.Entry(frame_form, width=22)
entry_apellido.grid(row=0, column=3, padx=5, pady=3)
tk.Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO).grid(row=0, column=4, sticky="e", padx=5)
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
tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")
# =======================================================================================================================================
#                                                   VENTANA PARA ENTREVISTAS
# =======================================================================================================================================


ventana.mainloop()
