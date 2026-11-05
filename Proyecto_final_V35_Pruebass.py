# ============================================================================
# BLOQUE 1: IMPORTACIONES
# Aca traemos todas las librerías que vamos a usar.
# ============================================================================
import sqlite3  # Para manejar la base de datos SQLite (crear tablas, insertar, borrar, etc.)
import tkinter as tk  # La librería de interfaces gráficas (ventanas, botones, etc.)
# De tkinter traemos cosas específicas que vamos a usar directo:
from tkinter import filedialog, messagebox, ttk, Label, Button, Entry, Frame, Toplevel, Listbox, font
from io import BytesIO  # BytesIO convierte bytes en un "archivo virtual" para que PIL lo pueda leer
from PIL import Image, ImageTk  # PIL (Pillow) abre, redimensiona y muestra imágenes
import string  # Lo usamos para sacar los signos de puntuación en comprobar_fecha()
import os  # Para manejar rutas y archivos (os.path.basename, os.remove, etc.)
import textwrap

# ============================================================================
# BLOQUE 2: VARIABLES GLOBALES
# Las variables globales son las que se pueden usar desde cualquier función.
# ============================================================================
imagenes_cargadas = []  # Lista vacia donde guardamos las RUTAS de las imagenes que el usuario va agregando en el editor

#Redondeo de botones
class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg_color, fg_color, text="", command=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        
        # Dibujar esquinas redondeadas en el Canvas
        self.rect = self.round_rectangle(0, 0, width, height, radius=corner_radius, fill=bg_color, outline="")
        self.text_id = self.create_text(width / 2, height / 2, text=text, fill=fg_color, font=("Helvetica", 12, "bold"))
        
        # Eventos para simular el botón
        self.tag_bind(self.rect, "<ButtonPress-1>", self._on_press)
        self.tag_bind(self.text_id, "<ButtonPress-1>", self._on_press)

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_press(self, event):
        if self.command:
            self.command()

# ============================================================================
# BLOQUE 3: BASE DE DATOS
# Aca conectamos a SQLite y creamos las tablas si no existen.
# ============================================================================
conexion = sqlite3.connect("PROYECTO_FINal.db")  # Abre (o crea) el archivo de base de datos
cursor = conexion.cursor()  # El cursor es el que ejecuta las consultas SQL
cursor.execute("PRAGMA foreign_keys = ON;")  # Activa las claves foraneas

# Crea la tabla "personas"
cursor.execute("""CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    edad INTEGER,
    fecha_nacimiento TEXT,
    fecha_ingreso TEXT,
    telefono TEXT,
    direccion TEXT,
    contacto_emergencia TEXT,
    telefono_emergencia TEXT,
    obra_social TEXT,
    estado TEXT DEFAULT 'activo',
    consentimiento TEXT,
    foto BLOB)""")

# Crea la tabla "entrevistas"
cursor.execute("""CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_profecional TEXT NOT NULL,
    apellido_profecional TEXT,
    dni_profecional TEXT,
    matricula TEXT,
    especialidad TEXT,
    telefono_profecional TEXT,
    email_profecional TEXT,
    activo_profecional TEXT,
    entrevista TEXT NOT NULL,
    dni_paciente INTEGER NOT NULL,
    fecha_entrevista TEXT NOT NULL,
    hora_entrevista TEXT,
    tipo_entrevista TEXT,
    proxima_sesion_entrevista TEXT)""")

#especialidad TEXT NOT NULL,  "Psicologo", "Psiquiatra", "Operador socio-terapeutico",etc
#activo_profecional TEXT NOT NULL, si sigue atendiendo al paciente o no, tipo poner solo ACTIVO o NO ACTIVO
#tipo_entrevista TEXT NOT NULL, "individual" / "grupal" / "familiar"
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
#fede no estubo aqui :(

# ============================================================================
# BLOQUE 6: BANNER (franja del titulo abajo)
# ============================================================================
banner = tk.Frame(ventana, bg=AZUL_SERENO, height=80)  # Frame de 80px
banner.pack(side="top", fill="x")                    # Pegado abajo
banner.pack_propagate(False)                            # No se achica
banner_label = tk.Label(banner,text="✚ MEDTRACK",bg=AZUL_SERENO, fg=BLANCO, font=("Segoe UI", 24, "bold"))
banner_label.pack(pady=20) # Centrado

# ============================================================================
# BLOQUE 7: FUNCIONES PRINCIPALES PARA VENTANA PRINCIPAL
# ============================================================================
def refrescar_lista(): # Borra el Listbox y lo vuelve a llenar con los datos de la BD
    lista_personas.delete(0, tk.END)
    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")
    for nombre, apellido, dni in cursor.fetchall():
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")

def mostrar_foto(dni):# Busca la foto en la BD
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
    # Ocultar confirmaciones
    boton_busqueda_definitivo.grid_remove()
    boton_agregar_definitivo.grid_remove()
    grids_nom_ape()
    grids_dni()
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
    boton_busqueda_definitivo.grid_remove()
    grids_nom_ape()
    grids_dni()
    boton_agregar_definitivo.grid()

def agregar_definitivo():
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
    ruta = filedialog.askopenfilename(title="Foto (opcional)", filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])
    contenido = None
    if ruta:
        with open(ruta, "rb") as f:
            contenido = sqlite3.Binary(f.read())
    # Inserta en BD
    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)",
                       (nombre, apellido, dni, contenido))
        conexion.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Ya existe una persona con ese DNI.\nVerifica el numero ingresado.")
        return
    except Exception:
        messagebox.showerror("Error inesperado", 'No se pudo guardar')
        return
    refrescar_lista()
    limpiar()
    boton_agregar_definitivo.grid_remove()
    messagebox.showinfo("OK", "Persona agregada.")

def eliminar():
    seleccion = lista_personas.curselection()
    if not seleccion:
        messagebox.showwarning("Atencion", "Selecciona una persona de la lista para eliminar.")
        return
    texto = lista_personas.get(seleccion[0])
    dni = int(texto.split("DNI ")[1])
    if not messagebox.askyesno("Confirmar eliminación", f"¿Estas seguro de que deseas eliminar a esta persona?\n\n{texto}"):
        return
    boton_busqueda_definitivo.grid_remove()
    boton_agregar_definitivo.grid_remove()
    grids_remove_nom_ape()
    grids_remove_dni()
    cursor.execute("DELETE FROM entrevistas WHERE dni_paciente = ?", (dni,))
    cursor.execute("DELETE FROM personas WHERE dni = ?", (dni,))
    conexion.commit()
    refrescar_lista()
    visor_foto.configure(image="", text="Sin foto")
    visor_foto.image = None
    messagebox.showinfo("OK", "Persona eliminada correctamente.")

