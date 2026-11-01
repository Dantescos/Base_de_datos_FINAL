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
imagenes_cargadas = []  # Lista vacía donde guardamos las RUTAS de las imágenes que el usuario va agregando en el editor

# ============================================================================
# BLOQUE 3: BASE DE DATOS
# Acá conectamos a SQLite y creamos las tablas si no existen.
# ============================================================================
conexion = sqlite3.connect("Trabajo_FINAL_V.db")  # Abre (o crea) el archivo de base de datos
cursor = conexion.cursor()  # El cursor es el que ejecuta las consultas SQL
cursor.execute("PRAGMA foreign_keys = ON;")  # Activa las claves foráneas (para que las relaciones funcionen)

# Crea la tabla "personas" si no existe todavía:
# - id: número único autoincremental
# - nombre, apellido: texto obligatorio
# - dni: entero único (no puede haber 2 personas con el mismo DNI)
# - foto: binario grande (BLOB) para guardar la foto adentro de la base
cursor.execute("""CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    foto BLOB)""")

# Crea la tabla "imagenes" para guardar varias fotos por persona:
# - id_empleado: a qué persona pertenece (debería ser id de personas)
# - contenido: la imagen en binario (BLOB)
cursor.execute("""CREATE TABLE IF NOT EXISTS imagenes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
formato TEXT NOT NULL,
contenido BLOB NOT NULL,
id_empleado INTEGER)""")

# Crea la tabla "entrevistas" con los datos de cada entrevista:
# - entrevista: el texto largo de la entrevista
# - dni: de qué persona es
# - nombre_profecional: quién hizo la entrevista (¡ojo con la "c" de profesional!)
# - fecha: la fecha de la entrevista
cursor.execute("""CREATE TABLE IF NOT EXISTS entrevistas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
entrevista TEXT NOT NULL,
dni INTEGER NOT NULL,
nombre_profecional TEXT NOT NULL,
fecha TEXT NOT NULL)""")

conexion.commit()  # "Confirma" los cambios, o sea, los guarda realmente en el archivo .db

# ============================================================================
# BLOQUE 4: PALETA DE COLORES
# Son variables con códigos hexadecimales (#RRGGBB) de los colores que usamos.
# ============================================================================
ROJO = "#E3000F"
AMARILLO = "#FCAF17"
NEGRO = "#0a0a0a"
GRIS = "#222222"
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_TERMINAL = "#00FF00"
# Colores del modo claro (usados en la mayor parte de la interfaz)
GRIS_NIEBLA = "#F4F7F6"       # Fondo general clarito
BLANCO = "#FFFFFF"             # Fondo de paneles
GRIS_AZULADO = "#2C3E50"       # Texto y fondo de listas
GRIS_MEDIO = "#7F8C8D"         # Texto secundario (como "Sin foto")
AZUL_SERENO = "#4A90E2"        # Banner y acentos
VERDE_AZULADO = "#26A69A"      # Color de los botones

# ============================================================================
# BLOQUE 5: VENTANA PRINCIPAL
# Creamos la ventana raíz donde vive toda la app.
# ============================================================================
ventana = tk.Tk()                         # Crea la ventana principal
ventana.title("✚ MEDTRACK")               # Título que aparece arriba
ventana.geometry("1000x700")              # Tamaño inicial ancho x alto
ventana.config(bg=GRIS_NIEBLA)            # Color de fondo de la ventana

# ============================================================================
# BLOQUE 6: BANNER (franja del título abajo)
# Es la franja azul con el nombre "✚ MEDTRACK" que aparece abajo de la ventana.
# ============================================================================
banner = tk.Frame(ventana, bg=AZUL_SERENO, height=80)  # Un Frame (contenedor) de 80px de alto
banner.pack(side="bottom", fill="x")                    # Lo pega abajo y lo estira a todo el ancho
banner.pack_propagate(False)                            # Evita que el Frame se achique al contenido
banner_label = tk.Label(banner, text="✚ MEDTRACK", bg=AZUL_SERENO, fg=BLANCO, font=("Segoe UI", 24, "bold"))
banner_label.pack(pady=20)  # Lo centra con 20px de margen arriba y abajo

# ============================================================================
# BLOQUE 7: FUNCIONES PRINCIPALES
# Son las funciones que hacen la lógica de la ventana principal.
# ============================================================================

def refrescar_lista():
    # Borra todo el contenido del Listbox de personas y lo vuelve a llenar desde la BD
    lista_personas.delete(0, tk.END)  # Borra desde el primer elemento hasta el final
    # Trae todas las personas ordenadas por apellido y luego por nombre
    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")
    # cursor.fetchall() devuelve todas las filas; cada fila es una tupla (nombre, apellido, dni)
    for nombre, apellido, dni in cursor.fetchall():
        # Inserta en el Listbox el texto formateado
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")

