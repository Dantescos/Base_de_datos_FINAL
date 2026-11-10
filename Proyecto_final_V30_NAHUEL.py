# ============================================================================
# BLOQUE 1: IMPORTACIONES
# Acá traemos todas las librerías que vamos a usar.
# ============================================================================
import sqlite3  # Para manejar la base de datos SQLite (crear tablas, insertar, borrar, etc.)
import tkinter as tk  # La librería de interfaces gráficas (ventanas, botones, etc.)
# De tkinter traemos cosas específicas que vamos a usar directo:
from tkinter import filedialog, messagebox, ttk, Label, Button, Entry, Frame, Toplevel, Listbox, font
from io import BytesIO  # BytesIO convierte bytes en un "archivo virtual" para que PIL lo pueda leer
from PIL import Image, ImageTk  # PIL (Pillow) abre, redimensiona y muestra imágenes
import string  # Lo usamos para sacar los signos de puntuación en comprobar_fecha()
import os  # Para manejar rutas y archivos (os.path.basename, os.remove, etc.)
import shutil  # Para copiar archivos (shutil.copy)
import re  # (Importado pero no usado en este archivo actualmente)

# ============================================================================
# BLOQUE 2: VARIABLES GLOBALES
# Las variables globales son las que se pueden usar desde cualquier función.
# ============================================================================
imagenes_cargadas = []  # Lista vacia donde guardamos las RUTAS de las imagenes que el usuario va agregando en el editor

# ============================================================================
# BLOQUE 3: BASE DE DATOS
# Acá conectamos a SQLite y creamos las tablas si no existen.
# ============================================================================
conexion = sqlite3.connect("Trabajo_FINAL.db")  # Abre (o crea) el archivo de base de datos
cursor = conexion.cursor()  # El cursor es el que ejecuta las consultas SQL
cursor.execute("PRAGMA foreign_keys = ON;")  # Activa las claves foráneas

# Crea la tabla "personas"
cursor.execute("""CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    foto BLOB)""")

# Crea la tabla "imagenes"
cursor.execute("""CREATE TABLE IF NOT EXISTS imagenes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
formato TEXT NOT NULL,
contenido BLOB NOT NULL,
id_empleado INTEGER)""")

# Crea la tabla "entrevistas" (¡Ojo! Agregamos nivel_avance aqui)
cursor.execute("""CREATE TABLE IF NOT EXISTS entrevistas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
entrevista TEXT NOT NULL,
dni INTEGER NOT NULL,
nombre_profecional TEXT NOT NULL,
fecha TEXT NOT NULL,
nivel_avance INTEGER DEFAULT 0
)""")
# Creo una tabla para que guarde la imagen de Sanca, mientras se tenga los archivos descargados la imagen vive aca, recomiendo tener todo descargado
cursor.execute("""CREATE TABLE IF NOT EXISTS recursos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT UNIQUE NOT NULL,
contenido BLOB)""")#con esto lo que hago es perdirle a la base de datos que es solo una sola imagen la que guarde y busque

conexion.commit()  # Guarda los cambios

# ============================================================================
# BLOQUE 4: PALETA DE COLORES
# ============================================================================
ROJO = "#E3000F"
AMARILLO = "#FCAF17"
NEGRO = "#0a0a0a"
GRIS = "#222222"
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_TERMINAL = "#00FF00"
# Colores del modo claro
GRIS_NIEBLA = "#F4F7F6"       
BLANCO = "#FFFFFF"             
GRIS_AZULADO = "#2C3E50"       
GRIS_MEDIO = "#7F8C8D"         
AZUL_SERENO = "#4A90E2"        
VERDE_AZULADO = "#26A69A"      

# ============================================================================
# BLOQUE 5: VENTANA PRINCIPAL
# ============================================================================
ventana = tk.Tk()                        # Crea la ventana principal
ventana.title("✚ MEDTRACK")              # Titulo de la ventana
ventana.geometry("1000x800")             # Tamaño inicial
ventana.config(bg=GRIS_NIEBLA)           # Color de fondo

# ============================================================================
# BLOQUE 6: BANNER (franja del titulo abajo)
# ============================================================================
banner = tk.Frame(ventana, bg=AZUL_SERENO, height=80)  # Frame de 80px
banner.pack(side="bottom", fill="x")                    # Pegado abajo
banner.pack_propagate(False)                            # No se achica
banner_label = tk.Label(banner,text="✚ MEDTRACK",bg=AZUL_SERENO, fg=BLANCO, font=("Segoe UI", 24, "bold"))
banner_label.pack(pady=20) # Centrado

