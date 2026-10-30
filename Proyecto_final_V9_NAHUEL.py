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
# TABLA DE ENTREVISTAS
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
GRIS_NIEBLA="#F4F7F6" 
BLANCO = "#FFFFFF" 
GRIS_AZULADO = "#2C3E50" 
GRIS_MEDIO ="#7F8C8D" 
AZUL_SERENO= "#4A90E2" 
VERDE_AZULADO="#26A69A" 

# ==================================================================================================================
# VENTANA PRINCIPAL
# ===================================================================================================================
ventana = tk.Tk()
ventana.title("✚ MEDTRACK")
ventana.geometry("1000x700") 
ventana.config(bg=GRIS_NIEBLA)

# =====================================================================================================================================
# Banner para el titulo
# =====================================================================================================================================
banner = tk.Frame(ventana,bg=AZUL_SERENO, height=70)
banner.pack(side="bottom",fill="x")
banner.pack_propagate(False)
banner_label = tk.Label(banner, text="✚ MEDTRACK", bg=AZUL_SERENO, fg=BLANCO, font=("Arial", 20, "bold"))
banner_label.pack(pady=18) 
# =======================================================================================================================================
# FUNCIONES PRINCIPALES
# =======================================================================================================================================

def refrescar_lista():
    lista_personas.delete(0, tk.END)
    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")
    for nombre, apellido, dni in cursor.fetchall():
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")
def mostrar_foto(dni):
    cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if fila and fila[0]:
        try:
            img = Image.open(BytesIO(fila[0]))
            img.thumbnail((300, 300))
            foto = ImageTk.PhotoImage(img)
            visor_foto.configure(image=foto, text="")
            visor_foto.image = foto
            return
        except Exception:
            pass
    visor_foto.configure(image="", text="Sin foto")
def al_seleccionar(event=None):
    sel = lista_personas.curselection()
    if not sel: return
    texto = lista_personas.get(sel[0])
    dni = int(texto.split("DNI ")[1])
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if not fila: return
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    entry_dni.delete(0, tk.END); entry_dni.insert(0, fila[2])
    mostrar_foto(dni)
    lista_personas.bind("<<ListboxSelect>>", al_seleccionar)

def agregar():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni_txt = entry_dni.get().strip()
    if not (nombre and apellido and dni_txt):
        messagebox.showwarning("Faltan datos", "Completa nombre, apellido y DNI.")
        return
    try:
        dni = int(dni_txt)
    except ValueError:
        messagebox.showerror("DNI invalido", "El DNI debe ser numerico.")
        return
    ruta = filedialog.askopenfilename(title="Foto (opcional)",
        filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])
    contenido = None
    if ruta:
        with open(ruta, "rb") as f:
            contenido = sqlite3.Binary(f.read())
    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)",
                       (nombre, apellido, dni, contenido))
        conexion.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Ya existe una persona con ese DNI.")
        return
    refrescar_lista()
    limpiar()
    messagebox.showinfo("OK", "Persona agregada.")

def eliminar():
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atención", "Selecciona o escribi un DNI.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Eliminar DNI {dni_txt}?"):
        return
    cursor.execute("DELETE FROM entrevistas WHERE dni_persona = ?", (dni_txt,))
    cursor.execute("DELETE FROM personas WHERE dni = ?", (dni_txt,))
    conexion.commit()
    refrescar_lista()
    limpiar()
    visor_foto.configure(image="", text="Sin foto")

def buscar():
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atencion", "Escribi de forma numerica un DNI para buscar.")
        return
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni_txt,))
    fila = cursor.fetchone()
    if not fila:
        messagebox.showinfo("Sin resultados", "No existe esa persona.")
        return
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    mostrar_foto(fila[2])
    # resaltar en lista
    for i in range(lista_personas.size()):
        if f"DNI {fila[2]}" in lista_personas.get(i):
            lista_personas.selection_clear(0, tk.END)
            lista_personas.selection_set(i)
            lista_personas.see(i)
            break

def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
# =====================================================================================================================================
# FRAME PARA BOTONERA Y BOTONES  
# ======================================================================================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn.pack(side="top", fill="x", padx=15, pady=10) 
tk.Button(frame_btn, text="Agregar",command=agregar,bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar",command=eliminar, bg=VERDE_AZULADO, fg="white", width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", command=buscar,bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar",command=limpiar, bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)

# ======================================================================================================================================
# FORMULARIO
# ======================================================================================================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top",fill="x", padx=15, pady=10)
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
# Cuerpo principal (PANTALLA PRINCIPAL)
# ======================================================================================================================================
cuerpo = tk.Frame(ventana,bg = GRIS_NIEBLA)
cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

# VISOR DE FOTOS 
frame_foto = tk.Frame(cuerpo, bg=BLANCO, relief="solid", bd=1)
frame_foto.pack(side="left", fill="both", expand=True, padx=(0, 15))
frame_foto.pack_propagate(False)
visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Arial", 14))
visor_foto.pack(expand=True, fill="both")

# LISTBOX PARA QUE SE PUEDA VER A LA PERSONA
frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO,relief="solid", bd=1)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)
titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Arial", 12, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)

scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")

lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set, font=("Arial", 11), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
lista_personas.pack(side="left", fill="both", expand=True)
scroll.config(command=lista_personas.yview)
# =======================================================================================================================================
# MODO OSCURO
# =======================================================================================================================================
tema_oscuro = False

def aplicar_tema():
    global tema_oscuro
    tema_oscuro = not tema_oscuro 

    if tema_oscuro:
        fondo_general = "#111111"
        panel = "#1B1B1B"
        panel_2 = "#202020"
        texto = "#F5F5F5"
        texto_secundario = "#D9D9D9"
        fondo_banner = "#0D0D0D"
        boton_accion = "#1A1A1A"
        boton_fill = "#FFFFFF"   
        boton_text = "#000000"   
        active_bg = "#EAEAEA"
        active_fg = "#000000"
        lista_bg = "#1B1B1B"
        lista_fg = "#F5F5F5"
    else:
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

    ventana.config(bg=fondo_general)
    banner.config(bg=fondo_banner)
    frame_btn.config(bg=fondo_general)
    frame_form.config(bg=fondo_general)
    cuerpo.config(bg=fondo_general)
    
    frame_foto.config(bg=panel)
    visor_foto.config(bg=panel, fg=texto_secundario)
    
    frame_lista.config(bg=panel_2)
    titulo_lista.config(bg=panel_2, fg="white" if tema_oscuro else BLANCO)
    lista_personas.config(bg=lista_bg, fg=lista_fg, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    
    banner_label.config(bg=fondo_banner, fg="white")

    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=fondo_general, fg=texto)
            
    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(bg=lista_bg, fg=lista_fg, insertbackground=lista_fg)

    for widget in frame_btn.winfo_children():
        if isinstance(widget, tk.Button) and widget is not btn_tema:
            widget.config(
                bg=boton_accion,
                fg="white",
                activebackground=VERDE_TERMINAL if not tema_oscuro else "#444444",
                activeforeground="white"
            )

    btn_tema.config(
        bg=boton_fill,
        fg=boton_text,
        activebackground=active_bg,
        activeforeground=active_fg
    )

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
# FUNCIONES AUXILIARES
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

def ver_list_entrevist(lista_widget):
    # Le paso la lista como parametro para no depender de una variable global porque el codigo de Mateo tenia problemas aca, no funcionaba bien aca.
    lista_widget.delete(0, tk.END)
    cursor.execute("SELECT * FROM entrevistas")
    for i in cursor.fetchall():
        dato=f"ID: {i[0]} // Fecha: {i[4]} // DNI: {i[2]} // Profecional: {i[3]} // Entrevista: {i[1]}"
        lista_widget.insert(tk.END, dato)

# ======================================================================================================================================
# VENTANA PARA EDITAR ENTREVISTAS
# ======================================================================================================================================
def pantalla_edit_entrevista(ventana_padre):# tuve varios problemas y puse un parametro para que funcione, no quedo otra
    # Recibe la ventana padre como parametro, monton de problemas no funcionaba o abria bien la ventana , directamente no me la reconocia bien me aparecio en rojo
    ventana_editar=tk.Toplevel(ventana_padre)
    ventana_editar.title("Editar entrevista")
    ventana_editar.geometry("300x200")
    label_id=tk.Label(ventana_editar,text="Ingrese el ID de la entrevista que desea editar")
    label_id.pack()
    entry_id=tk.Entry(ventana_editar)
    entry_id.pack()

    label_entrevista=tk.Label(ventana_editar, text="Entrevista")
    label_entrevista.pack()
    text_entrevista=tk.Text(ventana_editar)
    text_entrevista.pack()

    label_dni=tk.Label(ventana_editar, text="Dni")
    label_dni.pack()
    entry_dni=tk.Entry(ventana_editar)
    entry_dni.pack()

    label_nombre_profecional=tk.Label(ventana_editar, text="Nombre_profecional")
    label_nombre_profecional.pack()
    entry_nombre_profecional=tk.Entry(ventana_editar)
    entry_nombre_profecional.pack()

    label_fecha=tk.Label(ventana_editar, text="Fecha")
    label_fecha.pack()
    entry_fecha=tk.Entry(ventana_editar)
    entry_fecha.pack()

    def edit_entrevista():
        p_id=entry_id.get()
        cursor.execute("SELECT * FROM entrevistas")
        entrevistas=cursor.fetchall()
        for entrevista in entrevistas:
            if int(p_id)==entrevista[0]:
                entrevist=text_entrevista.get("1.0",tk.END)
                if entrevist.strip()=="":
                    entrevist=entrevista[1]
                dni=comprobar(entrevista,entry_dni,2)
                nom_profecional=comprobar(entrevista,entry_nombre_profecional,3)
                fecha=entry_fecha.get()
                if fecha=="":
                    fecha=entrevista[4]
                else:
                    fecha=comprobar_fecha(entry_fecha)
                conexion.execute("UPDATE entrevistas SET entrevista = ?, dni = ?, nombre_profecional = ?, fecha = ? WHERE id = ?",(entrevist,dni,nom_profecional,fecha,p_id))
                conexion.commit()
                break
        ver_list_entrevist(lista_entrevistas) 

    boton_edit_entrevista=tk.Button(ventana_editar,text="Editar entrevista",command=edit_entrevista)
    boton_edit_entrevista.pack()