def mostrar_foto(dni):
    # Busca en la BD la foto (BLOB) de la persona con ese DNI
    cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()  # Trae solo una fila (o None si no hay)
    if fila and fila[0]:  # Si existe la fila Y tiene foto cargada
        try:
            img = Image.open(BytesIO(fila[0]))  # Convierte los bytes en imagen
            img.thumbnail((300, 300))            # La achica a máximo 300x300 sin deformar
            foto = ImageTk.PhotoImage(img)       # La convierte a formato que Tkinter entiende
            visor_foto.configure(image=foto, text="")  # Pone la imagen en el visor y borra el texto
            visor_foto.image = foto               # ¡IMPORTANTE! Mantenemos una referencia o se pierde
            return                                # Sale de la función
        except Exception:
            pass  # Si falla al abrir la imagen, no hace nada y sigue abajo
    # Si no había foto o falló algo, muestra el texto "Sin foto" en el visor
    visor_foto.configure(image="", text="Sin foto")

def al_seleccionar(event=None):
    # Se dispara cuando el usuario hace click en una persona de la lista
    sel = lista_personas.curselection()  # Devuelve una tupla con los índices seleccionados
    if not sel: return  # Si no hay nada seleccionado, sale
    texto = lista_personas.get(sel[0])   # Toma el texto del elemento seleccionado
    dni = int(texto.split("DNI ")[1])    # Separa el texto por "DNI " y agarra el número
    # Busca los datos actuales de esa persona en la BD
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if not fila: return  # Si no existe (raro), sale
    # Rellena los Entry del formulario con los datos de la persona
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    entry_dni.delete(0, tk.END); entry_dni.insert(0, fila[2])
    mostrar_foto(dni)  # Muestra la foto de esa persona en el visor grande

def agregar():
    # Lee lo que hay en los 3 Entry y quita espacios al inicio/final con .strip()
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni_txt = entry_dni.get().strip()
    # Si alguno está vacío, muestra advertencia y sale
    if not (nombre and apellido and dni_txt):
        messagebox.showwarning("Faltan datos", "Completa nombre, apellido y DNI.")
        return
    try:
        dni = int(dni_txt)  # Convierte el DNI de texto a número
    except ValueError:
        # Si el usuario puso letras, avisa
        messagebox.showerror("DNI invalido", "El DNI debe ser numerico.")
        return
    # Abre un diálogo para que el usuario elija una foto (opcional)
    ruta = filedialog.askopenfilename(title="Foto (opcional)",
        filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])
    contenido = None
    if ruta:  # Si el usuario eligió una foto
        with open(ruta, "rb") as f:  # "rb" = read binary
            contenido = sqlite3.Binary(f.read())  # Lee los bytes y los convierte a BLOB
    try:
        # INSERT INTO: inserta una fila nueva en la tabla personas
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)",
                       (nombre, apellido, dni, contenido))
        conexion.commit()  # Guarda el cambio
    except sqlite3.IntegrityError:
        # Si el DNI ya existe (por el UNIQUE), avisa
        messagebox.showerror("Error", "Ya existe una persona con ese DNI.")
        return
    refrescar_lista()  # Vuelve a llenar la lista con el nuevo dato
    limpiar()          # Vuelve a poner los campos vacíos
    messagebox.showinfo("OK", "Persona agregada.")  # Confirma

def eliminar():
    # Toma el DNI que está en el entry
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atención", "Selecciona o escribi un DNI.")
        return
    # Pide confirmación antes de borrar
    if not messagebox.askyesno("Confirmar", f"¿Eliminar DNI {dni_txt}?"):
        return
    # Borra primero las entrevistas asociadas (para no dejar huérfanas)
    cursor.execute("DELETE FROM entrevistas WHERE dni = ?", (dni_txt,))
    # Después borra la persona
    cursor.execute("DELETE FROM personas WHERE dni = ?", (dni_txt,))
    conexion.commit()
    refrescar_lista()
    limpiar()
    visor_foto.configure(image="", text="Sin foto")  # Borra la foto del visor

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
    # Si la encuentra, rellena los campos
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    mostrar_foto(fila[2])
    # Recorre la lista para seleccionar visualmente el elemento encontrado
    for i in range(lista_personas.size()):  # size() devuelve cuántos elementos hay
        if f"DNI {fila[2]}" in lista_personas.get(i):
            lista_personas.selection_clear(0, tk.END)  # Deselecciona todo
            lista_personas.selection_set(i)             # Selecciona el encontrado
            lista_personas.see(i)                       # Hace scroll para que se vea
            break                                       # Sale del bucle

def limpiar():
    # Borra todo el contenido de los 3 Entry del formulario
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)

# ============================================================================
# BLOQUE 8: FRAME DE BOTONES
# Acá van los botones de acción principal.
# ============================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)  # Contenedor para los botones
frame_btn.pack(side="top", fill="x", padx=15, pady=10)  # Arriba, todo el ancho, con margen