def buscar():
    boton_agregar_definitivo.grid_remove()
    grids_remove_nom_ape()
    grids_dni()
    boton_busqueda_definitivo.grid()

def buscar_definitivo():
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atencion", "Escribi de forma numerica un DNI para buscar.")
        return
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni_txt,))
    fila = cursor.fetchone()
    if not fila:
        messagebox.showinfo("Sin resultados", "No existe esa persona.")
        return
    else:
        grids_nom_ape()
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
    visor_foto.configure(image="", text="Sin foto")
    visor_foto.image = None

# ============================================================================
# BLOQUE 8: FRAME DE BOTONES PARA LA PANTALLA PRINCIPAL
# ============================================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn_info = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn_info.pack(side="bottom", fill="x", padx=10, pady=15)
frame_btn.pack(side="top", fill="x", padx=15, pady=10)

btn_agregar = RoundedButton(frame_btn, 140, 40, 20, VERDE_AZULADO, BLANCO, text="Agregar", command=agregar)
btn_agregar.pack(side="left", padx=5, expand=True, fill="both")

btn_eliminar = RoundedButton(frame_btn, 140, 40, 20, VERDE_AZULADO, BLANCO, text="Eliminar", command=eliminar)
btn_eliminar.pack(side="left", padx=5, expand=True, fill="both")

btn_buscar = RoundedButton(frame_btn, 140, 40, 20, VERDE_AZULADO, BLANCO, text="Buscar", command=buscar)
btn_buscar.pack(side="left", padx=5, expand=True, fill="both")

btn_limpiar = RoundedButton(frame_btn, 140, 40, 20, VERDE_AZULADO, BLANCO, text="Limpiar", command=limpiar)
btn_limpiar.pack(side="left", padx=5, expand=True, fill="both")


# ============================================================================
# BLOQUE 9: FORMULARIO PRINCIPAL
# ============================================================================
frame_form = Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top", fill="x", padx=15, pady=10)#rellena en "x"
# Todo esto esta en fila 0

label_nombre = Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_nombre.grid(row=0, column=2, sticky="e", padx=5)
entry_nombre = Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_nombre.grid(row=0, column=3, padx=5, pady=3)

label_apellido = Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_apellido.grid(row=0, column=4, sticky="e", padx=5)
entry_apellido = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
entry_apellido.grid(row=0, column=5, padx=5, pady=3)

label_dni = Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12))
label_dni.grid(row=0, column=6, sticky="e", padx=5)
entry_dni = Entry(frame_form, width=15, font=("Segoe UI", 12))
entry_dni.grid(row=0, column=7, padx=5, pady=3)

def grids_nom_ape():
    label_nombre.grid()
    entry_nombre.grid()
    label_apellido.grid()
    entry_apellido.grid()
def grids_dni():
    label_dni.grid()
    entry_dni.grid()
def grids_remove_nom_ape():
    label_nombre.grid_remove()
    entry_nombre.grid_remove()
    label_apellido.grid_remove()
    entry_apellido.grid_remove()
def grids_remove_dni():
    label_dni.grid_remove()
    entry_dni.grid_remove()

grids_remove_nom_ape()
grids_remove_dni()

# ============================================================================
# BLOQUE 10: CUERPO (VISOR Y LISTA PRINCIPAL)
# ============================================================================
cuerpo = tk.Frame(ventana, bg=GRIS_NIEBLA)
cuerpo.pack(fill="both", expand=True)
frame_foto = tk.Frame(cuerpo, bg=BLANCO, relief="solid", bd=1)
frame_foto.pack(side="left",fill="x", padx=50, pady = 45) #aca hay que cambiar el tamaño del frame
visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 18)) #texto para la foto
visor_foto.pack(expand=True, fill="both",padx= 20,pady= 40)

frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO, relief="solid", bd=1)
frame_lista.pack(side="right", fill="both", expand = True,padx = 60, pady = 55)
titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)

scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")

lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
lista_personas.pack(side="left", fill="both",expand= True)
scroll.config(command=lista_personas.yview)


# ============================================================================
# BLOQUE 11: BOTONES PARA BUSCAR Y AGREGAR DEFINITIVAMENTE
# ============================================================================
# Viven dentro de frame_form (que usa grid), asi que van con grid tambien.
boton_agregar_definitivo = Button(frame_form, text="Confirmar agregar", command=agregar_definitivo, bg=VERDE_AZULADO, fg=BLANCO,
    activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
    relief="flat", font=("Segoe UI", 12)
)
boton_agregar_definitivo.grid(row=0, column=1, sticky="ew", padx=5)
boton_agregar_definitivo.grid_remove()

boton_busqueda_definitivo = Button(
    frame_form, text="Confirmar busqueda",
    command=buscar_definitivo,
    bg=VERDE_AZULADO, fg=BLANCO,
    activebackground=VERDE_TERMINAL, activeforeground=NEGRO,
    relief="flat", font=("Segoe UI", 12)
)
boton_busqueda_definitivo.grid(row=0, column=1, sticky="ew", padx=5)
boton_busqueda_definitivo.grid_remove()

# ============================================================================
# BLOQUE 12: MODO OSCURO
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
        widget.config(bg=acento, fg=BLANCO)

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
    banner_label.config(bg=fondo_banner, fg=BLANCO)

    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=fondo_general, fg=texto)
    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(bg=lista_bg, fg=lista_fg, insertbackground=lista_fg)

    for widget in frame_btn.winfo_children():
        if isinstance(widget, tk.Button) and widget is not btn_tema:
            widget.config(bg=boton_accion, fg=BLANCO, activebackground=VERDE_TERMINAL if not tema_oscuro else "#444444", activeforeground=BLANCO)

    btn_tema.config(bg=boton_fill, fg=boton_text, activebackground=active_bg, activeforeground=active_fg)
    actualizar_ventanas_secundarias()

btn_tema = Button(frame_btn, text="☾", command=aplicar_tema, bg="#111111", fg="#FFFFFF", font=("Segoe UI", 18, "bold"), width=3, height=1, relief="flat", bd=0, cursor="hand2")
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
    cursor.execute("""SELECT id, fecha_entrevista, hora_entrevista, dni_paciente,
                             nombre_profecional, apellido_profecional, tipo_entrevista
                      FROM entrevistas ORDER BY id""")
    for i in cursor.fetchall():
        dato = f"ID: {i[0]} // Fecha: {i[1]} {i[2] or ''} // DNI pac: {i[3]} // Prof: {i[4]} {i[5] or ''} // Tipo: {i[6] or '-'}"
        lista_widget.insert(tk.END, dato)

