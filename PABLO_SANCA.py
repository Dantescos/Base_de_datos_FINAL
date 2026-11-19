# BLOQUE 1: IMPORTACIONES
import zipfile
import traceback
import sqlite3  # Importo sqlite3 para trabajar con la base de datos
import tkinter as tk  # Importo tkinter para la interfaz gráfica
from tkinter import filedialog, messagebox, Label, Button, Entry, Frame, Toplevel, Listbox  # Elementos de tkinter
from io import BytesIO  # Para tratar bytes como archivos en memoria
from PIL import Image, ImageTk, ImageOps  # Pillow para manejo de imágenes
import string  # Para constantes de strings
import os  # Para rutas y archivos
import textwrap  # Para cortar texto
import re  # Para expresiones regulares
import base64  # Para codificar/decodificar base64
#import PyPDF2  # Para leer archivos PDF
import shutil  # Para mover archivos

# BLOQUE 2: IMÁGENES EN BASE64


# BLOQUE 3: BASE DE DATOS
conexion = sqlite3.connect("Centro de Formación Profesional 401  Escuela de oficios SANCA.db")  # Abro o creo la base de datos
cursor = conexion.cursor()  # Creo el cursor

# Base de datos para los cursos
cursor.execute("""CREATE TABLE IF NOT EXISTS personas(id INTEGER PRIMARY KEY AUTOINCREMENT,
especialidad TEXT,
fecha_de_iniciacion TEXT,
lugar_en_el_que_se_dicta TEXT,
fecha_de_terminacion TEXT,
tipo TEXT,
dias TEXT,
horarios TEXT,
docente TEXT,
cantidad_de_modulos TEXT,
curso_numero INTEGER)""")  

# Creo tabla personas
cursor.execute("""CREATE TABLE IF NOT EXISTS personas(
nombres TEXT,
apellido TEXT,
nacionalidad TEXT,
fecha_de_nacimiento TEXT,
documento_de_identidad TEXT,
direccion_domicilio TEXT,
localidad_TEXT,
dni INTEGER UNIQUE NOT NULL, 
edad INTEGER, 
fecha_ingreso TEXT,
telefono TEXT, 
contacto_emergencia TEXT, 
telefono_emergencia TEXT,
obra_social TEXT,
foto BLOB)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS pdf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    formato TEXT NOT NULL,
    contenido BLOB NOT NULL, 
    dni_personas INTEGER)""")  # Creo tabla pdf para fotos/documentos

cursor.execute("""CREATE TABLE IF NOT EXISTS recursos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL, 
    contenido BLOB)""")  # Creo tabla recursos

cursor.execute("PRAGMA table_info(personas)")  # Obtengo info de las columnas
_columnas_personas = {fila[1] for fila in cursor.fetchall()}  # Guardo los nombres de las columnas

for _col, _tipo in (("fecha_egreso", "TEXT"), ("tipo_egreso", "TEXT"), ("motivo_egreso", "TEXT")):
    if _col not in _columnas_personas: cursor.execute(f"ALTER TABLE personas ADD COLUMN {_col} {_tipo}")  # Agrego columnas si no existen

conexion.commit()  # Confirmo los cambios

# BLOQUE 4: PALETA DE COLORES
# PALETA SANCA CFP 401
COLOR_FONDO        = "#FBFAF7"  # fondo general ventana
COLOR_NAVBAR       = "#1B3A6B"  # barra superior
COLOR_TEXTO_NAVBAR = "#FFFFFF"  # letras sobre navbar
COLOR_PANEL        = "#F7E7C6"  # fondo formularios
COLOR_TITULO       = "#2E2E2E"  # labels de títulos
COLOR_LABEL        = "#6B7A8F"  # labels de campos
COLOR_BOTON        = "#3E6FA8"  # botones principales
COLOR_BOTON_TEXTO  = "#FFFFFF"  # letra botones azules
COLOR_ACENTO       = "#F2A63B"  # botones importantes
COLOR_ACENTO_TEXTO = "#2E2E2E"  # letra sobre ámbar
COLOR_EXITO        = "#5E8C6A"  # mensajes OK
COLOR_ERROR        = "#C0392B"  # errores / eliminar
# Viejo colores
# BLOQUE 5: PALETA DE COLORES
ROJO = "#E3000F"  # Rojo fuerte
AMARILLO = "#FCAF17"  # Amarillo
NEGRO = "#0a0a0a"  # Casi negro
GRIS = "#222222"  # Gris oscuro
AZUL_PETROLEO = "#006080"  # Azul petróleo
BLANCO_HUESO = "#F5F5DC"  # Blanco hueso
VERDE_TERMINAL = "#00FF00"  # Verde brillante
GRIS_NIEBLA = "#F4F7F6"  # Gris claro para fondos
BLANCO = "#FFFFFF"  # Blanco puro
GRIS_AZULADO = "#2C3E50"  # Gris azulado oscuro
GRIS_MEDIO = "#7F8C8D"  # Gris medio
AZUL_SERENO = "#4A90E2"  # Azul sereno para selección
VERDE_AZULADO = "#26A69A"  # Verde azulado para botones


# Instrucciones para los colores
#Resumen rápido de uso
#Fondo ventana → Blanco cálido FBFAF7
#Barra superior / navbar → Azul oscuro 1B3A6B con letras blancas
#Fondo de formularios / paneles → Arena F7E7C6
#Labels de títulos → Grafito #2E2E2E
#Labels de campos ("Nombre:", "DNI:") → Gris azulado #6B7A8F
#Botón Guardar/Buscar → Azul medio #3E6FA8 con letra blanca
#Botón Inscribir/Confirmar → Ámbar #F2A63B con letra grafito
#Botón Eliminar → Rojo ladrillo #C0392B con letra blanca
#Mensaje OK → Verde salvia #5E8C6A
#Mensaje Error → Rojo ladrillo #C0392B

#🎨 PALETA SANCA CFP 401
#Color          	HEX	                    Para qué
#Azul oscuro	#1B3A6B	            Fondo de la barra superior (navbar) y títulos grandes. Es el color "institucional", da confianza.
#Azul medio	    #3E6FA8	            Botones principales (Guardar, Buscar, Agregar). También para los bordes de los frames.
#Ámbar/Dorado	#F2A63B	            Botones de acción importante (Inscribir, Confirmar) y para resaltar lo que el usuario tiene que mirar sí o sí.
#Arena clarito	#F7E7C6	            Fondo de los paneles donde van los formularios (el "papel" donde escribís).
#Blanco cálido	#FBFAF7	            Fondo general de la ventana. No es blanco puro, es más suave para la vista.
#Grafito	    #2E2E2E             #Texto de los Labels que son títulos o datos importantes. Letras oscuras sobre fondo claro.
#Gris azulado	#6B7A8F	            Labels secundarios (los que dicen "Nombre:", "DNI:", etc.) y textos de ayuda.
#Blanco	        #FFFFFF             Letras sobre fondo azul oscuro (navbar, botones azules). Para que se lea bien.
#Verde salvia	#5E8C6A	            Mensajes de éxito ("Curso guardado", "Persona registrada"). También para el estado "Activo".
#Rojo ladrillo	#C0392B	            Errores, alertas, botón Eliminar. Solo para cosas que el usuario tiene que frenar y leer.

# BLOQUE 5: VENTANA PRINCIPAL
ventana = tk.Tk()  # Creo la ventana principal
ventana.title("Centro de Formación Profesional 401  Escuela de oficios SANCA")  # Título de la ventana
ventana.config(bg=COLOR_FONDO)  # Fondo

ancho_pantalla = ventana.winfo_screenwidth()  # Ancho de pantalla
alto_pantalla = ventana.winfo_screenheight()  # Alto de pantalla
ancho_ventana = min(1000, int(ancho_pantalla * 0.92))  # Ancho de la ventana
alto_ventana = min(750, int(alto_pantalla * 0.88))  # Alto de la ventana
_x = (ancho_pantalla - ancho_ventana) // 2  # Centrado horizontal
_y = (alto_pantalla - alto_ventana) // 2  # Centrado vertical
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{_x}+{_y}")  # Aplico geometría
ventana.minsize(900, 550)  # Tamaño mínimo

# BLOQUE 6: BANNER
banner = tk.Frame(ventana, bg=COLOR_NAVBAR, height=150)  # Frame del banner
banner.pack(side="top", fill="x")  # Empaquetado arriba
banner.pack_propagate(False)  # Evito que se achique

banner_label = tk.Label(banner, bg=COLOR_NAVBAR, fg=COLOR_FONDO)  # Label del banner
banner_label.pack(expand=True, fill="both")  # Estirado

try:
    if SANCA_BASE64:
        imagen_bytes_SANCA = base64.b64decode(SANCA_BASE64)  # Decodifico base64
        imagen_casa_SANCA = Image.open(BytesIO(imagen_bytes_SANCA))  # Abro la imagen
        imagen_casa_SANCA = ImageOps.fit(imagen_casa_SANCA, (ancho_pantalla, 150), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))  # Ajusto tamaño
        foto_banner = ImageTk.PhotoImage(imagen_casa_SANCA)  # Convierto a PhotoImage
        banner_label.configure(image=foto_banner)  # Aplico al Label
        banner_label.imagen_casa_SANCA = foto_banner  # Guardo referencia
except Exception:
    print('Error')  # Si falla, no rompo la app


