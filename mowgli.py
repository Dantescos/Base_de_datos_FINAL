import os
import tkinter as tk
from tkinter import ttk, font, filedialog
from PIL import Image, ImageTk

# -------------------------------
# COLORES
# -------------------------------
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_AZULADO = "#008080"
VERDE_TERMINAL = "#00FF00"

# -------------------------------
# VARIABLES GLOBALES
# -------------------------------
indice_edicion = None
imagenes_cargadas = []

# -------------------------------
# FUNCIONES DE EMPLEADOS
# -------------------------------
def agregar_empleado():
    nombre = entrada_nombre.get().strip()
    apellido = entrada_apellido.get().strip()
    dni = entrada_dni.get().strip()
    fecha_ingreso = entrada_fecha_ingreso.get().strip()

    if nombre and apellido and dni and fecha_ingreso:
        registro = (
            f"Nombre: {nombre} | Apellido: {apellido} | DNI: {dni} | "
            f"Fecha de ingreso: {fecha_ingreso}"
        )

        lista_empleados.insert(tk.END, registro)
        limpiar_formulario()


def eliminar_empleado():
    try:
        indice_seleccionado = lista_empleados.curselection()[0]
        lista_empleados.delete(indice_seleccionado)
    except IndexError:
        pass


def cargar_empleado_a_editar():
    global indice_edicion
    try:
        indice_edicion = lista_empleados.curselection()[0]
        texto_registro = lista_empleados.get(indice_edicion)

        limpiar_formulario()

        partes = [p.split(": ", 1)[1] for p in texto_registro.split(" | ")]

        entrada_nombre.insert(0, partes[0])
        entrada_apellido.insert(0, partes[1])
        entrada_dni.insert(0, partes[2])
        entrada_fecha_ingreso.insert(0, partes[3])

    except IndexError:
        pass


def guardar_edicion():
    global indice_edicion
    if indice_edicion is not None:
        nombre = entrada_nombre.get().strip()
        apellido = entrada_apellido.get().strip()
        dni = entrada_dni.get().strip()
        fecha_ingreso = entrada_fecha_ingreso.get().strip()

        if nombre and apellido and dni and fecha_ingreso:
            registro_actualizado = (
                f"Nombre: {nombre} | Apellido: {apellido} | DNI: {dni} | "
                f"Fecha de ingreso: {fecha_ingreso}"
            )

            lista_empleados.delete(indice_edicion)
            lista_empleados.insert(indice_edicion, registro_actualizado)

            indice_edicion = None
            limpiar_formulario()


def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    entrada_apellido.delete(0, tk.END)
    entrada_dni.delete(0, tk.END)
    entrada_fecha_ingreso.delete(0, tk.END)
    if "entrada_entrevista" in globals():
        entrada_entrevista.delete(0, tk.END)
    if "entrada_resultado" in globals():
        entrada_resultado.delete(0, tk.END)
    if "entrada_observaciones" in globals():
        entrada_observaciones.delete(0, tk.END)

# -------------------------------
# FUNCIONES DE IMÁGENES
# -------------------------------
def mostrar_previa(ruta):
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize((180, 180))
        imagen_tk = ImageTk.PhotoImage(imagen)

        label_foto.config(image=imagen_tk)
        label_foto.image = imagen_tk
    except Exception as e:
        print("Error al mostrar la imagen:", e)


def agregar_imagen():
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if not ruta:
        return

    imagenes_cargadas.append(ruta)
    lista_imagenes.insert(tk.END, os.path.basename(ruta))
    mostrar_previa(ruta)


def eliminar_imagen():
    try:
        indice = lista_imagenes.curselection()[0]
    except IndexError:
        return

    ruta = imagenes_cargadas[indice]

    # Elimina el archivo físico
    if os.path.exists(ruta):
        os.remove(ruta)

    # Elimina el archivo de la lista interna
    del imagenes_cargadas[indice]
    lista_imagenes.delete(indice)

    # Limpia la vista previa
    label_foto.config(image="")
    label_foto.image = None


# -------------------------------
# VENTANA PRINCIPAL
# -------------------------------
ventana = tk.Tk()
ventana.title("BASE DE DATOS")
ventana.geometry("980x980")
ventana.configure(bg=VERDE_AZULADO)

# Encabezado
encabezado = tk.Frame(ventana, height=105, bg=AZUL_PETROLEO)
encabezado.pack(fill="x")
encabezado.pack_propagate(False)

tk.Label(
    encabezado,
    text="BASE DE DATOS",
    font=("Consolas", 25, "bold"),
    bg=AZUL_PETROLEO,
    fg="black",
).pack(anchor="center", pady=(28, 0))

