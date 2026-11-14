# ============================================================================
# BLOQUE 1: IMPORTACIONES
# Acá traigo todo lo que necesito para que la app funcione. Son las
# herramientas que uso después en el resto del código.
# ============================================================================

import sqlite3
# Importo el módulo sqlite3, que me permite trabajar con bases de datos
# SQLite (motor liviano que se guarda en un único archivo .db, sin
# servidor). Con esto puedo crear tablas, insertar filas, consultar,
# actualizar y borrar datos.

import tkinter as tk
# Importo tkinter (la librería de interfaz gráfica incluida con Python)
# y la renombro como "tk" para escribir menos. Con tkinter hago
# ventanas, botones, listas, entradas, etc.

from tkinter import filedialog, messagebox, Label, Button, Entry, Frame, Toplevel, Listbox
# Del paquete tkinter traigo clases y módulos específicos:
# - filedialog: diálogos "abrir archivo" / "guardar archivo".
# - messagebox: cartelitos de aviso, error, confirmación.
# - Label: etiqueta de texto (no editable).
# - Entry: caja de texto de una línea.
# - Frame: contenedor rectangular.
# - Toplevel: ventana secundaria.
# - Listbox: lista con elementos seleccionables.

from io import BytesIO
# Importo BytesIO del módulo io. BytesIO permite tratar bytes en memoria
# como si fueran un archivo (con .read(), .write(), etc.). Lo uso para
# que Pillow pueda leer imágenes guardadas como BLOB en la base sin
# tener que escribirlas a disco.

from PIL import Image, ImageTk, ImageOps
# De la librería Pillow (PIL) importo:
# - Image: abrir, redimensionar y manipular imágenes.
# - ImageTk: convertir imágenes PIL a PhotoImage (formato Tkinter).
# - ImageOps: utilidades como "fit" (ajustar manteniendo aspecto).

import string
# Módulo de la stdlib con constantes de strings. Uso
# string.punctuation (todos los signos de puntuación) para normalizar
# fechas.

import os
# Módulo para rutas y archivos del sistema operativo: crear carpetas
# con makedirs, unir rutas con path.join, obtener nombre de archivo con
# path.basename, borrar con os.remove, etc.

import textwrap
# Módulo para cortar texto en líneas de ancho fijo. Lo uso al armar el
# PDF para que las anotaciones largas no se salgan del ancho de página.

import re
# Módulo de expresiones regulares. Lo uso para detectar fechas y horas
# embebidas en texto (por ejemplo "03/11/2026 14:30").

import base64
# Módulo para codificar y decodificar base64. base64 es una forma de
# representar bytes arbitrarios como texto imprimible. Lo uso para las
# imágenes embebidas en el código.

import PyPDF2
# Librería externa para leer y extraer texto de archivos PDF. La uso en
# la ventana de documentos cuando el usuario importa un PDF.

import shutil
# Módulo de operaciones de archivos de alto nivel. Lo uso para mover
# archivos (shutil.move) a una carpeta por DNI.

# ============================================================================
# BLOQUE 2: IMÁGENES EN BASE64
# ============================================================================

# ----------------------------------------------------------------------------
# NOTA: Acá estaban los strings gigantes SANCA_BASE64 y CASA_JOVENES_64
# (imágenes codificadas en base64). Los omito para que el archivo sea
# legible. Si querés usarlos, pegá el string correspondiente acá.
# ----------------------------------------------------------------------------

SANCA_BASE64 = ""
# String base64 con la imagen de SANCA (mascota de la app). Lo dejo
# vacío acá para no ensuciar el archivo con 200 KB de texto.

CASA_JOVENES_64 = ""
# String base64 con la imagen del banner (Casa de Jóvenes). Idem, lo
# dejo vacío.

entry_dni_perfil_ref = None
# Variable global que va a apuntar al tk.Entry del DNI dentro de la
# ventana de perfil. Arranca en None porque todavía no se abrió. El
# editor de fotos y otras funciones usan esta referencia para saber a
# qué paciente asociar las imágenes.

# ============================================================================
# BLOQUE 3: BOTONES REDONDOS
# ============================================================================

class RoundedButton(tk.Canvas):
    # Defino una clase propia que hereda de tk.Canvas. No uso tk.Button
    # porque Canvas me deja dibujar formas libres (arcos y rectángulos)
    # para simular esquinas redondeadas.

    def __init__(self, parent, width, height, radius, bg_color, fg_color,
                 text="", command=None, hover_color="#3FBFB3"):
        # Constructor. Parámetros:
        # - parent: widget padre.
        # - width, height: tamaño en píxeles.
        # - radius: radio de las esquinas.
        # - bg_color: color normal.
        # - fg_color: color del texto.
        # - text: texto del botón.
        # - command: función al hacer clic.
        # - hover_color: color cuando el mouse está encima.

        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0, bd=0)
        # Llamo al __init__ de Canvas:
        # - bg=parent["bg"]: fondo del canvas igual al del padre (así
        #   el botón "flota" sobre él).
        # - highlightthickness=0: saco el borde de foco.
        # - bd=0: sin borde 3D.

        self.width = width
        # Guardo el ancho como atributo.

        self.height = height
        # Guardo el alto.

        self.radius = radius
        # Guardo el radio de esquinas.

        self.bg_color = bg_color
        # Guardo el color normal.

        self.fg_color = fg_color
        # Guardo el color del texto.

        self.hover_color = hover_color
        # Guardo el color de hover.

        self.text = text
        # Guardo el texto.

        self.command = command
        # Guardo la función a ejecutar al hacer clic.

        self.hover = False
        # Bandera: ¿el mouse está encima? Arranca en False.

        self._dibujar()
        # Llamo al método que dibuja el botón por primera vez.

        self.bind("<ButtonRelease-1>", self._click)
        # Asocio el evento "soltar botón izquierdo" al método _click.

        self.bind("<Enter>", self._enter)
        # Asocio "el mouse entra" al método _enter.

        self.bind("<Leave>", self._leave)
        # Asocio "el mouse sale" al método _leave.

    def _dibujar(self):
        # Método interno que dibuja el botón entero.
        self.delete("all")
        # Primero borro todo lo que haya dibujado antes (para
        # redibujar limpio cuando cambia el color).

        w, h, r = self.width, self.height, self.radius
        # Desempaqueto en variables cortas.

        color = self.hover_color if self.hover else self.bg_color
        # Si el mouse está encima uso hover_color, si no bg_color.

        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90,
                        fill=color, outline=color)
        # Esquina superior izquierda: dibujo un arco que ocupa desde
        # (0,0) hasta (2r, 2r), empezando en 90° con extensión de 90°.

        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90,
                        fill=color, outline=color)
        # Esquina superior derecha: arco desde 0° hasta 90°.

        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90,
                        fill=color, outline=color)
        # Esquina inferior derecha: arco desde 270° hasta 360°.

        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90,
                        fill=color, outline=color)
        # Esquina inferior izquierda: arco desde 180° hasta 270°.

        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)
        # Rectángulo horizontal central (rellena el medio entre las
        # esquinas de arriba y abajo).

        self.create_rectangle(0, r, w, h-r, fill=color, outline=color)
        # Rectángulo vertical central (rellena el medio entre las
        # esquinas izquierda y derecha).

        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color,
                         font=("Segoe UI", 12, "bold"))
        # Dibujo el texto centrado (w/2, h/2 son las coordenadas del
        # centro), con fuente Segoe UI 12 en negrita.

    def _click(self, event):
        # Se ejecuta cuando el usuario suelta el botón izquierdo.
        if self.command:
            # Si hay una función asociada...
            self.command()
            # ...la llamo.

    def _enter(self, event):
        # Se ejecuta cuando el mouse entra al área del botón.
        self.hover = True
        # Marco hover=True.

        self.config(cursor="hand2")
        # Cambio el cursor a la "manito".

        self._dibujar()
        # Redibujo con color de hover.

    def _leave(self, event):
        # Se ejecuta cuando el mouse sale.
        self.hover = False
        # Marco hover=False.

        self._dibujar()
        # Redibujo con color normal.

    def set_colors(self, bg, hover, fg=None, parent_bg=None):
        # Cambio colores sin recrear el botón.
        self.bg_color = bg
        # Nuevo color normal.

        self.hover_color = hover
        # Nuevo color de hover.

        if fg is not None:
            # Si me pasan color de texto...
            self.fg_color = fg
            # Lo actualizo.

        if parent_bg is not None:
            # Si me pasan fondo del padre...
            self.config(bg=parent_bg)
            # Lo aplico al Canvas.

        self._dibujar()
        # Redibujo.

# ============================================================================
# BLOQUE 4: BASE DE DATOS
# ============================================================================

conexion = sqlite3.connect("PROYECTO_FINAL_45.db")
# Abro (o creo si no existe) el archivo SQLite "PROYECTO_FINAL_45.db".
# Devuelve un objeto Connection.

