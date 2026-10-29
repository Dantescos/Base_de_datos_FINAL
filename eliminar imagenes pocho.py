import os
import tkinter as tk
from tkinter import ttk, font, filedialog
from PIL import Image, ImageTk

# -------------------------------
# VARIABLES PARA IMÁGENES
# -------------------------------
imagenes_cargadas = []


# -------------------------------
# FUNCIONES PARA IMÁGENES
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

    # eliminar archivo físico
    if os.path.exists(ruta):
        os.remove(ruta)

    # eliminar de la lista interna
    del imagenes_cargadas[indice]
    lista_imagenes.delete(indice)

    # limpiar la vista previa
    label_foto.config(image="")
    
    label_foto.image = None
    
    
    
    
    # -------------------------------
# LISTA DE IMÁGENES
# -------------------------------
tk.Label(ventana, text="Imágenes cargadas:", font=("Consolas", 11, "bold"),
         bg=VERDE_AZULADO, fg="white").pack(pady=(10, 5))

lista_imagenes = tk.Listbox(ventana, width=50, height=6, font=("Consolas", 10))
lista_imagenes.pack()

# -------------------------------
# BOTONES DE IMAGENES
# -------------------------------
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

# -------------------------------
# VISTA PREVIA
# -------------------------------
label_foto = tk.Label(ventana, text="Vista previa", width=20, height=10, bg="gray")
label_foto.pack(pady=10)
    
    