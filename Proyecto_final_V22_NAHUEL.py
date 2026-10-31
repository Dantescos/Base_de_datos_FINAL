# LIBRERIAS A IMPORTAR/NECESITAMOS
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk,Label, Button, Entry, Frame, Toplevel,Listbox,font
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
conexion = sqlite3.connect("Trabajo_FINAL_V.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    foto BLOB)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS imagenes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
formato TEXT NOT NULL,
contenido BLOB NOT NULL,
id_empleado INTEGER)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS entrevistas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
entrevista TEXT NOT NULL,
dni INTEGER NOT NULL,
nombre_profecional TEXT NOT NULL,
fecha TEXT NOT NULL)""")
conexion.commit()

# =================================================================================================================
# PALETA DE COLORES 
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
# NUEVOS COLORES MODO CLARO
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
banner = tk.Frame(ventana,bg=AZUL_SERENO, height=80) # Aumente un poco la altura
banner.pack(side="bottom",fill="x")
banner.pack_propagate(False)
banner_label = tk.Label(banner, text="✚ MEDTRACK", bg=AZUL_SERENO, fg=BLANCO, font=("Segoe UI", 24, "bold")) # Letra mas grande
banner_label.pack(pady=20) 
# =======================================================================================================================================
# FUNCIONES PRINCIPALES PARA LA VENTANA PRINCIPAL
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
    cursor.execute("DELETE FROM entrevistas WHERE dni = ?", (dni_txt,))
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
# FRAME PARA BOTONERA Y BOTONES  PARA LA VENTANA PRINCIPAL
# ======================================================================================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn.pack(side="top", fill="x", padx=15, pady=10) 
tk.Button(frame_btn, text="Agregar",font=("Segoe UI", 12),command=agregar,bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar",font=("Segoe UI", 12),command=eliminar, bg=VERDE_AZULADO, fg="white", width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", font=("Segoe UI", 12),command=buscar,bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar",font=("Segoe UI", 12),command=limpiar, bg=VERDE_AZULADO, fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
# ======================================================================================================================================
# FORMULARIO PARA LA VENTANA PRINCIPAL
# ======================================================================================================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top",fill="x", padx=15, pady=10)

label_nombre = tk.Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA,fg=GRIS_AZULADO,font=("Segoe UI", 12))
label_nombre.grid(row=0, column=0, sticky="e", padx=5)
entry_nombre = tk.Entry(frame_form, width=22, font=("Segoe UI", 12)) # Letra mas grande en el entry
entry_nombre.grid(row=0, column=1, padx=5, pady=3)

label_apellido = tk.Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA,fg =GRIS_AZULADO,font=("Segoe UI", 12))
label_apellido.grid(row=0, column=2, sticky="e", padx=5)
entry_apellido = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_apellido.grid(row=0, column=3, padx=5, pady=3)

label_dni = tk.Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO,font=("Segoe UI", 12))
label_dni.grid(row=0, column=4, sticky="e", padx=5)
entry_dni = tk.Entry(frame_form, width=15, font=("Segoe UI", 12))
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
visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 18))
visor_foto.pack(expand=True, fill="both")

# LISTBOX PARA QUE SE PUEDA VER A LA PERSONA
frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO,relief="solid", bd=1)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)
titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)

scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")

lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
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

btn_tema = tk.Button(frame_btn,text="☾",command=aplicar_tema, bg="#111111",fg="#FFFFFF",font=("Segoe UI", 18, "bold"),width=3, height=1,relief="flat", bd=0,cursor="hand2")
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
    lista_widget.delete(0, tk.END)
    cursor.execute("SELECT * FROM entrevistas")
    for i in cursor.fetchall():
        dato=f"ID: {i[0]} // Fecha: {i[4]} // DNI: {i[2]} // Profecional: {i[3]} // Entrevista: {i[1]}"
        lista_widget.insert(tk.END, dato)

# ======================================================================================================================================
# VENTANA PARA EDITAR ENTREVISTAS
# ======================================================================================================================================
def pantalla_edit_entrevista(ventana_padre):
    ventana_editar=tk.Toplevel(ventana_padre)
    ventana_editar.title("Editar datos de entrevista")
    ventana_editar.geometry("800x650") # Un poco mas chica para que se vea mejor
    ventana_editar.config(bg=GRIS_NIEBLA)
    #Frame superior
    frame_editar_superior = tk.Frame(ventana_editar, bg=AZUL_PETROLEO, relief="solid", bd=1)
    frame_editar_superior.pack(side = "top" ,padx=20, pady=20, fill="x")

    Label(frame_editar_superior, text="ID de la entrevista a editar:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,font=("Segoe UI", 12)).grid(row=0,column=0)
    entry_id = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_id.grid(row=0,column=1)

    Label(frame_editar_superior, text="DNI:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,font=("Segoe UI", 12)).grid(row=1,column=0)
    entry_dni = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_dni.grid(row=1,column=1)
    
    Label(frame_editar_superior, text="Nombre del Profesional:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,font=("Segoe UI", 12)).grid(row=2,column=0)
    entry_nombre_profecional = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=2,column=1)
    Label(frame_editar_superior, text="Fecha:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,font=("Segoe UI", 12)).grid(row=3,column=0)
    entry_fecha = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_fecha.grid(row=3,column=1)
    #Frame medio
    frame_editar_medio =Frame(ventana_editar,bg=GRIS_NIEBLA,relief="solid",bd=1)
    frame_editar_medio.pack(fill="both",expand=True,padx=20, pady=10)
    Label(frame_editar_medio, text="Texto de la entrevista:",bg=AZUL_PETROLEO, fg=BLANCO_HUESO,font=("Segoe UI", 12)).pack(fill="x",side="top",padx=20,pady=5)
    text_entrevista = tk.Text(frame_editar_medio, bg=AZUL_SERENO,relief="solid", bd=1, font=("Segoe UI", 12)) 
    text_entrevista.pack(fill="both",expand=True,padx=15, pady=15)

    #########################################################################################################################
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
        ventana_editar.destroy() # Cierra la ventana al guardar
    #frame inferior y botones
    # Peso a los extremos para centrar los botones
    frame_editar_inferior =Frame(ventana_editar,bg=GRIS_NIEBLA)
    frame_editar_inferior.pack(fill="x",expand=True)
    frame_editar_inferior.grid_columnconfigure(0, weight=1)
    frame_editar_inferior.grid_columnconfigure(4, weight=1)
    boton_edit_entrevista= Button(frame_editar_inferior,text="Guardar cambios",font=("Segoe UI", 12, "bold"), command=edit_entrevista, bg=VERDE_AZULADO, fg=BLANCO, relief="flat", width=15)
    boton_edit_entrevista.grid(row=0,column=0)
# ==================================================================================================================================================================
# FUNCIONES DE LA VENTANA DE ENTREVISTAS
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
    seleccion=lista_entrevistas.curselection()
    if seleccion:
        dato=lista_entrevistas.get(seleccion)
        id_entrevista=dato.split("//")[0].replace("ID: ","").strip()
        cursor.execute("DELETE FROM entrevistas WHERE id = ?",(id_entrevista,))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)

def detalles_entrevsit(event=None):
    seleccion=lista_entrevistas.curselection()
    if seleccion:
        dato=lista_entrevistas.get(seleccion)
        datos=dato.split("//")

        ventana_detalle=tk.Toplevel(ventana)
        ventana_detalle.title("Detalle de entrevista")
        ventana_detalle.geometry("500x400")
        ventana_detalle.config(bg=GRIS_NIEBLA)

        frame_detalle = Frame(ventana_detalle, bg=BLANCO, relief="solid", bd=1)
        frame_detalle.pack(padx=20, pady=20, fill="both", expand=True)

        label_dato_fecha=tk.Label(frame_detalle, text=datos[1], bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 12, "bold"))
        label_dato_fecha.pack(pady=5)
        label_dato_dni=tk.Label(frame_detalle, text=datos[2], bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 12))
        label_dato_dni.pack()
        label_dato_profecional=tk.Label(frame_detalle, text=datos[3], bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 12))
        label_dato_profecional.pack(pady=10)

        text_dato_entrevista=tk.Text(frame_detalle, height=8, font=("Segoe UI", 12), relief="solid", bd=1)
        text_dato_entrevista.pack(fill="both", expand=True, padx=10, pady=10)
        text_dato_entrevista.insert("1.0",datos[4])
        text_dato_entrevista.config(state=tk.DISABLED)

# ======================================================================================================================================
# VENTANA EMERGENTE PARA ENTREVISTAS
# ======================================================================================================================================
def abrir_ventana_entrevistas(ventana_padre):
    ventana_entrevistas = tk.Toplevel(ventana_padre) 
    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("1000x800")
    ventana_entrevistas.config(bg=GRIS_NIEBLA)    
    
    global lista_entrevistas, text_entrevista, entry_dni_entrevista, entry_nombre_profecional, entry_fecha 

    # --- FRAME SUPERIOR (Formulario) ---
    frame_superior = Frame(ventana_entrevistas,bg=GRIS_AZULADO)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10) 

    label_dni = tk.Label(frame_superior, text="DNI:",bg=GRIS_AZULADO, fg=BLANCO,font=("Segoe UI", 12))
    label_dni.grid(row=0, column=0, sticky="e", padx=5, pady=10)
    entry_dni_entrevista=tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_dni_entrevista.grid(row=0, column=1, sticky="e", padx=5)

    label_nombre_profecional=tk.Label(frame_superior, text="Nombre del profesional:",bg=GRIS_AZULADO, fg=BLANCO,font=("Segoe UI", 12))
    label_nombre_profecional.grid(row=0, column=2, sticky="e", padx=5)
    entry_nombre_profecional=tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=0, column=3, sticky="e", padx=5)

    label_fecha=tk.Label(frame_superior, text="Fecha de entrevista:",bg=GRIS_AZULADO, fg=BLANCO,font=("Segoe UI", 12))
    label_fecha.grid(row=0, column=4, sticky="e", padx=5)
    entry_fecha=tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_fecha.grid(row=0, column=5, sticky="e", padx=5)

    # --- FRAMES DEL MEDIO (Lista y Texto) ---
    frame_medio_cuerpo = tk.Frame(ventana_entrevistas,bg =GRIS_NIEBLA)
    frame_medio_cuerpo.pack(fill="both", expand=True, padx=15, pady=10) 

    # LADO IZQUIERDO
    frame_lista_medio = Frame(frame_medio_cuerpo, bg=BLANCO,relief="solid", bd=1)
    frame_lista_medio.pack(side="left", fill="both", expand=True, padx=(0,10))
    tk.Label(frame_lista_medio, text="Historial de Entrevistas", bg=BLANCO, fg=GRIS_AZULADO,font=("Segoe UI", 13, "bold")).pack(pady=5)
    lista_entrevistas=tk.Listbox(frame_lista_medio,bg= BLANCO,fg=GRIS_AZULADO,selectbackground=AZUL_SERENO,selectforeground=BLANCO,bd = 0, font=("Segoe UI", 12))
    lista_entrevistas.pack(fill="both", expand=True, padx=5,pady=5)
    lista_entrevistas.bind("<<ListboxSelect>>",detalles_entrevsit)
    ver_list_entrevist(lista_entrevistas)

    # LADO DERECHO
    frame_texto= Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_texto.pack(side="left", fill="both", expand=True, padx=(10,0))
    label_entrevista=tk.Label(frame_texto, text="Anotaciones de la entrevista",bg=BLANCO, fg=GRIS_AZULADO,font=("Segoe UI", 13, "bold"))
    label_entrevista.pack(pady=5)
    text_entrevista=tk.Text(frame_texto,relief="solid", bd=1, bg=GRIS_NIEBLA, font=("Segoe UI", 12))
    text_entrevista.pack(fill="both", expand=True, padx=5, pady=5)

    # --- FRAME INFERIOR (Botones) ---
    frame_inferior = Frame(ventana_entrevistas,bg=GRIS_NIEBLA)
    frame_inferior.pack(side="bottom",fill="x", padx=20, pady=20) 
    
    # Peso a los extremos para centrar los botones
    frame_inferior.grid_columnconfigure(0, weight=1)
    frame_inferior.grid_columnconfigure(4, weight=1)
    
    # Botones centrados en las columnas 1, 2 y 3 (sin sticky para que queden al medio)
    boton_new_entrevista=tk.Button(frame_inferior,text="Nueva entrevista",command=new_entrevista,bg=VERDE_AZULADO, fg=BLANCO,font=("Segoe UI", 12, "bold"), relief="flat", width=15)
    boton_new_entrevista.grid(row=0,column=1, padx=10)    
    
    boton_eliminar_entrevista=tk.Button(frame_inferior,text="Eliminar entrevista",command=eliminar_entrevista,bg=ROJO, fg=BLANCO,font=("Segoe UI", 12, "bold"), relief="flat", width=15)
    boton_eliminar_entrevista.grid(row=0,column=2, padx=10)

    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
        
    boton_editar=tk.Button(frame_inferior, text="Editar entrevista", bg=AZUL_SERENO,fg=BLANCO,command=abrir_editar,font=("Segoe UI", 12, "bold"), relief="flat", width=15)
    boton_editar.grid(row=0,column=3,padx=10)

# ======================================================================================================================================
#                                                       VENTANA PARA PERFIL
# ======================================================================================================================================
def abrir_ventana_perfil():
    ventana_perfil = tk.Toplevel(ventana)
    ventana_perfil.title("PERFIL")
    ventana_perfil.geometry("1000x800")
    ventana_perfil.config(bg=GRIS_NIEBLA)

    frame_perfil = tk.Frame(ventana_perfil, bg=GRIS_NIEBLA)
    frame_perfil.pack(side="left", fill="y", padx=15, pady=10) 
    # ======================================================================================================================================
    #                                                      FORMULARIO PARA PERFIL
    # ======================================================================================================================================

    label_nombre = tk.Label(frame_perfil, text=" Nombre:", bg=GRIS_NIEBLA,fg=GRIS_AZULADO,font=("Segoe UI", 12))
    label_nombre.grid(row=0, column=0, sticky="e", padx=5)
    entry_nombre = tk.Entry(frame_perfil, width=22, font=("Segoe UI", 12)) # Letra mas grande en el entry
    entry_nombre.grid(row=0, column=1, padx=5, pady=3)

    label_apellido = tk.Label(frame_perfil, text=" Apellido:", bg=GRIS_NIEBLA,fg =GRIS_AZULADO,font=("Segoe UI", 12))
    label_apellido.grid(row=1, column=0, sticky="e", padx=5)
    entry_apellido = tk.Entry(frame_perfil, width=22, font=("Segoe UI", 12))
    entry_apellido.grid(row=1, column=1, padx=5, pady=3)

    label_dni = tk.Label(frame_perfil, text=" DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO,font=("Segoe UI", 12))
    label_dni.grid(row=2, column=0, sticky="e", padx=5)
    entry_dni = tk.Entry(frame_perfil, width=15, font=("Segoe UI", 12))
    entry_dni.grid(row=2, column=1, padx=5, pady=3)

    label_direccion = tk.Label(frame_perfil, text=" Direccion:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO,font=("Segoe UI", 12))
    label_direccion.grid(row=3, column=0, sticky="e", padx=5)
    entry_direccion = tk.Entry(frame_perfil, width=15, font=("Segoe UI", 12))
    entry_direccion.grid(row=3, column=1, padx=5, pady=3)

    label_f_nacimiento = tk.Label(frame_perfil, text=" Fecha de nacimiento:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO,font=("Segoe UI", 12))
    label_f_nacimiento.grid(row=4, column=0, sticky="e", padx=5)
    entry_f_nacimiento = tk.Entry(frame_perfil, width=15, font=("Segoe UI", 12))
    entry_f_nacimiento.grid(row=4, column=1, padx=5, pady=3)

    # VISOR DE FOTOS 
    frame_foto = Frame(ventana_perfil, bg=BLANCO, relief="solid", bd=1)
    frame_foto.pack(side="top", fill="both", expand=True, padx=(0, 15))
    frame_foto.pack_propagate(False)
    visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 18))
    visor_foto.pack(expand=True, fill="both")

    # LISTBOX PARA QUE SE PUEDA VER LAS ORDENES DE LA PERSONA
    frame_lista_perfil = tk.Frame(ventana_perfil, bg=GRIS_AZULADO,relief="solid", bd=1)
    frame_lista_perfil.pack(side="bottom", fill="both", expand=True, padx=10)
    titulo_lista_perfil = tk.Label(frame_lista_perfil, text="Ordenes registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold"))
    titulo_lista_perfil.pack(anchor="s", padx=5, pady=5)

    scroll_perfil = tk.Scrollbar(frame_lista_perfil, orient="vertical")
    scroll_perfil.pack(side="right", fill="y")

    lista_personas = tk.Listbox(frame_lista_perfil, yscrollcommand=scroll.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_personas.pack(side="left", fill="both", expand=True)
    scroll.config(command=lista_personas.yview)


    #BARRA PARA PDF



    #BARRA DE ESTADISTICA


# ======================================================================================================================================
# BOTONES PRINCIPALES QUE ABREN LAS VENTANAS
# ======================================================================================================================================
def abrir_desde_principal():
    abrir_ventana_entrevistas(ventana)

tk.Button(frame_btn, text="Entrevistas",command=abrir_desde_principal,bg=VERDE_AZULADO,fg="white",width=12,activebackground=VERDE_TERMINAL, activeforeground=NEGRO,font=("Segoe UI", 12)).pack(side="left", padx=5)
tk.Button(frame_btn,text="Perfil",command=abrir_ventana_perfil,bg=VERDE_AZULADO,fg=BLANCO,width=12,activebackground=VERDE_TERMINAL,activeforeground=NEGRO,font=("Segoe UI", 12)).pack(side="left", padx=5)


ventana.mainloop()