cursor = conexion.cursor()
# Creo un cursor a partir de la conexión. Con el cursor ejecuto
# queries y recorro resultados.

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
    estado TEXT,
    consentimiento TEXT,
    foto BLOB)""")
# Creo la tabla "personas" si no existe. Columnas:
# - id: PK autoincremental (1, 2, 3...).
# - nombre, apellido: obligatorios (NOT NULL).
# - dni: entero único y obligatorio.
# - edad: entero opcional.
# - fecha_nacimiento, fecha_ingreso: texto (fecha en formato string).
# - telefono, direccion, contacto_emergencia, telefono_emergencia,
#   obra_social, estado, consentimiento: texto opcional.
# - foto: BLOB (bytes de la imagen).

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
# Creo la tabla "entrevistas" con las columnas del profesional, la
# anotación en sí, el DNI del paciente, fecha, hora, tipo y próxima
# sesión. "profecional" está mal escrito pero lo dejo así para no
# romper el resto del código.

cursor.execute("""CREATE TABLE IF NOT EXISTS pdf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    formato TEXT NOT NULL,
    contenido BLOB NOT NULL,
    dni_personas INTEGER)""")
# Tabla "pdf" para documentos y fotos del editor:
# - nombre: nombre del archivo.
# - formato: extensión (jpg, png, pdf...).
# - contenido: bytes del archivo.
# - dni_personas: paciente al que pertenece.

cursor.execute("""CREATE TABLE IF NOT EXISTS recursos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    contenido BLOB)""")
# Tabla "recursos" para guardar cosas fijas (por ejemplo la imagen
# SANCA). "nombre" es UNIQUE para no duplicar.

cursor.execute("PRAGMA table_info(personas)")
# Devuelve información de las columnas de la tabla personas.

_columnas_personas = {fila[1] for fila in cursor.fetchall()}
# Armo un set con los nombres de las columnas (fila[1] es el nombre).
# Uso set por eficiencia al consultar "¿existe esta columna?".

for _col, _tipo in (("fecha_egreso", "TEXT"),
                    ("tipo_egreso", "TEXT"),
                    ("motivo_egreso", "TEXT")):
    # Recorro las tres columnas nuevas que quiero agregar si no están.
    if _col not in _columnas_personas:
        # Si la columna no existe...
        cursor.execute(f"ALTER TABLE personas ADD COLUMN {_col} {_tipo}")
        # ...la agrego con ALTER TABLE.

conexion.commit()
# Confirmo los cambios (sin esto, no se escriben en el archivo).

# ============================================================================
# BLOQUE 5: PALETA DE COLORES
# ============================================================================

ROJO = "#E3000F"
# Rojo fuerte (botón de cerrar autores).

AMARILLO = "#FCAF17"
# Amarillo (contador de legajos).

NEGRO = "#0a0a0a"
# Casi negro (tema oscuro).

GRIS = "#222222"
# Gris oscuro (paneles en oscuro).

AZUL_PETROLEO = "#006080"
# Azul petróleo (fondos de algunos frames).

BLANCO_HUESO = "#F5F5DC"
# Blanco hueso (texto sobre azul petróleo).

VERDE_TERMINAL = "#00FF00"
# Verde brillante (hover de botones).

GRIS_NIEBLA = "#F4F7F6"
# Gris claro (fondo principal tema claro).

BLANCO = "#FFFFFF"
# Blanco puro.

GRIS_AZULADO = "#2C3E50"
# Gris azulado oscuro (texto principal, fondo de listas).

GRIS_MEDIO = "#7F8C8D"
# Gris medio (texto secundario).

AZUL_SERENO = "#4A90E2"
# Azul sereno (selección en listas).

VERDE_AZULADO = "#26A69A"
# Verde azulado (botones, acentos).

# ============================================================================
# BLOQUE 6: VENTANA PRINCIPAL
# ============================================================================

ventana = tk.Tk()
# Creo la ventana principal (root). Es la ventana madre.

ventana.title("Casa de Jovenes Levantate y Camina. Parroquia San Juan Bautista. Obispado de San Isidro")
# Le pongo el título.

ventana.config(bg=GRIS_NIEBLA)
# Fondo gris niebla.

ancho_pantalla = ventana.winfo_screenwidth()
# Ancho de la pantalla del usuario en píxeles.

alto_pantalla = ventana.winfo_screenheight()
# Alto de la pantalla.

ancho_ventana = min(1000, int(ancho_pantalla * 0.92))
# Ancho de mi ventana: 1000 o 92% del ancho de pantalla (el menor).

alto_ventana = min(750, int(alto_pantalla * 0.88))
# Lo mismo con el alto: 750 o 88% del alto.

_x = (ancho_pantalla - ancho_ventana) // 2
# Coordenada X para centrar horizontalmente.

_y = (alto_pantalla - alto_ventana) // 2
# Coordenada Y para centrar verticalmente.

ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{_x}+{_y}")
# Aplico tamaño y posición. Formato "ANCHOxALTO+X+Y".

ventana.minsize(900, 550)
# Tamaño mínimo 900x550.

# ============================================================================
# BLOQUE 7: BANNER
# ============================================================================

banner = tk.Frame(ventana, bg=GRIS_NIEBLA, height=150)
# Frame de 150 píxeles de alto para el banner.

banner.pack(side="top", fill="x")
# Arriba, estirado horizontalmente.

banner.pack_propagate(False)
# Evito que el Frame se achique al tamaño del contenido.

banner_label = tk.Label(banner, bg=GRIS_NIEBLA, fg=GRIS_MEDIO)
# Label vacío al principio.

banner_label.pack(expand=True, fill="both")
# Se estira para ocupar el banner.

try:
    # Intento cargar la imagen del banner.
    imagen_bytes_casa_jovenes = base64.b64decode(CASA_JOVENES_64)
    # Decodifico el string base64 a bytes.

    imagen_casa_jovenes = Image.open(BytesIO(imagen_bytes_casa_jovenes))
    # Abro la imagen desde los bytes.

    imagen_casa_jovenes = ImageOps.fit(
        imagen_casa_jovenes,
        (ancho_pantalla, 150),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5)
    )
    # Ajusto la imagen al tamaño (ancho_pantalla x 150) manteniendo
    # aspecto. LANCZOS es resampling de alta calidad. centering (0.5,0.5)
    # = centro.

    foto_banner = ImageTk.PhotoImage(imagen_casa_jovenes)
    # Convierto a PhotoImage (formato Tkinter).

    banner_label.configure(image=foto_banner)
    # Le paso la foto al Label.

    banner_label.imagen_casa_jovenes = foto_banner
    # Guardo referencia para que el GC no la borre.

except Exception:
    # Si falla algo (base64 mal, imagen corrupta), no rompo la app.
    print('Error')

# ============================================================================
# BLOQUE 8: FUNCIONES PRINCIPALES
# ============================================================================

def refrescar_lista():
    # Refresco la lista de personas y el contador.
    lista_personas.delete(0, tk.END)
    # Borro todos los elementos de la Listbox.

    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")
    # Traigo nombre, apellido, dni ordenados por apellido y luego nombre.

    for nombre, apellido, dni in cursor.fetchall():
        # Recorro cada fila del resultado.
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")
        # Inserto al final de la lista.

    cursor.execute("SELECT COUNT(*) FROM personas WHERE LOWER(COALESCE(estado, 'activo')) = 'activo'")
    # Cuento cuántas personas tienen estado activo (o NULL, que cuenta
    # como activo).

    activos = cursor.fetchone()[0]
    # fetchone trae una sola fila (una tupla de un elemento). [0] saca
    # el número.

    contador_legajos.config(text=f"Legajos activos: {activos}")
    # Actualizo el label del contador.

def mostrar_foto(dni):
    # Muestro la foto del paciente en el visor principal.
    cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
    # Consulto la foto por DNI. "?" es placeholder parametrizado.

    fila = cursor.fetchone()
    # Una sola fila.

    if fila and fila[0]:
        # Si hay fila y la foto no es NULL...
        try:
            img = Image.open(BytesIO(fila[0]))
            # Abro la imagen desde bytes.

            img.thumbnail((300, 300))
            # Redimensiono manteniendo aspecto, máx 300x300.

            fondo = Image.new("RGB", (300, 300), BLANCO)
            # Creo lienzo blanco de 300x300.

            x = (300 - img.width) // 2
            y = (300 - img.height) // 2
            # Calculo posición para centrar.

            fondo.paste(img, (x, y))
            # Pego la imagen centrada.

            foto = ImageTk.PhotoImage(fondo)
            # Convierto a PhotoImage.

            visor_foto.configure(image=foto, text="")
            # Le aplico al visor y limpio el texto.

            visor_foto.image = foto
            # Referencia para que no la borre el GC.

            return
            # Salgo exitosamente.

        except Exception:
            # Si falla la carga, caigo al placeholder.
            pass

    visor_foto.configure(image="", text="👤\nSin foto")
    visor_foto.image = None

    # Muestro placeholder.

def al_seleccionar(event=None):
    # Se ejecuta al hacer clic en la lista o al cambiar selección.
    boton_busqueda_definitivo.grid_remove()
    boton_agregar_definitivo.grid_remove()
    # Oculto los botones "Confirmar" por si quedaron visibles.

    grids_nom_ape()
    grids_dni()
    # Muestro los campos.

    sel = lista_personas.curselection()
    # Índices de los elementos seleccionados.

    if not sel:
        # Sin selección...
        return

    texto = lista_personas.get(sel[0])
    # Texto del primer elemento seleccionado.

    dni = int(texto.split("DNI ")[1])
    # Extraigo el DNI del texto.

    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni,))
    # Consulto los datos.

    fila = cursor.fetchone()
    if not fila:
        return
    # Si no hay resultado, salgo.

    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, fila[0])
    # Cargo nombre.

    entry_apellido.delete(0, tk.END)
    entry_apellido.insert(0, fila[1])
    # Cargo apellido.

    entry_dni.delete(0, tk.END)
    entry_dni.insert(0, fila[2])
    # Cargo DNI.

    mostrar_foto(dni)
    # Muestro la foto.

def agregar():
    # Preparo el formulario para dar de alta.
    boton_busqueda_definitivo.grid_remove()
    # Oculto el botón de búsqueda.

    grids_nom_ape()
    grids_dni()
    # Muestro los campos.

    boton_agregar_definitivo.grid()
    # Muestro "Confirmar agregar".

def agregar_definitivo():
    # Guardo una persona nueva.
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni_txt = entry_dni.get().strip()
    # Leo y limpio los campos.

    if not (nombre and apellido and dni_txt):
        # Si falta alguno...
        messagebox.showwarning("Faltan datos", "Completa nombre, apellido y DNI.")
        return

    try:
        dni = int(dni_txt)
        # Convierto a entero.
    except ValueError:
        messagebox.showerror("DNI invalido", "El DNI debe ser numerico.")
        return

    ruta = filedialog.askopenfilename(
        title="Foto (opcional)",
        filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])
    # Abro diálogo de archivos.

    contenido = None
    # Al principio sin foto.

    if ruta:
        # Si eligió archivo...
        with open(ruta, "rb") as f:
            # Lo abro en binario.
            contenido = sqlite3.Binary(f.read())
            # Leo bytes y los envuelvo como sqlite3.Binary.

    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)",
                       (nombre, apellido, dni, contenido))
        conexion.commit()
        # Inserto la fila.

    except sqlite3.IntegrityError:
        # Este error salta por DNI duplicado (UNIQUE).
        messagebox.showerror("Error",
                             "Ya existe una persona con ese DNI.\nVerifica el numero ingresado.")
        return

    except Exception:
        messagebox.showerror("Error inesperado", 'No se pudo guardar')
        return

    refrescar_lista()
    # Refresco.

    limpiar()
    # Limpio.

    boton_agregar_definitivo.grid_remove()
    # Oculto el botón.

    messagebox.showinfo("OK", "Persona agregada.")

def eliminar():
    # Elimino la persona seleccionada y sus datos asociados.
    seleccion = lista_personas.curselection()
    if not seleccion:
        messagebox.showwarning("Atencion",
                                "Selecciona una persona de la lista para eliminar.")
        return

    texto = lista_personas.get(seleccion[0])
    dni = int(texto.split("DNI ")[1])
    # Extraigo el DNI.

    if not messagebox.askyesno("Confirmar eliminación",
                                f"¿Estas seguro de que deseas eliminar a esta persona?\n\n{texto}"):
        return
        # askyesno devuelve True/False.

    boton_busqueda_definitivo.grid_remove()
    boton_agregar_definitivo.grid_remove()
    grids_remove_nom_ape()
    grids_remove_dni()
    # Oculto botones y campos.

    cursor.execute("DELETE FROM entrevistas WHERE dni_paciente = ?", (dni,))
    # Borro primero las entrevistas.

    cursor.execute("DELETE FROM pdf WHERE dni_personas = ?", (dni,))
    # Borro los PDFs/fotos.

    cursor.execute("DELETE FROM personas WHERE dni = ?", (dni,))
    # Borro la persona.

    conexion.commit()
    # Confirmo.

    refrescar_lista()
    # Refresco.

    visor_foto.configure(image="", text="👤\nSin foto")
    visor_foto.image = None
    # Reseteo el visor.

    messagebox.showinfo("OK", "Persona eliminada correctamente.")

def buscar():
    # Preparo el formulario para buscar por DNI.
    boton_agregar_definitivo.grid_remove()
    # Oculto botón de agregar.

    grids_remove_nom_ape()
    # Oculto nombre y apellido.

    grids_dni()
    # Muestro DNI.

    boton_busqueda_definitivo.grid()
    # Muestro "Confirmar búsqueda".

def buscar_definitivo():
    # Busco una persona por DNI.
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atencion",
                                "Escribi de forma numerica un DNI para buscar.")
        return

    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni_txt,))
    fila = cursor.fetchone()

    if not fila:
        messagebox.showinfo("Sin resultados", "No existe esa persona.")
        return

    grids_nom_ape()
    # Muestro los campos.

    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END)
    entry_apellido.insert(0, fila[1])
    # Cargo nombre y apellido.

    mostrar_foto(fila[2])
    # Muestro la foto.

    for i in range(lista_personas.size()):
        # Recorro la lista.
        if f"DNI {fila[2]}" in lista_personas.get(i):
            # Si el texto de la fila i contiene el DNI...
            lista_personas.selection_clear(0, tk.END)
            # Deselecciono todo.
            lista_personas.selection_set(i)
            # Selecciono la fila i.
            lista_personas.see(i)
            # Hago scroll para que se vea.
            break
            # Corto el bucle.

def limpiar():
    # Limpio los campos del formulario y la foto.
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    visor_foto.configure(image="", text="👤\nSin foto")
    visor_foto.image = None

# ============================================================================
# BLOQUE 9: FRAME DE BOTONES
# ============================================================================

frame_btn = Frame(ventana, bg=GRIS_NIEBLA, height=55)
# Frame para los botones principales.

frame_btn_info = Frame(ventana, bg=GRIS_NIEBLA)
# Frame para el botón Info.

frame_btn_info.pack(side="bottom", fill="x", padx=10, pady=15)
# Lo empaqueto abajo.

frame_btn.pack(side="top", fill="x", padx=15, pady=10)
# Arriba.

frame_btn.pack_propagate(False)
# Respeto el alto.

btn_tema = RoundedButton(frame_btn, 50, 40, 20, NEGRO, BLANCO, text="☾",command= lambda: aplicar_tema())
# Botón de tema. Uso lambda para no ejecutar al crear.

btn_tema.pack(side="right", padx=5, pady=7)
# Lo pongo a la derecha.

sub_btn = Frame(frame_btn, bg=GRIS_NIEBLA)
sub_btn.pack(side="left", fill="both", expand=True)
# Sub-frame para los 4 botones.

sub_btn.columnconfigure(0, weight=1)
sub_btn.columnconfigure(5, weight=1)
# Columnas fantasma para centrar.

btn_agregar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO,
                             text="Agregar", command=agregar, hover_color=VERDE_TERMINAL)
# Botón Agregar.

btn_agregar.grid(row=0, column=1, padx=5, pady=7)
# Lo ubico en columna 1.

btn_eliminar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO,
                              text="Eliminar", command=eliminar,
                              hover_color=VERDE_TERMINAL)
# Botón Eliminar con hover verde.

btn_eliminar.grid(row=0, column=2, padx=5, pady=7)

btn_buscar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO,
                            text="Buscar", command=buscar,
                            hover_color=VERDE_TERMINAL)
# Botón Buscar.

btn_buscar.grid(row=0, column=3, padx=5, pady=7)

btn_limpiar = RoundedButton(sub_btn, 200, 40, 20, VERDE_AZULADO, BLANCO,
                             text="Limpiar", command=limpiar,
                             hover_color=VERDE_TERMINAL)
# Botón Limpiar.

btn_limpiar.grid(row=0, column=4, padx=5, pady=7)

# ============================================================================
# BLOQUE 10: FORMULARIO
# ============================================================================

frame_form = Frame(ventana, bg=GRIS_NIEBLA)
# Frame para el formulario.

frame_form.pack(side="top", fill="x", padx=15, pady=10)
# Arriba, estirado.

label_nombre = Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA,
                     fg=GRIS_AZULADO, font=("Segoe UI", 12))
# Label Nombre.

label_nombre.grid(row=0, column=2, sticky="e", padx=5)
# En columna 2, alineado a la derecha.

entry_nombre = Entry(frame_form, width=22, font=("Segoe UI", 12))
# Entry Nombre.

entry_nombre.grid(row=0, column=3, padx=5, pady=3)
# Columna 3.

label_apellido = Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA,
                        fg=GRIS_AZULADO, font=("Segoe UI", 12))
# Label Apellido.

label_apellido.grid(row=0, column=4, sticky="e", padx=5)
# Columna 4.

entry_apellido = tk.Entry(frame_form, width=22, font=("Segoe UI", 12))
# Entry Apellido.

entry_apellido.grid(row=0, column=5, padx=5, pady=3)
# Columna 5.

label_dni = Label(frame_form, text="DNI:", bg=GRIS_NIEBLA,
                   fg=GRIS_AZULADO, font=("Segoe UI", 12))
# Label DNI.

label_dni.grid(row=0, column=6, sticky="e", padx=5)
# Columna 6.

entry_dni = Entry(frame_form, width=15, font=("Segoe UI", 12))
# Entry DNI.

entry_dni.grid(row=0, column=7, padx=5, pady=3)
# Columna 7.

def grids_nom_ape():
    # Muestro los campos de nombre y apellido.
    label_nombre.grid()
    entry_nombre.grid()
    label_apellido.grid()
    entry_apellido.grid()

def grids_dni():
    # Muestro el campo DNI.
    label_dni.grid()
    entry_dni.grid()

def grids_remove_nom_ape():
    # Oculto nombre y apellido.
    label_nombre.grid_remove()
    entry_nombre.grid_remove()
    label_apellido.grid_remove()
    entry_apellido.grid_remove()

def grids_remove_dni():
    # Oculto DNI.
    label_dni.grid_remove()
    entry_dni.grid_remove()

grids_remove_nom_ape()
# Arranco con nombre/apellido ocultos.

grids_remove_dni()
# Arranco con DNI oculto.

# ============================================================================
# BLOQUE 11: CUERPO
# ============================================================================

cuerpo = Frame(ventana, bg=GRIS_NIEBLA)
# Frame grande que contiene foto y lista.

cuerpo.pack(fill="both", expand=True, padx=40, pady=10)
# Ocupa todo el espacio libre.

cuerpo.columnconfigure(0, weight=0)
# Columna 0 (foto): no se estira.

cuerpo.columnconfigure(1, weight=1)
# Columna 1 (lista): se estira.

cuerpo.rowconfigure(0, weight=1)
# Fila 0: se estira verticalmente.

frame_izquierda = Frame(cuerpo, bg=GRIS_NIEBLA)
# Frame para la foto.

frame_izquierda.grid(row=0, column=0, sticky="n",
                     padx=(20, 40), pady=(45, 0))
# Ubicado en (0,0), pegado arriba. Márgenes 20/40 y 45/0.

frame_foto = Frame(frame_izquierda, bg=BLANCO, relief="solid", bd=1,
                    width=250, height=250)
# Caja blanca 250x250 para la foto.

frame_foto.pack()
# La empaqueto.

frame_foto.pack_propagate(False)
# Evito que se achique al contenido.

visor_foto = Label(frame_foto, text="👤\nSin foto", bg=BLANCO,
                    fg=GRIS_MEDIO, font=("Segoe UI", 18))
# Label con placeholder.

visor_foto.pack(expand=True, fill="both")
# Centrado y estirado.

frame_lista = Frame(cuerpo, bg=GRIS_AZULADO, relief="solid", bd=1)
# Frame para la lista.

frame_lista.grid(row=0, column=1, sticky="nsew", pady=10)
# En (0,1), estirado a los 4 lados.

titulo_lista = tk.Label(frame_lista, text="Personas registradas",
                         bg=GRIS_AZULADO, fg=BLANCO,
                         font=("Segoe UI", 15, "bold"))
# Título.

titulo_lista.pack(anchor="w", padx=10, pady=(10, 5))
# Alineado a la izquierda.

contador_legajos = tk.Label(frame_lista, text="Legajos activos: 0",
                             bg=GRIS_AZULADO, fg=AMARILLO,
                             font=("Segoe UI", 11, "bold"))
# Contador.

contador_legajos.pack(anchor="w", padx=10, pady=(0, 10))
# Alineado a la izquierda.

caja_lista = Frame(frame_lista, bg=BLANCO)
# Caja blanca interna para la lista.

caja_lista.pack(fill="both", expand=True, padx=10, pady=(0, 10))
# Estirada.

scroll = tk.Scrollbar(caja_lista, orient="vertical")
# Barra de scroll vertical.

scroll.pack(side="right", fill="y")
# A la derecha de la caja.

lista_personas = Listbox(caja_lista, yscrollcommand=scroll.set,
                          font=("Segoe UI", 12), bg=BLANCO,
                          fg=GRIS_AZULADO, selectbackground=AZUL_SERENO,
                          selectforeground=BLANCO)
# La lista.

lista_personas.pack(side="left", fill="both", expand=True)
# A la izquierda, estirada.

scroll.config(command=lista_personas.yview)
# Conecto scroll con lista.

# ============================================================================
# BLOQUE 12: BOTONES DEFINITIVOS
# ============================================================================

boton_agregar_definitivo = RoundedButton(
    frame_form, 350, 40, 20, VERDE_AZULADO, BLANCO,
    text="Confirmar agregar", command=agregar_definitivo)
# Botón Confirmar agregar.

boton_agregar_definitivo.grid(row=1, column=0, columnspan=8,sticky="ew", padx=5, pady=(5, 0))
# Ocupa las 8 columnas, estirado.

boton_agregar_definitivo.grid_remove()
# Oculto por defecto.

boton_busqueda_definitivo = RoundedButton(frame_form, 350, 40, 20, VERDE_AZULADO, BLANCO,text="Confirmar busqueda", command=buscar_definitivo)
# Botón Confirmar búsqueda.

boton_busqueda_definitivo.grid(row=1, column=0, columnspan=8,sticky="ew", padx=5, pady=(5, 0))
# Ocupa las 8 columnas.

boton_busqueda_definitivo.grid_remove()
# Oculto por defecto.

# ============================================================================
# BLOQUE 13: MODO OSCURO
# ============================================================================

tema_oscuro = False
# Flag: ¿está activo el modo oscuro? Arranca en False.

ventanas_secundarias = []
# Lista de Toplevel abiertas, para aplicables el tema.

_ventana_entrevistas_abierta = None
# Referencia a la ventana de entrevistas para no abrir dos.

def actualizar_widget(widget, fondo, panel, texto, acento):
    # Aplica el tema recursivamente a un widget y todos sus hijos.
    # fondo: color de la ventana.
    # panel: color de cajas (entries, listas, menús).
    # texto: color del texto.
    # acento: color de botones y resaltados.

    if isinstance(widget, RoundedButton):
        # Si es un botón redondo propio...
        if widget == btn_tema:
            # El botón ☾/☀️ es especial: sus colores se INVIERTEN con el tema.
            # En claro: fondo negro, texto blanco. En oscuro: fondo blanco, texto negro.
            # Por eso acá `panel` va de fondo y `texto` de foreground:
            # el "panel" del tema (blanco/gris) queda como fondo del botón,
            # y el "texto" del tema queda como color de la luna.
            # `acento` es el hover (gris en oscuro, verde-azulado en claro).
            widget.set_colors(panel, acento, texto, fondo)
        else:
            # Cualquier otro RoundedButton (Agregar, Eliminar, Buscar, etc.):
            # - fondo del botón: `acento` (verde-azulado en claro, gris en oscuro)
            # - hover: VERDE_TERMINAL (verde brillante) siempre
            # - texto: BLANCO siempre
            # - fondo del canvas: `fondo` (para que combine con la ventana)
            widget.set_colors(acento, VERDE_TERMINAL, BLANCO, fondo)

        # Un Canvas puede tener hijos widgets embebidos (create_window).
        # Recorro esos hijos también para que hereden el tema.
        for hijo in widget.winfo_children():
            actualizar_widget(hijo, fondo, panel, texto, acento)
        return  # Ya terminé con este botón, no sigo con los `elif` de abajo.
                # Sin este return, un RoundedButton también caería en
                # `elif clase == "Canvas"` y se le pisaría el bg.

    if isinstance(widget, tk.OptionMenu):# Si es un OptionMenu...
        widget.config(bg=panel,fg=texto,activebackground=panel,activeforeground=BLANCO,highlightthickness=0,bd=0,)
        # Configuro la parte visible (Menubutton).

        widget["menu"].config(bg=panel,fg=texto,activebackground=acento,activeforeground=BLANCO,bd=0,)
        # Configuro el menú desplegable interno.
        return
        # Salgo.

    clase = widget.winfo_class()
    # Obtengo la clase del widget.

    if clase in ("Frame", "Labelframe", "Canvas"):
        widget.config(bg=fondo)
        # Frames: solo cambio fondo.

    elif clase == "Label":
        widget.config(bg=fondo, fg=texto)
        # Labels: fondo y texto.

    elif clase in ("Entry", "Text"):
        widget.config(bg=panel, fg=texto, insertbackground=texto)
        # Entradas: fondo panel, texto del tema, cursor del color del texto.

    elif clase == "Listbox":
        widget.config(
            bg=panel,
            fg=texto,
            selectbackground=AZUL_SERENO,
            selectforeground=BLANCO,
        )
        # Listas.

    elif clase in ("Button", "Menubutton"):
        widget.config(
            bg=acento,
            fg=BLANCO,
            activebackground=acento,
            activeforeground=BLANCO,
        )
        # Botones nativos.

    for hijo in widget.winfo_children():
        actualizar_widget(hijo, fondo, panel, texto, acento)
    # Recursión a los hijos.

def actualizar_ventanas_secundarias():
    # Aplico el tema a todas las Toplevel abiertas.
    if tema_oscuro:
        # Paleta oscura.
        fondo = NEGRO
        panel = GRIS_AZULADO
        texto = BLANCO
        acento = GRIS_MEDIO
        boton_luna_bg = BLANCO
        boton_luna_fg = NEGRO
    else:
        # Paleta clara.
        fondo = GRIS_NIEBLA
        panel = BLANCO
        texto = GRIS_AZULADO
        acento = VERDE_AZULADO
        boton_luna_bg = NEGRO
        boton_luna_fg = BLANCO

    ventanas_secundarias[:] = [v for v in ventanas_secundarias if v.winfo_exists()]
    # Filtro la lista: me quedo con las ventanas que existen.

    for ventana_hija in ventanas_secundarias:
        # Recorro cada ventana.
        ventana_hija.config(bg=fondo)
        # Aplico fondo.

        for widget in ventana_hija.winfo_children():
            actualizar_widget(widget, fondo, panel, texto, acento)
            # Pinto cada widget de la ventana.

def agregar_boton_luna(ventana_hija):
    # Registro una ventana nueva.
    if ventana_hija not in ventanas_secundarias:
        ventanas_secundarias.append(ventana_hija)
    actualizar_ventanas_secundarias()
    # La pinto con el tema actual.

def aplicar_tema():
    # Alterno entre claro y oscuro.
    global tema_oscuro
    tema_oscuro = not tema_oscuro
    # Invierto el flag.

    if tema_oscuro:
        # Paleta oscura.
        fondo_general = NEGRO
        panel = GRIS
        panel_2 = GRIS
        texto = BLANCO
        texto_secundario = BLANCO_HUESO
        fondo_banner = NEGRO
        boton_accion = GRIS
        boton_hover = VERDE_AZULADO
        boton_texto = BLANCO
        lista_bg = GRIS
        lista_fg = BLANCO
        btn_luna_bg = BLANCO
        btn_luna_hover = GRIS_MEDIO
        btn_luna_fg = NEGRO
    else:
        # Paleta clara.
        fondo_general = GRIS_NIEBLA
        panel = BLANCO
        panel_2 = GRIS_AZULADO
        texto = GRIS_AZULADO
        texto_secundario = GRIS_MEDIO
        fondo_banner = AZUL_SERENO
        boton_accion = VERDE_AZULADO
        boton_hover = VERDE_TERMINAL
        boton_texto = BLANCO
        lista_bg = BLANCO
        lista_fg = GRIS_AZULADO
        btn_luna_bg = NEGRO
        btn_luna_hover = GRIS
        btn_luna_fg = BLANCO

    ventana.config(bg=fondo_general)
    banner.config(bg=fondo_general)
    banner_label.config(bg=fondo_general, fg=texto_secundario)
    # Pinto la ventana principal.

    frame_btn.config(bg=fondo_general)
    frame_btn_info.config(bg=fondo_general)
    frame_form.config(bg=fondo_general)
    cuerpo.config(bg=fondo_general)
    # Pinto los frames grandes.

    frame_foto.config(bg=panel)
    visor_foto.config(bg=panel, fg=texto_secundario)
    # Pinto el visor de foto.

    frame_lista.config(bg=panel_2)
    titulo_lista.config(bg=panel_2, fg=texto)
    contador_legajos.config(bg=panel_2, fg=AMARILLO)
    lista_personas.config(bg=lista_bg, fg=lista_fg,
                           selectbackground=AZUL_SERENO,
                           selectforeground=BLANCO)
    # Pinto la lista.

    for widget in frame_form.winfo_children():
        # Recorro los hijos del formulario.
        if isinstance(widget, Label):
            widget.config(bg=fondo_general, fg=texto)
            # Labels.

        elif isinstance(widget, Entry):
            widget.config(bg=lista_bg, fg=lista_fg, insertbackground=lista_fg)
            # Entries.

    sub_btn.config(bg=fondo_general)
    # Pinto el sub-frame.

    for widget in (btn_agregar, btn_eliminar, btn_buscar, btn_limpiar):
        # Recorro los 4 botones.
        widget.set_colors(boton_accion, boton_hover, boton_texto, fondo_general)
    btn_tema.set_colors(btn_luna_bg, btn_luna_hover, btn_luna_fg, fondo_general)

    for widget in frame_form.winfo_children():
        # Recorro los hijos del formulario.
        if isinstance(widget, RoundedButton):
            widget.set_colors(boton_accion, boton_hover, boton_texto, fondo_general)
            # Botones redondos del formulario.

    for widget in frame_btn_info.winfo_children():
        # Recorro el frame del botón Info.
        if isinstance(widget, RoundedButton):
            widget.set_colors(boton_accion, boton_hover, boton_texto, fondo_general)

    actualizar_ventanas_secundarias()
    # Pinto también las ventanas hijas abiertas.

# ============================================================================
# BLOQUE 14: AUXILIARES
# ============================================================================
def normalizar_fecha(texto):
    # Reemplazo separadores raros por "/".
    texto = texto.strip()
    for i in string.punctuation:
        if i in (":", "/"):
            continue
        # No toco : ni /.
        texto = texto.replace(i, "/")
    return texto

def separar_fecha_hora(texto):
    # Separa "fecha hora" en tupla.
    texto = normalizar_fecha(texto)
    match = re.search(r"\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*$", texto)
    # Busco "HH:MM" o "HH:MM:SS" al final.
    if match:
        hora = match.group(1)
        fecha = texto[:match.start()].strip()
        return fecha, hora
    return texto, ""

def comprobar_fecha(entry_fecha):
    # Devuelvo solo la parte de fecha.
    fecha, _ = separar_fecha_hora(entry_fecha.get())
    return fecha

def ver_list_entrevist(lista_widget):
    # Refresco la lista de entrevistas.
    lista_widget.delete(0, tk.END)
    cursor.execute("""SELECT e.id, e.fecha_entrevista, e.hora_entrevista, e.dni_paciente,
                             e.nombre_profecional, e.apellido_profecional, e.tipo_entrevista,
                             e.especialidad, e.activo_profecional, e.proxima_sesion_entrevista,
                             p.nombre, p.apellido
                      FROM entrevistas AS e
                      LEFT JOIN personas AS p ON p.dni = e.dni_paciente
                      ORDER BY e.id""")
    # LEFT JOIN trae paciente si existe.
    for i in cursor.fetchall():
        paciente = ""
        if i[10] or i[11]:
            paciente = f" ({i[11] or ''} {i[10] or ''})".strip()
        dato = f"ID: {i[0]} // Fecha: {i[1]} {i[2] or ''} // DNI pac: {i[3]}{paciente} // Prof: {i[4]} {i[5] or ''} // Esp: {i[7] or '-'} // Tipo: {i[6] or '-'} // Estado: {i[8] or '-'}"
        if i[9]:
            dato += f" // Prox: {i[9]}"
        lista_widget.insert(tk.END, dato)

# ============================================================================
# BLOQUE 15: EDITAR ENTREVISTA
# ============================================================================

def pantalla_edit_entrevista(ventana_padre):
    ventana_editar = tk.Toplevel(ventana_padre)
    # Ventana hija.

    ventana_editar.title("Editar datos de entrevista")
    ventana_editar.geometry("800x950")
    ventana_editar.config(bg=GRIS_NIEBLA)

    frame_editar_superior = tk.Frame(ventana_editar, bg=AZUL_PETROLEO,
                                      relief="solid", bd=1)
    # Frame superior azul petróleo.

    frame_editar_superior.pack(side="top", padx=20, pady=20, fill="x")
    # Arriba.

    Label(frame_editar_superior, text="ID de la entrevista a editar:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=0, column=0)
    # Label de ID.

    entry_id = tk.Entry(frame_editar_superior, width=30, relief="solid",
                         bd=1, font=("Segoe UI", 12))
    # Entry de ID.

    entry_id.grid(row=0, column=1)
    # En columna 1.

    Label(frame_editar_superior, text="DNI paciente:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=1, column=0)
    # Label DNI paciente.

    entry_dni_edit = tk.Entry(frame_editar_superior, width=30, relief="solid",
                          bd=1, font=("Segoe UI", 12))
    # Entry DNI paciente.

    entry_dni_edit.grid(row=1, column=1)
    # En columna 1.

    Label(frame_editar_superior, text="Nombre del Profesional:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=2, column=0)
    # Label nombre profesional.

    entry_nombre_profecional = tk.Entry(frame_editar_superior, width=30,
                                         relief="solid", bd=1,
                                         font=("Segoe UI", 12))
    # Entry nombre profesional.

    entry_nombre_profecional.grid(row=2, column=1)

    Label(frame_editar_superior, text="Apellido del Profesional:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=3, column=0)
    # Label apellido profesional.

    entry_apellido_profecional = tk.Entry(frame_editar_superior, width=30,
                                           relief="solid", bd=1,
                                           font=("Segoe UI", 12))
    # Entry apellido profesional.

    entry_apellido_profecional.grid(row=3, column=1)

    Label(frame_editar_superior, text="DNI del Profesional:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=4, column=0)
    # Label DNI profesional.

    entry_dni_profesional = tk.Entry(frame_editar_superior, width=30,
                                      relief="solid", bd=1,
                                      font=("Segoe UI", 12))
    # Entry DNI profesional.

    entry_dni_profesional.grid(row=4, column=1)

    Label(frame_editar_superior, text="Matricula:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=5, column=0)
    # Label matrícula.

    entry_matricula = tk.Entry(frame_editar_superior, width=30,
                                relief="solid", bd=1,
                                font=("Segoe UI", 12))
    # Entry matrícula.

    entry_matricula.grid(row=5, column=1)

    Label(frame_editar_superior, text="Especialidad:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=6, column=0)
    # Label especialidad.

    entry_especialidad = tk.Entry(frame_editar_superior, width=30,
                                   relief="solid", bd=1,
                                   font=("Segoe UI", 12))
    # Entry especialidad.

    entry_especialidad.grid(row=6, column=1)

    Label(frame_editar_superior, text="Telefono del Profesional:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=7, column=0)
    # Label teléfono.

    entry_tel_profesional = tk.Entry(frame_editar_superior, width=30,
                                      relief="solid", bd=1,
                                      font=("Segoe UI", 12))
    # Entry teléfono.

    entry_tel_profesional.grid(row=7, column=1)

    Label(frame_editar_superior, text="Email del Profesional:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=8, column=0)
    # Label email.

    entry_email_profesional = tk.Entry(frame_editar_superior, width=30,
                                        relief="solid", bd=1,
                                        font=("Segoe UI", 12))
    # Entry email.

    entry_email_profesional.grid(row=8, column=1)

    Label(frame_editar_superior, text="Estado:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=9, column=0)
    # Label estado.

    var_estado_profesional = tk.StringVar(value="")
    # Variable para el menú desplegable.

    menu_estado_profesional = tk.OptionMenu(frame_editar_superior,
                                             var_estado_profesional,
                                             "Activo", "No activo")
    # Menú desplegable con dos opciones.

    menu_estado_profesional.config(font=("Segoe UI", 12), width=30)
    # Configuro fuente y ancho.

    menu_estado_profesional.grid(row=9, column=1)
    # En su fila.

    Label(frame_editar_superior, text="Fecha:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=10, column=0)
    # Label fecha.

    entry_fecha = tk.Entry(frame_editar_superior, width=30, relief="solid",
                            bd=1, font=("Segoe UI", 12))
    # Entry fecha.

    entry_fecha.grid(row=10, column=1)

    Label(frame_editar_superior, text="Hora:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=11, column=0)
    # Label hora.

    entry_hora = tk.Entry(frame_editar_superior, width=30, relief="solid",
                           bd=1, font=("Segoe UI", 12))
    # Entry hora.

    entry_hora.grid(row=11, column=1)

    Label(frame_editar_superior, text="Tipo:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=12, column=0)
    # Label tipo.

    var_tipo = tk.StringVar(value="")
    # Variable del menú de tipo.

    menu_tipo = tk.OptionMenu(frame_editar_superior, var_tipo,
                              "individual", "grupal", "familiar")
    # Menú de tipo.

    menu_tipo.config(font=("Segoe UI", 12), width=30)

    menu_tipo.grid(row=12, column=1)

    Label(frame_editar_superior, text="Proxima Sesion:", bg=AZUL_PETROLEO,
          fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=13, column=0)
    # Label próxima sesión.

    entry_proxima = tk.Entry(frame_editar_superior, width=30, relief="solid",
                              bd=1, font=("Segoe UI", 12))
    # Entry próxima sesión.

    entry_proxima.grid(row=13, column=1)

    frame_editar_inferior = tk.Frame(ventana_editar, bg=GRIS_NIEBLA)
    # Frame inferior (para el botón Guardar).

    frame_editar_inferior.pack(side="bottom", fill="x", padx=20, pady=10)
    # Anclado abajo.

    frame_editar_medio = tk.Frame(ventana_editar, bg=GRIS_NIEBLA,
                                    relief="solid", bd=1)
    # Frame del medio (para el texto de la entrevista).

    frame_editar_medio.pack(fill="both", expand=True, padx=20, pady=10)
    # Relleno del centro.

    Label(frame_editar_medio, text="Texto de la entrevista:",
          bg=AZUL_PETROLEO, fg=BLANCO_HUESO,
          font=("Segoe UI", 12)).pack(fill="x", side="top", padx=20, pady=5)
    # Título del cuadro de texto.

    text_entrevista_edit = tk.Text(frame_editar_medio, bg=GRIS_NIEBLA,
                                     relief="solid", bd=1,
                                     font=("Segoe UI", 12))
    # Cuadro de texto grande.

    text_entrevista_edit.pack(fill="both", expand=True, padx=15, pady=15)
    # Estirado.

    def cargar_entrevista():
        # Cargo los datos de la entrevista con el ID ingresado.
        p_id = entry_id.get().strip()
        if not p_id:
            return

        cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (p_id,))
        e = cursor.fetchone()
        if not e:
            messagebox.showinfo("Error", "No existe esa entrevista.")
            return

        text_entrevista_edit.delete("1.0", tk.END)
        # Limpio el Text.

        text_entrevista_edit.insert("1.0", e[9] or "")
        # Inserto el texto de la entrevista (columna 9).

        entry_dni_edit.delete(0, tk.END)
        entry_dni_edit.insert(0, e[10] or "")
        # Cargo DNI paciente.

        entry_nombre_profecional.delete(0, tk.END)
        entry_nombre_profecional.insert(0, e[1] or "")
        # Cargo nombre profesional.

        entry_apellido_profecional.delete(0, tk.END)
        entry_apellido_profecional.insert(0, e[2] or "")
        # Cargo apellido profesional.

        entry_dni_profesional.delete(0, tk.END)
        entry_dni_profesional.insert(0, e[3] or "")
        # Cargo DNI profesional.

        entry_matricula.delete(0, tk.END)
        entry_matricula.insert(0, e[4] or "")
        # Cargo matrícula.

        entry_especialidad.delete(0, tk.END)
        entry_especialidad.insert(0, e[5] or "")
        # Cargo especialidad.

        entry_tel_profesional.delete(0, tk.END)
        entry_tel_profesional.insert(0, e[6] or "")
        # Cargo teléfono.

        entry_email_profesional.delete(0, tk.END)
        entry_email_profesional.insert(0, e[7] or "")
        # Cargo email.

        var_estado_profesional.set(e[8] or "")
        # Cargo estado en el menú.

        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, e[11] or "")
        # Cargo fecha.

        entry_hora.delete(0, tk.END)
        entry_hora.insert(0, e[12] or "")
        # Cargo hora.

        var_tipo.set(e[13] or "")
        # Cargo tipo en el menú.

        entry_proxima.delete(0, tk.END)
        entry_proxima.insert(0, e[14] or "")
        # Cargo próxima sesión.

    def guardar_entrevista():
        # Guardo los cambios.
        p_id = entry_id.get().strip()
        if not p_id:
            return

        cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (p_id,))
        entrevista = cursor.fetchone()
        if not entrevista:
            messagebox.showinfo("Error", "No existe esa entrevista.")
            return

        texto_nuevo = text_entrevista_edit.get("1.0", tk.END).strip()
        # Traigo el texto nuevo del Text.

        if texto_nuevo == "":
            texto_nuevo = entrevista[9]
            # Si quedó vacío, mantengo el viejo.

        dni_entry_txt = entry_dni_edit.get().strip()
        if dni_entry_txt:
            # Si escribieron DNI...
            try:
                dni_nuevo = int(dni_entry_txt)
            except ValueError:
                messagebox.showerror("DNI invalido",
                                      "El DNI del paciente debe ser numerico.")
                return
        else:
            dni_nuevo = entrevista[10]
            # Si quedó vacío, mantengo el viejo.

        cursor.execute("SELECT 1 FROM personas WHERE dni = ?", (dni_nuevo,))
        if not cursor.fetchone():
            # El paciente no existe.
            messagebox.showwarning(
                "Paciente no registrado",
                "No hay ninguna persona con ese DNI.\nAgregala primero en la pantalla principal.")
            return

        nom_prof_nuevo = entry_nombre_profecional.get().strip() or entrevista[1]
        # Uso "or" para mantener el viejo si está vacío.

        ape_prof_nuevo = entry_apellido_profecional.get().strip() or entrevista[2]
        dni_prof_nuevo = entry_dni_profesional.get().strip() or entrevista[3]
        matricula_nueva = entry_matricula.get().strip() or entrevista[4]
        especialidad_nueva = entry_especialidad.get().strip() or entrevista[5]
        tel_prof_nuevo = entry_tel_profesional.get().strip() or entrevista[6]
        email_prof_nuevo = entry_email_profesional.get().strip() or entrevista[7]
        estado_nuevo = var_estado_profesional.get() or entrevista[8]

        fecha_nueva = entry_fecha.get().strip()
        if fecha_nueva == "":
            fecha_nueva = entrevista[11]
        else:
            fecha_nueva = comprobar_fecha(entry_fecha)
        # Normalizo la fecha nueva.

        hora_nueva = normalizar_fecha(entry_hora.get()) or entrevista[12]
        tipo_nuevo = var_tipo.get() or entrevista[13]
        proxima_nueva = comprobar_fecha(entry_proxima)

        cursor.execute("""UPDATE entrevistas SET entrevista = ?, dni_paciente = ?,
                            nombre_profecional = ?, apellido_profecional = ?, dni_profecional = ?,
                            matricula = ?, especialidad = ?, telefono_profecional = ?,
                            email_profecional = ?, activo_profecional = ?, fecha_entrevista = ?,
                            hora_entrevista = ?, tipo_entrevista = ?, proxima_sesion_entrevista = ?
                            WHERE id = ?""",
                         (texto_nuevo, dni_nuevo, nom_prof_nuevo, ape_prof_nuevo,
                          dni_prof_nuevo, matricula_nueva, especialidad_nueva,
                          tel_prof_nuevo, email_prof_nuevo, estado_nuevo,
                          fecha_nueva, hora_nueva, tipo_nuevo, proxima_nueva, p_id))
        # Actualizo la fila.

        conexion.commit()

        ver_list_entrevist(lista_entrevistas)
        # Refresco la lista.

        ventana_editar.destroy()
        # Cierro la ventana de edición.

    boton_guardar_cambios = RoundedButton(frame_editar_inferior, 200, 35, 15,
                                            VERDE_AZULADO, BLANCO,
                                            text="Guardar cambios",
                                            command=guardar_entrevista)
    # Botón Guardar.

    boton_guardar_cambios.pack(pady=5)
    # Centrado.

    seleccion = lista_entrevistas.curselection()
    if seleccion:
        # Si había una entrevista seleccionada, la autocargo.
        dato = lista_entrevistas.get(seleccion[0])
        id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()
        entry_id.delete(0, tk.END)
        entry_id.insert(0, id_entrevista)
        cargar_entrevista()

    agregar_boton_luna(ventana_editar)
    # Aplico el tema.

# ============================================================================
# BLOQUE 16: FUNCIONES DE ENTREVISTAS
# ============================================================================

def new_entrevista():
    # Creo una entrevista nueva.
    entrevista = text_entrevista.get("1.0", tk.END).strip()
    # Texto del cuadro.

    dni = entry_dni_entrevista.get().strip()
    # DNI paciente.

    dni_profesional = entry_dni_profesional.get().strip()
    # DNI profesional.

    nom_profecional = entry_nombre_profecional.get().strip()
    # Nombre profesional.

    ape_profecional = entry_apellido_profecional.get().strip()
    # Apellido profesional.

    tel_profecional = entry_tel_profesional.get().strip()
    # Teléfono.

    mail_profecional = entry_mail_profesional.get().strip()
    # Email.

    estado_profesional = var_tipo_estado.get()
    # Estado.

    fecha = comprobar_fecha(entry_fecha)
    # Fecha normalizada.

    matricula = entry_matricula.get().strip()
    # Matrícula.

    especialidad = entry_especialidad.get().strip()
    # Especialidad.

    hora = normalizar_fecha(entry_hora_entrevista.get())
    # Hora.

    tipo = var_tipo_entrevista.get()
    # Tipo.

    proxima_sesion = comprobar_fecha(entry_proxima_sesion)
    # Próxima sesión.

    if entrevista == "" or dni == "" or nom_profecional == "":
        # Validación mínima.
        messagebox.showwarning("Faltan datos",
                                "Complete la entrevista, DNI del paciente y Profesional.")
        return

    try:
        dni = int(dni)
        # Convertir a entero.
    except ValueError:
        messagebox.showerror("DNI invalido", "El DNI del paciente debe ser numerico.")
        return

    cursor.execute("SELECT 1 FROM personas WHERE dni = ?", (dni,))
    if not cursor.fetchone():
        # Paciente no registrado.
        messagebox.showwarning(
            "Paciente no registrado",
            "No hay ninguna persona con ese DNI.\nAgregala primero en la pantalla principal.")
        return

    try:
        cursor.execute("""INSERT INTO entrevistas
            (nombre_profecional, apellido_profecional, dni_profecional,
             telefono_profecional, email_profecional, activo_profecional,
             entrevista, dni_paciente, matricula, especialidad,
             fecha_entrevista, hora_entrevista, tipo_entrevista, proxima_sesion_entrevista)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (nom_profecional, ape_profecional, dni_profesional,
             tel_profecional, mail_profecional, estado_profesional,
             entrevista, dni, matricula, especialidad,
             fecha, hora, tipo, proxima_sesion))
        conexion.commit()
    except Exception:
        messagebox.showerror("Error")
        return

    ver_list_entrevist(lista_entrevistas)
    # Refresco.

    text_entrevista.delete("1.0", tk.END)
    # Limpio el Text.