# Lista de empleados
marco_lista = tk.Frame(ventana, bg=AZUL_PETROLEO)
marco_lista.pack(pady=20, fill="both", expand=True, padx=50)

scrollbar = tk.Scrollbar(marco_lista, orient="vertical")
scrollbar.pack(side="right", fill="y")

lista_empleados = tk.Listbox(
    marco_lista,
    font=("Consolas", 10),
    bg=VERDE_AZULADO,
    fg="white",
    selectbackground="#fffefe",
    selectforeground="black",
    yscrollcommand=scrollbar.set
)
lista_empleados.pack(side="left", fill="both", expand=True)
scrollbar.config(command=lista_empleados.yview)

# -------------------------------
# FORMULARIO DE DATOS
# -------------------------------
tk.Label(ventana, text="Nombre:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_nombre = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_nombre.pack(pady=3)

tk.Label(ventana, text="Apellido:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_apellido = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_apellido.pack(pady=3)

tk.Label(ventana, text="DNI:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_dni = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_dni.pack(pady=3)

tk.Label(ventana, text="Fecha de ingreso:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_fecha_ingreso = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_fecha_ingreso.pack(pady=3)

# -------------------------------
# SECCIÓN DE IMÁGENES
# -------------------------------
tk.Label(ventana, text="Imágenes cargadas:", font=("Consolas", 11, "bold"),
         bg=VERDE_AZULADO, fg="white").pack(pady=(10, 5))

lista_imagenes = tk.Listbox(ventana, width=50, height=6, font=("Consolas", 10))
lista_imagenes.pack()

frame_imagenes = tk.Frame(ventana, bg=VERDE_AZULADO)
frame_imagenes.pack(pady=10)

btn_agregar_imagen = tk.Button(
    frame_imagenes,
    text="Agregar imagen",
    font=("Consolas", 10, "bold"),
    bg=AZUL_PETROLEO,
    fg="white",
    command=agregar_imagen
)
btn_agregar_imagen.pack(side="left", padx=5)

btn_eliminar_imagen = tk.Button(
    frame_imagenes,
    text="Eliminar imagen",
    font=("Consolas", 10, "bold"),
    bg=BLANCO_HUESO,
    fg="black",
    command=eliminar_imagen
)
btn_eliminar_imagen.pack(side="left", padx=5)

label_foto = tk.Label(ventana, text="Vista previa", width=20, height=10, bg="gray")
label_foto.pack(pady=10)

# -------------------------------
# BOTONES DE EMPLEADOS
# -------------------------------
marco_botones = tk.Frame(ventana, bg=VERDE_AZULADO)
marco_botones.pack(pady=15)

boton_crear = tk.Button(
    marco_botones,
    text="Agregar Perfil",
    font=("Consolas", 11, "bold"),
    bg=AZUL_PETROLEO,
    fg="white",
    command=agregar_empleado,
    padx=8,
    pady=4
)
boton_crear.pack(side="left", padx=5)

boton_cargar = tk.Button(
    marco_botones,
    text="Seleccionar para editar",
    font=("Consolas", 11, "bold"),
    bg=BLANCO_HUESO,
    fg="black",
    command=cargar_empleado_a_editar,
    padx=8,
    pady=4
)
boton_cargar.pack(side="left", padx=5)

boton_actualizar = tk.Button(
    marco_botones,
    text="Confirmar edición",
    font=("Consolas", 11, "bold"),
    bg=AZUL_PETROLEO,
    fg="white",
    command=guardar_edicion,
    padx=8,
    pady=4
)
boton_actualizar.pack(side="left", padx=5)

boton_eliminar = tk.Button(
    marco_botones,
    text="Eliminar Perfil",
    font=("Consolas", 11, "bold"),
    bg=BLANCO_HUESO,
    fg="black",
    command=eliminar_empleado,
    padx=8,
    pady=4
)
boton_eliminar.pack(side="left", padx=5)

# Datos iniciales
empleados_iniciales = [
    ("Kenny", "Galindo", "44555666", "21/6/2026"),
    ("Juancho", "Tazo", "11222333", "13/10/2026"),
    ("Solomeo", "Paredes", "77888999", "1/1/2026")
]

for nombre, apellido, dni, fecha_ingreso in empleados_iniciales:
    registro = (
        f"Nombre: {nombre} | Apellido: {apellido} | DNI: {dni} | "
        f"Fecha de ingreso: {fecha_ingreso}"
    )
    lista_empleados.insert(tk.END, registro)

ventana.mainloop()