# ============================================================================
# BLOQUE 7: FUNCIONES PRINCIPALES
# ============================================================================
def refrescar_lista():
    # Borra el Listbox y lo vuelve a llenar con los datos de la BD
    lista_personas.delete(0, tk.END)
    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")
    for nombre, apellido, dni in cursor.fetchall():
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")
def mostrar_foto(dni):
    # Busca la foto en la BD
    cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if fila and fila[0]:
        try:
            img = Image.open(BytesIO(fila[0]))
            img.thumbnail((300, 300))
            foto = ImageTk.PhotoImage(img)
            visor_foto.configure(image=foto, text="")
            visor_foto.image = foto  # Mantiene referencia
            return
        except Exception:
            pass
    visor_foto.configure(image="", text="Sin foto")
def al_seleccionar(event=None):
    # Se dispara al hacer click en la lista
    sel = lista_personas.curselection()
    if not sel: return
    texto = lista_personas.get(sel[0])
    dni = int(texto.split("DNI ")[1])
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if not fila: return
    # Rellena el formulario
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    entry_dni.delete(0, tk.END); entry_dni.insert(0, fila[2])
    mostrar_foto(dni)
def agregar():
    # Lee los datos
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
    # Pide foto (opcional)
    ruta = filedialog.askopenfilename(title="Foto (opcional)", filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])
    contenido = None
    if ruta:
        with open(ruta, "rb") as f:
            contenido = sqlite3.Binary(f.read())
    # Inserta en BD
    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)", (nombre, apellido, dni, contenido))
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
    # Borra entrevistas y luego persona
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
    # Resalta en lista
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

# ============================================================================
# BLOQUE 8: FRAME DE BOTONES PRINCIPALES
# ============================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn.pack(side="top", fill="x", padx=15, pady=10)

tk.Button(frame_btn, text="Agregar", font=("Segoe UI", 12), command=agregar, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar", font=("Segoe UI", 12), command=eliminar, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", font=("Segoe UI", 12), command=buscar, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar", font=("Segoe UI", 12), command=limpiar, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, relief="flat").pack(side="left", padx=5)

# ============================================================================
# BLOQUE 9: FORMULARIO PRINCIPAL
# ============================================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top", fill="x", padx=15, pady=10)

label_nombre = tk.Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_nombre.grid(row=0, column=0, sticky="e", padx=5)
entry_nombre = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_nombre.grid(row=0, column=1, padx=5, pady=3)

label_apellido = tk.Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_apellido.grid(row=0, column=2, sticky="e", padx=5)
entry_apellido = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_apellido.grid(row=0, column=3, padx=5, pady=3)

label_dni = tk.Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_dni.grid(row=0, column=4, sticky="e", padx=5)
entry_dni = tk.Entry(frame_form, width=15, font=("Segoe UI", 12))
entry_dni.grid(row=0, column=5, padx=5, pady=3)

# ============================================================================
# BLOQUE 10: CUERPO (VISOR Y LISTA PRINCIPAL)
# ============================================================================
cuerpo = tk.Frame(ventana, bg=GRIS_NIEBLA)
cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

frame_foto = tk.Frame(cuerpo, bg=BLANCO, relief="solid", bd=1)
frame_foto.pack(side="left", fill="both", expand=True, padx=(0, 15))
frame_foto.pack_propagate(False)
visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 18))
visor_foto.pack(expand=True, fill="both")

frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO, relief="solid", bd=1)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)
titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)

scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")

lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
lista_personas.pack(side="left", fill="both", expand=True)
scroll.config(command=lista_personas.yview)

# ============================================================================
# BLOQUE 11: MODO OSCURO
# ============================================================================
tema_oscuro = False
ventanas_secundarias = []

def actualizar_widget(widget, fondo, panel, texto, acento):
    clase = widget.winfo_class()

    if clase in ("Frame", "Labelframe"):
        widget.config(bg=fondo)
    elif clase == "Label":
        widget.config(bg=fondo, fg=texto)
    elif clase in ("Entry", "Text"):
        widget.config(bg=panel, fg=texto, insertbackground=texto)
    elif clase == "Listbox":
        widget.config(
            bg=panel,
            fg=texto,
            selectbackground=AZUL_SERENO,
            selectforeground=BLANCO,
        )
    elif clase in ("Button", "Menubutton"):
        widget.config(bg=acento, fg="white")

    for hijo in widget.winfo_children():
        actualizar_widget(hijo, fondo, panel, texto, acento)