# Botón "Agregar": llama a la función agregar()
tk.Button(frame_btn, text="Agregar", font=("Segoe UI", 12), command=agregar,
          bg=VERDE_AZULADO, fg="white", width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          relief="flat").pack(side="left", padx=5)

# Botón "Eliminar"
tk.Button(frame_btn, text="Eliminar", font=("Segoe UI", 12), command=eliminar,
          bg=VERDE_AZULADO, fg="white", width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          relief="flat").pack(side="left", padx=5)

# Botón "Buscar"
tk.Button(frame_btn, text="Buscar", font=("Segoe UI", 12), command=buscar,
          bg=VERDE_AZULADO, fg="white", width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          relief="flat").pack(side="left", padx=5)

# Botón "Limpiar"
tk.Button(frame_btn, text="Limpiar", font=("Segoe UI", 12), command=limpiar,
          bg=VERDE_AZULADO, fg="white", width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          relief="flat").pack(side="left", padx=5)

# ============================================================================
# BLOQUE 9: FORMULARIO (Nombre, Apellido, DNI)
# Usamos grid porque queremos que los campos queden alineados en una fila.
# ============================================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top", fill="x", padx=15, pady=10)

# Label "Nombre:" en la columna 0, alineado a la derecha (east)
label_nombre = tk.Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_nombre.grid(row=0, column=0, sticky="e", padx=5)
# Entry (campo de texto) en la columna 1
entry_nombre = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_nombre.grid(row=0, column=1, padx=5, pady=3)

# Label "Apellido:" en la columna 2
label_apellido = tk.Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_apellido.grid(row=0, column=2, sticky="e", padx=5)
# Entry apellido en la columna 3
entry_apellido = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_apellido.grid(row=0, column=3, padx=5, pady=3)

# Label "DNI:" en la columna 4
label_dni = tk.Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_dni.grid(row=0, column=4, sticky="e", padx=5)
# Entry DNI en la columna 5
entry_dni = tk.Entry(frame_form, width=15, font=("Segoe UI", 12))
entry_dni.grid(row=0, column=5, padx=5, pady=3)

# ============================================================================
# BLOQUE 10: CUERPO (visor de foto + lista de personas)
# Es la parte grande del medio de la ventana.
# ============================================================================
cuerpo = tk.Frame(ventana, bg=GRIS_NIEBLA)
cuerpo.pack(fill="both", expand=True, padx=15, pady=10)  # Ocupa todo el espacio libre

# --- VISOR DE FOTOS (panel izquierdo) ---
frame_foto = tk.Frame(cuerpo, bg=BLANCO, relief="solid", bd=1)  # borde sólido de 1px
frame_foto.pack(side="left", fill="both", expand=True, padx=(0, 15))  # Al lado izquierdo
frame_foto.pack_propagate(False)  # No achicar al contenido (mantiene el tamaño del pack)
# Label que muestra "👤\nSin foto" por defecto
visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 18))
visor_foto.pack(expand=True, fill="both")  # Se expande en todo el frame

# --- LISTA DE PERSONAS (panel derecho) ---
frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO, relief="solid", bd=1)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)
titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO,
                        fg=BLANCO, font=("Segoe UI", 15, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)  # anchor="w" lo pega a la izquierda (west)

# Scrollbar vertical para la lista
scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")  # Pegada a la derecha, todo el alto

# Listbox: caja con varios ítems seleccionables
lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set, font=("Segoe UI", 12),
                            bg=BLANCO, fg=GRIS_AZULADO,
                            selectbackground=AZUL_SERENO, selectforeground=BLANCO)
lista_personas.pack(side="left", fill="both", expand=True)
scroll.config(command=lista_personas.yview)  # Conecta la scrollbar con la lista

# ============================================================================
# BLOQUE 11: MODO OSCURO
# La variable global guarda si está activo o no.
# ============================================================================
tema_oscuro = False  # Al arrancar está apagado

def aplicar_tema():
    # global nos permite MODIFICAR la variable global desde adentro de la función
    global tema_oscuro
    tema_oscuro = not tema_oscuro  # Cambia entre True y False

    if tema_oscuro:
        # Paleta del MODO OSCURO
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
        # Paleta del MODO CLARO (los colores normales)
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

    # Ahora aplicamos los colores a cada widget
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

    # Recorre los widgets del formulario y les cambia el color
    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=fondo_general, fg=texto)
    # (loop separado por claridad, aunque se podría unir)
    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(bg=lista_bg, fg=lista_fg, insertbackground=lista_fg)

    # Recorre los botones del frame_btn y les cambia el color
    # (menos btn_tema, que tiene su propio color)
    for widget in frame_btn.winfo_children():
        if isinstance(widget, tk.Button) and widget is not btn_tema:
            widget.config(
                bg=boton_accion,
                fg="white",
                activebackground=VERDE_TERMINAL if not tema_oscuro else "#444444",
                activeforeground="white"
            )

    # Al botón del tema le aplicamos su propio color invertido
    btn_tema.config(bg=boton_fill, fg=boton_text,
                    activebackground=active_bg, activeforeground=active_fg)