# BLOQUE 8: FUNCIONES PRINCIPALES
def refrescar_lista():
    lista_personas.delete(0, tk.END)  # Borro la lista
    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")  # Consulto personas
    for nombre, apellido, dni in cursor.fetchall():
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")  # Inserto en la lista
    cursor.execute("SELECT COUNT(*) FROM personas WHERE LOWER(COALESCE(estado, 'activo')) = 'activo'")  # Cuento activos
    activos = cursor.fetchone()[0]  # Obtengo el número
    contador_legajos.config(text=f"Legajos activos: {activos}")  # Actualizo contador

def mostrar_foto(dni):
    cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))  # Busco la foto
    fila = cursor.fetchone()
    if fila and fila[0]:
        try:
            img = Image.open(BytesIO(fila[0]))  # Abro la imagen
            img.thumbnail((300, 300))  # Redimensiono
            fondo = Image.new("RGB", (300, 300), BLANCO)  # Fondo blanco
            x = (300 - img.width) // 2
            y = (300 - img.height) // 2
            fondo.paste(img, (x, y))  # Pego la imagen
            foto = ImageTk.PhotoImage(fondo)  # Convierto
            visor_foto.configure(image=foto, text="")  # Muestro
            visor_foto.image = foto  # Guardo referencia
            return
        except Exception: pass
    visor_foto.configure(image="", text="👤\nSin foto")  # Placeholder
    visor_foto.image = None

def al_seleccionar(event=None):
    #boton_busqueda_definitivo.grid_remove()  # Oculto botones
    #boton_agregar_definitivo.grid_remove()
    grids_nom_ape()  # Muestro campos
    grids_dni()
    sel = lista_personas.curselection()
    if not sel: return
    texto = lista_personas.get(sel[0])
    dni = int(texto.split("DNI ")[1])  # Extraigo el DNI
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if not fila: return
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, fila[0])  # Cargo nombre
    entry_apellido.delete(0, tk.END)
    entry_apellido.insert(0, fila[1])  # Cargo apellido
    entry_dni.delete(0, tk.END)
    entry_dni.insert(0, fila[2])  # Cargo DNI
    mostrar_foto(dni)  # Muestro foto

def agregar():
    #boton_busqueda_definitivo.grid_remove()  # Oculto buscar
    grids_nom_ape()  # Muestro campos
    grids_dni()
    #boton_agregar_definitivo.grid()  # Muestro confirmar agregar

def agregar_definitivo():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni_txt = entry_dni.get().strip()
    if not (nombre and apellido and dni_txt):
        messagebox.showwarning("Faltan datos", "Completa nombre, apellido y DNI.")  # Aviso
        return
    try: dni = int(dni_txt)  # Convierto a entero
    except ValueError:
        messagebox.showerror("DNI invalido", "El DNI debe ser numerico.")
        return
    ruta = filedialog.askopenfilename(title="Foto (opcional)", filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])  # Pido foto
    contenido = None
    if ruta:
        with open(ruta, "rb") as f: contenido = sqlite3.Binary(f.read())  # Leo bytes
    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)", (nombre, apellido, dni, contenido))  # Inserto
        conexion.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Ya existe una persona con ese DNI.\nVerifica el numero ingresado.")  # DNI duplicado
        return
    except Exception:
        messagebox.showerror("Error inesperado", 'No se pudo guardar')
        return
    refrescar_lista()  # Refresco
    limpiar()  # Limpio
    #boton_agregar_definitivo.grid_remove()  # Oculto botón
    messagebox.showinfo("OK", "Persona agregada.")

def eliminar():
    seleccion = lista_personas.curselection()
    if not seleccion:
        messagebox.showwarning("Atencion", "Selecciona una persona de la lista para eliminar.")
        return
    texto = lista_personas.get(seleccion[0])
    dni = int(texto.split("DNI ")[1])
    if not messagebox.askyesno("Confirmar eliminación", f"¿Estas seguro de que deseas eliminar a esta persona?\n\n{texto}"): return
    #boton_busqueda_definitivo.grid_remove()
    #boton_agregar_definitivo.grid_remove()
    grids_remove_nom_ape()
    grids_remove_dni()
    cursor.execute("DELETE FROM pdf WHERE dni_personas = ?", (dni,))  # Borro pdfs
    cursor.execute("DELETE FROM personas WHERE dni = ?", (dni,))  # Borro persona
    conexion.commit()
    refrescar_lista()
    visor_foto.configure(image="", text="👤\nSin foto")
    visor_foto.image = None
    messagebox.showinfo("OK", "Persona eliminada correctamente.")

def buscar():
    #boton_agregar_definitivo.grid_remove()  # Oculto agregar
    grids_remove_nom_ape()  # Oculto nombre y apellido
    grids_dni()  # Muestro DNI
   # boton_busqueda_definitivo.grid()  # Muestro confirmar búsqueda

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
    grids_nom_ape()
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END)
    entry_apellido.insert(0, fila[1])
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
    visor_foto.configure(image="", text="👤\nSin foto")
    visor_foto.image = None

# BLOQUE 9: FRAME DE BOTONES
frame_btn = Frame(ventana, bg=GRIS_NIEBLA, height=55)  # Frame de botones
frame_btn_info = Frame(ventana, bg=GRIS_NIEBLA)  # Frame botón info
frame_btn_info.pack(side="bottom", fill="x", padx=10, pady=15)
frame_btn.pack(side="top", fill="x", padx=15, pady=10)
frame_btn.pack_propagate(False)

#btn_tema = RoundedButton(frame_btn, 50, 40, 20, NEGRO, BLANCO, text="☾", command=lambda: aplicar_tema())  # Botón tema
#btn_tema.pack(side="right", padx=5, pady=7)

sub_btn = Frame(frame_btn, bg=GRIS_NIEBLA)  # Sub-frame botones
sub_btn.pack(side="left", fill="both", expand=True)
sub_btn.columnconfigure(0, weight=1)
sub_btn.columnconfigure(5, weight=1)

#btn_agregar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO, text="Agregar", command=agregar, hover_color=VERDE_TERMINAL)
#btn_agregar.grid(row=0, column=1, padx=5, pady=7)
#btn_eliminar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO, text="Eliminar", command=eliminar, hover_color=VERDE_TERMINAL)
#btn_eliminar.grid(row=0, column=2, padx=5, pady=7)
#btn_buscar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO, text="Buscar", command=buscar, hover_color=VERDE_TERMINAL)
#btn_buscar.grid(row=0, column=3, padx=5, pady=7)
#btn_limpiar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO, text="Limpiar", command=limpiar, hover_color=VERDE_TERMINAL)
#btn_limpiar.grid(row=0, column=4, padx=5, pady=7)

# BLOQUE 10: FORMULARIO
frame_form = Frame(ventana, bg=GRIS_NIEBLA)  # Frame formulario
frame_form.pack(side="top", fill="x", padx=15, pady=10)

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

# BLOQUE 11: CUERPO
cuerpo = Frame(ventana, bg=GRIS_NIEBLA)  # Frame cuerpo
cuerpo.pack(fill="both", expand=True, padx=40, pady=10)
cuerpo.columnconfigure(0, weight=0)
cuerpo.columnconfigure(1, weight=1)
cuerpo.rowconfigure(0, weight=1)

frame_izquierda = Frame(cuerpo, bg=GRIS_NIEBLA)  # Frame izquierdo
frame_izquierda.grid(row=0, column=0, sticky="n", padx=(20, 40), pady=(45, 0))

frame_foto = Frame(frame_izquierda, bg=BLANCO, relief="solid", bd=1, width=250, height=250)  # Frame foto
frame_foto.pack()
frame_foto.pack_propagate(False)

visor_foto = Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 18))  # Visor foto
visor_foto.pack(expand=True, fill="both")

frame_lista = Frame(cuerpo, bg=GRIS_AZULADO, relief="solid", bd=1)  # Frame lista
frame_lista.grid(row=0, column=1, sticky="nsew", pady=10)

titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold"))
titulo_lista.pack(anchor="w", padx=10, pady=(10, 5))

contador_legajos = tk.Label(frame_lista, text="Legajos activos: 0", bg=GRIS_AZULADO, fg=AMARILLO, font=("Segoe UI", 11, "bold"))
contador_legajos.pack(anchor="w", padx=10, pady=(0, 10))

caja_lista = Frame(frame_lista, bg=BLANCO)  # Caja para la lista
caja_lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))

scroll = tk.Scrollbar(caja_lista, orient="vertical")  # Scroll
scroll.pack(side="right", fill="y")

