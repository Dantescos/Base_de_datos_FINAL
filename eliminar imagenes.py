import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# -------------------------
# Variables globales
# -------------------------
imagenes_cargadas = []

# -------------------------
# Funciones de imágenes
# -------------------------
def agregar_imagen():
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if not ruta:
        return

    imagenes_cargadas.append(ruta)
    lista_imagenes.insert(tk.END, os.path.basename(ruta))

    # mostrar la imagen en una vista previa
    mostrar_previa(ruta)


def mostrar_previa(ruta):
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize((150, 150))
        imagen_tk = ImageTk.PhotoImage(imagen)

        label_foto.config(image=imagen_tk)
        label_foto.image = imagen_tk

    except Exception as e:
        print("Error al cargar la imagen:", e)


def eliminar_imagen():
    try:
        indice = lista_imagenes.curselection()[0]
    except IndexError:
        return

    ruta = imagenes_cargadas[indice]

    # borrar archivo físico
    if os.path.exists(ruta):
        os.remove(ruta)

    # quitar de la lista
    del imagenes_cargadas[indice]
    lista_imagenes.delete(indice)

    # limpiar vista previa
    label_foto.config(image="")
    label_foto.image = None


# -------------------------
# Ventana
# -------------------------
ventana = tk.Tk()
ventana.title("Carga de imágenes")
ventana.geometry("500x500")

# lista de imágenes
lista_imagenes = tk.Listbox(ventana, width=40, height=8)
lista_imagenes.pack(pady=10)

# botón agregar
btn_agregar = tk.Button(ventana, text="Agregar imagen", command=agregar_imagen)
btn_agregar.pack()

# botón eliminar
btn_eliminar = tk.Button(ventana, text="Eliminar imagen", command=eliminar_imagen)
btn_eliminar.pack(pady=5)

# vista previa
label_foto = tk.Label(ventana, text="Vista previa", width=20, height=10, bg="gray")
label_foto.pack(pady=10)

ventana.mainloop()