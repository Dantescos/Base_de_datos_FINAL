Python

# En buscar_persona_perfil (línea 2092):
cursor.execute(
    "SELECT id, nombres, apellido, dni, edad, domicilio, fecha_ingreso, telefono, mail, "
    "fecha_nacimiento, contacto_emergencia, telefono_emergencia, obra_social, nacionalidad, localidad "
    "FROM personas WHERE dni = ? ORDER BY id",
    (dni_txt,)
)

# En importar_documento (líneas 2851-2855):
if extension == ".pdf":
    try:
        import PyPDF2
    except ImportError:
        messagebox.showerror("Falta librería", "No está instalado PyPDF2 para leer archivos PDF.")
        return
    with open(ruta, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += (pagina.extract_text() or "") + "\n"
            import io
import re
import tokenize

with open("Nahuel_parte_12.py", "r", encoding="utf-8") as f:
    lineas = f.readlines()

# 1. Eliminar bloques duplicados (lines 1-indexed):
# - Líneas 135-148: duplicado de SANCA_BASE64 y segunda conexión 'mammaasda'
# - Líneas 197-204: segunda definición de agregar_columna_si_falta sin validación
# - Líneas 390-507: duplicado de RUTA_LEGAJOS y funciones de legajos
# - Líneas 2898-2971: duplicado de crear_word_de_texto y crear_pdf_de_texto sin foto_bytes
rangos_a_borrar = [
    (135, 148),
    (197, 204),
    (390, 507),
    (2898, 2971),
]

filtradas = []
for idx, linea in enumerate(lineas, start=1):
    if any(inicio <= idx <= fin for inicio, fin in rangos_a_borrar):
        continue
    filtradas.append(linea)

codigo = "".join(filtradas)

# 2. Corregir errores puntuales de SQL, excepciones y llamadas
reemplazos = [
    ("WHERE dni_paciente = ? ORDER BY id", "WHERE dni = ? ORDER BY id"),
    (
        "p.obra_social,p.nacionalidad,p.localidad personas AS p ON p.dni",
        "p.obra_social,p.nacionalidad,p.localidad FROM personas AS p",
    ),
    ("p.contacto_emergecia", "p.contacto_emergencia"),
    (
        "p.telefono_emergencia,p.obra_social,p.nacionalidad,p.localidad FROM personas AS p ON p.dni",
        "p.telefono_emergencia,p.obra_social,p.nacionalidad,p.localidad FROM personas AS p",
    ),
    ("WHERE e.dni_paciente = ? ORDER BY e.id", "WHERE p.dni = ? ORDER BY p.id"),
    ("ORDER BY e.id", "ORDER BY p.id"),
    ("except: salida.append(ch)", "except Exception: salida.append(ch)"),
    ('messagebox.showerror("Error")', 'messagebox.showerror("Error", "No se pudo completar la operación.")'),
    ('messagebox.showerror("Error al importar")', 'messagebox.showerror("Error al importar", "No se pudo leer el archivo.")'),
    (
        'Button(frame_btn, bg =  COLOR_BOTON, fg = COLOR_BOTON_TEXTO,text="Autores",command=abrir_ventana_autores).pack(side="left", padx=5)',
        '    Button(frame_btn, bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, text="Autores", command=abrir_ventana_autores).pack(side="left", padx=5)',
    ),
]

for viejo, nuevo in reemplazos:
    codigo = codigo.replace(viejo, nuevo)

# 3. Eliminar todos los comentarios usando tokenize (sin tocar strings ni docstrings)
tokens = []
for tok in tokenize.generate_tokens(io.StringIO(codigo).readline):
    if tok.type != tokenize.COMMENT:
        tokens.append(tok)

codigo_sin_comentarios = tokenize.untokenize(tokens)

# Limpiar líneas en blanco múltiples generadas al borrar comentarios
codigo_sin_comentarios = re.sub(r"\n{3,}", "\n\n", codigo_sin_comentarios)

with open("archivo.py", "w", encoding="utf-8") as f:
    f.write(codigo_sin_comentarios)

print("Archivo generado correctamente: archivo.py")