lista_personas = Listbox(caja_lista, yscrollcommand=scroll.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
lista_personas.pack(side="left", fill="both", expand=True)
scroll.config(command=lista_personas.yview)

# BLOQUE 12: BOTONES DEFINITIVOS
#boton_agregar_definitivo = RoundedButton(frame_form, 350, 40, 20, VERDE_AZULADO, BLANCO, text="Confirmar agregar", command=agregar_definitivo)
#boton_agregar_definitivo.grid(row=1, column=0, columnspan=8,sticky="ew", padx=5, pady=(5, 0))
#boton_agregar_definitivo.grid_remove()

#boton_busqueda_definitivo = RoundedButton(frame_form, 350, 40, 20, VERDE_AZULADO, BLANCO,text="Confirmar busqueda", command=buscar_definitivo)
#boton_busqueda_definitivo.grid(row=1, column=0, columnspan=8,sticky="ew", padx=5, pady=(5, 0))
#boton_busqueda_definitivo.grid_remove()

# BLOQUE 13: MODO OSCURO
tema_oscuro = False  # Bandera modo oscuro
ventanas_secundarias = []  # Lista de ventanas abiertas
_ventana_entrevistas_abierta = None  # Referencia a ventana entrevistas

def actualizar_widget(widget, fondo, panel, texto, acento):
    #if isinstance(widget, RoundedButton):
    #    if widget == btn_tema: widget.set_colors(panel, acento, texto, fondo)  # Botón tema invertido
    #    else: widget.set_colors(acento, VERDE_TERMINAL, BLANCO, fondo)  # Otros botones
        for hijo in widget.winfo_children(): actualizar_widget(hijo, fondo, panel, texto, acento)
        return

    #if isinstance(widget, tk.OptionMenu):
    #    widget.config(bg=panel,fg=texto,activebackground=VERDE_TERMINAL,activeforeground=BLANCO,highlightthickness=0,bd=0,)
        widget["menu"].config(bg=panel,fg=texto,activebackground=acento,activeforeground=BLANCO,bd=0,)
        return

    #clase = widget.winfo_class()
    #if clase in ("Frame", "Labelframe", "Canvas"): widget.config(bg=fondo)
    #elif clase == "Label": widget.config(bg=fondo, fg=texto)
     #elif clase in ("Entry", "Text"): widget.config(bg=panel, fg=texto, insertbackground=texto)
    #elif clase == "Listbox": widget.config(bg=panel, fg=texto, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    #elif clase in ("Button", "Menubutton"): widget.config(bg=acento, fg=BLANCO, activebackground=acento, activeforeground=BLANCO)
    
    #for hijo in widget.winfo_children(): actualizar_widget(hijo, fondo, panel, texto, acento)

def actualizar_ventanas_secundarias():
    if tema_oscuro:
        fondo, panel, texto, acento, boton_luna_bg, boton_luna_fg = NEGRO, GRIS_AZULADO, BLANCO, GRIS_MEDIO, BLANCO, NEGRO
    else:
        fondo, panel, texto, acento, boton_luna_bg, boton_luna_fg = GRIS_NIEBLA, BLANCO, GRIS_AZULADO, VERDE_AZULADO, NEGRO, BLANCO

    ventanas_secundarias[:] = [v for v in ventanas_secundarias if v.winfo_exists()]
    for ventana_hija in ventanas_secundarias:
        ventana_hija.config(bg=fondo)
        for widget in ventana_hija.winfo_children(): actualizar_widget(widget, fondo, panel, texto, acento)

def agregar_boton_luna(ventana_hija):
    if ventana_hija not in ventanas_secundarias: ventanas_secundarias.append(ventana_hija)
    actualizar_ventanas_secundarias()

def aplicar_tema():
    global tema_oscuro
    tema_oscuro = not tema_oscuro

    if tema_oscuro:
        fondo_general, panel, panel_2, texto, texto_secundario = NEGRO, GRIS, GRIS, BLANCO, BLANCO_HUESO
        fondo_banner, boton_accion, boton_hover, boton_texto = NEGRO, GRIS, VERDE_AZULADO, BLANCO
        lista_bg, lista_fg, btn_luna_bg, btn_luna_hover, btn_luna_fg = GRIS, BLANCO, BLANCO, GRIS_MEDIO, NEGRO
    else:
        fondo_general, panel, panel_2, texto, texto_secundario = GRIS_NIEBLA, BLANCO, GRIS_AZULADO, GRIS_AZULADO, GRIS_MEDIO
        fondo_banner, boton_accion, boton_hover, boton_texto = AZUL_SERENO, VERDE_AZULADO, VERDE_TERMINAL, BLANCO
        lista_bg, lista_fg, btn_luna_bg, btn_luna_hover, btn_luna_fg = BLANCO, GRIS_AZULADO, NEGRO, GRIS, BLANCO

    ventana.config(bg=fondo_general)
    banner.config(bg=fondo_general)
    banner_label.config(bg=fondo_general, fg=texto_secundario)
    frame_btn.config(bg=fondo_general)
    frame_btn_info.config(bg=fondo_general)
    frame_form.config(bg=fondo_general)
    cuerpo.config(bg=fondo_general)
    frame_foto.config(bg=panel)
    visor_foto.config(bg=panel, fg=texto_secundario)
    frame_lista.config(bg=panel_2)
    titulo_lista.config(bg=panel_2, fg=texto)
    contador_legajos.config(bg=panel_2, fg=AMARILLO)
    lista_personas.config(bg=lista_bg, fg=lista_fg, selectbackground=AZUL_SERENO, selectforeground=BLANCO)

    for widget in frame_form.winfo_children():
        if isinstance(widget, Label): widget.config(bg=fondo_general, fg=texto)
        elif isinstance(widget, Entry): widget.config(bg=lista_bg, fg=lista_fg, insertbackground=lista_fg)
            
    sub_btn.config(bg=fondo_general)
    #for widget in (btn_agregar, btn_eliminar, btn_buscar, btn_limpiar): widget.set_colors(boton_accion, boton_hover, boton_texto, fondo_general)
    #btn_tema.set_colors(btn_luna_bg, btn_luna_hover, btn_luna_fg, fondo_general)
    for widget in frame_form.winfo_children():
    #    if isinstance(widget, RoundedButton): widget.set_colors(boton_accion, boton_hover, boton_texto, fondo_general)
    #for widget in frame_btn_info.winfo_children():
    #    if isinstance(widget, RoundedButton): widget.set_colors(boton_accion, boton_hover, boton_texto, fondo_general)

#    actualizar_ventanas_secundarias()

# BLOQUE 14: AUXILIARES
#def normalizar_fecha(texto):
#    texto = texto.strip()
#    for i in string.punctuation:
#        if i in (":", "/"): continue
#        texto = texto.replace(i, "/")
#    return texto

#def separar_fecha_hora(texto):
#    texto = normalizar_fecha(texto)
#    match = re.search(r"\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$", texto)
#    if match:
#        hora = match.group(1)
#        fecha = texto[:match.start()].strip()
#        return fecha, hora
#    return texto, ""

#def comprobar_fecha(entry_fecha):
#    fecha, _ = separar_fecha_hora(entry_fecha.get())
#    return fecha

# BLOQUE 18: VENTANA DE PERFIL
#def abrir_ventana_perfil():
#    global entry_dni_perfil_ref
#    ventana_perfil = Toplevel(ventana)
#    ventana_perfil.title("PERFIL")
#    ventana_perfil.geometry("1500x800")
#    ventana_perfil.config(bg=GRIS_NIEBLA)

#    def al_cerrar_perfil():
#        global entry_dni_perfil_ref
#        entry_dni_perfil_ref = None
#        ventana_perfil.destroy()

#    ventana_perfil.protocol("WM_DELETE_WINDOW", al_cerrar_perfil)

#    foto_pendiente = {"bytes": None}
#    dni_original = {"valor": entry_dni.get().strip()}

 #   frame_izquierdo = Frame(ventana_perfil, bg=GRIS_NIEBLA)
  #  frame_izquierdo.pack(side="left", fill="y", padx=15, pady=15)

   # Label(frame_izquierdo, text=" Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", padx=5)
   # entry_nombre_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
   # entry_nombre_perfil.grid(row=0, column=1, padx=5, pady=3)
   # entry_nombre_perfil.insert(0, entry_nombre.get())

    #Label(frame_izquierdo, text=" Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=5)
    #entry_apellido_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_apellido_perfil.grid(row=1, column=1, padx=5, pady=3)
    #entry_apellido_perfil.insert(0, entry_apellido.get())

    #Label(frame_izquierdo, text="Edad:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=5)
    #entry_edad_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_edad_perfil.grid(row=2, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text=" DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=5)
    #entry_dni_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_dni_perfil.grid(row=3, column=1, padx=5, pady=3)
    #entry_dni_perfil.insert(0, entry_dni.get())
    #entry_dni_perfil_ref = entry_dni_perfil

    #Label(frame_izquierdo, text=" Domicilio:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", padx=5)
    #entry_direccion_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_direccion_perfil.grid(row=4, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text=" Fecha de nacimiento:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=5, column=0, sticky="e", padx=5)
    #entry_f_nacimiento_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_f_nacimiento_perfil.grid(row=5, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text=" Fecha de ingreso al instituto:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=6, column=0, sticky="e", padx=5)
    #entry_f_ingreso_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_f_ingreso_perfil.grid(row=6, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Telefono:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=7, column=0, sticky="e", padx=5)
    #entry_telefono_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_telefono_perfil.grid(row=7, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Nombre del contacto de emergencia:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=8, column=0, sticky="e", padx=5)
    #entry_contacto_emergencia_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_contacto_emergencia_perfil.grid(row=8, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Telefono del contacto de emergencia:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=9, column=0, sticky="e", padx=5)
    #entry_tel_emergencia_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_tel_emergencia_perfil.grid(row=9, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Obra social:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=10, column=0, sticky="e", padx=5)
    #entry_obra_social_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_obra_social_perfil.grid(row=10, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Estado:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=11, column=0, sticky="e", padx=5)
    #var_tipo_estado_perfil = tk.StringVar(value="")
    #menu_estado_perfil = tk.OptionMenu(frame_izquierdo, var_tipo_estado_perfil, "Activo", "No activo")
    #menu_estado_perfil.config(font=("Segoe UI", 12), width=22)
    #menu_estado_perfil.grid(row=11, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="direccion:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=12, column=0, sticky="e", padx=5)
    #var_tipo_direccion_perfil = tk.StringVar(value="")
    #menu_direccion_perfil = tk.OptionMenu(frame_izquierdo, var_tipo_direccion_perfil, "Si", "No")
    #menu_direccion_perfil.config(font=("Segoe UI", 12), width=22)
    #menu_direccion_perfil.grid(row=12, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Fecha de ingreso:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=13, column=0, sticky="e", padx=5)
    #entry_fecha_egreso_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_fecha_egreso_perfil.grid(row=13, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Tipo de egreso:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=14, column=0, sticky="e", padx=5)
    #var_tipo_egreso_perfil = tk.StringVar(value="")
    #menu_tipo_egreso_perfil = tk.OptionMenu(frame_izquierdo, var_tipo_egreso_perfil, "Alta", "Derivación", "Voluntario", "Fallecimiento", "Otro", "-")
    #menu_tipo_egreso_perfil.config(font=("Segoe UI", 12), width=22)
    #menu_tipo_egreso_perfil.grid(row=14, column=1, padx=5, pady=3)

    #Label(frame_izquierdo, text="Motivo de egreso:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=15, column=0, sticky="e", padx=5)
    #entry_motivo_egreso_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    #entry_motivo_egreso_perfil.grid(row=15, column=1, padx=5, pady=3)

#    def mostrar_foto_en_perfil():
 #       dni_txt = entry_dni_perfil.get().strip()
        #if dni_txt:
        #    cursor.execute("SELECT nombre FROM pdf WHERE dni_personas = ? ORDER BY id", (dni_txt,))
            filas = cursor.fetchall()
         #   if lista_fotos_galeria.size() != len(filas):
          #      lista_fotos_galeria.delete(0, tk.END)
           #     for (nombre,) in filas: lista_fotos_galeria.insert(tk.END, nombre)
  #      if foto_pendiente["bytes"] == b"":
            #visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            #visor_foto_perfil.image = None
            return
    #     if foto_pendiente["bytes"] is not None:
            try:
                img = Image.open(BytesIO(foto_pendiente["bytes"]))
                img.thumbnail((300, 300))
                foto_tk = ImageTk.PhotoImage(img)
                visor_foto_perfil.configure(image=foto_tk, text="")
                visor_foto_perfil.image = foto_tk
                return
            except Exception: pass
     #   dni_txt = entry_dni_perfil.get().strip()
      #  if not dni_txt:
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return
       # cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni_txt,))
        #fila = cursor.fetchone()
        #if fila and fila[0]:
            try:
                img = Image.open(BytesIO(fila[0]))
                img.thumbnail((300, 300))
                foto = ImageTk.PhotoImage(img)
                visor_foto_perfil.configure(image=foto, text="")
                visor_foto_perfil.image = foto
                return
            except Exception: pass
        #visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
       # visor_foto_perfil.image = None

    def subir_foto_perfil(event=None):
        et = entry_dni_perfil_ref.get()
        ruta = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not ruta: return
        #try:
        #    with open(ruta, "rb") as f: foto_pendiente["bytes"] = f.read()
        #    mostrar_foto_en_perfil()
        #except Exception: messagebox.showerror("Error", 'No se pudo cargar la foto')
        #os.makedirs(str(et), exist_ok=True)
        #shutil.move(ruta, str(et))

    def asignar_foto_galeria(event=None):
      #  sel = lista_fotos_galeria.curselection()
       # if not sel: return
        #dni_txt = entry_dni_perfil.get().strip()
        #if not dni_txt: return
      #  cursor.execute("SELECT contenido FROM pdf WHERE dni_personas = ? ORDER BY id", (dni_txt,))
        filas = cursor.fetchall()
      #  if sel[0] >= len(filas): return
        #foto_pendiente["bytes"] = filas[sel[0]][0]
        #mostrar_foto_en_perfil()

    def quitar_foto_perfil():
        #foto_pendiente["bytes"] = b""
        #mostrar_foto_en_perfil()

    #def guardar_cambios_perfil():
    #    nombre = entry_nombre_perfil.get().strip()
    #    apellido = entry_apellido_perfil.get().strip()
    #    dni_txt = entry_dni_perfil.get().strip()
    #    if not (nombre and apellido and dni_txt):
            messagebox.showwarning("Faltan datos", "Completa nombre, apellido y DNI.")
            return
    #    try: dni = int(dni_txt)
    #    except ValueError:
    #        messagebox.showerror("Error", "El DNI debe ser numerico.")
            return
    #    edad_txt = entry_edad_perfil.get().strip()
    #    edad = int(edad_txt) if edad_txt.isdigit() else None
    #    direccion = entry_direccion_perfil.get().strip()
  #      f_nacimiento = comprobar_fecha(entry_f_nacimiento_perfil)
  #      f_ingreso = comprobar_fecha(entry_f_ingreso_perfil)
  #      telefono = entry_telefono_perfil.get().strip()
 #       contacto_emergencia = entry_contacto_emergencia_perfil.get().strip()
 #       tel_emergencia = entry_tel_emergencia_perfil.get().strip()
  #      obra_social = entry_obra_social_perfil.get().strip()
   #     estado = var_tipo_estado_perfil.get()
    #    direccion = var_tipo_direccion_perfil.get()
    #    fecha_egreso = comprobar_fecha(entry_fecha_egreso_perfil)
     #   tipo_egreso = var_tipo_egreso_perfil.get().strip()
     #   motivo_egreso = entry_motivo_egreso_perfil.get().strip()
      #  if estado != "No activo":
            estado = "No activo"
            var_tipo_estado_perfil.set("No activo")
     #   if tipo_egreso == "-" and estado != "Activo":
            estado = "Activo"
            var_tipo_estado_perfil.set("Activo")
   #     if foto_pendiente["bytes"] == b"":
            foto_contenido = None
            borrar_foto = True
    #    elif foto_pendiente["bytes"] is not None:
            foto_contenido = sqlite3.Binary(foto_pendiente["bytes"])
            borrar_foto = False
     #   else:
            foto_contenido = None
            borrar_foto = False
      #  dni_cargado = dni_original["valor"]
     #   if dni_cargado:
            if str(dni) != str(dni_cargado):
                cursor.execute("SELECT id FROM personas WHERE dni = ?", (dni,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Ya existe otra persona con ese DNI.")
                    return
                cursor.execute("UPDATE pdf SET dni_personas = ? WHERE dni_personas = ?", (dni, dni_cargado))
                cursor.execute("""UPDATE personas SET nombre = ?, apellido = ?, edad = ?, direccion = ?, fecha_nacimiento = ?,
                                fecha_ingreso = ?, telefono = ?, contacto_emergencia = ?, telefono_emergencia = ?, obra_social = ?, estado = ?, direccion = ?,
                                fecha_egreso = ?, tipo_egreso = ?, motivo_egreso = ? WHERE dni = ?""",
                                (nombre, apellido, edad, direccion, f_nacimiento, f_ingreso, telefono, contacto_emergencia, tel_emergencia, obra_social, estado,
                                 direccion, fecha_egreso, tipo_egreso, motivo_egreso, dni))
                dni_original["valor"] = str(dni)
                entry_dni_perfil.delete(0, tk.END)
                entry_dni_perfil.insert(0, dni)
                if borrar_foto: cursor.execute("UPDATE personas SET foto = NULL WHERE dni = ?", (dni,))
                elif foto_contenido is not None: cursor.execute("UPDATE personas SET foto = ? WHERE dni = ?", (foto_contenido, dni))
            else:
                cursor.execute("""UPDATE personas SET dni = ?, nombre = ?, apellido = ?, edad = ?, direccion = ?, fecha_nacimiento = ?, fecha_ingreso = ?,
                                telefono = ?, contacto_emergencia = ?, telefono_emergencia = ?, obra_social = ?, estado = ?, direccion = ?, fecha_egreso = ?,
                                tipo_egreso = ?, motivo_egreso = ? WHERE dni = ?""",
                                (dni, nombre, apellido, edad, direccion, f_nacimiento, f_ingreso, telefono, contacto_emergencia, tel_emergencia, obra_social,
                                 estado, direccion, fecha_egreso, tipo_egreso, motivo_egreso, dni_cargado))
                if borrar_foto: cursor.execute("UPDATE personas SET foto = NULL WHERE dni = ?", (dni,))
                elif foto_contenido is not None: cursor.execute("UPDATE personas SET foto = ? WHERE dni = ?", (foto_contenido, dni))
    #    else:
            try:
                cursor.execute("""INSERT INTO personas(nombre, apellido, dni, edad, direccion, fecha_nacimiento, fecha_ingreso, telefono, contacto_emergencia,
                                telefono_emergencia, obra_social, estado, direccion, fecha_egreso, tipo_egreso, motivo_egreso, foto)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (nombre, apellido, dni, edad, direccion, f_nacimiento, f_ingreso, telefono, contacto_emergencia, tel_emergencia, obra_social,
                                 estado, direccion, fecha_egreso, tipo_egreso, motivo_egreso, foto_contenido))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ya existe una persona con ese DNI.")
                return
        #    dni_original["valor"] = str(dni)
    #    conexion.commit()
   #     refrescar_lista()
        #foto_pendiente["bytes"] = None
    #    messagebox.showinfo("OK", "Datos guardados.")

    def cargar_perfil():
        dni_txt = entry_dni.get().strip()
        #lista_personas_perfil.delete(0, tk.END)
        #foto_pendiente["bytes"] = None
        cursor.execute("""SELECT nombre, apellido, edad, direccion, fecha_nacimiento, fecha_ingreso, telefono, contacto_emergencia,
                        telefono_emergencia, obra_social, estado, direccion, fecha_egreso, tipo_egreso, motivo_egreso FROM personas WHERE dni = ?""", (dni_txt,))
        #fila = cursor.fetchone()
    #    if fila:
      #      entry_nombre_perfil.delete(0, tk.END)
     #       entry_nombre_perfil.insert(0, fila[0])
       #     entry_apellido_perfil.delete(0, tk.END)
        #    entry_apellido_perfil.insert(0, fila[1])
         #   entry_edad_perfil.delete(0, tk.END)
          #  entry_edad_perfil.insert(0, fila[2] or "")
           # entry_direccion_perfil.delete(0, tk.END)
            #entry_direccion_perfil.insert(0, fila[3] or "")
            #entry_f_nacimiento_perfil.delete(0, tk.END)
 #           entry_f_nacimiento_perfil.insert(0, fila[4] or "")
  #          entry_f_ingreso_perfil.delete(0, tk.END)
  #          entry_f_ingreso_perfil.insert(0, fila[5] or "")
   #         entry_telefono_perfil.delete(0, tk.END)
    #        entry_telefono_perfil.insert(0, fila[6] or "")
     #       entry_contacto_emergencia_perfil.delete(0, tk.END)
      #      entry_contacto_emergencia_perfil.insert(0, fila[7] or "")
       #     entry_tel_emergencia_perfil.delete(0, tk.END)
        #    entry_tel_emergencia_perfil.insert(0, fila[8] or "")
         #   entry_obra_social_perfil.delete(0, tk.END)
          #  entry_obra_social_perfil.insert(0, fila[9] or "")
           # var_tipo_estado_perfil.set(fila[10] or "")
            #var_tipo_direccion_perfil.set(fila[11] or "")
            #entry_fecha_egreso_perfil.delete(0, tk.END)
#            entry_fecha_egreso_perfil.insert(0, fila[12] or "")
 #           var_tipo_egreso_perfil.set(fila[13] or "")
  #          entry_motivo_egreso_perfil.delete(0, tk.END)
   #         entry_motivo_egreso_perfil.insert(0, fila[14] or "")
    #        dni_original["valor"] = dni_txt
      #      mostrar_foto_en_perfil()
       # else: messagebox.showinfo("Error", "No existe ese DNI.")

    #def _texto_ficha_paciente():
    #    dni_txt = entry_dni_perfil.get().strip()
   #     if not dni_txt:
            #messagebox.showwarning("Atencion", "Escribi un DNI primero.")
            #return None
        cursor.execute("""SELECT nombre, apellido, dni, edad, fecha_nacimiento, fecha_ingreso, telefono, direccion, contacto_emergencia,
                        telefono_emergencia, obra_social, estado, direccion, fecha_egreso, tipo_egreso, motivo_egreso FROM personas WHERE dni = ?""", (dni_txt,))
        p = cursor.fetchone()
        if not p:
            messagebox.showinfo("Sin resultados", "No existe ese DNI.")
            return None
        nombre_completo = f"{p[0] or ''} {p[1] or ''}".strip()
        # El ## es para el título, el # para los subtítulos
        lineas = [
            f"## {nombre_completo}",
            f"DNI: {p[2] or '-'}  |  Edad: {p[3] or '-'}  |  Estado: {p[11] or '-'}",
            "",
            "# DATOS PERSONALES",
            f"Nombre: {p[0] or '-'}",
            f"Apellido: {p[1] or '-'}",
            f"DNI: {p[2] or '-'}",
            f"Edad: {p[3] or '-'}",
            f"Fecha de nacimiento: {p[4] or '-'}",
            "",
            "# CONTACTO",
            f"Telefono: {p[6] or '-'}",
            f"Domicilio: {p[7] or '-'}",
            f"Contacto de emergencia: {p[8] or '-'}",
            f"Telefono de emergencia: {p[9] or '-'}",
            "",
            "# SALUD",
            f"Obra social: {p[10] or '-'}",
            f"direccion: {p[12] or '-'}",
            "",
            "# ESTADO",
            f"Fecha de ingreso: {p[5] or '-'}",
            f"Fecha de egreso: {p[13] or '-'}",
            f"Tipo de egreso: {p[14] or '-'}",
            f"Motivo de egreso: {p[15] or '-'}",
        ]
        return "\n".join(lineas)

    def exportar_pdf_paciente():
     #   texto = _texto_ficha_paciente()
       # if texto is None: return
        #ruta = filedialog.asksaveasfilename(title="Guardar perfil como PDF", defaultextension=".pdf",
      #      initialfile=f"perfil_{entry_dni_perfil.get().strip()}.pdf", filetypes=[("PDF", "*.pdf")])
       # if not ruta: return
        #dni = entry_dni_perfil.get().strip()
        #cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
        fila = cursor.fetchone()
        foto_bytes = fila[0] if fila and fila[0] else None
        #try:
        #    crear_pdf_de_texto(ruta, texto, foto_bytes)
         #   messagebox.showinfo("OK", f"Perfil guardado en:\n{ruta}")
        #except Exception:
        #    traceback.print_exc()
        #    messagebox.showerror("Error", "No se pudo crear el PDF.")

    def exportar_word_paciente():
        #texto = _texto_ficha_paciente()
        if texto is None: return
       # ruta = filedialog.asksaveasfilename(title="Guardar perfil como Word", defaultextension=".rtf",
       #      initialfile=f"perfil_{entry_dni_perfil.get().strip()}.rtf", filetypes=[("Word (RTF)", "*.rtf")])
        #if not ruta: return
        
        # --- NUEVO: Obtener la foto ---
        #dni = entry_dni_perfil.get().strip()
        #cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
        fila = cursor.fetchone()
        foto_bytes = fila[0] if fila and fila[0] else None
        # ------------------------------

       # try:
            # --- NUEVO: Pasar la foto ---
         #   crear_word_de_texto(ruta, texto, foto_bytes)
            # -----------------------------
    #        messagebox.showinfo("OK", f"Perfil guardado en:\n{ruta}")
      #  except Exception:
     #       traceback.print_exc()
       #     messagebox.showerror("Error", "No se pudo crear el Word.")

    #boton_guardar_perfil = RoundedButton(frame_izquierdo, 160, 40, 20,VERDE_AZULADO, BLANCO,text="Guardar cambios",command=guardar_cambios_perfil)
    #boton_guardar_perfil.grid(row=16, column=0, padx=10, pady=5, sticky="ew")
    #boton_editor_fotos = RoundedButton(frame_izquierdo, 120, 40, 20,VERDE_AZULADO, BLANCO,text="Editar fotos",command=abrir_ventana_editor_fotos)
    #boton_editor_fotos.grid(row=16, column=1, padx=10, sticky="ew")
    
    #boton_pdf_paciente = RoundedButton(frame_izquierdo, 200, 40, 20,VERDE_AZULADO, BLANCO,text="PDF de este paciente",command=exportar_pdf_paciente)
    #boton_pdf_paciente.grid(row=17, column=0, padx=10, sticky="ew")
    #boton_word_paciente = RoundedButton(frame_izquierdo, 210, 40, 20,VERDE_AZULADO, BLANCO,text="Word de este paciente",command=exportar_word_paciente)
    #boton_word_paciente.grid(row=17, column=1, padx=10, sticky="ew")
    #boton_ver_doc = RoundedButton(frame_izquierdo, 210, 40, 20,VERDE_AZULADO, BLANCO,text="Ver/Editar documento",command=lambda: abrir_ventana_ver_documento(entry_dni_perfil.get().strip()))
    #boton_ver_doc.grid(row=17, column=2, columnspan=2, padx=10, pady=5, sticky="ew")
    #boton_word_legajo = RoundedButton(frame_izquierdo, 230, 40, 20, VERDE_AZULADO, BLANCO, text="Legajo en formato Word", command=lambda: exportar_entrevistas_word(entry_dni_perfil.get().strip() or None))
    #boton_word_legajo.grid(row=18, column=1, padx=10, pady=5, sticky="ew")
    #boton_pdf_legajo = RoundedButton(frame_izquierdo, 230, 40, 20, VERDE_AZULADO, BLANCO, text="Legajo en formato PDF", command=lambda: exportar_entrevistas_pdf(entry_dni_perfil.get().strip() or None))
    #boton_pdf_legajo.grid(row=18, column=0, padx=10, pady=5, sticky="ew")

    #frame_derecha = tk.Frame(ventana_perfil, bg=GRIS_NIEBLA)
    #frame_derecha.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)
    #frame_foto_perfil = Frame(frame_derecha, bg=BLANCO, relief="solid",bd=1, height=280)
    #frame_foto_perfil.pack(side="top", fill="x", pady=(0, 10))
    #frame_foto_perfil.pack_propagate(False)
    #visor_foto_perfil = tk.Label(frame_foto_perfil,text="👤\nClic para subir foto",bg=BLANCO, fg=GRIS_MEDIO,font=("Segoe UI", 20), cursor="hand2")
    #visor_foto_perfil.pack(fill="both", expand=True, padx=10, pady=10)
    #visor_foto_perfil.bind("<Button-1>", subir_foto_perfil)
    #boton_quitar_foto = RoundedButton(frame_derecha, 100, 40, 20,VERDE_AZULADO, BLANCO,text="Quitar foto",command=quitar_foto_perfil)
    #boton_quitar_foto.pack(side="top", padx=10, pady=5)
    #frame_galeria = Frame(frame_derecha, bg=GRIS_NIEBLA)
    #frame_galeria.pack(side="top", fill="x", pady=(0, 10))
    #Label(frame_galeria, text="Fotos del editor:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
    #frame_galeria_inner = Frame(frame_galeria, bg=GRIS_NIEBLA, height=120)
    #frame_galeria_inner.pack(fill="x")
    #frame_galeria_inner.pack_propagate(False)
    #scroll_galeria = tk.Scrollbar(frame_galeria_inner, orient="vertical")
    #scroll_galeria.pack(side="right", fill="y")
    #lista_fotos_galeria = tk.Listbox(frame_galeria_inner, font=("Segoe UI", 10), yscrollcommand=scroll_galeria.set, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    #lista_fotos_galeria.pack(side="left", fill="both", expand=True)
    #scroll_galeria.config(command=lista_fotos_galeria.yview)
    #lista_fotos_galeria.bind("<<ListboxSelect>>", asignar_foto_galeria)
    #frame_lista_perfil = Frame(frame_derecha, bg=GRIS_AZULADO, relief="solid", bd=1)
    #frame_lista_perfil.pack(side="top", fill="both", expand=True, pady=(0, 20))
    #Label(frame_lista_perfil, text="Entrevistas del paciente", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold")).pack(side="top", padx=10, pady=10)
     #scroll_perfil = tk.Scrollbar(frame_lista_perfil, orient="vertical")
    #scroll_perfil.pack(side="right", fill="y")
    #lista_curos_hechos = Listbox(frame_lista_perfil, yscrollcommand=scroll_perfil.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    #lista_curos_hechos.pack(side="left", fill="both", expand=True)
    #scroll_perfil.config(command=lista_curos_hechos.yview)
    #mostrar_foto_en_perfil()
    #agregar_boton_luna(ventana_perfil)
    cargar_perfil()

# BLOQUE 19: EDITOR DE FOTOS
def abrir_ventana_editor_fotos():
    ventana_editor_fotos = tk.Toplevel(ventana)
    ventana_editor_fotos.title("Editor de fotos")
    ventana_editor_fotos.geometry("600x750")
    ventana_editor_fotos.config(bg=GRIS_NIEBLA)

    try: dni_actual = entry_dni_perfil_ref.get().strip() if entry_dni_perfil_ref is not None else ""
    except tk.TclError: dni_actual = ""

    frame_editor_fotos_superior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_superior.pack(side="top", fill="both", expand=True)
    visor_foto_editor = Label(frame_editor_fotos_superior, text="👤\nSin foto", bg=BLANCO, fg=NEGRO, relief="solid", bd=1, font=("Segoe UI", 20))
    visor_foto_editor.pack(fill="both", expand=True, padx=10, pady=10)

    frame_lista_imgs = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_lista_imgs.pack(fill="x", padx=10, pady=5)
    label_contador = Label(frame_lista_imgs, text="Imagenes cargadas: 0", font=("Segoe UI", 11, "bold"), bg=VERDE_AZULADO, fg=BLANCO)
    label_contador.pack(fill="x")
    frame_lista_scroll = Frame(frame_lista_imgs, bg=GRIS_NIEBLA)
    frame_lista_scroll.pack(fill="x", pady=5)
    scroll_imgs = tk.Scrollbar(frame_lista_scroll, orient="vertical")
    scroll_imgs.pack(side="right", fill="y")
    lista_imagenes = Listbox(frame_lista_scroll, height=8, font=("Segoe UI", 10), yscrollcommand=scroll_imgs.set)
    lista_imagenes.pack(side="left", fill="both", expand=True)
    scroll_imgs.config(command=lista_imagenes.yview)
    frame_editor_fotos_inferior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    frame_editor_fotos_inferior.pack(side="bottom", fill="x", pady=10)
    ids_imagenes = []

    def refrescar_lista_imagenes():
        lista_imagenes.delete(0, tk.END)
        ids_imagenes.clear()
        if not dni_actual:
            label_contador.config(text="Imagenes cargadas: 0")
            return
        cursor.execute("SELECT id, nombre FROM pdf WHERE dni_personas = ? ORDER BY id", (dni_actual,))
        filas = cursor.fetchall()
        for id_img, nombre in filas:
            lista_imagenes.insert(tk.END, nombre)
            ids_imagenes.append(id_img)
        label_contador.config(text=f"Imagenes cargadas: {len(filas)}")

    def mostrar_previa_desde_db(index):
        if not (0 <= index < len(ids_imagenes)): return
        id_img = ids_imagenes[index]
        cursor.execute("SELECT contenido FROM pdf WHERE id = ?", (id_img,))
        fila = cursor.fetchone()
        if fila and fila[0]:
            try:
                imagen = Image.open(BytesIO(fila[0]))
                imagen.thumbnail((400, 400))
                imagen_tk = ImageTk.PhotoImage(imagen)
                visor_foto_editor.config(image=imagen_tk, text="")
                visor_foto_editor.image = imagen_tk
            except Exception:
                visor_foto_editor.image = None
                print("Error al mostrar la imagen:")

    def mostrar_previa_seleccionada(event=None):
        sel = lista_imagenes.curselection()
        if not sel: return
        mostrar_previa_desde_db(sel[0])

    lista_imagenes.bind("<<ListboxSelect>>", mostrar_previa_seleccionada)

    def agregar_imagen():
        et = entry_dni_perfil_ref.get()
        if not dni_actual:
            messagebox.showwarning("Atencion","Primero carga un DNI en el perfil para asociar las fotos.")
            return
        ruta = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not ruta: return
        try:
            with open(ruta, "rb") as archivo: contenido = archivo.read()
            nombre = os.path.basename(ruta)
            formato = os.path.splitext(nombre)[1].lstrip(".").lower() or "img"
            cursor.execute("INSERT INTO pdf (nombre, formato, contenido, dni_personas) VALUES (?, ?, ?, ?)", (nombre, formato, sqlite3.Binary(contenido), dni_actual))
            conexion.commit()
            refrescar_lista_imagenes()
            lista_imagenes.selection_clear(0, tk.END)
            lista_imagenes.selection_set(tk.END)
            mostrar_previa_desde_db(len(ids_imagenes) - 1)
        except Exception: messagebox.showerror('Error')
        os.makedirs(str(dni_actual), exist_ok=True)
        shutil.move(ruta, str(dni_actual))

    def eliminar_imagen():
        sel = lista_imagenes.curselection()
        if not sel:
            messagebox.showwarning("Atencion", "Selecciona una foto de la lista.")
            return
        id_img = ids_imagenes[sel[0]]
        if not messagebox.askyesno("Confirmar", "¿Eliminar esta foto?"): return
        cursor.execute("DELETE FROM pdf WHERE id = ?", (id_img,))
        conexion.commit()
        visor_foto_editor.config(image="", text="👤\nSin foto")
        visor_foto_editor.image = None
        refrescar_lista_imagenes()

    def limpiar_todas():
        if not dni_actual:
            messagebox.showwarning("Atencion", "No hay DNI cargado.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Borrar TODAS las fotos del DNI {dni_actual}?"): return
        cursor.execute("DELETE FROM pdf WHERE dni_personas = ?", (dni_actual,))
        conexion.commit()
        visor_foto_editor.config(image="", text="👤\nSin foto")
        visor_foto_editor.image = None
        refrescar_lista_imagenes()

    frame_editor_fotos_inferior.columnconfigure(0, weight=1)
    frame_editor_fotos_inferior.columnconfigure(5, weight=1)
    #RoundedButton(frame_editor_fotos_inferior, 250, 40, 20, VERDE_AZULADO, BLANCO, text="Agregar imagen", command=agregar_imagen).grid(row=0, column=2, padx=10, sticky="ew")
    #RoundedButton(frame_editor_fotos_inferior, 250, 40, 20, VERDE_AZULADO, BLANCO, text="Eliminar imagen", command=eliminar_imagen).grid(row=0, column=3, padx=10, sticky="ew")
    #RoundedButton(frame_editor_fotos_inferior, 250, 40, 20, VERDE_AZULADO, BLANCO, text="Limpiar TODAS", command=limpiar_todas).grid(row=0, column=4, padx=10, sticky="ew")
    agregar_boton_luna(ventana_editor_fotos)
    refrescar_lista_imagenes()

# BLOQUE 20: IMAGEN DE SANCA
def cargar_imagen():
    def cargar_perfil():
        #fede estubo aqui :3
     #   ista_curos_hechos.delete(0, tk.END)
        cursor.execute("SELECT * FROM empleados")
    
        for u in cursor.fetchall():
      #      lista_curos_hechos.insert(tk.END, u)
            print("222")

def obtener_bytes_sanca():
    if not SANCA_BASE64: return None
    cursor.execute("SELECT contenido FROM recursos WHERE nombre = ?", ("sanca",))
    fila = cursor.fetchone()
    if not fila or not fila[0]: return None
    return fila[0]

# BLOQUE 21: AUTORES
def abrir_ventana_autores():
    cargar_imagen()
    ventana_autores = tk.Toplevel(ventana)
    ventana_autores.title("Licencia y autores")
    ventana_autores.geometry("1000x650")
    ventana_autores.config(bg=AZUL_PETROLEO)

    frame_textos = Frame(ventana_autores, bg=AZUL_PETROLEO, width=450)
    frame_textos.pack(side="left", fill="y", padx=(60, 0)) 
    frame_textos.pack_propagate(False)
    Label(frame_textos, text="AUTORES", bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 32, "bold")).pack(pady=(40, 5))
    Label(frame_textos, text="EQUIPO DE DESARROLLO", bg=AZUL_PETROLEO,fg=AMARILLO, font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
    nombres = ["Antonio Garcia", "Nahuel Villafañe", "Mateo Dabruzzo Wilczek", "Federico 'Fedelobo'", "Ignacio", "Thiago", "Pablo Laporta", "Fernando 'Master' Yapuray",]
    for nombre in nombres: Label(frame_textos, text=nombre, bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 12)).pack(pady=2)
    Label(frame_textos, text="___________________________________________", bg=AZUL_PETROLEO, fg=GRIS_MEDIO).pack(pady=15)
    Label(frame_textos, text="LICENCIA", bg=AZUL_PETROLEO, fg=BLANCO, font=("Segoe UI", 18, "bold")).pack(pady=5)
    texto_legal = ("© 2026 Equipo de programación Sanca.\n" "Todos los derechos reservados.\n\n" "Prohibida la copia, modificación, distribución\n" "y uso comercial del software sin\n" "autorización escrita del titular.\n\n" "Ley 11.723 de Propiedad Intelectual.")
    Label(frame_textos, text=texto_legal, bg=AZUL_PETROLEO, fg=GRIS_NIEBLA, font=("Segoe UI", 12), justify="center").pack()

    frame_foto = Frame(ventana_autores, bg=BLANCO)
    frame_foto.pack(side="right", fill="both", expand=True, padx=(20, 40))
    bytes_sanca = obtener_bytes_sanca()
    if bytes_sanca:
        img = Image.open(BytesIO(bytes_sanca))
        img.thumbnail((550, 550))
        foto_tk = ImageTk.PhotoImage(img)
        label_foto = Label(frame_foto, image=foto_tk, bg=BLANCO)
        label_foto.image = foto_tk
        label_foto.pack(expand=True)
    else:
        Label(frame_foto, text="No se encontró la imagen", bg=BLANCO, fg=NEGRO).pack(expand=True)

#    boton_cerrar = RoundedButton(ventana_autores, 40, 30, 15, ROJO, BLANCO, text="X", command=ventana_autores.destroy)
#    boton_cerrar.place(relx=1.0, rely=0.0, anchor="ne", x=-15, y=15)
    agregar_boton_luna(ventana_autores)

# BLOQUE 22: DOBLE CLIC PARA PERFIL
def abrir_perfil_doble_clic(event=None):
    if not lista_personas.curselection(): return
    al_seleccionar()
#    abrir_ventana_perfil()
lista_personas.bind("<Double-Button-1>", abrir_perfil_doble_clic)
lista_personas.bind("<<ListboxSelect>>", al_seleccionar)

# BLOQUE 24: crear_word_de_texto

def crear_word_de_texto(ruta, texto, foto_bytes=None):
    def escapar_rtf(s):
        salida = []
        for ch in s:
            if ch == "\\": salida.append("\\\\")
            elif ch == "{": salida.append("\\{")
            elif ch == "}": salida.append("\\}")
            elif ord(ch) > 127:
                try:
                    val = ord(ch)
                    if val < 0: val += 65536
                    if val < 32768: salida.append(f"\\u{val}?")
                    else: salida.append(f"\\u{val - 65536}?")
                except: salida.append(ch)
            else: salida.append(ch)
        return "".join(salida)

    partes = [
        "{\\rtf1\\ansi\\deff0",
        "{\\fonttbl{\\f0 Arial;}}",
        "{\\colortbl ;\\red0\\green0\\blue0;}",
        "\\paperw11906\\paperh16838\\margl1000\\margr1000\\margt1000\\margb1000",
        "\\viewkind4\\uc1\\pard\\cf1\\f0\\fs24\n"
    ]

    img_rtf = ""
    if foto_bytes:
        try:
            img = Image.open(BytesIO(foto_bytes))
            ancho_orig, alto_orig = img.size
            
            # =====================================================================
            # TAMAÑO DE LA FOTO EN EL WORD:
            # Acá definimos el ancho y alto EXACTO en "twips" (1 pulgada = 1440 twips).
            # \picwgoal4320 = 3 pulgadas de ancho (aprox 7.6 cm).
            # \pichgoal5760 = 4 pulgadas de alto (aprox 10 cm).
            # 
            # SI QUERÉS LA FOTO MÁS GRANDE: aumentá estos dos números.
            # SI QUERÉS LA FOTO MÁS CHICA: reducilos.
            # Para mantener la proporción, calculá: (4320 * alto_orig) / ancho_orig
            # =====================================================================
            
            ancho_deseado = 4320 
            alto_deseado = int((ancho_deseado * alto_orig) / ancho_orig) if ancho_orig else 4320

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_hex = buffer.getvalue().hex()

            # Usamos \picwgoal y \pichgoal para forzar el tamaño visual
            img_rtf = f"{{\\pict\\pngblip\\picw{ancho_orig}\\pich{alto_orig}\\picwgoal{ancho_deseado}\\pichgoal{alto_deseado} {img_hex}}}"
        except Exception as e:
            print("Error al cargar la imagen:", e)

    # --- ESTRUCTURA DE LA TABLA ---
    # \cellx4000 = La columna del texto ocupa hasta el twip 4000 (aprox 7cm).
    # \cellx9500 = La columna de la foto ocupa desde 4000 hasta 9500.
    partes.append("\\trowd\\trgaph108\\trleft0\\trpaddl108\\trpaddr108\\trpaddfl3\\trpaddfr3")
    partes.append("\\cellx4000\\cellx9500")
    
    # --- COLUMNA IZQUIERDA (TEXTO) ---
    partes.append("\\pard\\intbl\\ql ")
    
    for linea in (texto.splitlines() or [""]):
        if linea.startswith("## "): 
            partes.append(f"\\pard\\intbl\\b\\fs48 {escapar_rtf(linea[3:])}\\b0\\fs24\\sa200\\par\n")
        elif linea.startswith("# "): 
            partes.append(f"\\pard\\intbl\\b\\fs32 {escapar_rtf(linea[2:])}\\b0\\fs24\\sb200\\sa100\\par\n")
        elif linea.strip() == "":
            partes.append("\\pard\\intbl\\par\n")
        else: 
            partes.append(f"\\pard\\intbl {escapar_rtf(linea)}\\par\n")
    
    partes.append("\\cell")

    # --- COLUMNA DERECHA (FOTO) ---
    # \qc = Centrado en su celda.
    # \sb0 = Espacio antes de la foto (0 para que pegue arriba).
    partes.append("\\pard\\intbl\\qc\\sb0 ")
    if img_rtf:
        partes.append(img_rtf)
    partes.append("\\cell")

    partes.append("\\row\\pard\n")
    partes.append("}")
    
    with open(ruta, "wb") as archivo:
        archivo.write("\n".join(partes).encode('utf-8'))

def crear_pdf_de_texto(ruta, texto, foto_bytes=None):
    foto_jpeg = None
    foto_ancho = 0
    foto_alto = 0

    if foto_bytes:
        try:
            img = Image.open(BytesIO(foto_bytes))
            img.thumbnail((150, 150))
            img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            foto_jpeg = buffer.getvalue()
            foto_ancho, foto_alto = img.size
        except Exception: foto_jpeg = None

    paginas = []
    lineas_pagina = []
    # Subimos el texto (730 en vez de 640) para que no quede ese hueco enorme abajo
    y = 730 if foto_jpeg else 805

    def cerrar_pagina():
        nonlocal lineas_pagina, y
        if lineas_pagina: paginas.append(lineas_pagina)
        lineas_pagina = []
        y = 805

    for linea in texto.splitlines() or [""]:
        if y < 55: cerrar_pagina()
        
        if linea.startswith("## "):
            texto_linea = linea[3:]
            tamano = 24  # Título más grande
            es_header = True
            espacio = 36
        elif linea.startswith("# "):
            texto_linea = linea[2:]
            tamano = 14  # Subtítulos un poco más grandes
            es_header = True
            espacio = 24
        else:
            texto_linea = linea
            tamano = 10
            es_header = False
            espacio = 15
            
        lineas_pagina.append((texto_linea, y, es_header, tamano))
        y -= espacio

    cerrar_pagina()
    if not paginas: paginas = [[]]
    for n, lineas in enumerate(paginas, start=1): lineas.append((f"Pagina {n} de {len(paginas)}", 35, False, 10))

    objetos = [None, None]
    referencias = []
    id_fuente = 3 + 2 * len(paginas)
    id_fuente_bold = id_fuente + 1
    id_imagen = id_fuente_bold + 1 if foto_jpeg else None

    for idx, lineas in enumerate(paginas):
        contenido_str = ""
        if idx == 0 and foto_jpeg:
            ancho_pt = 120
            alto_pt = int(120 * foto_alto / foto_ancho) if foto_ancho else 120
            x = 595 - 50 - ancho_pt
            y_img = 842 - 50 - alto_pt
            contenido_str += (f"q {ancho_pt} 0 0 {alto_pt} {x} {y_img} cm /Im1 Do Q\n")

        def _fmt(linea, pos_y, es_header, tamano):
            fuente = "F2" if es_header else "F1"
            return (f"BT /{fuente} {tamano} Tf 1 0 0 1 50 {pos_y} Tm <{linea.encode('cp1252', errors='replace').hex().upper()}> Tj ET\n")

        contenido_str += "".join(_fmt(linea, pos_y, es_header, tam) for linea, pos_y, es_header, tam in lineas)
        contenido = contenido_str.encode("ascii")

        id_pagina = len(objetos) + 1
        id_contenido = id_pagina + 1
        referencias.append(f"{id_pagina} 0 R")
        if idx == 0 and foto_jpeg: recursos = (f"/Resources << /Font << /F1 {id_fuente} 0 R /F2 {id_fuente_bold} 0 R >> /XObject << /Im1 {id_imagen} 0 R >> >>")
        else: recursos = f"/Resources << /Font << /F1 {id_fuente} 0 R /F2 {id_fuente_bold} 0 R >> >>"

        objetos.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] {recursos} /Contents {id_contenido} 0 R >>".encode("ascii"))
        objetos.append(f"<< /Length {len(contenido)} >>\nstream\n".encode("ascii") + contenido + b"\nendstream")

    objetos[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objetos[1] = (f"<< /Type /Pages /Kids [{' '.join(referencias)}] /Count {len(referencias)} >>".encode("ascii"))
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    if foto_jpeg:
        objetos.append(f"<< /Type /XObject /Subtype /Image /Width {foto_ancho} /Height {foto_alto} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(foto_jpeg)} >>\n".encode("ascii") + b"stream\n" + foto_jpeg + b"\nendstream")

    salida = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for numero, objeto in enumerate(objetos, start=1):
        offsets.append(len(salida))
        salida.extend(f"{numero} 0 obj\n".encode("ascii"))
        salida.extend(objeto)
        salida.extend(b"\nendobj\n")

    pos = len(salida)
    salida.extend(f"xref\n0 {len(objetos)+1}\n".encode("ascii"))
    salida.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]: salida.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    salida.extend(f"trailer\n<< /Size {len(objetos)+1} /Root 1 0 R >>\nstartxref\n{pos}\n%%EOF\n".encode("ascii"))
    with open(ruta, "wb") as archivo: archivo.write(salida)

# BLOQUE 27: VENTANA DE DOCUMENTOS
def abrir_ventana_ver_documento(dni_paciente=None):
    ventana_doc = Toplevel(ventana)
    ventana_doc.title("Ver / Editar documento")
    ventana_doc.geometry("900x750")
    ventana_doc.config(bg=GRIS_NIEBLA)

    frame_sup = Frame(ventana_doc, bg=GRIS_NIEBLA)
    frame_sup.pack(side="top", fill="x", padx=10, pady=10)
    Label(frame_sup, text="DNI del paciente:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).pack(side="left", padx=5)
    entry_dni_doc = Entry(frame_sup, width=20, font=("Segoe UI", 12))
    entry_dni_doc.pack(side="left", padx=5)
    if dni_paciente: entry_dni_doc.insert(0, dni_paciente)

    frame_texto = Frame(ventana_doc, bg=BLANCO, relief="solid", bd=1)
    frame_texto.pack(fill="both", expand=True, padx=10, pady=5)
    scroll_doc = tk.Scrollbar(frame_texto, orient="vertical")
    scroll_doc.pack(side="right", fill="y")
    text_doc = tk.Text(frame_texto, font=("Segoe UI", 11), wrap="word", yscrollcommand=scroll_doc.set, bg=BLANCO, fg=GRIS_AZULADO)
    text_doc.pack(side="left", fill="both", expand=True)
    scroll_doc.config(command=text_doc.yview)

    def cargar_documento():
        dni = entry_dni_doc.get().strip()
        text_doc.delete("1.0", tk.END)
        if not dni:
            messagebox.showwarning("Atención", "Escribí un DNI primero.")
            return
        cursor.execute("""SELECT id, fecha_entrevista, hora_entrevista, nombre_profecional, apellido_profecional, entrevista FROM entrevistas WHERE dni_paciente = ? ORDER BY id""", (dni,))
        filas = cursor.fetchall()
        if not filas:
            text_doc.insert("1.0", "No hay entrevistas para ese DNI.")
            return
        for f in filas:
            text_doc.insert(tk.END, f"=== Entrevista {f[0]} ===\n")
            text_doc.insert(tk.END, f"Fecha: {f[1]} {f[2] or ''}\n")
            text_doc.insert(tk.END, f"Profesional: {f[3]} {f[4] or ''}\n\n")
            text_doc.insert(tk.END, f"{f[5] or ''}\n\n")

    def guardar_pdf():
        texto = text_doc.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Atención", "El documento está vacío.")
            return
        ruta = filedialog.asksaveasfilename(title="Guardar como PDF", defaultextension=".pdf", initialfile="documento.pdf", filetypes=[("PDF", "*.pdf")])
        if not ruta: return
        try:
            crear_pdf_de_texto(ruta, texto)
            messagebox.showinfo("OK", f"PDF guardado en:\n{ruta}")
        except Exception: messagebox.showerror("Error")

    def guardar_word():
        texto = text_doc.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Atención", "El documento está vacío.")
            return
        ruta = filedialog.asksaveasfilename(title="Guardar como Word", defaultextension=".rtf", initialfile="documento.rtf", filetypes=[("Word (RTF)", "*.rtf")])
        if not ruta: return
        try:
            crear_word_de_texto(ruta, texto)
            messagebox.showinfo("OK", f"Word guardado en:\n{ruta}")
        except Exception: messagebox.showerror("Error")

    def eliminar_archivo():
        ruta = filedialog.askopenfilename(title="Elegir archivo a eliminar", filetypes=[("Documentos", "*.pdf *.doc *.docx *.txt")])
        if not ruta: return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar este archivo?\n{ruta}"): return
        try:
            os.remove(ruta)
            messagebox.showinfo("OK", "Archivo eliminado.")
        except Exception: messagebox.showerror("Error")

    def importar_documento():
        ruta = filedialog.askopenfilename(title="Importar documento", filetypes=[("Documentos", "*.pdf *.doc *.docx *.txt"), ("Todos", "*.*")])
        if not ruta: return
        extension = os.path.splitext(ruta)[1].lower()
        texto = ""
        try:
            if extension == ".pdf":
                with open(ruta, "rb") as archivo:
                    #lector = PyPDF2.PdfReader(archivo)
                    #for pagina in lector.pages: texto += pagina.extract_text() + "\n"
            #elif extension in (".doc", ".docx", ".txt"):
            #    try:
                    with open(ruta, "r", encoding="utf-8") as archivo: contenido = archivo.read()
                    if "<p>" in contenido: contenido = re.sub(r"<[^>]+>", "", contenido)
                    texto = contenido
              #  except UnicodeDecodeError:
             #        messagebox.showerror("Error", "No se pudo leer el archivo (codificación no soportada).")
                    return
            else:
                messagebox.showwarning("Formato", "Formato no soportado. Usá PDF, DOC, DOCX o TXT.")
                return
        except Exception:
            messagebox.showerror("Error al importar")
            return
        text_doc.delete("1.0", tk.END)
        text_doc.insert("1.0", texto.strip() or "(El documento no tiene texto extraíble.)")
        messagebox.showinfo("Importado", f"Documento cargado:\n{ruta}")

    frame_btn = Frame(ventana_doc, bg=GRIS_NIEBLA)
    frame_btn.pack(anchor="center")
    #RoundedButton(frame_btn, 130, 40, 20, VERDE_AZULADO, BLANCO, text="⟳", command=cargar_documento).pack(side="left", padx=5)
    #RoundedButton(frame_btn, 150, 40, 20, VERDE_AZULADO, BLANCO, text="Guardar PDF", command=guardar_pdf).pack(side="left", padx=5)
    #RoundedButton(frame_btn, 150, 40, 20, VERDE_AZULADO, BLANCO, text="Guardar Word", command=guardar_word).pack(side="left", padx=5)
    #RoundedButton(frame_btn, 180, 40, 20, VERDE_AZULADO, BLANCO, text="Eliminar archivo", command=eliminar_archivo).pack(side="left", padx=5)
    #RoundedButton(frame_btn, 170, 40, 20, VERDE_AZULADO, BLANCO, text="Importar PDF/Word", command=importar_documento).pack(side="left", padx=5)
    if dni_paciente: cargar_documento()
    agregar_boton_luna(ventana_doc)

# BLOQUE 28: INICIO
def al_cerrar_app():
    try: conexion.close()
    except Exception: pass
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", al_cerrar_app)
ventana.mainloop()
import tkinter as tk


def al_hacer_clic():
  etiqueta.config(text="¡Botón presionado!")


# 1. Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi primera ventana")
ventana.geometry("300x150")

# 2. Crear una etiqueta de texto
etiqueta = tk.Label(ventana, text="Presiona el botón de abajo")
etiqueta.pack(pady=10)

# 3. Crear el botón y vincularlo a la función
boton = tk.Button(ventana, text="Haz clic aquí", command=al_hacer_clic)
boton.pack(pady=10)

# 4. Mantener la ventana abierta
ventana.mainloop()
print(f"{mi_variable=}, tipo={type(mi_variable)}")

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.debug("Mensaje de depuración")
logging.info("Aplicación iniciada")
logging.warning("Espacio en disco bajo")
logging.error("Error al conectar con la base de datos")
logging.critical("Fallo crítico del sistema")