def actualizar_ventanas_secundarias():
    if tema_oscuro:
        fondo = "#111111"
        panel = "#1B1B1B"
        texto = "#F5F5F5"
        acento = "#1A1A1A"
        boton_luna_bg = "#FFFFFF"
        boton_luna_fg = "#000000"
    else:
        fondo = GRIS_NIEBLA
        panel = BLANCO
        texto = GRIS_AZULADO
        acento = VERDE_AZULADO
        boton_luna_bg = "#111111"
        boton_luna_fg = "#FFFFFF"

    ventanas_secundarias[:] = [
        ventana_hija for ventana_hija in ventanas_secundarias
        if ventana_hija.winfo_exists()
    ]

    for ventana_hija in ventanas_secundarias:
        ventana_hija.config(bg=fondo)
        for widget in ventana_hija.winfo_children():
            actualizar_widget(widget, fondo, panel, texto, acento)

        boton_luna = getattr(ventana_hija, "boton_luna", None)
        if boton_luna and boton_luna.winfo_exists():
            boton_luna.config(bg=boton_luna_bg, fg=boton_luna_fg)
def agregar_boton_luna(ventana_hija):
    if ventana_hija not in ventanas_secundarias:
        ventanas_secundarias.append(ventana_hija)

    actualizar_ventanas_secundarias()
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
            widget.config(bg=boton_accion, fg="white", activebackground=VERDE_TERMINAL if not tema_oscuro else "#444444", activeforeground="white")

    btn_tema.config(bg=boton_fill, fg=boton_text, activebackground=active_bg, activeforeground=active_fg)
    actualizar_ventanas_secundarias()

btn_tema = tk.Button(frame_btn, text="☾", command=aplicar_tema, bg="#111111", fg="#FFFFFF", font=("Segoe UI", 18, "bold"), width=3, height=1, relief="flat", bd=0, cursor="hand2")
btn_tema.pack(side="right", padx=5)

# ============================================================================
# BLOQUE 12: FUNCIONES AUXILIARES
# ============================================================================
def comprobar(i_del_for, entry_, orden):
    # Si el Entry está vacío, devuelve el valor viejo de la BD
    variable = entry_.get()
    if variable == "":
        return i_del_for[orden]
    else:
        return variable

def comprobar_fecha(entry_fecha):
    # Reemplaza signos de puntuacion por "/"
    fecha = entry_fecha.get()
    for i in string.punctuation:
        fecha = fecha.replace(i, "/")
    return str(fecha)

def ver_list_entrevist(lista_widget):
    # Llena el Listbox de entrevistas
    lista_widget.delete(0, tk.END)
    cursor.execute("SELECT * FROM entrevistas")
    for i in cursor.fetchall():
        dato = f"ID: {i[0]} // Fecha: {i[4]} // DNI: {i[2]} // Profecional: {i[3]} // Entrevista: {i[1]}"
        lista_widget.insert(tk.END, dato)