# Botón ☾ (luna) para alternar modo oscuro
btn_tema = tk.Button(frame_btn, text="☾", command=aplicar_tema,
                     bg="#111111", fg="#FFFFFF", font=("Segoe UI", 18, "bold"),
                     width=3, height=1, relief="flat", bd=0, cursor="hand2")
btn_tema.pack(side="right", padx=5)  # Lo pega a la derecha del frame de botones

# ============================================================================
# BLOQUE 12: FUNCIONES AUXILIARES
# Funciones chiquitas que se usan en otras partes del código.
# ============================================================================
def comprobar(i_del_for, entry_, orden):
    # Si el Entry está vacío, devuelve el valor viejo de la BD (posición "orden")
    # Si tiene algo, devuelve ese algo
    variable = entry_.get()
    if variable == "":
        return i_del_for[orden]
    else:
        return variable

def comprobar_fecha(entry_fecha):
    # Toma el texto del entry y reemplaza TODOS los signos de puntuación por "/"
    # Ej: "12-05-2024" → "12/05/2024"
    fecha = entry_fecha.get()
    for i in string.punctuation:
        fecha = fecha.replace(i, "/")
    return str(fecha)

def ver_list_entrevist(lista_widget):
    # Llena el Listbox de entrevistas con los datos de la BD
    lista_widget.delete(0, tk.END)
    cursor.execute("SELECT * FROM entrevistas")
    # i es una tupla: (id, entrevista, dni, nombre_profecional, fecha)
    for i in cursor.fetchall():
        dato = f"ID: {i[0]} // Fecha: {i[4]} // DNI: {i[2]} // Profecional: {i[3]} // Entrevista: {i[1]}"
        lista_widget.insert(tk.END, dato)