# ==================================================================================================================================================================
# FUNCIONES DE LA VENTANA DE ENTREVISTAS (la que vendria a abrirse de la ventana principal)
# ==================================================================================================================================================================
def new_entrevista():
    entrevista=text_entrevista.get("1.0",tk.END)
    dni=entry_dni_entrevista.get()
    nom_profecional=entry_nombre_profecional.get()
    fecha=comprobar_fecha(entry_fecha)
    cursor.execute("INSERT INTO entrevistas (entrevista,dni,nombre_profecional,fecha) VALUES (?,?,?,?)",(entrevista,dni,nom_profecional,fecha))
    conexion.commit()
    ver_list_entrevist(lista_entrevistas)

def eliminar_entrevista():
    p_dni=entry_dni_entrevista.get()
    cursor.execute("DELETE FROM entrevistas WHERE dni = ?",(p_dni,))
    conexion.commit()
    ver_list_entrevist(lista_entrevistas)

def detalles_entrevsit(event=None):
    seleccion=lista_entrevistas.curselection()
    if seleccion:
        dato=lista_entrevistas.get(seleccion)
        datos=dato.split("//")

        ventana_detalle=tk.Toplevel(ventana)
        ventana_detalle.title("entrevista")
        ventana_detalle.geometry("300x200")

        label_dato_fecha=tk.Label(ventana_detalle,text=datos[1])
        label_dato_fecha.pack()
        label_dato_dni=tk.Label(ventana_detalle,text=datos[2])
        label_dato_dni.pack()
        label_dato_profecional=tk.Label(ventana_detalle,text=datos[3])
        label_dato_profecional.pack()

        text_dato_entrevista=tk.Text(ventana_detalle)
        text_dato_entrevista.pack()
        text_dato_entrevista.insert("1.0",datos[4])
        text_dato_entrevista.config(state=tk.DISABLED)

# Creo la ventana emergente para ENTREVISTAS, la creo aca y paso parametro para que funcione porque no me la reconoce
def abrir_ventana_entrevistas(ventana_padre):
    ventana_entrevistas = tk.Toplevel(ventana_padre) 
    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("400x650")
    
    global lista_entrevistas, text_entrevista, entry_dni_entrevista, entry_nombre_profecional, entry_fecha # declaro variables globales para que funcione, 
    # no se porque el codigo de Mateo no funcionaba bien aca. Aclaro que no digo que lo hizo mal. Capaz por la complejidad del codigo que revento Python
    
    lista_entrevistas=tk.Listbox(ventana_entrevistas)
    lista_entrevistas.pack()
    lista_entrevistas.bind("<<ListboxSelect>>",detalles_entrevsit)
    ver_list_entrevist(lista_entrevistas)

    label_entrevista=tk.Label(ventana_entrevistas, text="Entrevista")
    label_entrevista.pack()
    text_entrevista=tk.Text(ventana_entrevistas)
    text_entrevista.pack()

    label_dni=tk.Label(ventana_entrevistas, text="Dni")
    label_dni.pack()
    # LE CAMBIE EL NOMBRE A entry_dni_entrevista PARA QUE NO CHOQUE CON EL DE LA VENTANA PRINCIPAL porque reventaba, literalmente
    entry_dni_entrevista=tk.Entry(ventana_entrevistas)
    entry_dni_entrevista.pack()

    label_nombre_profecional=tk.Label(ventana_entrevistas, text="Nombre profesional")
    label_nombre_profecional.pack()
    entry_nombre_profecional=tk.Entry(ventana_entrevistas)
    entry_nombre_profecional.pack()

    label_fecha=tk.Label(ventana_entrevistas, text="fecha")
    label_fecha.pack()
    entry_fecha=tk.Entry(ventana_entrevistas)
    entry_fecha.pack()
            
    boton_new_entrevista=tk.Button(ventana_entrevistas,text="Nueva entrevista",command=new_entrevista)
    boton_new_entrevista.pack()

    # ESTE ES EL BOTON PARA ABRIR LA VENTANA DE EDITAR
    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
        
    boton_editar=tk.Button(ventana_entrevistas, text="editar_entrevista", command=abrir_editar)
    boton_editar.pack()

# ======================================================================================================================================
# BOTON PRINCIPAL QUE ABRE ENTREVISTAS
# ======================================================================================================================================
def abrir_desde_principal():
    abrir_ventana_entrevistas(ventana)

tk.Button(frame_btn, text="Entrevistas",command=abrir_desde_principal,bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO).pack(side="left", padx=5)


ventana.mainloop()