# ============================================================================
# BLOQUE 13: VENTANA PARA EDITAR ENTREVISTA
# ============================================================================
def pantalla_edit_entrevista(ventana_padre):
    ventana_editar = tk.Toplevel(ventana_padre)
    ventana_editar.title("Editar datos de entrevista")
    ventana_editar.geometry("800x650")
    ventana_editar.config(bg=GRIS_NIEBLA)

    frame_editar_superior = tk.Frame(ventana_editar, bg=AZUL_PETROLEO, relief="solid", bd=1)
    frame_editar_superior.pack(side="top", padx=20, pady=20, fill="x")

    Label(frame_editar_superior, text="ID de la entrevista a editar:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=0, column=0)
    entry_id = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_id.grid(row=0, column=1)

    Label(frame_editar_superior, text="DNI:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=1, column=0)
    entry_dni = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_dni.grid(row=1, column=1)

    Label(frame_editar_superior, text="Nombre del Profesional:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=2, column=0)
    entry_nombre_profecional = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=2, column=1)

    Label(frame_editar_superior, text="Fecha:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=3, column=0)
    entry_fecha = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_fecha.grid(row=3, column=1)

    # NUEVO CAMPO: Nivel de avance para editar
    Label(frame_editar_superior, text="Nivel de avance (1-10):", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=4, column=0)
    entry_nivel_editar = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_nivel_editar.grid(row=4, column=1)

    frame_editar_medio = tk.Frame(ventana_editar, bg=GRIS_NIEBLA, relief="solid", bd=1)
    frame_editar_medio.pack(fill="both", expand=True, padx=20, pady=10)
    Label(frame_editar_medio, text="Texto de la entrevista:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).pack(fill="x", side="top", padx=20, pady=5)
    text_entrevista = tk.Text(frame_editar_medio, bg=AZUL_SERENO, relief="solid", bd=1, font=("Segoe UI", 12))
    text_entrevista.pack(fill="both", expand=True, padx=15, pady=15)

    def edit_entrevista():
        p_id = entry_id.get()
        if p_id == "": return
        cursor.execute("SELECT * FROM entrevistas")
        entrevistas = cursor.fetchall()
        for entrevista in entrevistas:
            if int(p_id) == entrevista[0]:
                # Toma texto nuevo o mantiene viejo
                entrevist = text_entrevista.get("1.0", tk.END)
                if entrevist.strip() == "":
                    entrevist = entrevista[1]
                dni = comprobar(entrevista, entry_dni, 2)
                nom_profecional = comprobar(entrevista, entry_nombre_profecional, 3)
                fecha = entry_fecha.get()
                if fecha == "":
                    fecha = entrevista[4]
                else:
                    fecha = comprobar_fecha(entry_fecha)
                # Toma nivel nuevo o mantiene viejo
                nivel = entry_nivel_editar.get()
                if nivel == "":
                    nivel = entrevista[5] 
                
                # UPDATE de todos los campos
                conexion.execute("UPDATE entrevistas SET entrevista = ?, dni = ?, nombre_profecional = ?, fecha = ?, nivel_avance = ? WHERE id = ?",
                                 (entrevist, dni, nom_profecional, fecha, nivel, p_id))
                conexion.commit()
                break
        ver_list_entrevist(lista_entrevistas)
        ventana_editar.destroy()

    frame_editar_inferior = tk.Frame(ventana_editar, bg=GRIS_NIEBLA)
    frame_editar_inferior.pack(fill="x", expand=True)
    frame_editar_inferior.grid_columnconfigure(0, weight=1)
    frame_editar_inferior.grid_columnconfigure(1, weight=1)
    boton_edit_entrevista = Button(frame_editar_inferior, text="Guardar cambios", font=("Segoe UI", 12, "bold"), command=edit_entrevista, bg=VERDE_AZULADO, fg=BLANCO, relief="flat", width=15)
    boton_edit_entrevista.grid(row=0, column=1)

# ============================================================================
# BLOQUE 14: FUNCIONES DE LA VENTANA DE ENTREVISTAS
# ============================================================================
def new_entrevista():
    entrevista = text_entrevista.get("1.0", tk.END).strip() # .strip() borra los enters de mas
    dni = entry_dni_entrevista.get()
    nom_profecional = entry_nombre_profecional.get()
    fecha = comprobar_fecha(entry_fecha)
    nivel = nivel_avance_var.get() # Toma el nivel del menu

    if entrevista == "" or dni == "" or nom_profecional == "":
        messagebox.showwarning("Faltan datos", "Complete la entrevista, DNI y Profesional.")
        return

    cursor.execute("INSERT INTO entrevistas (entrevista, dni, nombre_profecional, fecha, nivel_avance) VALUES (?,?,?,?,?)",
                   (entrevista, dni, nom_profecional, fecha, nivel))
    conexion.commit()
    ver_list_entrevist(lista_entrevistas)
def eliminar_entrevista():
    seleccion = lista_entrevistas.curselection()
    if seleccion:
        dato = lista_entrevistas.get(seleccion[0])
        id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()
        cursor.execute("DELETE FROM entrevistas WHERE id = ?", (id_entrevista,))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)
def detalles_entrevsit(event=None):
    seleccion = lista_entrevistas.curselection()
    if seleccion:
        dato = lista_entrevistas.get(seleccion[0])
        datos = dato.split("//")

        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Detalle de entrevista")
        ventana_detalle.geometry("500x400")
        ventana_detalle.config(bg=GRIS_NIEBLA)

        frame_detalle = Frame(ventana_detalle, bg=BLANCO, relief="solid", bd=1)
        frame_detalle.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame_detalle, text=datos[1], bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 12, "bold")).pack(pady=5)
        tk.Label(frame_detalle, text=datos[2], bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 12)).pack()
        tk.Label(frame_detalle, text=datos[3], bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 12)).pack(pady=10)

        text_dato_entrevista = tk.Text(frame_detalle, height=8, font=("Segoe UI", 12), relief="solid", bd=1)
        text_dato_entrevista.pack(fill="both", expand=True, padx=10, pady=10)
        text_dato_entrevista.insert("1.0", datos[4])
        text_dato_entrevista.config(state=tk.DISABLED)