def eliminar_entrevista():
    # Borro la entrevista seleccionada.
    seleccion = lista_entrevistas.curselection()
    if seleccion:
        dato = lista_entrevistas.get(seleccion[0])
        id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()
        cursor.execute("DELETE FROM entrevistas WHERE id = ?", (id_entrevista,))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)

def detalles_entrevista(event=None):
    # Muestro todos los detalles en ventana nueva.
    seleccion = lista_entrevistas.curselection()
    if not seleccion:
        return
    dato = lista_entrevistas.get(seleccion[0])
    id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()

    cursor.execute("""SELECT nombre_profecional, apellido_profecional, dni_profecional,
                             matricula, especialidad, telefono_profecional,
                             email_profecional, activo_profecional, entrevista,
                             dni_paciente, fecha_entrevista, hora_entrevista,
                             tipo_entrevista, proxima_sesion_entrevista
                      FROM entrevistas WHERE id = ?""", (id_entrevista,))
    e = cursor.fetchone()
    if not e:
        return

    ventana_detalle = Toplevel()
    ventana_detalle.title(f"Detalle de entrevista #{id_entrevista}")
    ventana_detalle.geometry("600x550")
    ventana_detalle.config(bg=GRIS_NIEBLA)

    frame_detalle = Frame(ventana_detalle, bg=BLANCO, relief="solid", bd=1)
    frame_detalle.pack(padx=20, pady=20, fill="both", expand=True)

    info = [
        ("ID", id_entrevista),
        ("Nombre del profesional", e[0] or "-"),
        ("Apellido del profesional", e[1] or "-"),
        ("DNI del profesional", e[2] or "-"),
        ("Matricula", e[3] or "-"),
        ("Especialidad", e[4] or "-"),
        ("Telefono profesional", e[5] or "-"),
        ("Email profesional", e[6] or "-"),
        ("Estado profesional", e[7] or "-"),
        ("DNI paciente", e[9] or "-"),
        ("Fecha", e[10] or "-"),
        ("Hora", e[11] or "-"),
        ("Tipo de entrevista", e[12] or "-"),
        ("Proxima sesion", e[13] or "-"),
    ]
    # Armo la lista de etiqueta + valor.

    for etiqueta, valor in info:
        # Recorro.
        fila = Frame(frame_detalle, bg=BLANCO)
        fila.pack(fill="x", padx=10, pady=2)

        Label(fila, text=f"{etiqueta}:", bg=BLANCO, fg=GRIS_AZULADO,
              font=("Segoe UI", 11, "bold"), width=16,
              anchor="e").pack(side="left")
        # Label de la etiqueta.

        Label(fila, text=valor, bg=BLANCO, fg=GRIS_AZULADO,
              font=("Segoe UI", 11), anchor="w").pack(side="left", padx=5)
        # Label del valor.

    Label(frame_detalle, text="Anotaciones:", bg=BLANCO, fg=GRIS_AZULADO,
          font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x",
                                                          padx=10,
                                                          pady=(10, 2))
    # Título "Anotaciones".

    text_dato = tk.Text(frame_detalle, height=8, font=("Segoe UI", 11),
                          relief="solid", bd=1)
    # Cuadro de texto.

    text_dato.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    text_dato.insert("1.0", e[8] or "")
    # Inserto el texto de la entrevista.

    text_dato.config(state=tk.DISABLED)
    # Lo dejo solo lectura.

    agregar_boton_luna(ventana_detalle)