# ============================================================================
# BLOQUE 13: VENTANA PARA EDITAR ENTREVISTA
# Es una Toplevel (ventana aparte) con el formulario de edición.
# ============================================================================
def pantalla_edit_entrevista(ventana_padre):
    ventana_editar = tk.Toplevel(ventana_padre)  # Crea ventana hija
    ventana_editar.title("Editar datos de entrevista")
    ventana_editar.geometry("800x650")
    ventana_editar.config(bg=GRIS_NIEBLA)

    # Frame superior con el formulario de edición
    frame_editar_superior = tk.Frame(ventana_editar, bg=AZUL_PETROLEO, relief="solid", bd=1)
    frame_editar_superior.pack(side="top", padx=20, pady=20, fill="x")

    # ID de la entrevista a editar
    Label(frame_editar_superior, text="ID de la entrevista a editar:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=0, column=0)
    entry_id = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_id.grid(row=0, column=1)

    # DNI
    Label(frame_editar_superior, text="DNI:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,
          font=("Segoe UI", 12)).grid(row=1, column=0)
    entry_dni = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_dni.grid(row=1, column=1)

    # Nombre del profesional
    Label(frame_editar_superior, text="Nombre del Profesional:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=2, column=0)
    entry_nombre_profecional = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=2, column=1)

    # Fecha
    Label(frame_editar_superior, text="Fecha:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,
          font=("Segoe UI", 12)).grid(row=3, column=0)
    entry_fecha = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_fecha.grid(row=3, column=1)

    # Frame medio con el texto largo
    frame_editar_medio = tk.Frame(ventana_editar, bg=GRIS_NIEBLA, relief="solid", bd=1)
    frame_editar_medio.pack(fill="both", expand=True, padx=20, pady=10)
    Label(frame_editar_medio, text="Texto de la entrevista:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).pack(fill="x", side="top", padx=20, pady=5)
    text_entrevista = tk.Text(frame_editar_medio, bg=AZUL_SERENO, relief="solid", bd=1, font=("Segoe UI", 12))
    text_entrevista.pack(fill="both", expand=True, padx=15, pady=15)

    def edit_entrevista():
        # Función interna que se ejecuta al apretar "Guardar cambios"
        p_id = entry_id.get()
        if p_id == "":  # Si no escribió ID, sale sin hacer nada
            return
        cursor.execute("SELECT * FROM entrevistas")
        entrevistas = cursor.fetchall()
        for entrevista in entrevistas:  # Recorre todas las entrevistas
            if int(p_id) == entrevista[0]:  # Si el ID coincide
                # Toma el texto nuevo; si está vacío, mantiene el viejo
                entrevist = text_entrevista.get("1.0", tk.END)
                if entrevist.strip() == "":
                    entrevist = entrevista[1]
                # Los demás campos también: si están vacíos, mantienen el viejo
                dni = comprobar(entrevista, entry_dni, 2)
                nom_profecional = comprobar(entrevista, entry_nombre_profecional, 3)
                fecha = entry_fecha.get()
                if fecha == "":
                    fecha = entrevista[4]
                else:
                    fecha = comprobar_fecha(entry_fecha)
                # UPDATE: actualiza la fila en la BD
                conexion.execute("UPDATE entrevistas SET entrevista = ?, dni = ?, nombre_profecional = ?, fecha = ? WHERE id = ?",
                                 (entrevist, dni, nom_profecional, fecha, p_id))
                conexion.commit()
                break  # Sale del loop
        ver_list_entrevist(lista_entrevistas)  # Refresca la lista del padre
        ventana_editar.destroy()  # Cierra la ventana

    # Frame inferior con el botón de guardar
    frame_editar_inferior = tk.Frame(ventana_editar, bg=GRIS_NIEBLA)
    frame_editar_inferior.pack(fill="x", expand=True)
    # Peso en columnas 0 y 1 para centrar el botón de la columna 1
    frame_editar_inferior.grid_columnconfigure(0, weight=1)
    frame_editar_inferior.grid_columnconfigure(1, weight=1)
    boton_edit_entrevista = Button(frame_editar_inferior, text="Guardar cambios",
                                    font=("Segoe UI", 12, "bold"), command=edit_entrevista,
                                    bg=VERDE_AZULADO, fg=BLANCO, relief="flat", width=15)
    boton_edit_entrevista.grid(row=0, column=1)

# ============================================================================
# BLOQUE 14: FUNCIONES DE LA VENTANA DE ENTREVISTAS
# ============================================================================
def new_entrevista():
    # Toma los valores de los widgets del formulario de entrevistas
    entrevista = text_entrevista.get("1.0", tk.END)  # "1.0" = desde línea 1, columna 0
    dni = entry_dni_entrevista.get()
    nom_profecional = entry_nombre_profecional.get()
    fecha = comprobar_fecha(entry_fecha)  # Normaliza la fecha con "/"
    # Inserta en la BD
    cursor.execute("INSERT INTO entrevistas (entrevista, dni, nombre_profecional, fecha) VALUES (?,?,?,?)",
                   (entrevista, dni, nom_profecional, fecha))
    conexion.commit()
    ver_list_entrevist(lista_entrevistas)  # Refresca el listado

def eliminar_entrevista():
    seleccion = lista_entrevistas.curselection()  # Tupla con índices seleccionados
    if seleccion:
        # curselection() devuelve tupla, hay que tomar [0]
        dato = lista_entrevistas.get(seleccion[0])
        # Separa por "//" y toma la primera parte, saca "ID: " y limpia espacios
        id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()
        cursor.execute("DELETE FROM entrevistas WHERE id = ?", (id_entrevista,))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)

def detalles_entrevsit(event=None):
    # Se dispara al hacer click en una entrevista de la lista
    seleccion = lista_entrevistas.curselection()
    if seleccion:
        dato = lista_entrevistas.get(seleccion[0])  # ¡Ojo con [0]!
        datos = dato.split("//")  # Separa en partes por "//"

        # Ventana nueva para mostrar el detalle completo
        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Detalle de entrevista")
        ventana_detalle.geometry("500x400")
        ventana_detalle.config(bg=GRIS_NIEBLA)

        frame_detalle = Frame(ventana_detalle, bg=BLANCO, relief="solid", bd=1)
        frame_detalle.pack(padx=20, pady=20, fill="both", expand=True)

        # Muestra cada campo en su propio Label
        label_dato_fecha = tk.Label(frame_detalle, text=datos[1], bg=BLANCO, fg=GRIS_AZULADO,
                                     font=("Segoe UI", 12, "bold"))
        label_dato_fecha.pack(pady=5)
        label_dato_dni = tk.Label(frame_detalle, text=datos[2], bg=BLANCO, fg=GRIS_AZULADO,
                                   font=("Segoe UI", 12))
        label_dato_dni.pack()
        label_dato_profecional = tk.Label(frame_detalle, text=datos[3], bg=BLANCO, fg=GRIS_AZULADO,
                                           font=("Segoe UI", 12))
        label_dato_profecional.pack(pady=10)

        # El texto largo de la entrevista va en un Text (solo lectura)
        text_dato_entrevista = tk.Text(frame_detalle, height=8, font=("Segoe UI", 12),
                                        relief="solid", bd=1)
        text_dato_entrevista.pack(fill="both", expand=True, padx=10, pady=10)
        text_dato_entrevista.insert("1.0", datos[4])  # datos[4] = el texto de la entrevista
        text_dato_entrevista.config(state=tk.DISABLED)  # Lo hace solo lectura

# ============================================================================
# BLOQUE 15: VENTANA EMERGENTE DE ENTREVISTAS
# ============================================================================
def abrir_ventana_entrevistas(ventana_padre):
    ventana_entrevistas = tk.Toplevel(ventana_padre)
    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("1000x800")
    ventana_entrevistas.config(bg=GRIS_NIEBLA)

    # GLOBAL: estas variables se usan en otras funciones (new_entrevista, etc.)
    global lista_entrevistas, text_entrevista, entry_dni_entrevista
    global entry_nombre_profecional, entry_fecha

    # --- FRAME SUPERIOR con el formulario ---
    frame_superior = Frame(ventana_entrevistas, bg=GRIS_AZULADO)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)

    # DNI
    label_dni = tk.Label(frame_superior, text="DNI:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12))
    label_dni.grid(row=0, column=0, sticky="e", padx=5, pady=10)
    entry_dni_entrevista = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_dni_entrevista.grid(row=0, column=1, sticky="e", padx=5)

    # Profesional
    label_nombre_profecional = tk.Label(frame_superior, text="Nombre del profesional:",
                                         bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12))
    label_nombre_profecional.grid(row=0, column=2, sticky="e", padx=5)
    entry_nombre_profecional = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=0, column=3, sticky="e", padx=5)

    # Fecha
    label_fecha = tk.Label(frame_superior, text="Fecha de entrevista:",
                            bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12))
    label_fecha.grid(row=0, column=4, sticky="e", padx=5)
    entry_fecha = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_fecha.grid(row=0, column=5, sticky="e", padx=5)

    # --- FRAME DEL MEDIO (lista izquierda + texto derecha) ---
    frame_medio_cuerpo = tk.Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_medio_cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

    # LADO IZQUIERDO: lista de entrevistas
    frame_lista_medio = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_lista_medio.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(frame_lista_medio, text="Historial de Entrevistas", bg=BLANCO,
             fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    lista_entrevistas = tk.Listbox(frame_lista_medio, bg=BLANCO, fg=GRIS_AZULADO,
                                    selectbackground=AZUL_SERENO, selectforeground=BLANCO,
                                    bd=0, font=("Segoe UI", 12))
    lista_entrevistas.pack(fill="both", expand=True, padx=5, pady=5)
    # Bindeo: cada vez que se selecciona una entrevista, se abre el detalle
    lista_entrevistas.bind("<<ListboxSelect>>", detalles_entrevsit)
    ver_list_entrevist(lista_entrevistas)  # Llena la lista al abrir

    # LADO DERECHO: text de anotaciones
    frame_texto = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_texto.pack(side="left", fill="both", expand=True, padx=(10, 0))
    tk.Label(frame_texto, text="Anotaciones de la entrevista", bg=BLANCO,
             fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    text_entrevista = tk.Text(frame_texto, relief="solid", bd=1, bg=GRIS_NIEBLA, font=("Segoe UI", 12))
    text_entrevista.pack(fill="both", expand=True, padx=5, pady=5)

    # --- FRAME INFERIOR (botones) ---
    frame_inferior = Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_inferior.pack(side="bottom", fill="x", padx=20, pady=20)

    # Pesos en los extremos para centrar los botones del medio
    frame_inferior.grid_columnconfigure(0, weight=1)
    frame_inferior.grid_columnconfigure(4, weight=1)

    # Botón "Nueva entrevista"
    boton_new_entrevista = tk.Button(frame_inferior, text="Nueva entrevista", command=new_entrevista,
                                      bg=VERDE_AZULADO, fg=BLANCO, font=("Segoe UI", 12, "bold"),
                                      relief="flat", width=15)
    boton_new_entrevista.grid(row=0, column=1, padx=10)

    # Botón "Eliminar entrevista"
    boton_eliminar_entrevista = tk.Button(frame_inferior, text="Eliminar entrevista", command=eliminar_entrevista,
                                           bg=ROJO, fg=BLANCO, font=("Segoe UI", 12, "bold"),
                                           relief="flat", width=15)
    boton_eliminar_entrevista.grid(row=0, column=2, padx=10)

    # Botón "Editar entrevista"
    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
    boton_editar = tk.Button(frame_inferior, text="Editar entrevista", bg=AZUL_SERENO, fg=BLANCO,
                              command=abrir_editar, font=("Segoe UI", 12, "bold"),
                              relief="flat", width=15)
    boton_editar.grid(row=0, column=3, padx=10)

# ============================================================================
# BLOQUE 16: VENTANA DE PERFIL
# ============================================================================
def abrir_ventana_perfil():
    ventana_perfil = tk.Toplevel(ventana)
    ventana_perfil.title("PERFIL")
    ventana_perfil.geometry("1000x800")
    ventana_perfil.config(bg=GRIS_NIEBLA)

    # --- FRAME IZQUIERDO (formulario) ---
    frame_izquierdo = tk.Frame(ventana_perfil, bg=AZUL_PETROLEO)
    frame_izquierdo.pack(side="left", fill="y", padx=15, pady=15)  # fill="y" = todo el alto

    # Nombre (¡ojo con el sufijo _perfil! Antes pisaba la global de la ventana principal)
    label_nombre = Label(frame_izquierdo, text=" Nombre:", bg=GRIS_NIEBLA,
                          fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_nombre.grid(row=0, column=0, sticky="e", padx=5)
    entry_nombre_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_nombre_perfil.grid(row=0, column=1, padx=5, pady=3)

    # Apellido (también _perfil)
    label_apellido = Label(frame_izquierdo, text=" Apellido:", bg=GRIS_NIEBLA,
                            fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_apellido.grid(row=1, column=0, sticky="e", padx=5)
    entry_apellido_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_apellido_perfil.grid(row=1, column=1, padx=5, pady=3)

    # DNI (también _perfil)
    label_dni = Label(frame_izquierdo, text=" DNI:", bg=GRIS_NIEBLA,
                       fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_dni.grid(row=2, column=0, sticky="e", padx=5)
    entry_dni_perfil = tk.Entry(frame_izquierdo, width=15, font=("Segoe UI", 12))
    entry_dni_perfil.grid(row=2, column=1, padx=5, pady=3)

    # Dirección
    label_direccion = Label(frame_izquierdo, text=" Direccion:", bg=GRIS_NIEBLA,
                             fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_direccion.grid(row=3, column=0, sticky="e", padx=5)
    entry_direccion = tk.Entry(frame_izquierdo, width=15, font=("Segoe UI", 12))
    entry_direccion.grid(row=3, column=1, padx=5, pady=3)

    # Fecha de nacimiento
    label_f_nacimiento = tk.Label(frame_izquierdo, text=" Fecha de nacimiento:",
                                    bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_f_nacimiento.grid(row=4, column=0, sticky="e", padx=5)
    entry_f_nacimiento = tk.Entry(frame_izquierdo, width=15, font=("Segoe UI", 12))
    entry_f_nacimiento.grid(row=4, column=1, padx=5, pady=3)

    # PDF (Entry de solo lectura por ahora, no está conectado a nada)
    label_pdf_perfil = tk.Label(frame_izquierdo, text=" Cargar pdfs aqui", bg=GRIS_NIEBLA,
                                 fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_pdf_perfil.grid(row=10, column=1, sticky="e", padx=10)
    entry_pdf_perfil = tk.Entry(frame_izquierdo, font=("Segoe UI", 12))
    entry_pdf_perfil.grid(row=11, column=1, sticky="e", padx=10, pady=3)

    # Barra de progreso (por ahora es un Entry, no una Progressbar real)
    label_barra_progreso_perfil = tk.Label(frame_izquierdo, text=" Barra de progreso",
                                            bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
    label_barra_progreso_perfil.grid(row=12, column=1, sticky="e", padx=10)
    entry_barra_progreso_perfil = tk.Entry(frame_izquierdo, font=("Segoe UI", 12))
    entry_barra_progreso_perfil.grid(row=13, column=1, sticky="e", padx=10, pady=3)

    # --- FRAME DERECHO (visor de foto + lista de entrevistas) ---
    frame_derecha = tk.Frame(ventana_perfil, bg=ROJO)  # Acordate: puede que quieras cambiarlo a GRIS_NIEBLA
    frame_derecha.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

    # Visor de foto
    frame_foto_perfil = Frame(frame_derecha, bg=BLANCO, relief="solid", bd=1, height=350)
    frame_foto_perfil.pack(side="top", fill="both", expand=True, pady=(0, 10))
    frame_foto_perfil.pack_propagate(False)  # Mantiene el alto de 350
    visor_foto_perfil = tk.Label(frame_foto_perfil, text="👤\nSin foto", bg=BLANCO,
                                   fg=GRIS_MEDIO, font=("Segoe UI", 20))
    visor_foto_perfil.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Lista de entrevistas/órdenes
    frame_lista = Frame(frame_derecha, bg=GRIS_AZULADO, relief="solid", bd=1)
    frame_lista.pack(fill="both", expand=True, side="bottom", pady=(0, 20))
    titulo_lista_perfil = Label(frame_lista, text="Ordenes registradas", bg=GRIS_AZULADO,
                                  fg=BLANCO, font=("Segoe UI", 15, "bold"))
    titulo_lista_perfil.pack(side="top", padx=10, pady=10)

    # Scrollbar PROPIA del perfil (¡no usar la global "scroll"!)
    scroll_perfil = tk.Scrollbar(frame_lista, orient="vertical")
    scroll_perfil.pack(side="right", fill="y")
    # Listbox PROPIO del perfil (con sufijo _perfil para no pisar la global)
    lista_personas_perfil = Listbox(frame_lista, yscrollcommand=scroll_perfil.set,
                                      font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO,
                                      selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_personas_perfil.pack(side="left", fill="both", expand=True)
    scroll_perfil.config(command=lista_personas_perfil.yview)

# ============================================================================
# BLOQUE 17: VENTANA DEL EDITOR DE FOTOS
# ============================================================================
def abrir_ventana_editor_fotos():
    ventana_editor_fotos = tk.Toplevel(ventana)
    ventana_editor_fotos.title("Editor de fotos")
    ventana_editor_fotos.geometry("500x600")
    ventana_editor_fotos.config(bg=GRIS_NIEBLA)

    # --- FRAME SUPERIOR: visor grande ---
    frame_editor_fotos_superior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_superior.pack(side="top", fill="both", expand=True)

    visor_foto_perfil = tk.Label(frame_editor_fotos_superior, text="👤\nSin foto",
                                   bg=BLANCO, fg=NEGRO, relief="solid", bd=1,
                                   font=("Segoe UI", 20))
    visor_foto_perfil.pack(fill="both", expand=True, padx=10, pady=10)

    # --- FRAME MEDIO: lista de imágenes cargadas ---
    frame_lista_imgs = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_lista_imgs.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(frame_lista_imgs, text="Imágenes cargadas:", font=("Segoe UI", 11, "bold"),
             bg=VERDE_AZULADO, fg="white").pack(fill="x")
    lista_imagenes = tk.Listbox(frame_lista_imgs, height=6, font=("Segoe UI", 10))
    lista_imagenes.pack(fill="both", expand=True, pady=5)

    # --- FRAME INFERIOR: botones ---
    frame_editor_fotos_inferior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_inferior.pack(side="bottom", fill="x", pady=10)

    # Columnas 0 y 3 con peso para centrar los botones (columnas 1 y 2)
    frame_editor_fotos_inferior.grid_columnconfigure(0, weight=1)
    frame_editor_fotos_inferior.grid_columnconfigure(3, weight=1)

    # ---------- FUNCIONES INTERNAS ----------
    def mostrar_previa(ruta):
        # Abre la imagen de la ruta, la achica a 180x180 y la muestra en el visor
        try:
            imagen = Image.open(ruta).resize((180, 180))
            imagen_tk = ImageTk.PhotoImage(imagen)
            visor_foto_perfil.config(image=imagen_tk, text="")  # text="" para que no quede el emoji debajo
            visor_foto_perfil.image = imagen_tk  # Mantener referencia
        except Exception as e:
            print("Error al mostrar la imagen:", e)

    def agregar_imagen():
        # Abre diálogo para elegir una imagen
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if not ruta:
            return  # Si canceló, sale
        # Guarda la ruta en la lista global y muestra el nombre en el Listbox
        imagenes_cargadas.append(ruta)
        lista_imagenes.insert(tk.END, os.path.basename(ruta))  # basename = nombre sin carpeta
        mostrar_previa(ruta)

    def eliminar_imagen():
        # Intenta agarrar el índice seleccionado en el Listbox
        try:
            indice = lista_imagenes.curselection()[0]
        except IndexError:
            return  # Si no hay nada seleccionado, sale
        # Lo borra de la lista global y del Listbox (¡NO del disco!)
        del imagenes_cargadas[indice]
        lista_imagenes.delete(indice)
        # Limpia el visor
        visor_foto_perfil.config(image="", text="👤\nSin foto")
        visor_foto_perfil.image = None

    # ---------- BOTONES ----------
    tk.Button(frame_editor_fotos_inferior, text="Añadir fotos", command=agregar_imagen,
              bg=VERDE_AZULADO, fg="white", width=12,
              activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
              font=("Segoe UI", 12)).grid(row=0, column=1, padx=10)

    tk.Button(frame_editor_fotos_inferior, text="Eliminar fotos", command=eliminar_imagen,
              bg=VERDE_AZULADO, fg="white", width=12,
              activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
              font=("Segoe UI", 12)).grid(row=0, column=2, padx=10)

# ============================================================================
# BLOQUE 18: BOTONES PRINCIPALES QUE ABREN LAS OTRAS VENTANAS
# ============================================================================
def abrir_desde_principal():
    # Función intermedia por si después querés agregar algo antes de abrir
    abrir_ventana_entrevistas(ventana)

# Botón "Entrevistas"
tk.Button(frame_btn, text="Entrevistas", command=abrir_desde_principal,
          bg=VERDE_AZULADO, fg="white", width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          font=("Segoe UI", 12)).pack(side="left", padx=5)

# Botón "Perfil"
tk.Button(frame_btn, text="Perfil", command=abrir_ventana_perfil,
          bg=VERDE_AZULADO, fg=BLANCO, width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          font=("Segoe UI", 12)).pack(side="left", padx=5)

# Botón "Editor de fotos"
tk.Button(frame_btn, text="Editor de fotos", command=abrir_ventana_editor_fotos,
          bg=VERDE_AZULADO, fg=BLANCO, width=12,
          activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
          font=("Segoe UI", 12)).pack(side="left", padx=5)

# ============================================================================
# BLOQUE 19: INICIO DEL PROGRAMA
# ============================================================================
ventana.mainloop()  # Este es el "loop infinito" que mantiene la ventana abierta y escuchando eventos