# ============================================================================
# BLOQUE 15: VENTANA EMERGENTE DE ENTREVISTAS
# ============================================================================
def abrir_ventana_entrevistas(ventana_padre):
    ventana_entrevistas = tk.Toplevel(ventana_padre)
    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("1000x800")
    ventana_entrevistas.config(bg=GRIS_NIEBLA)

    global lista_entrevistas, text_entrevista, entry_dni_entrevista
    global entry_nombre_profecional, entry_fecha, nivel_avance_var
    
    nivel_avance_var = tk.StringVar(ventana_entrevistas)
    nivel_avance_var.set("5") # Valor por defecto

    frame_superior = Frame(ventana_entrevistas, bg=GRIS_AZULADO)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)

    # DNI
    tk.Label(frame_superior, text="DNI:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=10)
    entry_dni_entrevista = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_dni_entrevista.grid(row=0, column=1, sticky="e", padx=5)

    # Profesional
    tk.Label(frame_superior, text="Profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=0, column=2, sticky="e", padx=5)
    entry_nombre_profecional = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=0, column=3, sticky="e", padx=5)

    # Fecha
    tk.Label(frame_superior, text="Fecha:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=0, column=4, sticky="e", padx=5)
    entry_fecha = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_fecha.grid(row=0, column=5, sticky="e", padx=5)

    # Nivel de avance (Nota del 1 al 10)
    tk.Label(frame_superior, text="Nivel (1-10):", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=0, column=6, sticky="e", padx=5)
    opciones_nivel = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    menu_nivel = tk.OptionMenu(frame_superior, nivel_avance_var, *opciones_nivel)
    menu_nivel.grid(row=0, column=7, sticky="e", padx=5)

    frame_medio_cuerpo = tk.Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_medio_cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

    # LADO IZQUIERDO: lista
    frame_lista_medio = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_lista_medio.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(frame_lista_medio, text="Historial de Entrevistas", bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    lista_entrevistas = tk.Listbox(frame_lista_medio, bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO, bd=0, font=("Segoe UI", 12))
    lista_entrevistas.pack(fill="both", expand=True, padx=5, pady=5)
    lista_entrevistas.bind("<<ListboxSelect>>", detalles_entrevsit)
    ver_list_entrevist(lista_entrevistas)

    # LADO DERECHO: texto
    frame_texto = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_texto.pack(side="left", fill="both", expand=True, padx=(10, 0))
    tk.Label(frame_texto, text="Anotaciones de la entrevista", bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    text_entrevista = tk.Text(frame_texto, relief="solid", bd=1, bg=GRIS_NIEBLA, font=("Segoe UI", 12))
    text_entrevista.pack(fill="both", expand=True, padx=5, pady=5)

    frame_inferior = Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_inferior.pack(side="bottom", fill="x", padx=20, pady=20)

    frame_inferior.grid_columnconfigure(0, weight=1)
    frame_inferior.grid_columnconfigure(4, weight=1)

    tk.Button(frame_inferior, text="Nueva entrevista", command=new_entrevista, bg=VERDE_AZULADO, fg=BLANCO, font=("Segoe UI", 12, "bold"), relief="flat", width=15).grid(row=0, column=1, padx=10)
    tk.Button(frame_inferior, text="Eliminar entrevista", command=eliminar_entrevista, bg=ROJO, fg=BLANCO, font=("Segoe UI", 12, "bold"), relief="flat", width=15).grid(row=0, column=2, padx=10)

    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
    tk.Button(frame_inferior, text="Editar entrevista", bg=AZUL_SERENO, fg=BLANCO, command=abrir_editar, font=("Segoe UI", 12, "bold"), relief="flat", width=15).grid(row=0, column=3, padx=10)

    agregar_boton_luna(ventana_entrevistas)

# ============================================================================
# BLOQUE 15.5: FUNCION PARA ACTUALIZAR LA BARRA (AHORA ES GLOBAL)
# ============================================================================
def actualizar_barra_perfil(dni, barra, label):
    # Buscamos el promedio de las notas de ese paciente
    cursor.execute("SELECT AVG(nivel_avance) FROM entrevistas WHERE dni = ?", (dni,))
    promedio = cursor.fetchone()[0]
    
    if promedio is not None:
        # Si el promedio es 7.5, la barra va al 75%
        porcentaje = promedio * 10
        barra['value'] = porcentaje
        label.config(text=f"{porcentaje:.1f}%")
    else:
        # Si no tiene entrevistas, queda en 0
        barra['value'] = 0
        label.config(text="0%")

# ============================================================================
# BLOQUE 16: VENTANA DE PERFIL
# ============================================================================
def abrir_ventana_perfil():
    ventana_perfil = tk.Toplevel(ventana)
    ventana_perfil.title("PERFIL")
    ventana_perfil.geometry("1000x800")
    ventana_perfil.config(bg=GRIS_NIEBLA)

    frame_izquierdo = tk.Frame(ventana_perfil, bg=AZUL_PETROLEO)
    frame_izquierdo.pack(side="left", fill="y", padx=15, pady=15)

    # Nombre
    Label(frame_izquierdo, text=" Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_nombre_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_nombre_perfil.grid(row=0, column=1, padx=5, pady=3)
    entry_nombre_perfil.insert(0, entry_nombre.get())      # <-- precarga desde ventana principal

    # Apellido
    Label(frame_izquierdo, text=" Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=5)
    entry_apellido_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_apellido_perfil.grid(row=1, column=1, padx=5, pady=3)
    entry_apellido_perfil.insert(0, entry_apellido.get())      # <-- precarga desde ventana principal

    # DNI y Boton Cargar
    Label(frame_izquierdo, text=" DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=5)
    entry_dni_perfil = tk.Entry(frame_izquierdo, width=15, font=("Segoe UI", 12))
    entry_dni_perfil.grid(row=2, column=1, padx=5, pady=3)
    entry_dni_perfil.insert(0, entry_dni.get())      # <-- precarga desde ventana principal

    # Direccion
    Label(frame_izquierdo, text=" Direccion:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=5)
    entry_direccion = tk.Entry(frame_izquierdo, width=15, font=("Segoe UI", 12))
    entry_direccion.grid(row=3, column=1, padx=5, pady=3)

    # F. Nacimiento
    Label(frame_izquierdo, text=" Fecha de nacimiento:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", padx=5)
    entry_f_nacimiento = tk.Entry(frame_izquierdo, width=15, font=("Segoe UI", 12))
    entry_f_nacimiento.grid(row=4, column=1, padx=5, pady=3)

    # PDF (Placeholder)
    Label(frame_izquierdo, text=" Cargar pdfs aqui", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=10, column=1, sticky="e", padx=10)
    entry_pdf_perfil = tk.Entry(frame_izquierdo, font=("Segoe UI", 12))
    entry_pdf_perfil.grid(row=11, column=1, sticky="e", padx=10, pady=3)

    # BARRA DE PROGRESO REAL
    label_barra_progreso_perfil = tk.Label(frame_izquierdo, text="Progreso:", bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 12))
    label_barra_progreso_perfil.grid(row=12, column=0, sticky="e", padx=5, pady=10)

    barra_progreso = ttk.Progressbar(frame_izquierdo, orient="horizontal", length=150, mode="determinate")
    barra_progreso.grid(row=12, column=1, padx=5, pady=10)
    
    label_porcentaje = tk.Label(frame_izquierdo, text="0%", bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 12, "bold"))
    label_porcentaje.grid(row=13, column=1, sticky="w", padx=5)

    # --- FUNCION INTERNA PARA CARGAR EL PERFIL ---
    def cargar_perfil():
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            messagebox.showwarning("Atención", "Escriba un DNI")
            return
            
        cursor.execute("SELECT nombre, apellido FROM personas WHERE dni = ?", (dni_txt,))
        fila = cursor.fetchone()
        
        if fila:
            entry_nombre_perfil.delete(0, tk.END); entry_nombre_perfil.insert(0, fila[0])
            entry_apellido_perfil.delete(0, tk.END); entry_apellido_perfil.insert(0, fila[1])
            # Llamamos a la funcion global que calcula el promedio
            actualizar_barra_perfil(dni_txt, barra_progreso, label_porcentaje)
        else:
            messagebox.showinfo("Error", "No existe ese DNI.")

    # Boton para cargar perfil (ubicado al lado del DNI)
    boton_cargar_perfil = tk.Button(frame_izquierdo, text="Cargar", command=cargar_perfil, bg=VERDE_AZULADO, fg="white", font=("Segoe UI", 10))
    boton_cargar_perfil.grid(row=2, column=2, padx=5)

    # --- FRAME DERECHO ---
    frame_derecha = tk.Frame(ventana_perfil, bg=ROJO)
    frame_derecha.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)
    frame_foto_perfil = Frame(frame_derecha, bg=BLANCO, relief="solid", bd=1, height=350)
    frame_foto_perfil.pack(side="top", fill="both", expand=True, pady=(0, 10))
    frame_foto_perfil.pack_propagate(False)
    visor_foto_perfil = tk.Label(frame_foto_perfil, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 20))
    visor_foto_perfil.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    frame_lista_perfil = Frame(frame_derecha, bg=GRIS_AZULADO, relief="solid", bd=1)
    frame_lista_perfil.pack(fill="both", expand=True, side="bottom", pady=(0, 20))
    Label(frame_lista_perfil, text="Ordenes registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold")).pack(side="top", padx=10, pady=10)
    scroll_perfil = tk.Scrollbar(frame_lista_perfil, orient="vertical")
    scroll_perfil.pack(side="right", fill="y")
    lista_personas_perfil = Listbox(frame_lista_perfil, yscrollcommand=scroll_perfil.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_personas_perfil.pack(side="left", fill="both", expand=True)
    scroll_perfil.config(command=lista_personas_perfil.yview)
    agregar_boton_luna(ventana_perfil)

# ============================================================================
# BLOQUE 17: VENTANA DEL EDITOR DE FOTOS
# ============================================================================
def abrir_ventana_editor_fotos():
    ventana_editor_fotos = tk.Toplevel(ventana)
    ventana_editor_fotos.title("Editor de fotos")
    ventana_editor_fotos.geometry("500x600")
    ventana_editor_fotos.config(bg=GRIS_NIEBLA)

    frame_editor_fotos_superior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_superior.pack(side="top", fill="both", expand=True)

    visor_foto_perfil = tk.Label(frame_editor_fotos_superior, text="👤\nSin foto", bg=BLANCO, fg=NEGRO, relief="solid", bd=1, font=("Segoe UI", 20))
    visor_foto_perfil.pack(fill="both", expand=True, padx=10, pady=10)

    frame_lista_imgs = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_lista_imgs.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(frame_lista_imgs, text="Imágenes cargadas:", font=("Segoe UI", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(fill="x")
    lista_imagenes = tk.Listbox(frame_lista_imgs, height=6, font=("Segoe UI", 10))
    lista_imagenes.pack(fill="both", expand=True, pady=5)

    frame_editor_fotos_inferior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_inferior.pack(side="bottom", fill="x", pady=10)

    frame_editor_fotos_inferior.grid_columnconfigure(0, weight=1)
    frame_editor_fotos_inferior.grid_columnconfigure(3, weight=1)

    def mostrar_previa(ruta):
        try:
            imagen = Image.open(ruta).resize((180, 180))
            imagen_tk = ImageTk.PhotoImage(imagen)
            visor_foto_perfil.config(image=imagen_tk, text="")
            visor_foto_perfil.image = imagen_tk
        except Exception as e:
            print("Error al mostrar la imagen:", e)

    def agregar_imagen():
        ruta = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if not ruta: return
        imagenes_cargadas.append(ruta)
        lista_imagenes.insert(tk.END, os.path.basename(ruta))
        mostrar_previa(ruta)

    def eliminar_imagen():
        try:
            indice = lista_imagenes.curselection()[0]
        except IndexError:
            return
        del imagenes_cargadas[indice]
        lista_imagenes.delete(indice)
        visor_foto_perfil.config(image="", text="👤\nSin foto")
        visor_foto_perfil.image = None

    tk.Button(frame_editor_fotos_inferior, text="Añadir fotos", command=agregar_imagen, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12)).grid(row=0, column=1, padx=10)
    tk.Button(frame_editor_fotos_inferior, text="Eliminar fotos", command=eliminar_imagen, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12)).grid(row=0, column=2, padx=10)

    agregar_boton_luna(ventana_editor_fotos)
# ============================================================================
# BLOQUE 18: CARGAR IMAGEN DE SANCA
# ============================================================================
def cargar_imagen():
    #1. Pregunto si esta en la base de datos
    cursor.execute("SELECT 1 FROM recursos WHERE nombre=?",("sanca",))
    if cursor.fetchall():
        return True
    #2. Pregunto si esta, si existe esa imagen
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sanca.jpg")
    if not os.path.exists(ruta):
        return False
    #3. Si existe la imagen que la lea
    with open(ruta,"rb") as f: #guardo la imagen como una variable "f"
        imagen_sanca =sqlite3.Binary(f.read()) #aca le pido a la base de datos que lea la imagen, la imagen son bytes asi que lee esos bytes 
        cursor.execute('INSERT INTO recursos (nombre,contenido) VALUES(?,?)',("sanca",imagen_sanca))
        conexion.commit()
        return True
# ============================================================================
# BLOQUE 19: DERECHOS DE AUTOR
# ============================================================================
def abrir_ventana_autores():
    hay_imagen =cargar_imagen() #chequeo si la imagen existe
    ventana_autores = tk.Toplevel(ventana)
    ventana_autores.title("Licencia y autores de la aplicacion")
    ventana_autores.geometry("1000x800")
    ventana_autores.config(bg=GRIS_NIEBLA)
    canvas = tk.Canvas(ventana_autores, width=1000, height=800, highlightthickness=0) # esto sirve mucho mas que un frame como queria hacer al principio
    canvas.pack(fill="both", expand=True)
    # Imagen de fondo
    if hay_imagen:
        cursor.execute("SELECT contenido FROM recursos WHERE nombre =? ",("sanca",))
        fila = cursor.fetchone()
        img = Image.open(BytesIO(fila[0])).resize((1000,800))
        foto = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=foto)
        ventana_autores.fondo = foto
    else:
        canvas.configure(bg="black")  # sin imagen, fondo liso
        canvas.create_text(450, 60,text="AUTORES",fill=NEGRO,font=("Segoe UI", 28, "bold") )
        canvas.create_text(450, 110,text="EQUIPO DE DESARROLLO ",fill=NEGRO,font=("Segoe UI", 16, "bold"))
    nombres = ["Antonio Garcia",
        "Nahuel Villafañe",
        "Mateo Dabruzzo Wilczek",
        "Federico 'Fedelobo'",
        "Ignacio",
        "Thiago",
        "Pablo Laporta",
        "Fernando 'Master'",
        "Joaquin Arana",]

    y = 150
    for nombre in nombres:
        canvas.create_text(
            450, y,
            text=f" {nombre} ",
            fill=NEGRO,
            font=("Segoe UI", 14)
        )
        y += 28

    # Licencia
    y += 30
    canvas.create_text(
        450, y,
        text=" LICENCIA ",
        fill=NEGRO,
        font=("Segoe UI", 16, "bold")
    )

    y += 35
    canvas.create_text(450, y,text="© 2026 Equipo de programacion Sanca. Todos los derechos reservados.\n"
             "Queda prohibida la copia, modificación, distribución,\n"
             "ingeniería inversa y uso comercial sin autorización escrita.",fill=NEGRO,font=("Segoe UI", 12),
        justify="center",width=800)
    # Boton cerrar
    tk.Button(ventana_autores,text="Cerrar",command=ventana_autores.destroy,bg=VERDE_AZULADO,fg="white",font=("Segoe UI", 12, "bold")).place(relx=0.95, rely=0.95, anchor="se")
    agregar_boton_luna(ventana_autores)
# ============================================================================
# BLOQUE 20: BOTONES PRINCIPALES QUE ABREN LAS OTRAS VENTANAS
# ============================================================================
def abrir_desde_principal():
    abrir_ventana_entrevistas(ventana)
tk.Button(frame_btn, text="Entrevistas", command=abrir_desde_principal, bg=VERDE_AZULADO, fg="white", width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12)).pack(side="left", padx=5)
tk.Button(frame_btn, text="Perfil", command=abrir_ventana_perfil, bg=VERDE_AZULADO, fg=BLANCO, width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12)).pack(side="left", padx=5)
tk.Button(frame_btn, text="Editor de fotos", command=abrir_ventana_editor_fotos, bg=VERDE_AZULADO, fg=BLANCO, width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12)).pack(side="left", padx=5)
tk.Button(frame_btn, text="Autores",command=abrir_ventana_autores, bg=VERDE_AZULADO, fg=BLANCO, width=12, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12)).pack(side="left", padx=5)

# ============================================================================
# BLOQUE 21: INICIO DEL PROGRAMA
# ============================================================================
ventana.mainloop()
