# LIBRERIAS
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================
# BASE DE DATOS
# ============================================================
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
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni_persona INTEGER NOT NULL,
    entrevistador TEXT NOT NULL,
    fecha TEXT NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (dni_persona) REFERENCES personas(dni)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS imagenes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    formato TEXT NOT NULL,
    contenido BLOB NOT NULL,
    id_empleado INTEGER
)
""")

conexion.commit()

# ============================================================
# PALETA DE COLORES
# ============================================================
# Colores originales
ROJO = "#E3000F"
AMARILLO = "#FCAF17"
NEGRO = "#0a0a0a"
VERDE = "#00FF00"
GRIS = "#222222"
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_AZULADO = "#008080"
VERDE_TERMINAL = "#00FF00"

# Modo claro
GRIS_NIEBLA = "#F4F7F6"
BLANCO = "#FFFFFF"
GRIS_AZULADO = "#2C3E50"
GRIS_MEDIO = "#7F8C8D"
AZUL_SERENO = "#4A90E2"
VERDE_AZULADO = "#26A69A"

# Modo oscuro
OSCURO_BG = "#111111"
OSCURO_PANEL = "#1B1B1B"
OSCURO_PANEL_2 = "#202020"
OSCURO_TEXTO = "#F5F5F5"
OSCURO_TEXTO_SEC = "#D9D9D9"
OSCURO_BANNER = "#0D0D0D"
OSCURO_ACCENT = "#1A1A1A"

# ============================================================
# VENTANA PRINCIPAL
# ============================================================
ventana = tk.Tk()
ventana.title("✚ MEDTRACK")
ventana.geometry("1000x700")
ventana.config(bg=GRIS_NIEBLA)

# ============================================================
# BANNER
# ============================================================
banner = tk.Frame(ventana, bg=AZUL_SERENO, height=70)
banner.pack(side="bottom", fill="x")
banner.pack_propagate(False)

banner_label = tk.Label(
    banner,
    text="✚ MEDTRACK",
    bg=AZUL_SERENO,
    fg=BLANCO,
    font=("Arial", 20, "bold")
)
banner_label.pack(pady=18)

# ============================================================
# BOTONERA SUPERIOR
# ============================================================
frame_btn = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_btn.pack(side="top", fill="x", padx=15, pady=10)

btn_agregar = tk.Button(
    frame_btn,
    text="Agregar",
    bg=VERDE_AZULADO,
    fg="white",
    width=12,
    activebackground=VERDE_TERMINAL,
    activeforeground=NEGRO,
    relief="flat",
    bd=0,
    cursor="hand2"
)
btn_agregar.pack(side="left", padx=5)

btn_eliminar = tk.Button(
    frame_btn,
    text="Eliminar",
    bg=VERDE_AZULADO,
    fg="white",
    width=12,
    activebackground=VERDE_TERMINAL,
    activeforeground=NEGRO,
    relief="flat",
    bd=0,
    cursor="hand2"
)
btn_eliminar.pack(side="left", padx=5)

btn_buscar = tk.Button(
    frame_btn,
    text="Buscar",
    bg=VERDE_AZULADO,
    fg="white",
    width=12,
    activebackground=VERDE_TERMINAL,
    activeforeground=NEGRO,
    relief="flat",
    bd=0,
    cursor="hand2"
)
btn_buscar.pack(side="left", padx=5)

btn_limpiar = tk.Button(
    frame_btn,
    text="Limpiar",
    bg=VERDE_AZULADO,
    fg="white",
    width=12,
    activebackground=VERDE_TERMINAL,
    activeforeground=NEGRO,
    relief="flat",
    bd=0,
    cursor="hand2"
)
btn_limpiar.pack(side="left", padx=5)

# ============================================================
# FORMULARIO
# ============================================================
frame_form = tk.Frame(ventana, bg=GRIS_NIEBLA)
frame_form.pack(side="top", fill="x", padx=15, pady=10)

lbl_nombre = tk.Label(frame_form, text="Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO)
lbl_nombre.grid(row=0, column=0, sticky="e", padx=5)

entry_nombre = tk.Entry(frame_form, width=22)
entry_nombre.grid(row=0, column=1, padx=5, pady=3)

lbl_apellido = tk.Label(frame_form, text="Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO)
lbl_apellido.grid(row=0, column=2, sticky="e", padx=5)

entry_apellido = tk.Entry(frame_form, width=22)
entry_apellido.grid(row=0, column=3, padx=5, pady=3)

lbl_dni = tk.Label(frame_form, text="DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO)
lbl_dni.grid(row=0, column=4, sticky="e", padx=5)

entry_dni = tk.Entry(frame_form, width=15)
entry_dni.grid(row=0, column=5, padx=5, pady=3)

# ============================================================
# CUERPO PRINCIPAL
# ============================================================
cuerpo = tk.Frame(ventana, bg=GRIS_NIEBLA)
cuerpo.pack(side="left", fill="both", expand=True, padx=(15, 10), pady=10)

# Visor de foto
frame_foto = tk.Frame(cuerpo, bg=BLANCO, relief="solid", bd=1)
frame_foto.pack(side="left", fill="both", expand=True, padx=(0, 15))
frame_foto.pack_propagate(False)

visor_foto = tk.Label(frame_foto, text="👤\nSin foto", bg=BLANCO, fg=GRIS_MEDIO, font=("Arial", 14))
visor_foto.pack(expand=True, fill="both")

# Listado
frame_lista = tk.Frame(cuerpo, bg=GRIS_AZULADO, relief="solid", bd=1)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)

titulo_lista = tk.Label(frame_lista, text="Personas registradas", bg=GRIS_AZULADO, fg=BLANCO, font=("Arial", 12, "bold"))
titulo_lista.pack(anchor="w", padx=5, pady=5)

scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")
# --------------------------------------------------------------------------------------------------------------------------------------
# BOTON DE TEMA: SOLO LUNA, COMPACTO Y CON CONTRASTE INVERSO
# --------------------------------------------------------------------------------------------------------------------------------------
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
        boton_fill = "#FFFFFF"   # cuando fondo oscuro, botón blanco
        boton_text = "#000000"   # luna negra
        active_bg = "#EAEAEA"
        active_fg = "#000000"
    else:
        fondo_general = GRIS_NIEBLA
        panel = BLANCO
        panel_2 = GRIS_NIEBLA
        texto = GRIS_AZULADO
        texto_secundario = GRIS_MEDIO
        fondo_banner = AZUL_SERENO
        boton_accion = VERDE_AZULADO
        boton_fill = "#111111"   # cuando fondo claro, botón negro
        boton_text = "#FFFFFF"   # luna blanca
        active_bg = "#333333"
        active_fg = "#FFFFFF"

    ventana.config(bg=fondo_general)
    banner.config(bg=fondo_banner)
    frame_btn.config(bg=fondo_general)
    frame_form.config(bg=fondo_general)
    cuerpo.config(bg=fondo_general)
    frame_foto.config(bg=panel)
    frame_lista.config(bg=panel_2)

    visor_foto.config(bg=panel, fg=texto_secundario)
    titulo_lista.config(bg=panel_2, fg=texto)
    banner_label.config(bg=fondo_banner, fg="#FFFFFF")

    for widget in frame_form.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=fondo_general, fg=texto)

    for widget in frame_btn.winfo_children():
        if isinstance(widget, tk.Button):
            if widget is not btn_tema:
                widget.config(
                    bg=boton_accion,
                    fg="white",
                    activebackground=VERDE_TERMINAL if not tema_oscuro else "#444444",
                    activeforeground="white",
                    relief="flat",
                    bd=0
                )

    btn_tema.config(
        bg=boton_fill,
        fg=boton_text,
        activebackground=active_bg,
        activeforeground=active_fg,
        relief="flat",
        bd=0
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
    cursor="hand2",
    activebackground="#333333",
    activeforeground="#FFFFFF",
    padx=0,
    pady=0
)
btn_tema.pack(side="right", padx=5)
ventana.mainloop()