# ============================================================================
# BLOQUE 13: VENTANA PARA EDITAR ENTREVISTA
# ============================================================================
def pantalla_edit_entrevista(ventana_padre):
    ventana_editar = tk.Toplevel(ventana_padre)
    ventana_editar.title("Editar datos de entrevista")
    ventana_editar.geometry("800x900")
    ventana_editar.config(bg=GRIS_NIEBLA)

    frame_editar_superior = tk.Frame(ventana_editar, bg=AZUL_PETROLEO, relief="solid", bd=1)
    frame_editar_superior.pack(side="top", padx=20, pady=20, fill="x")

    Label(frame_editar_superior, text="ID de la entrevista a editar:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=0, column=0)
    entry_id = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_id.grid(row=0, column=1)

    Label(frame_editar_superior, text="DNI paciente:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=1, column=0)
    entry_dni = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_dni.grid(row=1, column=1)

    Label(frame_editar_superior, text="Nombre del Profesional:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=2, column=0)
    entry_nombre_profecional = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_nombre_profecional.grid(row=2, column=1)

    Label(frame_editar_superior, text="Fecha:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=3, column=0)
    entry_fecha = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_fecha.grid(row=3, column=1)

    frame_editar_medio = tk.Frame(ventana_editar, bg=GRIS_NIEBLA, relief="solid", bd=1)
    frame_editar_medio.pack(fill="both", expand=True, padx=20, pady=10)
    Label(frame_editar_medio, text="Texto de la entrevista:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).pack(fill="x", side="top", padx=20, pady=5)
    text_entrevista_edit = tk.Text(frame_editar_medio, bg=GRIS_NIEBLA, relief="solid", bd=1, font=("Segoe UI", 12))
    text_entrevista_edit.pack(fill="both", expand=True, padx=15, pady=15)

    # Funcion para precargar los datos de la entrevista a partir del ID
    def cargar_entrevista():
        p_id = entry_id.get().strip()
        if not p_id:
            return
        cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (p_id,))
        e = cursor.fetchone()
        if not e:
            messagebox.showinfo("Error", "No existe esa entrevista.")
            return
        # indice: 0=id, 1=nombre_prof, 2=apellido_prof, 3=dni_prof, 4=matricula,
        # 5=especialidad, 6=tel_prof, 7=email_prof, 8=activo, 9=entrevista,
        # 10=dni_paciente, 11=fecha, 12=hora, 13=tipo, 14=proxima_sesion
        text_entrevista_edit.delete("1.0", tk.END)
        text_entrevista_edit.insert("1.0", e[9] or "")
        entry_dni.delete(0, tk.END); entry_dni.insert(0, e[10] or "")
        entry_nombre_profecional.delete(0, tk.END); entry_nombre_profecional.insert(0, e[1] or "")
        entry_fecha.delete(0, tk.END); entry_fecha.insert(0, e[11] or "")

    boton_cargar = Button(frame_editar_superior, text="Cargar datos", command=cargar_entrevista,
                          bg=VERDE_AZULADO, fg=BLANCO, font=("Segoe UI", 10))
    boton_cargar.grid(row=0, column=2, padx=10, sticky="ew")

    def guardar_entrevista():
        p_id = entry_id.get()
        if p_id == "":
            return
        cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (p_id,))
        entrevista = cursor.fetchone()
        if not entrevista:
            messagebox.showinfo("Error", "No existe esa entrevista.")
            return
        texto_nuevo = text_entrevista_edit.get("1.0", tk.END).strip()
        if texto_nuevo == "":
            texto_nuevo = entrevista[9]
        dni_nuevo = entry_dni.get().strip() or entrevista[10]
        prof_nuevo = entry_nombre_profecional.get().strip() or entrevista[1]
        fecha_nueva = entry_fecha.get().strip()
        if fecha_nueva == "":
            fecha_nueva = entrevista[11]
        else:
            fecha_nueva = comprobar_fecha(entry_fecha)
        conexion.execute("""UPDATE entrevistas
                            SET entrevista = ?, dni_paciente = ?, nombre_profecional = ?, fecha_entrevista = ?
                            WHERE id = ?""",
                         (texto_nuevo, dni_nuevo, prof_nuevo, fecha_nueva, p_id))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)
        ventana_editar.destroy()

    frame_editar_inferior = tk.Frame(ventana_editar, bg=GRIS_NIEBLA)
    frame_editar_inferior.pack(fill="x", expand=True)
    boton_guardar_entrevista = Button(frame_editar_superior, text="Guardar cambios",font=("Segoe UI", 10), command=guardar_entrevista,bg=VERDE_AZULADO, fg=BLANCO)
    boton_guardar_entrevista.grid(row=0, column=3, padx=5, sticky="ew")

# ============================================================================
# BLOQUE 14: FUNCIONES DE LA VENTANA DE ENTREVISTAS
# ============================================================================
def new_entrevista():
    entrevista = text_entrevista.get("1.0", tk.END).strip() # .strip() borra los enters de mas
    dni = entry_dni_entrevista.get().strip()
    nom_profecional = entry_nombre_profecional.get().strip()
    fecha = comprobar_fecha(entry_fecha)
    hora = entry_hora_entrevista.get().strip()
    tipo = var_tipo_entrevista.get()

    if entrevista == "" or dni == "" or nom_profecional == "":
        messagebox.showwarning("Faltan datos", "Complete la entrevista, DNI del paciente y Profesional.")
        return

    try:
        cursor.execute("""INSERT INTO entrevistas
            (nombre_profecional, entrevista, dni_paciente, fecha_entrevista, hora_entrevista, tipo_entrevista)
            VALUES (?,?,?,?,?,?)""",
            (nom_profecional, entrevista, dni, fecha, hora, tipo))
        conexion.commit()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la entrevista: {e}")
        return

    ver_list_entrevist(lista_entrevistas)
    text_entrevista.delete("1.0", tk.END)

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
    if not seleccion:
        return
    dato = lista_entrevistas.get(seleccion[0])
    id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()

    cursor.execute("""SELECT nombre_profecional, apellido_profecional, dni_profecional,
                             matricula, especialidad, entrevista, dni_paciente,
                             fecha_entrevista, hora_entrevista, tipo_entrevista,
                             proxima_sesion_entrevista
                      FROM entrevistas WHERE id = ?""", (id_entrevista,))
    e = cursor.fetchone()
    if not e:
        return

    ventana_detalle = tk.Toplevel()
    ventana_detalle.title(f"Detalle de entrevista #{id_entrevista}")
    ventana_detalle.geometry("600x550")
    ventana_detalle.config(bg=GRIS_NIEBLA)

    frame_detalle = Frame(ventana_detalle, bg=BLANCO, relief="solid", bd=1)
    frame_detalle.pack(padx=20, pady=20, fill="both", expand=True)

    info = [
        ("ID", id_entrevista),
        ("Profesional", f"{e[0]} {e[1] or ''}"),
        ("DNI profesional", e[2] or "-"),
        ("Matricula", e[3] or "-"),
        ("Especialidad", e[4] or "-"),
        ("DNI paciente", e[6]),
        ("Fecha", f"{e[7]} {e[8] or ''}"),
        ("Tipo", e[9] or "-"),
        ("Proxima sesion", e[10] or "-"),
    ]
    for etiqueta, valor in info:
        fila = Frame(frame_detalle, bg=BLANCO)
        fila.pack(fill="x", padx=10, pady=2)
        tk.Label(fila, text=f"{etiqueta}:", bg=BLANCO, fg=GRIS_AZULADO,
                 font=("Segoe UI", 11, "bold"), width=16, anchor="e").pack(side="left")
        tk.Label(fila, text=valor, bg=BLANCO, fg=GRIS_AZULADO,
                 font=("Segoe UI", 11), anchor="w").pack(side="left", padx=5)

    tk.Label(frame_detalle, text="Anotaciones:", bg=BLANCO, fg=GRIS_AZULADO,
             font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", padx=10, pady=(10, 2))
    text_dato = tk.Text(frame_detalle, height=8, font=("Segoe UI", 11), relief="solid", bd=1)
    text_dato.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    text_dato.insert("1.0", e[5] or "")
    text_dato.config(state=tk.DISABLED)

# ============================================================================
# BLOQUE 15: VENTANA EMERGENTE DE ENTREVISTAS
# ============================================================================
def abrir_ventana_entrevistas(ventana_padre):
    ventana_entrevistas = tk.Toplevel(ventana_padre)
    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("1000x800")
    ventana_entrevistas.config(bg=GRIS_NIEBLA)

    global lista_entrevistas, text_entrevista, entry_dni_entrevista
    global entry_nombre_profecional, entry_fecha
    global entry_hora_entrevista, var_tipo_entrevista

    frame_superior = Frame(ventana_entrevistas, bg=GRIS_AZULADO)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)

    # DNI paciente
    tk.Label(frame_superior, text="DNI del paciente:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=10)
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

    # Hora
    tk.Label(frame_superior, text="Hora:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=5)
    entry_hora_entrevista = tk.Entry(frame_superior, font=("Segoe UI", 12))
    entry_hora_entrevista.grid(row=1, column=1, sticky="e", padx=5, pady=(0, 10))

    # Tipo
    tk.Label(frame_superior, text="Tipo:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 12)).grid(row=1, column=2, sticky="e", padx=5)
    var_tipo_entrevista = tk.StringVar(value="individual")
    tk.OptionMenu(frame_superior, var_tipo_entrevista, "individual", "grupal", "familiar").grid(row=1, column=3, sticky="w", padx=5, pady=(0, 10))

    frame_medio_cuerpo = tk.Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_medio_cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

    # LADO IZQUIERDO: lista
    frame_lista_medio = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_lista_medio.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(frame_lista_medio, text="Historial de Entrevistas", bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    lista_entrevistas = tk.Listbox(frame_lista_medio, bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO, bd=0, font=("Segoe UI", 10))
    lista_entrevistas.pack(fill="both", expand=True, padx=5, pady=5)
    lista_entrevistas.bind("<Double-Button-1>", detalles_entrevsit)
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

    frame_inferior.columnconfigure(1, weight=1)
    frame_inferior.columnconfigure(2, weight=1)
    frame_inferior.columnconfigure(3, weight=1)

    Button(frame_inferior, text="Nueva entrevista", command=new_entrevista, bg=VERDE_AZULADO, fg=BLANCO, font=("Segoe UI", 12, "bold"), relief="flat").grid(row=0, column=1, padx=10, sticky="ew")
    Button(frame_inferior, text="Eliminar entrevista", command=eliminar_entrevista, bg=ROJO, fg=BLANCO, font=("Segoe UI", 12, "bold"), relief="flat").grid(row=0, column=2, padx=10, sticky="ew")

    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
    Button(frame_inferior, text="Editar entrevista", bg=AZUL_SERENO, fg=BLANCO, command=abrir_editar, font=("Segoe UI", 12, "bold"), relief="flat").grid(row=0, column=3, padx=10, sticky="ew")
    Button(frame_inferior, text="Imprimir PDF", command=exportar_entrevistas_pdf, bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 12, "bold"), relief="flat", width=15).grid(row=0, column=4, padx=10)

# ============================================================================
# BLOQUE 16: VENTANA DE PERFIL
# ============================================================================
def abrir_ventana_perfil():
    ventana_perfil = tk.Toplevel(ventana)
    ventana_perfil.title("PERFIL")
    ventana_perfil.geometry("1000x800")
    ventana_perfil.config(bg=GRIS_NIEBLA)
    ventana_perfil.resizable(False, False)

    # Foto pendiente (dict para poder mutarlo desde funciones anidadas)
    foto_pendiente = {"bytes": None}

    frame_izquierdo = tk.Frame(ventana_perfil, bg=GRIS_NIEBLA)
    frame_izquierdo.pack(side="left", fill="y", padx=15, pady=15)

    # Nombre
    Label(frame_izquierdo, text=" Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_nombre_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_nombre_perfil.grid(row=0, column=1, padx=5, pady=3)
    entry_nombre_perfil.insert(0, entry_nombre.get())

    # Apellido
    Label(frame_izquierdo, text=" Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=5)
    entry_apellido_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_apellido_perfil.grid(row=1, column=1, padx=5, pady=3)
    entry_apellido_perfil.insert(0, entry_apellido.get())

    # DNI
    Label(frame_izquierdo, text=" DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=5)
    entry_dni_perfil = tk.Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_dni_perfil.grid(row=2, column=1, padx=5, pady=3)
    entry_dni_perfil.insert(0, entry_dni.get())

    # Direccion
    Label(frame_izquierdo, text=" Direccion:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=5)
    entry_direccion_perfil = tk.Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_direccion_perfil.grid(row=3, column=1, padx=5, pady=3)

    # F. Nacimiento
    Label(frame_izquierdo, text=" Fecha de nacimiento:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", padx=5)
    entry_f_nacimiento_perfil = tk.Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_f_nacimiento_perfil.grid(row=4, column=1, padx=5, pady=3)

    def mostrar_foto_en_perfil():
        # Poblar galeria con fotos del editor
        lista_fotos_galeria.delete(0, tk.END)
        for ruta in imagenes_cargadas:
            lista_fotos_galeria.insert(tk.END, os.path.basename(ruta))
        # Si la foto pendiente es b"" significa "quitar foto", mostrar el placeholder
        if foto_pendiente["bytes"] == b"":
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return

        # Si hay foto pendiente nueva, mostrarla
        if foto_pendiente["bytes"] is not None:
            try:
                img = Image.open(BytesIO(foto_pendiente["bytes"]))
                img.thumbnail((300, 300))
                foto_tk = ImageTk.PhotoImage(img)
                visor_foto_perfil.configure(image=foto_tk, text="")
                visor_foto_perfil.image = foto_tk
                return
            except Exception:
                pass

        # Si no, mostrar la de la base
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return
        cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni_txt,))
        fila = cursor.fetchone()
        if fila and fila[0]:
            img = Image.open(BytesIO(fila[0]))
            img.thumbnail((300, 300))
            foto = ImageTk.PhotoImage(img)
            visor_foto_perfil.configure(image=foto, text="")
            visor_foto_perfil.image = foto
        else:
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None

    def subir_foto_perfil(event=None):
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not ruta:
            return
        try:
            with open(ruta, "rb") as f:
                foto_pendiente["bytes"] = f.read()
            mostrar_foto_en_perfil()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la foto: {e}")

    def asignar_foto_galeria(event=None):
        sel = lista_fotos_galeria.curselection()
        if not sel:
            return
        ruta = imagenes_cargadas[sel[0]]
        try:
            with open(ruta, "rb") as f:
                foto_pendiente["bytes"] = f.read()
            mostrar_foto_en_perfil()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo asignar la foto: {e}")
    
    def quitar_foto_perfil():
        foto_pendiente["bytes"] = b""  # b"" = "borrar foto al guardar"
        mostrar_foto_en_perfil()

    def guardar_cambios_perfil():
        nombre = entry_nombre_perfil.get().strip()
        apellido = entry_apellido_perfil.get().strip()
        dni_txt = entry_dni_perfil.get().strip()
        if not (nombre and apellido and dni_txt):
            messagebox.showwarning("Faltan datos", "Completá nombre, apellido y DNI.")
            return
        try:
            dni = int(dni_txt)
        except ValueError:
            messagebox.showerror("Error", "El DNI debe ser numérico.")
            return
        cursor.execute("SELECT id FROM personas WHERE dni = ?", (dni,))
        existe = cursor.fetchone()
        if existe:
            # Tres casos: foto nueva, quitar foto, o no tocar
            if foto_pendiente["bytes"] == b"":
                cursor.execute("""UPDATE personas
                                  SET nombre = ?, apellido = ?, direccion = ?, fecha_nacimiento = ?, foto = NULL
                                  WHERE dni = ?""",
                               (nombre, apellido,
                                entry_direccion_perfil.get().strip(),
                                entry_f_nacimiento_perfil.get().strip(),
                                dni))
            elif foto_pendiente["bytes"] is not None:
                cursor.execute("""UPDATE personas
                                  SET nombre = ?, apellido = ?, direccion = ?, fecha_nacimiento = ?, foto = ?
                                  WHERE dni = ?""",
                               (nombre, apellido,
                                entry_direccion_perfil.get().strip(),
                                entry_f_nacimiento_perfil.get().strip(),
                                sqlite3.Binary(foto_pendiente["bytes"]),
                                dni))
            else:
                cursor.execute("""UPDATE personas
                                  SET nombre = ?, apellido = ?, direccion = ?, fecha_nacimiento = ?
                                  WHERE dni = ?""",
                               (nombre, apellido,
                                entry_direccion_perfil.get().strip(),
                                entry_f_nacimiento_perfil.get().strip(),
                                dni))
        else:
            if foto_pendiente["bytes"] == b"":
                contenido = None
            elif foto_pendiente["bytes"] is not None:
                contenido = sqlite3.Binary(foto_pendiente["bytes"])
            else:
                contenido = None
            try:
                cursor.execute("""INSERT INTO personas (nombre, apellido, dni, direccion, fecha_nacimiento, foto)
                                  VALUES (?, ?, ?, ?, ?, ?)""",
                               (nombre, apellido, dni,
                                entry_direccion_perfil.get().strip(),
                                entry_f_nacimiento_perfil.get().strip(),
                                contenido))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ya existe una persona con ese DNI.")
                return
        conexion.commit()
        refrescar_lista()
        foto_pendiente["bytes"] = None
        messagebox.showinfo("OK", "Datos guardados.")

    def cargar_perfil():
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            messagebox.showwarning("Atencion", "Escriba un DNI")
            return
        lista_personas_perfil.delete(0, tk.END)
        foto_pendiente["bytes"] = None
        cursor.execute("""SELECT nombre, apellido, direccion, fecha_nacimiento
                          FROM personas WHERE dni = ?""", (dni_txt,))
        fila = cursor.fetchone()
        if fila:
            entry_nombre_perfil.delete(0, tk.END); entry_nombre_perfil.insert(0, fila[0])
            entry_apellido_perfil.delete(0, tk.END); entry_apellido_perfil.insert(0, fila[1])
            entry_direccion_perfil.delete(0, tk.END); entry_direccion_perfil.insert(0, fila[2] or "")
            entry_f_nacimiento_perfil.delete(0, tk.END); entry_f_nacimiento_perfil.insert(0, fila[3] or "")
            mostrar_foto_en_perfil()
            cursor.execute("""SELECT id, fecha_entrevista, nombre_profecional, apellido_profecional
                              FROM entrevistas WHERE dni_paciente = ? ORDER BY fecha_entrevista""", (dni_txt,))
            for e in cursor.fetchall():
                lista_personas_perfil.insert(tk.END, f"ID {e[0]} — {e[1]} — {e[2]} {e[3] or ''}")
        else:
            messagebox.showinfo("Error", "No existe ese DNI.")
    def exportar_pdf_paciente():
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            messagebox.showwarning("Atención", "Escribí un DNI primero.")
            return
        exportar_entrevistas_pdf(dni_paciente=dni_txt)

    # Botones
    boton_cargar_perfil = tk.Button(frame_izquierdo, text="Cargar", command=cargar_perfil, bg=VERDE_AZULADO, fg=BLANCO, font=("Segoe UI", 10))
    boton_cargar_perfil.grid(row=2, column=2, sticky="w", padx=5, pady=3)

    boton_entrevistas = Button(frame_izquierdo, text="Entrevistas", command=abrir_desde_principal, bg=VERDE_AZULADO, fg=BLANCO, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12))
    boton_entrevistas.grid(row=8, column=0, sticky="e", padx=5, pady=3)
    boton_editor_fotos = Button(frame_izquierdo, text="Editor de fotos", command=abrir_ventana_editor_fotos, bg=VERDE_AZULADO, fg=BLANCO, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, font=("Segoe UI", 12))
    boton_editor_fotos.grid(row=8, column=1, sticky="e", padx=5, pady=3)
    boton_guardar_perfil = tk.Button(frame_izquierdo, text="Guardar cambios", command=guardar_cambios_perfil, bg=VERDE_AZULADO, fg=BLANCO, font=("Segoe UI", 10))
    boton_guardar_perfil.grid(row=6, column=0, sticky="ew", padx=5, pady=3)
    boton_pdf_paciente = tk.Button(frame_izquierdo, text="PDF de este paciente",command=exportar_pdf_paciente,bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 10))
    boton_pdf_paciente.grid(row=7, column=0, sticky="ew", padx=5, pady=3)

    # --- FRAME DERECHO ---
    frame_derecha = tk.Frame(ventana_perfil, bg=GRIS_NIEBLA)
    frame_derecha.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

    # Foto grande clickeable
    frame_foto_perfil = Frame(frame_derecha, bg=BLANCO, relief="solid", bd=1, height=280)
    frame_foto_perfil.pack(side="top", fill="x", pady=(0, 10))
    frame_foto_perfil.pack_propagate(False)
    visor_foto_perfil = tk.Label(frame_foto_perfil, text="👤\nClic para subir foto",bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 20), cursor="hand2")
    visor_foto_perfil.pack(fill="both", expand=True, padx=10, pady=10)
    visor_foto_perfil.bind("<Button-1>", subir_foto_perfil)

    boton_quitar_foto = tk.Button(frame_derecha, text="Quitar foto", command=quitar_foto_perfil,
bg=ROJO, fg=BLANCO, font=("Segoe UI", 10))
    boton_quitar_foto.pack(side="top", pady=(0, 10))

    # Galeria con fotos del editor
    frame_galeria = Frame(frame_derecha, bg=GRIS_NIEBLA)
    frame_galeria.pack(side="top", fill="x", pady=(0, 10))
    Label(frame_galeria, text="Fotos del editor:",bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 10, "bold")).pack(anchor="w")

    frame_galeria_inner = Frame(frame_galeria, bg=GRIS_NIEBLA, height=120)
    frame_galeria_inner.pack(fill="x")
    frame_galeria_inner.pack_propagate(False)

    scroll_galeria = tk.Scrollbar(frame_galeria_inner, orient="vertical")
    scroll_galeria.pack(side="right", fill="y")
    lista_fotos_galeria = tk.Listbox(frame_galeria_inner, font=("Segoe UI", 10), yscrollcommand=scroll_galeria.set,selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_fotos_galeria.pack(side="left", fill="both", expand=True)
    scroll_galeria.config(command=lista_fotos_galeria.yview)
    lista_fotos_galeria.bind("<<ListboxSelect>>", asignar_foto_galeria)

    # Entrevistas del paciente
    frame_lista_perfil = Frame(frame_derecha, bg=GRIS_AZULADO, relief="solid", bd=1)
    frame_lista_perfil.pack(side="top", fill="both", expand=True, pady=(0, 20))
    Label(frame_lista_perfil, text="Entrevistas del paciente", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold")).pack(side="top", padx=10, pady=10)
    scroll_perfil = tk.Scrollbar(frame_lista_perfil, orient="vertical")
    scroll_perfil.pack(side="right", fill="y")
    lista_personas_perfil = Listbox(frame_lista_perfil, yscrollcommand=scroll_perfil.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_personas_perfil.pack(side="left", fill="both", expand=True)
    scroll_perfil.config(command=lista_personas_perfil.yview)

    mostrar_foto_en_perfil()

# ============================================================================
# BLOQUE 17: VENTANA DEL EDITOR DE FOTOS
# ============================================================================
def abrir_ventana_editor_fotos():
    ventana_editor_fotos = tk.Toplevel(ventana)
    ventana_editor_fotos.title("Editor de fotos")
    ventana_editor_fotos.geometry("600x750")
    ventana_editor_fotos.config(bg=GRIS_NIEBLA)

    frame_editor_fotos_superior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_superior.pack(side="top", fill="both", expand=True)

    visor_foto_editor = Label(frame_editor_fotos_superior, text="👤\nSin foto",
                              bg=BLANCO, fg=NEGRO, relief="solid", bd=1,
                              font=("Segoe UI", 20))
    visor_foto_editor.pack(fill="both", expand=True, padx=10, pady=10)

    frame_lista_imgs = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_lista_imgs.pack(fill="x", padx=10, pady=5)

    label_contador = Label(frame_lista_imgs, text="Imagenes cargadas: 0",font=("Segoe UI", 11, "bold"), bg=VERDE_AZULADO, fg=BLANCO)
    label_contador.pack(fill="x")

    frame_lista_scroll = Frame(frame_lista_imgs, bg=GRIS_NIEBLA)
    frame_lista_scroll.pack(fill="x", pady=5)

    scroll_imgs = tk.Scrollbar(frame_lista_scroll, orient="vertical")
    scroll_imgs.pack(side="right", fill="y")

    lista_imagenes = Listbox(frame_lista_scroll, height=8, font=("Segoe UI", 10),yscrollcommand=scroll_imgs.set)
    lista_imagenes.pack(side="left", fill="both", expand=True)
    scroll_imgs.config(command=lista_imagenes.yview)

    frame_editor_fotos_inferior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_inferior.pack(side="bottom", fill="x", pady=10)
    frame_editor_fotos_inferior.columnconfigure(1, weight=1)
    frame_editor_fotos_inferior.columnconfigure(2, weight=1)

    def actualizar_contador():
        label_contador.config(text=f"Imagenes cargadas: {len(imagenes_cargadas)}")

    def mostrar_previa(ruta):
        try:
            imagen = Image.open(ruta)
            imagen.thumbnail((400, 400))
            imagen_tk = ImageTk.PhotoImage(imagen)
            visor_foto_editor.config(image=imagen_tk, text="")
            visor_foto_editor.image = imagen_tk
        except Exception:
            print("Error al mostrar la imagen:")

    def mostrar_previa_seleccionada(event=None):
        sel = lista_imagenes.curselection()
        if not sel:
            return
        mostrar_previa(imagenes_cargadas[sel[0]])

    lista_imagenes.bind("<<ListboxSelect>>", mostrar_previa_seleccionada)

    def agregar_imagen():
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not ruta:
            return
        imagenes_cargadas.append(ruta)
        lista_imagenes.insert(tk.END, os.path.basename(ruta))
        lista_imagenes.see(tk.END)
        lista_imagenes.selection_clear(0, tk.END)
        lista_imagenes.selection_set(tk.END)
        mostrar_previa(ruta)
        actualizar_contador()

    def eliminar_imagen():
        sel = lista_imagenes.curselection()
        if not sel:
            return
        indice = sel[0]
        del imagenes_cargadas[indice]
        lista_imagenes.delete(indice)
        visor_foto_editor.config(image="", text="👤\nSin foto")
        visor_foto_editor.image = None
        actualizar_contador()
    def limpiar_todas():
        if not messagebox.askyesno("Confirmar", "¿Borrar todas las fotos cargadas?"):
            return
        imagenes_cargadas.clear()
        lista_imagenes.delete(0, tk.END)
        visor_foto_editor.config(image="", text="👤\nSin foto")
        visor_foto_editor.image = None
        actualizar_contador()

    Button(frame_editor_fotos_inferior, text="Añadir fotos", command=agregar_imagen,bg=VERDE_AZULADO, fg=BLANCO, activebackground=VERDE_TERMINAL,activeforeground=NEGRO, font=("Segoe UI", 12)).grid(row=0, column=1, padx=10, sticky="ew")
    Button(frame_editor_fotos_inferior, text="Eliminar fotos", command=eliminar_imagen,bg=VERDE_AZULADO, fg=BLANCO, activebackground=VERDE_TERMINAL,activeforeground=NEGRO, font=("Segoe UI", 12)).grid(row=0, column=2, padx=10, sticky="ew")
    Button(frame_editor_fotos_inferior, text="Limpiar TODAS fotos", command=limpiar_todas,bg=VERDE_AZULADO, fg=BLANCO, activebackground=VERDE_TERMINAL,activeforeground=NEGRO, font=("Segoe UI", 12)).grid(row=0, column=3, padx=10, sticky="ew")

    frame_editor_fotos_inferior.columnconfigure(1, weight=1)
    frame_editor_fotos_inferior.columnconfigure(3, weight=1)

    # Esto deberia generar la lista para ver las fotos
    for ruta in imagenes_cargadas:
        lista_imagenes.insert(tk.END, os.path.basename(ruta))
    actualizar_contador()
    if imagenes_cargadas:
        lista_imagenes.selection_set(tk.END)
        lista_imagenes.see(tk.END)
        mostrar_previa(imagenes_cargadas[-1])
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
    hay_imagen = cargar_imagen()  

    ventana_autores = tk.Toplevel(ventana)
    ventana_autores.title("Licencia y autores de la aplicacion")
    ventana_autores.geometry("1000x800")
    canvas = tk.Canvas(ventana_autores, width=1000, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # ---- Imagen de fondo (si existe) ----
    if hay_imagen:
        cursor.execute("SELECT contenido FROM recursos WHERE nombre = ?", ("sanca",))
        fila = cursor.fetchone()
        img = Image.open(BytesIO(fila[0])).resize((1000, 800))
        foto = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=foto)
        ventana_autores.fondo = foto
    else:
        canvas.configure(bg=BLANCO)       # sin imagen, fondo blanco

    # ---- Títulos (x=500 = mitad del ancho de 1000) ----
    canvas.create_text(500, 80, text="AUTORES",
                       fill=NEGRO, font=("Segoe UI", 28, "bold"))

    canvas.create_text(500, 130, text="EQUIPO DE DESARROLLO",
                       fill=NEGRO, font=("Segoe UI", 16, "bold"))

    # ---- Nombres ----
    nombres = [
        "Antonio Garcia",
        "Nahuel Villafañe",
        "Mateo Dabruzzo Wilczek",
        "Federico 'Fedelobo'",
        "Ignacio",
        "Thiago",
        "Pablo Laporta",
        "Fernando 'Master'",
        "Joaquin Arana",
    ]
    y = 180
    for nombre in nombres:
        canvas.create_text(500, y, text=nombre,
                           fill=NEGRO, font=("Segoe UI", 14))
        y += 30

    # ---- Licencia ----
    y += 30
    canvas.create_text(500, y, text="LICENCIA",
                       fill="#DFDBDB", font=("Segoe UI", 100, "bold"))
                        #fede estubo aqui :3
    y += 40
    canvas.create_text(500, y,
                       text=("© 2026 Equipo de programación Sanca. Todos los derechos reservados.\n\n"
                             "Prohibida la copia, modificación, distribución y uso comercial\n"
                             "del software sin autorización escrita del titular.\n"
                             "Ley 11.723 de Propiedad Intelectual (Argentina)."),
                       fill=NEGRO, font=("Segoe UI", 11),
                       justify="center", width=800)
    # ---- Boton cerrar (encima del canvas) ----
    tk.Button(ventana_autores, text="X", command=ventana_autores.destroy,bg=BLANCO, fg=NEGRO,font=("Segoe UI", 12, "bold")).place(relx=0.95, rely=0.05, anchor="ne")

# ============================================================================
# BLOQUE 20: BOTONES PRINCIPALES QUE ABREN LAS OTRAS VENTANAS
# ============================================================================
def abrir_desde_principal():
    abrir_ventana_entrevistas(ventana)
Button(frame_btn_info, text="Info", command=abrir_ventana_autores, bg=VERDE_AZULADO, fg=BLANCO, relief="flat", highlightthickness=0, activebackground=VERDE_TERMINAL, activeforeground=NEGRO, width=6, font=("Segoe UI", 10, "bold")).pack(side="left", padx=5, pady=5)
refrescar_lista()

# ============================================================================
# BLOQUE 21: DOBLE CLICK PARA ABRIR EL PERFIL
# ============================================================================
def abrir_perfil_doble_clic(event=None):
    if not lista_personas.curselection(): #curselection es para que seleccione con el mouse
        return
    al_seleccionar()
    abrir_ventana_perfil()
lista_personas.bind("<Double-Button-1>", abrir_perfil_doble_clic)
lista_personas.bind("<<ListboxSelect>>", al_seleccionar)
# ============================================================================
# BLOQUE 22: FUNCION GENERAR PDF
# ============================================================================
def crear_pdf_entrevistas(ruta, entrevistas):
    paginas = []
    lineas_pagina = []
    y = 0

    def nueva_pagina():
        nonlocal lineas_pagina, y
        if lineas_pagina:
            paginas.append(lineas_pagina)
        lineas_pagina = []
        y = 790
        lineas_pagina.append(("MEDTRACK | Entrevistas", "F2", 16, 50, y))
        y -= 25
        lineas_pagina.append(("Historial completo de entrevistas", "F1", 10, 50, y))
        y -= 30

    def agregar_linea(texto, negrita=False, tamano=10, sangria=0):
        nonlocal y
        if y < 55:
            nueva_pagina()
        fuente = "F2" if negrita else "F1"
        lineas_pagina.append((texto, fuente, tamano, 50 + sangria, y))
        y -= tamano + 5

    nueva_pagina()
    for entrevista in entrevistas:
        id_entrevista, fecha, dni, profesional, texto, nombre, apellido = entrevista
        agregar_linea(f"Entrevista #{id_entrevista}", negrita=True, tamano=12)
        agregar_linea(f"Fecha: {fecha}    DNI: {dni}")
        paciente = " ".join(parte for parte in (nombre, apellido) if parte) or "No registrado"
        agregar_linea(f"Paciente: {paciente}")
        agregar_linea(f"Profesional: {profesional}")
        agregar_linea("Anotaciones:", negrita=True)

        parrafos = (texto or "").splitlines() or ["Sin anotaciones"]
        for parrafo in parrafos:
            lineas = textwrap.wrap(
                parrafo, width=88, break_long_words=True, break_on_hyphens=False
            ) or [""]
            for linea in lineas:
                agregar_linea(linea, sangria=12)
        agregar_linea("")

    paginas.append(lineas_pagina)

    objetos = [None, None]
    referencias_paginas = []
    id_fuente_regular = 3 + 2 * len(paginas)
    id_fuente_negrita = id_fuente_regular + 1

    for numero, lineas in enumerate(paginas, start=1):
        lineas.append((f"Pagina {numero} de {len(paginas)}", "F1", 9, 490, 35))
        contenido = "".join(
            f"BT /{fuente} {tamano} Tf 1 0 0 1 {x} {pos_y} Tm "
            f"<{texto.encode('cp1252', errors='replace').hex().upper()}> Tj ET\n"
            for texto, fuente, tamano, x, pos_y in lineas
        ).encode("ascii")
        id_pagina = len(objetos) + 1
        id_contenido = id_pagina + 1
        referencias_paginas.append(f"{id_pagina} 0 R")
        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {id_fuente_regular} 0 R "
            f"/F2 {id_fuente_negrita} 0 R >> >> /Contents {id_contenido} 0 R >>".encode("ascii")
        )
        objetos.append(
            f"<< /Length {len(contenido)} >>\nstream\n".encode("ascii")
            + contenido
            + b"\nendstream"
        )

    objetos[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objetos[1] = (
        f"<< /Type /Pages /Kids [{' '.join(referencias_paginas)}] "
        f"/Count {len(referencias_paginas)} >>".encode("ascii")
    )
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    salida = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for numero, objeto in enumerate(objetos, start=1):   # <-- ACA TUVE QUE ARREGLARLO
        offsets.append(len(salida))
        salida.extend(f"{numero} 0 obj\n".encode("ascii"))
        salida.extend(objeto)
        salida.extend(b"\nendobj\n")

    posicion_xref = len(salida)
    salida.extend(f"xref\n0 {len(objetos)+1}\n".encode("ascii"))   # <--ACA TAMBIEN
    salida.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        salida.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    salida.extend(
        f"trailer\n<< /Size {len(objetos)+1} /Root 1 0 R >>\n"   # <-- FIX 4
        f"startxref\n{posicion_xref}\n%%EOF\n".encode("ascii")
    )

    with open(ruta, "wb") as archivo:
        archivo.write(salida)


def exportar_entrevistas_pdf(dni_paciente=None):
    try:
        if dni_paciente:
            cursor.execute(
                """SELECT e.id, e.fecha_entrevista, e.dni_paciente,
                          e.nombre_profecional, e.entrevista,
                          p.nombre, p.apellido
                   FROM entrevistas AS e
                   LEFT JOIN personas AS p ON p.dni = e.dni_paciente
                   WHERE e.dni_paciente = ?
                   ORDER BY e.id""", (dni_paciente,)
            )
        else:
            cursor.execute(
                """SELECT e.id, e.fecha_entrevista, e.dni_paciente,
                          e.nombre_profecional, e.entrevista,
                          p.nombre, p.apellido
                   FROM entrevistas AS e
                   LEFT JOIN personas AS p ON p.dni = e.dni_paciente
                   ORDER BY e.id"""
            )
        entrevistas = cursor.fetchall()
    except sqlite3.Error as error:
        messagebox.showerror("Error al consultar", f"No se pudieron leer las entrevistas: {error}")
        return
    if not entrevistas:
        if dni_paciente:
            messagebox.showinfo("Sin entrevistas", "Ese paciente no tiene entrevistas registradas.")
        else:
            messagebox.showinfo("Sin entrevistas", "No hay entrevistas para exportar.")
        return

    nombre_archivo = f"entrevistas_{dni_paciente}.pdf" if dni_paciente else "entrevistas.pdf"
    ruta = filedialog.asksaveasfilename(
        title="Guardar entrevistas como PDF",
        defaultextension=".pdf",
        initialfile=nombre_archivo,
        filetypes=[("Documento PDF", "*.pdf")],
    )
    if not ruta:
        return

    try:
        crear_pdf_entrevistas(ruta, entrevistas)
    except OSError as error:
        messagebox.showerror("Error al exportar", f"No se pudo crear el PDF: {error}")
        return
    except UnicodeEncodeError:
        messagebox.showerror("Error al exportar",
                             "El texto contiene caracteres no compatibles con la fuente PDF.")
        return
    messagebox.showinfo("PDF creado", f"Entrevistas guardadas en:\n{ruta}")


# ============================================================================
# BLOQUE 23: INICIO DEL PROGRAMA
# ============================================================================
ventana.mainloop()