# ============================================================================
# BLOQUE 17: VENTANA DE ENTREVISTAS
# ============================================================================

def abrir_ventana_entrevistas(ventana_padre):
    global _ventana_entrevistas_abierta

    if _ventana_entrevistas_abierta is not None and _ventana_entrevistas_abierta.winfo_exists():
        # Ya hay una ventana abierta.
        _ventana_entrevistas_abierta.lift()
        # La traigo al frente.

        _ventana_entrevistas_abierta.focus_force()
        # Le doy el foco.

        return

    ventana_entrevistas = tk.Toplevel(ventana_padre)
    # Creo la Toplevel.

    _ventana_entrevistas_abierta = ventana_entrevistas
    # Guardo la referencia.

    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("1600x800")
    ventana_entrevistas.config(bg=GRIS_NIEBLA)

    global lista_entrevistas, text_entrevista, entry_dni_entrevista
    global entry_nombre_profecional, entry_dni_profesional, entry_fecha
    global entry_apellido_profecional, entry_tel_profesional, entry_mail_profesional
    global entry_matricula, entry_especialidad, entry_hora_entrevista
    global var_tipo_entrevista, var_tipo_estado, entry_proxima_sesion
    # Declaro globales todos los widgets para usarlos en otras funciones.

    frame_superior = Frame(ventana_entrevistas, bg=GRIS_AZULADO)
    # Frame superior.

    frame_superior.pack(side="top", fill="x", padx=20, pady=10)
    # Arriba.

    Label(frame_superior, text="DNI Paciente:", bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="e",
                                              padx=10, pady=8)
    # Label DNI.

    entry_dni_entrevista = Entry(frame_superior, font=("Segoe UI", 11),
                                  width=15)
    # Entry DNI.

    entry_dni_entrevista.grid(row=0, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Fecha:", bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=0, column=2, sticky="e",
                                              padx=10, pady=8)
    # Label fecha.

    entry_fecha = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    # Entry fecha.

    entry_fecha.grid(row=0, column=3, sticky="w", padx=5)

    Label(frame_superior, text="Hora:", bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=0, column=4, sticky="e",
                                              padx=10, pady=8)
    # Label hora.

    entry_hora_entrevista = Entry(frame_superior, font=("Segoe UI", 11),
                                    width=15)
    # Entry hora.

    entry_hora_entrevista.grid(row=0, column=5, sticky="w", padx=5)

    Label(frame_superior, text="Nombre del profesional:", bg=GRIS_AZULADO,
          fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=0,
                                                          sticky="e",
                                                          padx=10, pady=8)
    # Label nombre profesional.

    entry_nombre_profecional = Entry(frame_superior, font=("Segoe UI", 11),
                                       width=15)
    # Entry nombre.

    entry_nombre_profecional.grid(row=1, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Apellido del profesional:",
          bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=1, column=2, sticky="e",
                                              padx=10, pady=8)
    # Label apellido.

    entry_apellido_profecional = Entry(frame_superior,
                                         font=("Segoe UI", 11), width=15)
    # Entry apellido.

    entry_apellido_profecional.grid(row=1, column=3, sticky="w", padx=5)

    Label(frame_superior, text="DNI del profesional:", bg=GRIS_AZULADO,
          fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=4,
                                                          sticky="e",
                                                          padx=10, pady=8)
    # Label DNI profesional.

    entry_dni_profesional = Entry(frame_superior, font=("Segoe UI", 11),
                                    width=15)
    # Entry DNI profesional.

    entry_dni_profesional.grid(row=1, column=5, sticky="w", padx=5)

    Label(frame_superior, text="Matricula:", bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="e",
                                              padx=10, pady=8)
    # Label matrícula.

    entry_matricula = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    # Entry matrícula.

    entry_matricula.grid(row=2, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Especialidad:", bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=2, column=2, sticky="e",
                                              padx=10, pady=8)
    # Label especialidad.

    entry_especialidad = Entry(frame_superior, font=("Segoe UI", 11),
                                 width=15)
    # Entry especialidad.

    entry_especialidad.grid(row=2, column=3, sticky="w", padx=5)

    Label(frame_superior, text="Proxima Sesión:", bg=GRIS_AZULADO,
          fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=4,
                                                          sticky="e",
                                                          padx=10, pady=8)
    # Label próxima sesión.

    entry_proxima_sesion = Entry(frame_superior, font=("Segoe UI", 11),
                                   width=15)
    # Entry próxima sesión.

    entry_proxima_sesion.grid(row=2, column=5, sticky="w", padx=5)

    Label(frame_superior, text="Tipo de visita:", bg=GRIS_AZULADO,
          fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=4, column=0,
                                                          sticky="e",
                                                          padx=10, pady=8)
    # Label tipo.

    var_tipo_entrevista = tk.StringVar(value="")
    # Variable del menú.

    menu_tipo = tk.OptionMenu(frame_superior, var_tipo_entrevista,
                              "individual", "grupal", "familiar")
    # Menú de tipo.

    menu_tipo.config(font=("Segoe UI", 10), width=12)

    menu_tipo.grid(row=4, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Telefono del profesional:",
          bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=0, column=6, sticky="e",
                                              padx=10, pady=8)
    # Label teléfono.

    entry_tel_profesional = Entry(frame_superior, font=("Segoe UI", 11),
                                    width=15)
    # Entry teléfono.

    entry_tel_profesional.grid(row=0, column=7, sticky="w", padx=5)

    Label(frame_superior, text="Mail del profesional:", bg=GRIS_AZULADO,
          fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=6,
                                                          sticky="e",
                                                          padx=10, pady=8)
    # Label mail.

    entry_mail_profesional = Entry(frame_superior, font=("Segoe UI", 11),
                                     width=15)
    # Entry mail.

    entry_mail_profesional.grid(row=2, column=7, sticky="w", padx=5)

    Label(frame_superior, text="Estado:", bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 11, "bold")).grid(row=1, column=6, sticky="e",
                                              padx=10, pady=8)
    # Label estado.

    var_tipo_estado = tk.StringVar(value="")
    # Variable del menú de estado.

    menu_estado = tk.OptionMenu(frame_superior, var_tipo_estado,
                                 "Activo", "No activo")
    # Menú de estado.

    menu_estado.config(font=("Segoe UI", 10), width=12)

    menu_estado.grid(row=1, column=7, sticky="w", padx=5)

    frame_inferior = Frame(ventana_entrevistas, bg=GRIS_NIEBLA, height=80)
    # Frame inferior con botones.

    frame_inferior.pack(side="bottom", fill="x", padx=20, pady=20)
    # Abajo.

    # Centrado.

    frame_inferior.columnconfigure(0, weight=1)
    frame_inferior.columnconfigure(1, weight=1)
    frame_inferior.columnconfigure(2, weight=1)
    frame_inferior.columnconfigure(3, weight=1)
    frame_inferior.columnconfigure(4, weight=1)
    # Columnas con peso para distribuir los botones uniformemente.

    RoundedButton(frame_inferior, 150, 40, 20, VERDE_AZULADO, BLANCO,
                  text="Nueva entrevista",
                  command=new_entrevista).grid(row=0, column=1, padx=10,
                                                sticky="ew")
    # Botón Nueva entrevista.

    RoundedButton(frame_inferior, 160, 40, 20, VERDE_AZULADO, BLANCO,
                  text="Eliminar entrevista",
                  command=eliminar_entrevista).grid(row=0, column=2, padx=10,
                                                     sticky="ew")

    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
    # Función interna para no pasar argumento en command.

    RoundedButton(frame_inferior, 180, 40, 20, VERDE_AZULADO, BLANCO,
                  text="Editar entrevista",
                  command=abrir_editar).grid(row=0, column=3, padx=10,
                                              sticky="ew")
    # Botón Editar.

    RoundedButton(frame_inferior, 150, 40, 20, VERDE_AZULADO, BLANCO,
                  text="Generar PDF",
                  command=exportar_entrevistas_pdf).grid(row=0, column=4,
                                                          padx=10, sticky="ew")
    # Botón Generar PDF.

    frame_medio_cuerpo = Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    # Frame del medio.

    frame_medio_cuerpo.pack(fill="both", expand=True, padx=15, pady=10)
    # Estirado.

    frame_lista_medio = Frame(frame_medio_cuerpo, bg=BLANCO,
                                relief="solid", bd=1)
    # Frame de la lista.

    frame_lista_medio.pack(side="left", fill="both", expand=True,
                            padx=(0, 10))
    # A la izquierda.

    Label(frame_lista_medio, text="Historial de Entrevistas", bg=BLANCO,
          fg=GRIS_AZULADO,
          font=("Segoe UI", 13, "bold")).pack(pady=5)
    # Título.

    lista_entrevistas = Listbox(frame_lista_medio, bg=BLANCO,
                                  fg=GRIS_AZULADO,
                                  selectbackground=AZUL_SERENO,
                                  selectforeground=BLANCO, bd=0,
                                  font=("Segoe UI", 10))
    # Listbox.

    lista_entrevistas.pack(fill="both", expand=True, padx=5, pady=5)

    lista_entrevistas.bind("<Double-Button-1>", detalles_entrevista)
    # Doble click = detalles.

    ver_list_entrevist(lista_entrevistas)
    # Cargo la lista.

    frame_texto = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    # Frame del texto.

    frame_texto.pack(side="left", fill="both", expand=True, padx=(10, 0))
    # A la derecha.

    Label(frame_texto, text="Anotaciones de la entrevista", bg=BLANCO,
          fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    # Título.

    text_entrevista = tk.Text(frame_texto, relief="solid", bd=1,
                                bg=GRIS_NIEBLA, font=("Segoe UI", 12))
    # Text grande para la anotación.

    text_entrevista.pack(fill="both", expand=True, padx=5, pady=5)

    agregar_boton_luna(ventana_entrevistas)

# ============================================================================
# BLOQUE 18: VENTANA DE PERFIL
# ============================================================================

def abrir_ventana_perfil():
    global entry_dni_perfil_ref
    # Necesito modificar la global.

    ventana_perfil = Toplevel(ventana)
    # Toplevel.

    ventana_perfil.title("PERFIL")
    ventana_perfil.geometry("1500x800")
    ventana_perfil.config(bg=GRIS_NIEBLA)

    def al_cerrar_perfil():
        global entry_dni_perfil_ref
        # Declaro global otra vez para poder setearla a None.

        entry_dni_perfil_ref = None
        # Limpio la referencia para que otras funciones sepan que el
        # Entry ya no existe.

        ventana_perfil.destroy()
        # Destruyo la ventana.

    ventana_perfil.protocol("WM_DELETE_WINDOW", al_cerrar_perfil)
    # Intercepto el evento "click en X" para hacer la limpieza.

    foto_pendiente = {"bytes": None}
    # Diccionario con la foto nueva (o b"") pendiente de guardar.
    # Uso dict porque necesito MUTARLO desde las funciones internas,
    # no reasignarlo.

    dni_original = {"valor": entry_dni.get().strip()}
    # Diccionario con el DNI original (para detectar si lo cambiaron).

    frame_izquierdo = Frame(ventana_perfil, bg=GRIS_NIEBLA)
    # Frame izquierdo (formulario).

    frame_izquierdo.pack(side="left", fill="y", padx=15, pady=15)
    # A la izquierda.

    Label(frame_izquierdo, text=" Nombre:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=0, column=0,
                                                       sticky="e", padx=5)
    # Label Nombre.

    entry_nombre_perfil = Entry(frame_izquierdo, width=22,
                                  font=("Segoe UI", 12))
    # Entry Nombre.

    entry_nombre_perfil.grid(row=0, column=1, padx=5, pady=3)

    entry_nombre_perfil.insert(0, entry_nombre.get())
    # Precargo con lo que tenga el entry principal.

    Label(frame_izquierdo, text=" Apellido:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=1, column=0,
                                                       sticky="e", padx=5)
    # Label Apellido.

    entry_apellido_perfil = Entry(frame_izquierdo, width=22,
                                    font=("Segoe UI", 12))
    # Entry Apellido.

    entry_apellido_perfil.grid(row=1, column=1, padx=5, pady=3)

    entry_apellido_perfil.insert(0, entry_apellido.get())
    # Precargo.

    Label(frame_izquierdo, text="Edad:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO,
          font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=5)
    # Label Edad.

    entry_edad_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    # Entry Edad.

    entry_edad_perfil.grid(row=2, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text=" DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO,
          font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=5)
    # Label DNI.

    entry_dni_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    # Entry DNI.

    entry_dni_perfil.grid(row=3, column=1, padx=5, pady=3)

    entry_dni_perfil.insert(0, entry_dni.get())
    # Precargo con el DNI del formulario principal.

    entry_dni_perfil_ref = entry_dni_perfil
    # Guardo la referencia global al Entry (para el editor de fotos).

    Label(frame_izquierdo, text=" Domicilio:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=4, column=0,
                                                       sticky="e", padx=5)
    # Label Domicilio.

    entry_direccion_perfil = Entry(frame_izquierdo, width=22,
                                     font=("Segoe UI", 12))
    # Entry Domicilio.

    entry_direccion_perfil.grid(row=4, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text=" Fecha de nacimiento:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=5, column=0,
                                                       sticky="e", padx=5)
    # Label fecha nacimiento.

    entry_f_nacimiento_perfil = Entry(frame_izquierdo, width=22,
                                        font=("Segoe UI", 12))
    # Entry fecha nacimiento.

    entry_f_nacimiento_perfil.grid(row=5, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text=" Fecha de ingreso al instituto:",
          bg=GRIS_NIEBLA, fg=GRIS_AZULADO,
          font=("Segoe UI", 12)).grid(row=6, column=0, sticky="e", padx=5)
    # Label fecha ingreso.

    entry_f_ingreso_perfil = Entry(frame_izquierdo, width=22,
                                     font=("Segoe UI", 12))
    # Entry fecha ingreso.

    entry_f_ingreso_perfil.grid(row=6, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Telefono:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=7, column=0,
                                                       sticky="e", padx=5)
    # Label teléfono.

    entry_telefono_perfil = Entry(frame_izquierdo, width=22,
                                    font=("Segoe UI", 12))
    # Entry teléfono.

    entry_telefono_perfil.grid(row=7, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Nombre del contacto de emergencia:",
          bg=GRIS_NIEBLA, fg=GRIS_AZULADO,
          font=("Segoe UI", 12)).grid(row=8, column=0, sticky="e", padx=5)
    # Label contacto emergencia.

    entry_contacto_emergencia_perfil = Entry(frame_izquierdo, width=22,
                                              font=("Segoe UI", 12))
    # Entry contacto emergencia.

    entry_contacto_emergencia_perfil.grid(row=8, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Telefono del contacto de emergencia:",
          bg=GRIS_NIEBLA, fg=GRIS_AZULADO,
          font=("Segoe UI", 12)).grid(row=9, column=0, sticky="e", padx=5)
    # Label teléfono emergencia.

    entry_tel_emergencia_perfil = Entry(frame_izquierdo, width=22,
                                          font=("Segoe UI", 12))
    # Entry teléfono emergencia.

    entry_tel_emergencia_perfil.grid(row=9, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Obra social:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=10, column=0,
                                                       sticky="e", padx=5)
    # Label obra social.

    entry_obra_social_perfil = Entry(frame_izquierdo, width=22,
                                       font=("Segoe UI", 12))
    # Entry obra social.

    entry_obra_social_perfil.grid(row=10, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Estado:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=11, column=0,
                                                       sticky="e", padx=5)
    # Label estado.

    var_tipo_estado_perfil = tk.StringVar(value="")
    # Variable del menú.

    menu_estado_perfil = tk.OptionMenu(frame_izquierdo, var_tipo_estado_perfil,
                                        "Activo", "No activo")
    # Menú de estado.

    menu_estado_perfil.config(font=("Segoe UI", 12), width=22)
    # Fuente y ancho.

    menu_estado_perfil.grid(row=11, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Consentimiento:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=12, column=0,
                                                       sticky="e", padx=5)
    # Label consentimiento.

    var_tipo_consentimiento_perfil = tk.StringVar(value="")
    # Variable del menú.

    menu_consentimiento_perfil = tk.OptionMenu(frame_izquierdo,
                                                 var_tipo_consentimiento_perfil,
                                                 "Si", "No")
    # Menú Sí/No.

    menu_consentimiento_perfil.config(font=("Segoe UI", 12), width=22)

    menu_consentimiento_perfil.grid(row=12, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Fecha de egreso:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=13, column=0,
                                                       sticky="e", padx=5)
    # Label fecha egreso.

    entry_fecha_egreso_perfil = Entry(frame_izquierdo, width=22,
                                        font=("Segoe UI", 12))
    # Entry fecha egreso.

    entry_fecha_egreso_perfil.grid(row=13, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Tipo de egreso:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=14, column=0,
                                                       sticky="e", padx=5)
    # Label tipo egreso.

    var_tipo_egreso_perfil = tk.StringVar(value="")
    # Variable del menú.

    menu_tipo_egreso_perfil = tk.OptionMenu(frame_izquierdo,
                                              var_tipo_egreso_perfil,
                                              "Alta", "Derivación", "Voluntario",
                                              "Fallecimiento", "Otro", "-")
    # Menú de tipo de egreso.

    menu_tipo_egreso_perfil.config(font=("Segoe UI", 12), width=22)

    menu_tipo_egreso_perfil.grid(row=14, column=1, padx=5, pady=3)

    Label(frame_izquierdo, text="Motivo de egreso:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=15, column=0,
                                                       sticky="e", padx=5)
    # Label motivo egreso.

    entry_motivo_egreso_perfil = Entry(frame_izquierdo, width=22,
                                         font=("Segoe UI", 12))
    # Entry motivo egreso.

    entry_motivo_egreso_perfil.grid(row=15, column=1, padx=5, pady=3)

    def mostrar_foto_en_perfil():
        # Refresco galería y visor de foto.
        dni_txt = entry_dni_perfil.get().strip()
        if dni_txt:
            # Si hay DNI, refresco la lista de fotos del editor.
            cursor.execute("SELECT nombre FROM pdf WHERE dni_personas = ? ORDER BY id",
                            (dni_txt,))
            filas = cursor.fetchall()
            if lista_fotos_galeria.size() != len(filas):
                # Solo refresco si cambió la cantidad.
                lista_fotos_galeria.delete(0, tk.END)
                for (nombre,) in filas:
                    lista_fotos_galeria.insert(tk.END, nombre)

        if foto_pendiente["bytes"] == b"":
            # Foto marcada para borrar.
            visor_foto_perfil.configure(image="",
                                          text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return

        if foto_pendiente["bytes"] is not None:
            # Foto nueva pendiente: la muestro.
            try:
                img = Image.open(BytesIO(foto_pendiente["bytes"]))
                img.thumbnail((300, 300))
                foto_tk = ImageTk.PhotoImage(img)
                visor_foto_perfil.configure(image=foto_tk, text="")
                visor_foto_perfil.image = foto_tk
                return
            except Exception:
                pass

        # Sin foto pendiente: busco la guardada.
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            visor_foto_perfil.configure(image="",
                                          text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return

        cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni_txt,))
        fila = cursor.fetchone()
        if fila and fila[0]:
            try:
                img = Image.open(BytesIO(fila[0]))
                img.thumbnail((300, 300))
                foto = ImageTk.PhotoImage(img)
                visor_foto_perfil.configure(image=foto, text="")
                visor_foto_perfil.image = foto
                return
            except Exception:
                pass

        visor_foto_perfil.configure(image="",
                                      text="👤\nClic para subir foto")
        visor_foto_perfil.image = None

    def subir_foto_perfil(event=None):
        # Abro diálogo de archivos y guardo bytes.
        et = entry_dni_perfil_ref.get()
        # DNI actual.

        ruta = filedialog.askopenfilename(
            title="Seleccionar foto",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        # Diálogo.

        if not ruta:
            return

        try:
            with open(ruta, "rb") as f:
                foto_pendiente["bytes"] = f.read()
            mostrar_foto_en_perfil()
        except Exception:
            messagebox.showerror("Error", 'No se pudo cargar la foto')

        ete = str(et)
        # DNI como string (nombre de carpeta).

        os.makedirs(ete, exist_ok=True)
        # Creo la carpeta si no existe.

        shutil.move(ruta, ete)
        # Muevo el archivo a la carpeta (respaldo).

    def asignar_foto_galeria(event=None):
        # Al clickear una foto de la galería, la paso a pendiente.
        sel = lista_fotos_galeria.curselection()
        if not sel:
            return

        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            return

        cursor.execute("SELECT contenido FROM pdf WHERE dni_personas = ? ORDER BY id",
                        (dni_txt,))
        filas = cursor.fetchall()
        if sel[0] >= len(filas):
            return

        foto_pendiente["bytes"] = filas[sel[0]][0]
        mostrar_foto_en_perfil()

    def quitar_foto_perfil():
        # Marco la foto para borrar al guardar.
        foto_pendiente["bytes"] = b""
        mostrar_foto_en_perfil()

    def guardar_cambios_perfil():
        # Guardo todos los datos.
        nombre = entry_nombre_perfil.get().strip()
        apellido = entry_apellido_perfil.get().strip()
        dni_txt = entry_dni_perfil.get().strip()
        # Leo los tres campos obligatorios.

        if not (nombre and apellido and dni_txt):
            messagebox.showwarning("Faltan datos",
                                    "Completa nombre, apellido y DNI.")
            return

        try:
            dni = int(dni_txt)
        except ValueError:
            messagebox.showerror("Error", "El DNI debe ser numerico.")
            return

        edad_txt = entry_edad_perfil.get().strip()
        edad = int(edad_txt) if edad_txt.isdigit() else None
        # isdigit = True si todos son dígitos.

        direccion = entry_direccion_perfil.get().strip()
        # Domicilio.

        f_nacimiento = entry_f_nacimiento_perfil.get().strip()
        # Fecha nacimiento.

        f_ingreso = entry_f_ingreso_perfil.get().strip()
        # Fecha ingreso.

        telefono = entry_telefono_perfil.get().strip()
        # Teléfono.

        contacto_emergencia = entry_contacto_emergencia_perfil.get().strip()
        # Nombre contacto emergencia.

        tel_emergencia = entry_tel_emergencia_perfil.get().strip()
        # Teléfono emergencia.

        obra_social = entry_obra_social_perfil.get().strip()
        # Obra social.

        estado = var_tipo_estado_perfil.get()
        # Estado del menú.

        consentimiento = var_tipo_consentimiento_perfil.get()
        # Consentimiento.

        fecha_egreso = comprobar_fecha(entry_fecha_egreso_perfil)
        # Fecha egreso normalizada.

        tipo_egreso = var_tipo_egreso_perfil.get().strip()
        # Tipo de egreso.

        motivo_egreso = entry_motivo_egreso_perfil.get().strip()
        # Motivo egreso.

        if fecha_egreso and estado != "No activo":
            estado = "No activo"
            var_tipo_estado_perfil.set("No activo")
        # Si hay fecha de egreso, fuerzo estado "No activo".

        if tipo_egreso == "-" and estado != "Activo":
            estado = "Activo"
            var_tipo_estado_perfil.set("Activo")
        # Si el tipo es "-", fuerzo estado "Activo".

        if foto_pendiente["bytes"] == b"":
            # Foto marcada para borrar.
            foto_contenido = None
            borrar_foto = True
        elif foto_pendiente["bytes"] is not None:
            # Foto nueva.
            foto_contenido = sqlite3.Binary(foto_pendiente["bytes"])
            borrar_foto = False
        else:
            # Sin cambios en la foto.
            foto_contenido = None
            borrar_foto = False

        dni_cargado = dni_original["valor"]
        # DNI con el que abrí el perfil.

        if dni_cargado:
            # EDICIÓN.
            if str(dni) != str(dni_cargado):
                # Cambiaron el DNI.
                cursor.execute("SELECT id FROM personas WHERE dni = ?", (dni,))
                if cursor.fetchone():
                    messagebox.showerror("Error",
                                          "Ya existe otra persona con ese DNI.")
                    return

                cursor.execute("UPDATE entrevistas SET dni_paciente = ? WHERE dni_paciente = ?",
                                (dni, dni_cargado))
                # Arrastro las entrevistas.

                cursor.execute("UPDATE pdf SET dni_personas = ? WHERE dni_personas = ?",
                                (dni, dni_cargado))
                # Arrastro los PDFs.

                cursor.execute("""UPDATE personas SET nombre = ?, apellido = ?,
                                edad = ?, direccion = ?, fecha_nacimiento = ?,
                                fecha_ingreso = ?, telefono = ?,
                                contacto_emergencia = ?, telefono_emergencia = ?,
                                obra_social = ?, estado = ?, consentimiento = ?,
                                fecha_egreso = ?, tipo_egreso = ?, motivo_egreso = ?
                                WHERE dni = ?""",
                                (nombre, apellido, edad, direccion, f_nacimiento,
                                 f_ingreso, telefono, contacto_emergencia,
                                 tel_emergencia, obra_social, estado,
                                 consentimiento, fecha_egreso, tipo_egreso,
                                 motivo_egreso, dni))
                # Actualizo el registro con el DNI nuevo.

                dni_original["valor"] = str(dni)
                # Actualizo el DNI recordado.

                entry_dni_perfil.delete(0, tk.END)
                entry_dni_perfil.insert(0, dni)
                # Actualizo el Entry.

                if borrar_foto:
                    cursor.execute("UPDATE personas SET foto = NULL WHERE dni = ?",
                                    (dni,))
                elif foto_contenido is not None:
                    cursor.execute("UPDATE personas SET foto = ? WHERE dni = ?",
                                    (foto_contenido, dni))
                # Foto contra DNI nuevo.

            else:
                # Mismo DNI: solo actualizo campos.
                cursor.execute("""UPDATE personas SET dni = ?, nombre = ?,
                                apellido = ?, edad = ?, direccion = ?,
                                fecha_nacimiento = ?, fecha_ingreso = ?,
                                telefono = ?, contacto_emergencia = ?,
                                telefono_emergencia = ?, obra_social = ?,
                                estado = ?, consentimiento = ?, fecha_egreso = ?,
                                tipo_egreso = ?, motivo_egreso = ?
                                WHERE dni = ?""",
                                (dni, nombre, apellido, edad, direccion,
                                 f_nacimiento, f_ingreso, telefono,
                                 contacto_emergencia, tel_emergencia,
                                 obra_social, estado, consentimiento,
                                 fecha_egreso, tipo_egreso, motivo_egreso,
                                 dni_cargado))

                if borrar_foto:
                    cursor.execute("UPDATE personas SET foto = NULL WHERE dni = ?",
                                    (dni,))
                elif foto_contenido is not None:
                    cursor.execute("UPDATE personas SET foto = ? WHERE dni = ?",
                                    (foto_contenido, dni))

        else:
            # ALTA nueva.
            try:
                cursor.execute("""INSERT INTO personas(nombre, apellido, dni,
                                edad, direccion, fecha_nacimiento, fecha_ingreso,
                                telefono, contacto_emergencia, telefono_emergencia,
                                obra_social, estado, consentimiento, fecha_egreso,
                                tipo_egreso, motivo_egreso, foto)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (nombre, apellido, dni, edad, direccion,
                                 f_nacimiento, f_ingreso, telefono,
                                 contacto_emergencia, tel_emergencia,
                                 obra_social, estado, consentimiento,
                                 fecha_egreso, tipo_egreso, motivo_egreso,
                                 foto_contenido))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error",
                                      "Ya existe una persona con ese DNI.")
                return

            dni_original["valor"] = str(dni)
            # Guardo el DNI.

        conexion.commit()
        # Confirmo.

        refrescar_lista()
        # Refresco la lista principal.

        foto_pendiente["bytes"] = None
        # Reseteo el pendiente.

        messagebox.showinfo("OK", "Datos guardados.")

    def cargar_perfil():
        # Cargo datos del paciente en el formulario.
        dni_txt = entry_dni.get().strip()
        lista_personas_perfil.delete(0, tk.END)
        # Limpio la lista de entrevistas.

        foto_pendiente["bytes"] = None
        # Reseteo pendiente.

        cursor.execute("""SELECT nombre, apellido, edad, direccion,
                        fecha_nacimiento, fecha_ingreso, telefono,
                        contacto_emergencia, telefono_emergencia, obra_social,
                        estado, consentimiento, fecha_egreso, tipo_egreso,
                        motivo_egreso FROM personas WHERE dni = ?""", (dni_txt,))
        # Traigo todos los datos.

        fila = cursor.fetchone()

        if fila:
            entry_nombre_perfil.delete(0, tk.END)
            entry_nombre_perfil.insert(0, fila[0])
            # Nombre.

            entry_apellido_perfil.delete(0, tk.END)
            entry_apellido_perfil.insert(0, fila[1])
            # Apellido.

            entry_edad_perfil.delete(0, tk.END)
            entry_edad_perfil.insert(0, fila[2] or "")
            # Edad.

            entry_direccion_perfil.delete(0, tk.END)
            entry_direccion_perfil.insert(0, fila[3] or "")
            # Dirección.

            entry_f_nacimiento_perfil.delete(0, tk.END)
            entry_f_nacimiento_perfil.insert(0, fila[4] or "")
            # Fecha nacimiento.

            entry_f_ingreso_perfil.delete(0, tk.END)
            entry_f_ingreso_perfil.insert(0, fila[5] or "")
            # Fecha ingreso.

            entry_telefono_perfil.delete(0, tk.END)
            entry_telefono_perfil.insert(0, fila[6] or "")
            # Teléfono.

            entry_contacto_emergencia_perfil.delete(0, tk.END)
            entry_contacto_emergencia_perfil.insert(0, fila[7] or "")
            # Contacto emergencia.

            entry_tel_emergencia_perfil.delete(0, tk.END)
            entry_tel_emergencia_perfil.insert(0, fila[8] or "")
            # Teléfono emergencia.

            entry_obra_social_perfil.delete(0, tk.END)
            entry_obra_social_perfil.insert(0, fila[9] or "")
            # Obra social.

            var_tipo_estado_perfil.set(fila[10] or "")
            # Estado.

            var_tipo_consentimiento_perfil.set(fila[11] or "")
            # Consentimiento.

            entry_fecha_egreso_perfil.delete(0, tk.END)
            entry_fecha_egreso_perfil.insert(0, fila[12] or "")
            # Fecha egreso.

            var_tipo_egreso_perfil.set(fila[13] or "")
            # Tipo egreso.

            entry_motivo_egreso_perfil.delete(0, tk.END)
            entry_motivo_egreso_perfil.insert(0, fila[14] or "")
            # Motivo egreso.

            dni_original["valor"] = dni_txt
            # Actualizo el DNI recordado.

            mostrar_foto_en_perfil()
            # Muestro la foto.

            cursor.execute("""SELECT id, fecha_entrevista, nombre_profecional,
                            apellido_profecional FROM entrevistas
                            WHERE dni_paciente = ? ORDER BY fecha_entrevista""",
                            (dni_txt,))
            # Traigo entrevistas.

            for e in cursor.fetchall():
                lista_personas_perfil.insert(tk.END,
                    f"ID {e[0]} — {e[1]} — {e[2]} {e[3] or ''}")
                # Las inserto.

        else:
            messagebox.showinfo("Error", "No existe ese DNI.")

    def _texto_ficha_paciente():
        # Armo el texto de la ficha del paciente (no entrevistas).
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            messagebox.showwarning("Atencion", "Escribi un DNI primero.")
            return None

        cursor.execute("""SELECT nombre, apellido, dni, edad, fecha_nacimiento,
                        fecha_ingreso, telefono, direccion, contacto_emergencia,
                        telefono_emergencia, obra_social, estado, consentimiento,
                        fecha_egreso, tipo_egreso, motivo_egreso
                        FROM personas WHERE dni = ?""", (dni_txt,))
        p = cursor.fetchone()
        if not p:
            messagebox.showinfo("Sin resultados", "No existe ese DNI.")
            return None

        lineas = [
            "Casa de Jovenes Levantate y Camina. Parroquia San Juan Bautista. Obispado de San Isidro",
            "Ficha de perfil del paciente",
            "",
            f"Nombre: {p[0] or '-'}",
            f"Apellido: {p[1] or '-'}",
            f"DNI: {p[2] or '-'}",
            f"Edad: {p[3] or '-'}",
            f"Fecha de nacimiento: {p[4] or '-'}",
            f"Fecha de ingreso: {p[5] or '-'}",
            f"Telefono: {p[6] or '-'}",
            f"Domicilio: {p[7] or '-'}",
            f"Contacto de emergencia: {p[8] or '-'}",
            f"Telefono de emergencia: {p[9] or '-'}",
            f"Obra social: {p[10] or '-'}",
            f"Estado: {p[11] or '-'}",
            f"Consentimiento: {p[12] or '-'}",
            f"Fecha de egreso: {p[13] or '-'}",
            f"Tipo de egreso: {p[14] or '-'}",
            f"Motivo de egreso: {p[15] or '-'}",
        ]
        return "\n".join(lineas)

    def exportar_pdf_paciente():
        texto = _texto_ficha_paciente()
        if texto is None:
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar perfil como PDF",
            defaultextension=".pdf",
            initialfile=f"perfil_{entry_dni_perfil.get().strip()}.pdf",
            filetypes=[("PDF", "*.pdf")])
        if not ruta:
            return
        try:
            crear_pdf_de_texto(ruta, texto)
            messagebox.showinfo("OK", f"Perfil guardado en:\n{ruta}")
        except Exception:
            messagebox.showerror("Error", "No se pudo crear el PDF.")

    def exportar_word_paciente():
        texto = _texto_ficha_paciente()
        if texto is None:
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar perfil como Word",
            defaultextension=".doc",
            initialfile=f"perfil_{entry_dni_perfil.get().strip()}.doc",
            filetypes=[("Word", "*.doc")])
        if not ruta:
            return
        try:
            crear_word_de_texto(ruta, texto)
            messagebox.showinfo("OK", f"Perfil guardado en:\n{ruta}")
        except Exception:
            messagebox.showerror("Error", "No se pudo crear el Word.")

    boton_guardar_perfil = RoundedButton(frame_izquierdo, 160, 40, 20,VERDE_AZULADO, BLANCO,text="Guardar cambios",command=guardar_cambios_perfil)
    # Botón Guardar.

    boton_guardar_perfil.grid(row=16, column=0, padx=10, pady=5, sticky="ew")

    boton_editor_fotos = RoundedButton(frame_izquierdo, 120, 40, 20,VERDE_AZULADO, BLANCO,text="Editar fotos",command=abrir_ventana_editor_fotos)

    # Botón Editor de fotos.

    boton_editor_fotos.grid(row=16, column=1, padx=10, sticky="ew")

    boton_entrevistas = RoundedButton(frame_izquierdo, 100, 40, 20,VERDE_AZULADO, BLANCO, text="Entrevista",command=abrir_desde_principal)
    # Botón Entrevista.

    boton_entrevistas.grid(row=16, column=3, padx=10, sticky="ew")

    boton_pdf_paciente = RoundedButton(frame_izquierdo, 200, 40, 20,VERDE_AZULADO, BLANCO,text="PDF de este paciente",command=exportar_pdf_paciente)
    # Botón PDF paciente.

    boton_pdf_paciente.grid(row=17, column=0, padx=10, sticky="ew")

    boton_word_paciente = RoundedButton(frame_izquierdo, 210, 40, 20,VERDE_AZULADO, BLANCO,text="Word de este paciente",command=exportar_word_paciente)
    # Botón Word paciente.

    boton_word_paciente.grid(row=17, column=1, padx=10, sticky="ew")

    boton_ver_doc = RoundedButton(frame_izquierdo, 210, 40, 20,VERDE_AZULADO, BLANCO,text="Ver/Editar documento",command=lambda: abrir_ventana_ver_documento(entry_dni_perfil.get().strip()))
    # Botón Ver/Editar documento. Uso lambda para pasar el DNI actual
    # al hacer clic (no al crear).

    boton_ver_doc.grid(row=17, column=2, columnspan=2, padx=10, pady=5,
                        sticky="ew")

    boton_word_legajo = RoundedButton(
        frame_izquierdo, 230, 40, 20, VERDE_AZULADO, BLANCO,
        text="Legajo en formato Word",
        command=lambda: exportar_entrevistas_word(entry_dni_perfil.get().strip() or None))
    boton_word_legajo.grid(row=18, column=1, padx=10, pady=5, sticky="ew")

    boton_pdf_legajo = RoundedButton(
        frame_izquierdo, 230, 40, 20, VERDE_AZULADO, BLANCO,
        text="Legajo en formato PDF",
        command=lambda: exportar_entrevistas_pdf(entry_dni_perfil.get().strip() or None))
    boton_pdf_legajo.grid(row=18, column=0, padx=10, pady=5, sticky="ew")

    frame_derecha = tk.Frame(ventana_perfil, bg=GRIS_NIEBLA)
    # Frame derecho.

    frame_derecha.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)
    # A la derecha.

    frame_foto_perfil = Frame(frame_derecha, bg=BLANCO, relief="solid",bd=1, height=280)
    # Frame de la foto grande.

    frame_foto_perfil.pack(side="top", fill="x", pady=(0, 10))

    frame_foto_perfil.pack_propagate(False)
    # Respeto el alto.

    visor_foto_perfil = tk.Label(frame_foto_perfil,text="👤\nClic para subir foto",bg=BLANCO, fg=GRIS_MEDIO,font=("Segoe UI", 20), cursor="hand2")
    # Label con manito.

    visor_foto_perfil.pack(fill="both", expand=True, padx=10, pady=10)

    visor_foto_perfil.bind("<Button-1>", subir_foto_perfil)
    # Al hacer clic, abro el diálogo.

    boton_quitar_foto = RoundedButton(frame_derecha, 100, 40, 20,VERDE_AZULADO, BLANCO,text="Quitar foto",command=quitar_foto_perfil)
    # Botón Quitar foto.

    boton_quitar_foto.pack(side="top", padx=10, pady=5)

    frame_galeria = Frame(frame_derecha, bg=GRIS_NIEBLA)
    # Frame de la galería.

    frame_galeria.pack(side="top", fill="x", pady=(0, 10))

    Label(frame_galeria, text="Fotos del editor:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO,
          font=("Segoe UI", 10, "bold")).pack(anchor="w")
    # Título de la galería.

    frame_galeria_inner = Frame(frame_galeria, bg=GRIS_NIEBLA, height=120)
    # Frame interno con altura fija.

    frame_galeria_inner.pack(fill="x")

    frame_galeria_inner.pack_propagate(False)

    scroll_galeria = tk.Scrollbar(frame_galeria_inner, orient="vertical")
    # Scroll vertical.

    scroll_galeria.pack(side="right", fill="y")

    lista_fotos_galeria = tk.Listbox(frame_galeria_inner,
                                       font=("Segoe UI", 10),
                                       yscrollcommand=scroll_galeria.set,
                                       selectbackground=AZUL_SERENO,
                                       selectforeground=BLANCO)
    # Lista de fotos.

    lista_fotos_galeria.pack(side="left", fill="both", expand=True)

    scroll_galeria.config(command=lista_fotos_galeria.yview)

    lista_fotos_galeria.bind("<<ListboxSelect>>", asignar_foto_galeria)
    # Al seleccionar una foto, la paso a pendiente.

    frame_lista_perfil = Frame(frame_derecha, bg=GRIS_AZULADO,
                                 relief="solid", bd=1)
    # Frame de la lista de entrevistas.

    frame_lista_perfil.pack(side="top", fill="both", expand=True, pady=(0, 20))

    Label(frame_lista_perfil, text="Entrevistas del paciente",
          bg=GRIS_AZULADO, fg=BLANCO,
          font=("Segoe UI", 15, "bold")).pack(side="top", padx=10, pady=10)
    # Título.

    scroll_perfil = tk.Scrollbar(frame_lista_perfil, orient="vertical")
    # Scroll.

    scroll_perfil.pack(side="right", fill="y")

    lista_personas_perfil = Listbox(frame_lista_perfil,
                                      yscrollcommand=scroll_perfil.set,
                                      font=("Segoe UI", 12),
                                      bg=BLANCO, fg=GRIS_AZULADO,
                                      selectbackground=AZUL_SERENO,
                                      selectforeground=BLANCO)
    # Lista.

    lista_personas_perfil.pack(side="left", fill="both", expand=True)

    scroll_perfil.config(command=lista_personas_perfil.yview)

    mostrar_foto_en_perfil()
    # Muestro la foto.

    agregar_boton_luna(ventana_perfil)
    # Aplico el tema.

    cargar_perfil()
    # Cargo los datos del paciente.

# ============================================================================
# BLOQUE 19: EDITOR DE FOTOS
# ============================================================================

def abrir_ventana_editor_fotos():
    ventana_editor_fotos = tk.Toplevel(ventana)
    # Toplevel del editor.

    ventana_editor_fotos.title("Editor de fotos")
    ventana_editor_fotos.geometry("600x750")
    ventana_editor_fotos.config(bg=GRIS_NIEBLA)

    try:
        dni_actual = entry_dni_perfil_ref.get().strip() if entry_dni_perfil_ref is not None else ""
        # Intento leer el DNI del perfil.
    except tk.TclError:
        # TclError si el Entry fue destruido (cerré el perfil).
        dni_actual = ""

    frame_editor_fotos_superior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    # Frame superior.

    frame_editor_fotos_superior.pack(side="top", fill="both", expand=True)

    visor_foto_editor = Label(frame_editor_fotos_superior,
                                text="👤\nSin foto",
                                bg=BLANCO, fg=NEGRO, relief="solid", bd=1,
                                font=("Segoe UI", 20))
    # Visor.

    visor_foto_editor.pack(fill="both", expand=True, padx=10, pady=10)

    frame_lista_imgs = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    # Frame de la lista.

    frame_lista_imgs.pack(fill="x", padx=10, pady=5)

    label_contador = Label(frame_lista_imgs, text="Imagenes cargadas: 0",
                             font=("Segoe UI", 11, "bold"),
                             bg=VERDE_AZULADO, fg=BLANCO)
    # Contador.

    label_contador.pack(fill="x")

    frame_lista_scroll = Frame(frame_lista_imgs, bg=GRIS_NIEBLA)
    # Frame con scroll.

    frame_lista_scroll.pack(fill="x", pady=5)

    scroll_imgs = tk.Scrollbar(frame_lista_scroll, orient="vertical")
    # Scroll.

    scroll_imgs.pack(side="right", fill="y")

    lista_imagenes = Listbox(frame_lista_scroll, height=8,
                               font=("Segoe UI", 10),
                               yscrollcommand=scroll_imgs.set)
    # Lista de imágenes.

    lista_imagenes.pack(side="left", fill="both", expand=True)

    scroll_imgs.config(command=lista_imagenes.yview)

    frame_editor_fotos_inferior = Frame(ventana_editor_fotos, bg=GRIS_NIEBLA)
    # Frame inferior para botones.

    frame_editor_fotos_inferior.pack(side="bottom", fill="x", pady=10)

    ids_imagenes = []
    # IDs de las filas pdf para saber cuál borrar.

    def refrescar_lista_imagenes():
        # Recargo la lista de imágenes.
        lista_imagenes.delete(0, tk.END)
        ids_imagenes.clear()

        if not dni_actual:
            label_contador.config(text="Imagenes cargadas: 0")
            return

        cursor.execute("SELECT id, nombre FROM pdf WHERE dni_personas = ? ORDER BY id",
                        (dni_actual,))
        filas = cursor.fetchall()

        for id_img, nombre in filas:
            lista_imagenes.insert(tk.END, nombre)
            ids_imagenes.append(id_img)
            # Guardo el id para después borrar.

        label_contador.config(text=f"Imagenes cargadas: {len(filas)}")

    def mostrar_previa_desde_db(index):
        # Muestro la imagen en la posición "index".
        if not (0 <= index < len(ids_imagenes)):
            return

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
        # Al seleccionar de la lista, muestro previa.
        sel = lista_imagenes.curselection()
        if not sel:
            return
        mostrar_previa_desde_db(sel[0])

    lista_imagenes.bind("<<ListboxSelect>>", mostrar_previa_seleccionada)

    def agregar_imagen():
        # Agrego una imagen a la base.
        et = entry_dni_perfil_ref.get()
        # DNI actual.
        if not dni_actual:
            messagebox.showwarning("Atencion","Primero carga un DNI en el perfil para asociar las fotos.")
            return

        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        # Diálogo.

        if not ruta:
            return

        try:
            with open(ruta, "rb") as archivo:
                contenido = archivo.read()
                # Bytes de la imagen.

            nombre = os.path.basename(ruta)
            # Nombre sin carpeta.

            formato = os.path.splitext(nombre)[1].lstrip(".").lower() or "img"
            # Extensión sin punto, en minúsculas. Si no hay, "img".

            cursor.execute("""INSERT INTO pdf (nombre, formato, contenido, dni_personas)
                            VALUES (?, ?, ?, ?)""",
                            (nombre, formato, sqlite3.Binary(contenido), dni_actual))
            # Inserto la fila.

            conexion.commit()

            refrescar_lista_imagenes()
            # Refresco la lista.

            lista_imagenes.selection_clear(0, tk.END)
            lista_imagenes.selection_set(tk.END)
            # Selecciono la recién agregada.

            mostrar_previa_desde_db(len(ids_imagenes) - 1)
            # La muestro.

        except Exception:
            messagebox.showerror('Error')

        ete = str(dni_actual)
        # DNI como carpeta.

        os.makedirs(ete, exist_ok=True)
        # Creo la carpeta.

        shutil.move(ruta, ete)
        # Muevo el archivo a la carpeta.

    def eliminar_imagen():
        # Elimino la imagen seleccionada.
        sel = lista_imagenes.curselection()
        if not sel:
            messagebox.showwarning("Atencion",
                                    "Selecciona una foto de la lista.")
            return

        id_img = ids_imagenes[sel[0]]
        # ID de la fila.

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta foto?"):
            return

        cursor.execute("DELETE FROM pdf WHERE id = ?", (id_img,))
        conexion.commit()

        visor_foto_editor.config(image="", text="👤\nSin foto")
        visor_foto_editor.image = None
        # Reseteo el visor.

        refrescar_lista_imagenes()

    def limpiar_todas():
        # Borro todas las fotos del DNI actual.
        if not dni_actual:
            messagebox.showwarning("Atencion", "No hay DNI cargado.")
            return

        if not messagebox.askyesno("Confirmar",
                                    f"¿Borrar TODAS las fotos del DNI {dni_actual}?"):
            return

        cursor.execute("DELETE FROM pdf WHERE dni_personas = ?", (dni_actual,))
        conexion.commit()

        visor_foto_editor.config(image="", text="👤\nSin foto")
        visor_foto_editor.image = None

        refrescar_lista_imagenes()

    frame_editor_fotos_inferior.columnconfigure(0, weight=1)
    frame_editor_fotos_inferior.columnconfigure(5, weight=1)
    # Columnas fantasma para centrar.

    RoundedButton(frame_editor_fotos_inferior, 250, 40, 20, VERDE_AZULADO,
                   BLANCO, text="Agregar imagen",
                   command=agregar_imagen).grid(row=0, column=2, padx=10,
                                                  sticky="ew")
    # Botón Agregar.

    RoundedButton(frame_editor_fotos_inferior, 250, 40, 20, VERDE_AZULADO,
                   BLANCO, text="Eliminar imagen",
                   command=eliminar_imagen).grid(row=0, column=3, padx=10,
                                                   sticky="ew")
    # Botón Eliminar.

    RoundedButton(frame_editor_fotos_inferior, 250, 40, 20, VERDE_AZULADO,
                   BLANCO, text="Limpiar TODAS",
                   command=limpiar_todas).grid(row=0, column=4, padx=10,
                                                  sticky="ew")
    # Botón Limpiar.

    agregar_boton_luna(ventana_editor_fotos)
    # Aplico tema.

    refrescar_lista_imagenes()
    # Cargo la lista inicial.

# ============================================================================
# BLOQUE 20: IMAGEN DE SANCA
# ============================================================================

def cargar_imagen():
    # Guardo la imagen SANCA en la tabla recursos si no existe.
    if not SANCA_BASE64:
        return False

    cursor.execute("SELECT 1 FROM recursos WHERE nombre=?", ("sanca",))
    if cursor.fetchall():
        return True
        # Ya existe.

    try:
        imagen_bytes = base64.b64decode(SANCA_BASE64)
        # Decodifico.

        cursor.execute('INSERT INTO recursos (nombre,contenido) VALUES(?,?)',
                        ("sanca", sqlite3.Binary(imagen_bytes)))
        # Inserto.

        conexion.commit()
        return True
    except Exception:
        print('Error al cargar la imagen invisible:')
        return False

def obtener_bytes_sanca():
    # Devuelvo los bytes de SANCA.
    if not SANCA_BASE64:
        return None

    cursor.execute("SELECT contenido FROM recursos WHERE nombre = ?",
                    ("sanca",))
    fila = cursor.fetchone()

    if not fila or not fila[0]:
        return None

    return fila[0]

# ============================================================================
# BLOQUE 21: AUTORES
# ============================================================================

def abrir_ventana_autores():
    cargar_imagen()
    # Aseguro que SANCA esté en la base.

    ventana_autores = tk.Toplevel(ventana)
    ventana_autores.title("Licencia y autores")
    ventana_autores.geometry("1000x650")
    ventana_autores.config(bg=AZUL_PETROLEO)

    frame_textos = Frame(ventana_autores, bg=AZUL_PETROLEO, width=450)
    # Frame de textos (izquierda).

    frame_textos.pack(side="left", fill="y", padx=(60, 0)) 

    frame_textos.pack_propagate(False)
    # Respeto el ancho fijo.

    Label(frame_textos, text="AUTORES", bg=AZUL_PETROLEO, fg=BLANCO,
          font=("Segoe UI", 32, "bold")).pack(pady=(40, 5))
    # Título.

    Label(frame_textos, text="EQUIPO DE DESARROLLO", bg=AZUL_PETROLEO,fg=AMARILLO,
          font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))
    # Subtítulo.

    nombres = ["Antonio Garcia", "Nahuel Villafañe", "Mateo Dabruzzo Wilczek",
               "Federico 'Fedelobo'", "Ignacio", "Thiago",
               "Pablo Laporta", "Fernando 'Master' Yapuray", "Joaquin Arana"]
    # Lista de nombres.

    for nombre in nombres:
        # Recorro y creo un Label por nombre.
        Label(frame_textos, text=nombre, bg=AZUL_PETROLEO, fg=BLANCO,
              font=("Segoe UI", 12)).pack(pady=2)

    Label(frame_textos,
          text="___________________________________________",
          bg=AZUL_PETROLEO, fg=GRIS_MEDIO).pack(pady=15)
    # Línea separadora.

    Label(frame_textos, text="LICENCIA", bg=AZUL_PETROLEO, fg=BLANCO,
          font=("Segoe UI", 18, "bold")).pack(pady=5)
    # Título licencia.

    texto_legal = ("© 2026 Equipo de programación Sanca.\n"
                   "Todos los derechos reservados.\n\n"
                   "Prohibida la copia, modificación, distribución\n"
                   "y uso comercial del software sin\n"
                   "autorización escrita del titular.\n\n"
                   "Ley 11.723 de Propiedad Intelectual.")
    # Texto legal.

    Label(frame_textos, text=texto_legal, bg=AZUL_PETROLEO,
          fg=GRIS_NIEBLA, font=("Segoe UI", 12),
          justify="center").pack()
    # Lo muestro centrado.

    frame_foto = Frame(ventana_autores, bg=BLANCO)
    # Frame de la foto (derecha).

    frame_foto.pack(side="right", fill="both", expand=True, padx=(20, 40))

    bytes_sanca = obtener_bytes_sanca()
    # Bytes de SANCA.

    if bytes_sanca:
        img = Image.open(BytesIO(bytes_sanca))
        img.thumbnail((550, 550))
        foto_tk = ImageTk.PhotoImage(img)
        # Preparo la imagen.

        label_foto = Label(frame_foto, image=foto_tk, bg=BLANCO)
        label_foto.image = foto_tk
        # Referencia para el GC.
        label_foto.pack(expand=True)
        # La muestro centrada.

    else:
        Label(frame_foto, text="No se encontró la imagen",
              bg=BLANCO, fg=NEGRO).pack(expand=True)

    boton_cerrar = RoundedButton(ventana_autores, 40, 30, 15, ROJO,
                                   BLANCO, text="X",
                                   command=ventana_autores.destroy)
    # Botón cerrar (X).

    boton_cerrar.place(relx=1.0, rely=0.0, anchor="ne", x=-15, y=15)
    # Lo ubico en la esquina superior derecha con margen.

    agregar_boton_luna(ventana_autores)

# ============================================================================
# BLOQUE 22: BOTONES DE APERTURA
# ============================================================================

def abrir_desde_principal():
    # Abro la ventana de entrevistas desde la principal.
    abrir_ventana_entrevistas(ventana)

btn_info = RoundedButton(frame_btn_info, 50, 40, 20, VERDE_AZULADO, BLANCO,
                           text="Info", command=abrir_ventana_autores)
# Botón Info.

btn_info.pack(side="left", padx=5, pady=5)
# A la izquierda.

refrescar_lista()
# Cargo la lista al arrancar.

# ============================================================================
# BLOQUE 23: DOBLE CLIC PARA PERFIL
# ============================================================================

def abrir_perfil_doble_clic(event=None):
    # Abro perfil con doble click en la lista.
    if not lista_personas.curselection():
        return
    al_seleccionar()
    # Cargo datos en el formulario principal.
    abrir_ventana_perfil()
    # Abro la ventana de perfil.

lista_personas.bind("<Double-Button-1>", abrir_perfil_doble_clic)
# Evento doble click.

lista_personas.bind("<<ListboxSelect>>", al_seleccionar)
# Evento selección simple.

# ============================================================================
# BLOQUE 24: GENERAR PDF
# ============================================================================

def crear_pdf_entrevistas(ruta, entrevistas):
    # Armo un PDF byte a byte con las entrevistas.
    paginas = []
    # Lista de páginas terminadas.

    lineas_pagina = []
    # Líneas de la página actual.

    rectangulos_pagina = []
    # Rectángulos de la página actual (por ahora no uso).

    y = 0
    # Coordenada Y actual (arranca en 0, se setea al empezar página).

    def nueva_pagina():
        # Empiezo una página nueva.
        nonlocal lineas_pagina, rectangulos_pagina, y
        # Para modificar las del scope superior.

        if lineas_pagina:
            paginas.append((lineas_pagina, rectangulos_pagina))
            # Guardo la página anterior si tiene contenido.

        lineas_pagina = []
        rectangulos_pagina = []
        # Reseteo.

        y = 790
        # Empiezo arriba.

        lineas_pagina.append(("Casa de Jovenes Levantate y Camina. Parroquia San Juan Bautista. Obispado de San Isidro | Archivos de perfil", "F2", 16, 50, y))
        # Header (negrita, tamaño 16).

        y -= 25
        lineas_pagina.append(("Historial completo de entrevistas", "F1", 10, 50, y))
        # Subtítulo (normal, tamaño 10).

        y -= 30
        # Bajo el cursor.

    def agregar_linea(texto, negrita=False, tamano=10, sangria=0):
        # Agrego una línea. Salto de página si no entra.
        nonlocal y

        if y < 55:
            nueva_pagina()

        fuente = "F2" if negrita else "F1"
        # F2 = negrita, F1 = normal.

        lineas_pagina.append((texto, fuente, tamano, 50 + sangria, y))
        # Guardo la línea.

        y -= tamano + 5
        # Bajo el cursor.

    nueva_pagina()
    # Arranco la primera página.

    for datos in entrevistas:
        # Recorro cada entrevista.
        (nombre_paciente, apellido_paciente, id_entrevista,
         fecha_nacimiento_paciente, fecha_ingreso, telefono_paciente,
         direccion_paciente, nombre_contacto_emergencia,
         telefono_emergencia, nombre_obra_social, estado_paciente,
         consentimiento, nombre_profecional, apellido_profecional,
         dni_profesional, matricula, especialidad, telefono_profecional,
         email_profecional, activo_profecional, entrevista, Dni_paciente,
         fecha_entrevista, hora_entrevista, tipo_entrevista,
         proxima_sesion) = datos
        # Desempaqueto todos los campos.

        agregar_linea(f"Entrevista {id_entrevista}", negrita=True, tamano=12)
        # Título.

        agregar_linea(f"Fecha: {fecha_entrevista}  Hora: {hora_entrevista or '-'}  DNI del paciente: {Dni_paciente}")
        # Datos básicos.

        paciente = " ".join(parte for parte in (nombre_paciente, apellido_paciente) if parte) or "No registrado"
        # Nombre completo o "No registrado".

        agregar_linea(f"Paciente: {paciente}")

        agregar_linea("--- Datos del profesional ---", negrita=True)
        agregar_linea(f"Nombre: {nombre_profecional or '-'}")
        agregar_linea(f"Apellido: {apellido_profecional or '-'}")
        agregar_linea(f"DNI: {dni_profesional or '-'}")
        agregar_linea(f"Matricula: {matricula or '-'}")
        agregar_linea(f"Especialidad: {especialidad or '-'}")
        agregar_linea(f"Telefono: {telefono_profecional or '-'}")
        agregar_linea(f"Email: {email_profecional or '-'}")
        agregar_linea(f"Estado: {activo_profecional or '-'}")
        agregar_linea(f"Tipo de entrevista: {tipo_entrevista or '-'}")
        agregar_linea(f"Proxima sesion: {proxima_sesion or '-'}")

        agregar_linea("--- Datos del paciente ---", negrita=True)
        agregar_linea(f"Fecha de nacimiento: {fecha_nacimiento_paciente or '-'}")
        agregar_linea(f"Fecha de ingreso al instituto: {fecha_ingreso or '-'}")
        agregar_linea(f"Telefono: {telefono_paciente or '-'}")
        agregar_linea(f"Domicilio: {direccion_paciente or '-'}")
        agregar_linea(f"Contacto de emergencia: {nombre_contacto_emergencia or '-'}")
        agregar_linea(f"Telefono de emergencia: {telefono_emergencia or '-'}")
        agregar_linea(f"Obra social: {nombre_obra_social or '-'}")
        agregar_linea(f"Estado del paciente: {estado_paciente or '-'}")
        agregar_linea(f"Consentimiento: {consentimiento or '-'}")

        agregar_linea("--- Anotaciones ---", negrita=True)
        parrafos = (entrevista or "").splitlines() or ["Sin anotaciones"]
        # Divido el texto en párrafos.

        for parrafo in parrafos:
            lineas = textwrap.wrap(parrafo, width=88,
                                    break_long_words=True,
                                    break_on_hyphens=False) or [""]
            # textwrap.wrap corta en líneas de 88 chars.

            for linea in lineas:
                agregar_linea(linea, sangria=12)
                # Cada línea con sangría.

        agregar_linea("")
        # Línea vacía entre entrevistas.

    if lineas_pagina:
        paginas.append((lineas_pagina, rectangulos_pagina))
        # Guardo la última página.

    objetos = [None, None]
    # Lista de objetos PDF (empiezo con 2 Nones).

    referencias_paginas = []
    # Referencias a las páginas.

    id_fuente_regular = 3 + 2 * len(paginas)
    # Calculo los IDs de fuentes (después de las páginas).

    id_fuente_negrita = id_fuente_regular + 1

    for numero, (lineas, rectangulos) in enumerate(paginas, start=1):
        # Recorro las páginas.
        lineas.append((f"Pagina {numero} de {len(paginas)}", "F1", 9, 490, 35))
        # Número de página.

        contenido_texto = "".join(
            f"BT /{fuente} {tamano} Tf 1 0 0 1 {x} {pos_y} Tm "
            f"<{texto.encode('cp1252', errors='replace').hex().upper()}> Tj ET\n"
            for texto, fuente, tamano, x, pos_y in lineas
        )
        # Para cada línea armo el comando PDF.
        # BT/ET = bloque de texto.
        # Tf = set font. Tm = posición. Tj = mostrar texto.
        # hex() = convertir a hexadecimal ASCII.

        contenido_rect = ""
        for x, y_rect, w_rect, h_rect in rectangulos:
            contenido_rect += f"0.8 0.8 0.8 RG {x} {y_rect} {w_rect} {h_rect} re S\n"
            # Dibuja rectángulos si hay.

        contenido = (contenido_texto + contenido_rect).encode("ascii")
        # A bytes.

        id_pagina = len(objetos) + 1
        id_contenido = id_pagina + 1
        referencias_paginas.append(f"{id_pagina} 0 R")

        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {id_fuente_regular} 0 R "
            f"/F2 {id_fuente_negrita} 0 R >> >> /Contents {id_contenido} 0 R >>".encode("ascii"))
        # Objeto Page.

        objetos.append(f"<< /Length {len(contenido)} >>\nstream\n".encode("ascii") + contenido + b"\nendstream")
        # Objeto de contenido (stream).

    objetos[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    # Catálogo.

    objetos[1] = f"<< /Type /Pages /Kids [{' '.join(referencias_paginas)}] /Count {len(referencias_paginas)} >>".encode("ascii")
    # Lista de páginas.

    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    # Fuente regular.

    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    # Fuente negrita.

    salida = bytearray(b"%PDF-1.4\n")
    # Armo el archivo como bytearray.

    offsets = [0]
    # Offsets para la xref.

    for numero, objeto in enumerate(objetos, start=1):
        # Escribo cada objeto.
        offsets.append(len(salida))
        salida.extend(f"{numero} 0 obj\n".encode("ascii"))
        salida.extend(objeto)
        salida.extend(b"\nendobj\n")

    posicion_xref = len(salida)
    # Posición de la tabla xref.

    salida.extend(f"xref\n0 {len(objetos)+1}\n".encode("ascii"))
    salida.extend(b"0000000000 65535 f \n")
    # Primera entrada (libre).

    for offset in offsets[1:]:
        salida.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        # Una entrada por objeto.

    salida.extend(f"trailer\n<< /Size {len(objetos)+1} /Root 1 0 R >>\n"
                  f"startxref\n{posicion_xref}\n%%EOF\n".encode("ascii"))
    # Trailer.

    with open(ruta, "wb") as archivo:
        archivo.write(salida)
        # Escribo el archivo.

# ============================================================================
# BLOQUE 25: WORD Y PDF DE TEXTO
# ============================================================================

def crear_word_de_texto(ruta, texto):
    # Armo un .doc como HTML.
    lineas = []

    for linea in texto.splitlines() or [""]:
        # Recorro líneas.

        linea_segura = linea.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Escapo HTML.

        if linea_segura == "":
            lineas.append("<p>&nbsp;</p>")
            # Línea vacía = párrafo con espacio no separable.

        else:
            lineas.append(f"<p>{linea_segura}</p>")

    html = "<html><head><meta charset='utf-8'></head><body>" + "\n".join(lineas) + "</body></html>"
    # Armo el HTML.

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(html)
        # Escribo el archivo.

def crear_pdf_de_texto(ruta, texto):
    # PDF simple de texto plano.
    paginas = []
    lineas_pagina = []
    y = 790

    def cerrar_pagina():
        nonlocal lineas_pagina, y
        if lineas_pagina:
            paginas.append(lineas_pagina)
        lineas_pagina = []
        y = 790

    for linea in texto.splitlines() or [""]:
        # Recorro las líneas.
        if y < 55:
            cerrar_pagina()
            # Salto de página si no entra.

        lineas_pagina.append((linea, y))
        y -= 15
        # Bajo el cursor.

    cerrar_pagina()
    # Guardo la última.

    if not paginas:
        paginas = [[]]
        # Si no hay páginas, creo una vacía.

    objetos = [None, None]
    referencias = []
    id_fuente = 3 + 2 * len(paginas)

    for lineas in paginas:
        contenido = "".join(
            f"BT /F1 10 Tf 1 0 0 1 50 {pos_y} Tm <{linea.encode('cp1252', errors='replace').hex().upper()}> Tj ET\n"
            for linea, pos_y in lineas
        ).encode("ascii")
        # Igual que antes: comando PDF por línea.

        id_pagina = len(objetos) + 1
        id_contenido = id_pagina + 1
        referencias.append(f"{id_pagina} 0 R")

        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {id_fuente} 0 R >> >> /Contents {id_contenido} 0 R >>".encode("ascii"))
        objetos.append(f"<< /Length {len(contenido)} >>\nstream\n".encode("ascii") + contenido + b"\nendstream")

    objetos[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objetos[1] = f"<< /Type /Pages /Kids [{' '.join(referencias)}] /Count {len(referencias)} >>".encode("ascii")
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")

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
    for offset in offsets[1:]:
        salida.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    salida.extend(f"trailer\n<< /Size {len(objetos)+1} /Root 1 0 R >>\nstartxref\n{pos}\n%%EOF\n".encode("ascii"))

    with open(ruta, "wb") as archivo:
        archivo.write(salida)

# ============================================================================
# BLOQUE 26: EXPORTAR
# ============================================================================

def exportar_entrevistas_word(dni_paciente=None):
    # Exporto entrevistas a .doc.
    try:
        query = """SELECT p.nombre, p.apellido, e.id, p.fecha_nacimiento,
                   p.fecha_ingreso, p.telefono, p.direccion,
                   p.contacto_emergencia, p.telefono_emergencia, p.obra_social,
                   p.estado, p.consentimiento, e.nombre_profecional,
                   e.apellido_profecional, e.dni_profecional, e.matricula,
                   e.especialidad, e.telefono_profecional, e.email_profecional,
                   e.activo_profecional, e.entrevista, e.dni_paciente,
                   e.fecha_entrevista, e.hora_entrevista, e.tipo_entrevista,
                   e.proxima_sesion_entrevista
                   FROM entrevistas AS e
                   LEFT JOIN personas AS p ON p.dni = e.dni_paciente"""
        # Query base.

        if dni_paciente:
            cursor.execute(query + " WHERE e.dni_paciente = ? ORDER BY e.id",
                            (dni_paciente,))
        else:
            cursor.execute(query + " ORDER BY e.id")

        entrevistas = cursor.fetchall()

    except sqlite3.Error:
        messagebox.showerror("Error al consultar",
                              'No se pudieron leer las entrevistas')
        return

    if not entrevistas:
        messagebox.showinfo("Sin entrevistas","No hay entrevistas para exportar.")
        return

    lineas = ["Casa de Jovenes Levantate y Camina. Parroquia San Juan Bautista. Obispado de San Isidro | Archivos de perfil",
              "Historial completo de entrevistas", ""]
    # Header.

    for datos in entrevistas:
        # Recorro cada entrevista.
        (nombre_paciente, apellido_paciente, id_entrevista,
         fecha_nacimiento_paciente, fecha_ingreso, telefono_paciente,
         direccion_paciente, nombre_contacto_emergencia,
         telefono_emergencia, nombre_obra_social, estado_paciente,
         consentimiento, nombre_profecional, apellido_profecional,
         dni_profesional, matricula, especialidad, telefono_profecional,
         email_profecional, activo_profecional, entrevista, Dni_paciente,
         fecha_entrevista, hora_entrevista, tipo_entrevista,
         proxima_sesion) = datos

        paciente = " ".join(p for p in (nombre_paciente, apellido_paciente) if p) or "No registrado"
        # Nombre completo.

        lineas.append(f"=== Entrevista {id_entrevista} ===")
        lineas.append(f"Fecha: {fecha_entrevista}  Hora: {hora_entrevista or '-'}  DNI paciente: {Dni_paciente}")
        lineas.append(f"Paciente: {paciente}")
        lineas.append("")
        lineas.append("--- Datos del profesional ---")
        lineas.append(f"Nombre: {nombre_profecional or '-'}  Apellido: {apellido_profecional or '-'}")
        lineas.append(f"DNI: {dni_profesional or '-'}  Matricula: {matricula or '-'}")
        lineas.append(f"Especialidad: {especialidad or '-'}  Estado: {activo_profecional or '-'}")
        lineas.append(f"Telefono: {telefono_profecional or '-'}  Email: {email_profecional or '-'}")
        lineas.append(f"Tipo: {tipo_entrevista or '-'}  Proxima sesion: {proxima_sesion or '-'}")
        lineas.append("")
        lineas.append("--- Datos del paciente ---")
        lineas.append(f"Fecha nacimiento: {fecha_nacimiento_paciente or '-'}  Fecha ingreso: {fecha_ingreso or '-'}")
        lineas.append(f"Telefono: {telefono_paciente or '-'}  Domicilio: {direccion_paciente or '-'}")
        lineas.append(f"Contacto emergencia: {nombre_contacto_emergencia or '-'}  Tel: {telefono_emergencia or '-'}")
        lineas.append(f"Obra social: {nombre_obra_social or '-'}  Estado: {estado_paciente or '-'}  Consentimiento: {consentimiento or '-'}")
        lineas.append("")
        lineas.append("--- Anotaciones ---")

        for parrafo in (entrevista or "").splitlines() or ["Sin anotaciones"]:
            lineas.append(parrafo)
            # Cada párrafo.

        lineas.append("")

    texto = "\n".join(lineas)
    # Uno todo con saltos de línea.

    nombre_archivo = f"entrevistas_{dni_paciente}.doc" if dni_paciente else "Archivo_perfil.doc"
    ruta = filedialog.asksaveasfilename(
        title="Guardar entrevistas como Word",
        defaultextension=".doc",
        initialfile=nombre_archivo,
        filetypes=[("Documento Word", "*.doc")])
    # Diálogo.

    if not ruta:
        return

    try:
        crear_word_de_texto(ruta, texto)
    except OSError:
        messagebox.showerror("Error al exportar", 'No se pudo crear el Word')
        return

    messagebox.showinfo("Word creado", f"Entrevistas guardadas en:\n{ruta}")

def exportar_entrevistas_pdf(dni_paciente=None):
    # Ídem para PDF.
    try:
        query = """SELECT p.nombre, p.apellido, e.id, p.fecha_nacimiento,
                   p.fecha_ingreso, p.telefono, p.direccion,
                   p.contacto_emergencia, p.telefono_emergencia, p.obra_social,
                   p.estado, p.consentimiento, e.nombre_profecional,
                   e.apellido_profecional, e.dni_profecional, e.matricula,
                   e.especialidad, e.telefono_profecional, e.email_profecional,
                   e.activo_profecional, e.entrevista, e.dni_paciente,
                   e.fecha_entrevista, e.hora_entrevista, e.tipo_entrevista,
                   e.proxima_sesion_entrevista
                   FROM entrevistas AS e
                   LEFT JOIN personas AS p ON p.dni = e.dni_paciente"""
        # Misma query.

        if dni_paciente:
            cursor.execute(query + " WHERE e.dni_paciente = ? ORDER BY e.id",
                            (dni_paciente,))
        else:
            cursor.execute(query + " ORDER BY e.id")

        entrevistas = cursor.fetchall()

    except sqlite3.Error:
        messagebox.showerror("Error al consultar",
                              'No se pudieron leer las entrevistas')
        return
   
    if not entrevistas:
        messagebox.showinfo("Sin entrevistas","No hay entrevistas para exportar.")
        return

    nombre_archivo = f"entrevistas_{dni_paciente}.pdf" if dni_paciente else "Archivo_perfil.pdf"
    ruta = filedialog.asksaveasfilename(
        title="Guardar entrevistas como PDF",
        defaultextension=".pdf",
        initialfile=nombre_archivo,
        filetypes=[("Documento PDF", "*.pdf")])
    # Diálogo.

    if not ruta:
        return

    try:
        crear_pdf_entrevistas(ruta, entrevistas)
    except OSError as error:
        messagebox.showerror("Error al exportar",
                              f"No se pudo crear el PDF: {error}")
        return
    except UnicodeEncodeError:
        messagebox.showerror("Error al exportar",
                              "El texto contiene caracteres no compatibles con la fuente PDF.")
        return

    messagebox.showinfo("PDF creado", f"Entrevistas guardadas en:\n{ruta}")

# ============================================================================
# BLOQUE 27: VENTANA DE DOCUMENTOS
# ============================================================================

def abrir_ventana_ver_documento(dni_paciente=None):
    ventana_doc = Toplevel(ventana)
    ventana_doc.title("Ver / Editar documento")
    ventana_doc.geometry("900x750")
    ventana_doc.config(bg=GRIS_NIEBLA)

    frame_sup = Frame(ventana_doc, bg=GRIS_NIEBLA)
    frame_sup.pack(side="top", fill="x", padx=10, pady=10)

    Label(frame_sup, text="DNI del paciente:", bg=GRIS_NIEBLA,
          fg=GRIS_AZULADO, font=("Segoe UI", 12)).pack(side="left", padx=5)
    # Label DNI.

    entry_dni_doc = Entry(frame_sup, width=20, font=("Segoe UI", 12))
    # Entry DNI.

    entry_dni_doc.pack(side="left", padx=5)

    if dni_paciente:
        entry_dni_doc.insert(0, dni_paciente)
        # Precargo si vino.

    frame_texto = Frame(ventana_doc, bg=BLANCO, relief="solid", bd=1)
    # Frame del texto.

    frame_texto.pack(fill="both", expand=True, padx=10, pady=5)

    scroll_doc = tk.Scrollbar(frame_texto, orient="vertical")
    # Scroll.

    scroll_doc.pack(side="right", fill="y")

    text_doc = tk.Text(frame_texto, font=("Segoe UI", 11), wrap="word",
                        yscrollcommand=scroll_doc.set, bg=BLANCO,
                        fg=GRIS_AZULADO)
    # Text grande con wrap por palabras.

    text_doc.pack(side="left", fill="both", expand=True)

    scroll_doc.config(command=text_doc.yview)

    def cargar_documento():
        # Cargo las entrevistas como texto.
        dni = entry_dni_doc.get().strip()
        text_doc.delete("1.0", tk.END)

        if not dni:
            messagebox.showwarning("Atención", "Escribí un DNI primero.")
            return

        cursor.execute("""SELECT id, fecha_entrevista, hora_entrevista,
                        nombre_profecional, apellido_profecional, entrevista
                        FROM entrevistas WHERE dni_paciente = ? ORDER BY id""",
                        (dni,))
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
        # Guardo el contenido como PDF.
        texto = text_doc.get("1.0", tk.END).strip()

        if not texto:
            messagebox.showwarning("Atención", "El documento está vacío.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar como PDF", defaultextension=".pdf",
            initialfile="documento.pdf", filetypes=[("PDF", "*.pdf")])

        if not ruta:
            return

        try:
            crear_pdf_de_texto(ruta, texto)
            messagebox.showinfo("OK", f"PDF guardado en:\n{ruta}")
        except Exception:
            messagebox.showerror("Error")

    def guardar_word():
        # Guardo como Word (HTML).
        texto = text_doc.get("1.0", tk.END).strip()

        if not texto:
            messagebox.showwarning("Atención", "El documento está vacío.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar como Word", defaultextension=".doc",
            initialfile="documento.doc", filetypes=[("Word", "*.doc")])

        if not ruta:
            return

        try:
            crear_word_de_texto(ruta, texto)
            messagebox.showinfo("OK", f"Word guardado en:\n{ruta}")
        except Exception:
            messagebox.showerror("Error")

    def eliminar_archivo():
        # Pido archivo y lo borro del disco.
        ruta = filedialog.askopenfilename(
            title="Elegir archivo a eliminar",
            filetypes=[("Documentos", "*.pdf *.doc *.docx *.txt")])

        if not ruta:
            return

        if not messagebox.askyesno("Confirmar",
                                    f"¿Eliminar este archivo?\n{ruta}"):
            return

        try:
            os.remove(ruta)
            messagebox.showinfo("OK", "Archivo eliminado.")
        except Exception:
            messagebox.showerror("Error")

    def importar_documento():
        # Importo texto de un PDF, DOC, DOCX o TXT.
        ruta = filedialog.askopenfilename(
            title="Importar documento",
            filetypes=[("Documentos", "*.pdf *.doc *.docx *.txt"),
                       ("Todos", "*.*")])

        if not ruta:
            return

        extension = os.path.splitext(ruta)[1].lower()
        # Extensión.

        texto = ""

        try:
            if extension == ".pdf":
                with open(ruta, "rb") as archivo:
                    lector = PyPDF2.PdfReader(archivo)
                    for pagina in lector.pages:
                        texto += pagina.extract_text() + "\n"
                        # Extraigo el texto de cada página.

            elif extension in (".doc", ".docx", ".txt"):
                try:
                    with open(ruta, "r", encoding="utf-8") as archivo:
                        contenido = archivo.read()

                    if "<p>" in contenido:
                        contenido = re.sub(r"<[^>]+>", "", contenido)
                        # Si tiene HTML, le saco las etiquetas.

                    texto = contenido

                except UnicodeDecodeError:
                    messagebox.showerror("Error",
                                          "No se pudo leer el archivo (codificación no soportada).")
                    return

            else:
                messagebox.showwarning("Formato",
                                        "Formato no soportado. Usá PDF, DOC, DOCX o TXT.")
                return

        except Exception:
            messagebox.showerror("Error al importar")
            return

        text_doc.delete("1.0", tk.END)
        text_doc.insert("1.0", texto.strip() or "(El documento no tiene texto extraíble.)")

        messagebox.showinfo("Importado", f"Documento cargado:\n{ruta}")

    frame_btn = Frame(ventana_doc, bg=GRIS_NIEBLA)
    # Frame de botones.

    frame_btn.pack(anchor="center")
    # Centrado.

    RoundedButton(frame_btn, 130, 40, 20, VERDE_AZULADO, BLANCO,
                   text="⟳",
                   command=cargar_documento).pack(side="left", padx=5)
    # Botón recargar.

    RoundedButton(frame_btn, 150, 40, 20, VERDE_AZULADO, BLANCO,
                   text="Guardar PDF",
                   command=guardar_pdf).pack(side="left", padx=5)
    # Botón PDF.

    RoundedButton(frame_btn, 150, 40, 20, VERDE_AZULADO, BLANCO,
                   text="Guardar Word",
                   command=guardar_word).pack(side="left", padx=5)
    # Botón Word.

    RoundedButton(frame_btn, 180, 40, 20, VERDE_AZULADO, BLANCO,
                   text="Eliminar archivo",
                   command=eliminar_archivo).pack(side="left", padx=5)
    # Botón eliminar.

    RoundedButton(frame_btn, 170, 40, 20, VERDE_AZULADO, BLANCO,
                   text="Importar PDF/Word",
                   command=importar_documento).pack(side="left", padx=5)
    # Botón importar.

    if dni_paciente:
        cargar_documento()
        # Autocargo si vino DNI.

    agregar_boton_luna(ventana_doc)

# ============================================================================
# BLOQUE 28: INICIO
# ============================================================================

def al_cerrar_app():
    # Cierro la base y la ventana.
    try:
        conexion.close()
        # Cierro la conexión.
    except Exception:
        pass
        # Si falla, no importa.

    ventana.destroy()
    # Destruyo la ventana principal (todas las Toplevel se cierran).

ventana.protocol("WM_DELETE_WINDOW", al_cerrar_app)
# Asocio la X de la ventana principal a al_cerrar_app.

if __name__ == "__main__":
    ventana.mainloop()
    # Arranco el bucle de eventos (sin esto la ventana se cierra al instante).
