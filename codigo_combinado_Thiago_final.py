import os
import shutil
import sqlite3
import tkinter as tk
from io import BytesIO
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

conexion = None
cursor = None
CARPETA_COPIAS = "copias_imagenes"

def conectar_base_de_datos():
    global conexion, cursor
    nombre_defecto = "base de datos trabajo final.db"
    if os.path.exists(nombre_defecto):
        conexion = sqlite3.connect(nombre_defecto)
        cursor = conexion.cursor()
        return
    messagebox.showinfo(
        "Configuracion Inicial",
        "Por favor, selecciona donde deseas guardar el archivo de la Base de Datos.",
        parent=ventana,
    )
    ruta_personalizada = filedialog.asksaveasfilename(
        parent=ventana,
        title="Crear o Seleccionar archivo de Base de Datos",
        initialfile=nombre_defecto,
        filetypes=[("Base de Datos", "*.db"), ("Todos los archivos", "*.*")],
    )
    if not ruta_personalizada:
        ruta_personalizada = nombre_defecto
    conexion = sqlite3.connect(ruta_personalizada)
    cursor = conexion.cursor()

def crear_tablas():
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        dni INTEGER UNIQUE
    )            
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS imagenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        formato TEXT NOT NULL,
        contenido BLOB NOT NULL,
        id_empleado INTEGER,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id)
    )
    """)
    conexion.commit()
    if not os.path.exists(CARPETA_COPIAS):
        os.makedirs(CARPETA_COPIAS)

# --- FUNCIONES ---
def agragar_data():
    t1 = entrada1.get().strip()
    t2 = entrada2.get().strip()
    t3 = entrada3.get().strip()
    if t1 == "" or t2 == "" or t3 == "":
        print("Por favor complete los campos")
        return
    try:
        cursor.execute(
            "INSERT INTO empleados (nombre, apellido, dni) VALUES (?, ?, ?)",
            (t1, t2, t3),
        )
        conexion.commit()
        ver_lista()
    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error", "El DNI ingresado ya existe para otro empleado."
        )

def ver_lista():
    lista.delete(0, tk.END)
    cursor.execute("SELECT nombre, apellido, dni FROM empleados")
    for u in cursor.fetchall():
        lista.insert(tk.END, f"{u[0]} {u[1]} - DNI: {u[2]}")

def modificar_nombre():
    t_dni = entrada.get().strip()
    t_nuevo_nombre = entrada1.get().strip()
    if not t_dni or not t_nuevo_nombre:
        print(
            "Complete el DNI en el primer campo y el nuevo nombre en el campo 'nombre'"
        )
        return
    cursor.execute(
        "UPDATE empleados SET nombre = ? WHERE dni = ?", (t_nuevo_nombre, t_dni)
    )
    conexion.commit()
    ver_lista()

def modificar_apellido():
    t_dni = entrada.get().strip()
    t_nuevo_apellido = entrada2.get().strip()
    if not t_dni or not t_nuevo_apellido:
        print(
            "Complete el DNI en el primer campo y el nuevo apellido en el campo 'apellido'"
        )
        return
    cursor.execute(
        "UPDATE empleados SET apellido = ? WHERE dni = ?",
        (t_nuevo_apellido, t_dni),
    )
    conexion.commit()
    ver_lista()

def borrar():
    t_dni = entrada.get().strip()
    if not t_dni:
        print("Introduce el DNI del empleado en el primer campo.")
        return
    cursor.execute("SELECT id FROM empleados WHERE dni = ?", (t_dni,))
    fila = cursor.fetchone()
    if fila:
        id_empleado = fila[0]
        cursor.execute(
            "DELETE FROM imagenes WHERE id_empleado = ?", (id_empleado,)
        )
        cursor.execute("DELETE FROM empleados WHERE id = ?", (id_empleado,))
        conexion.commit()
        ver_lista()
        actualizar_lista_imagenes_vacia()
    else:
        print("Empleado no encontrado con ese DNI.")

def buscar():
    texto = entrada.get().strip()
    if not texto:
        busca.config(text="Por favor complete el campo.")
        return
    try:
        et = int(texto)
    except ValueError:
        busca.config(text="El DNI debe ser un numero.")
        return
    cursor.execute(
        "SELECT nombre, apellido, dni FROM empleados WHERE dni = ?", (et,)
    )
    idbusca = cursor.fetchall()
    if idbusca:
        for i in idbusca:
            busca.config(text=f"{i[0]} {i[1]} (DNI: {i[2]})")
    else:
        busca.config(text="contacto no encontrado")

def actualizar_lista_imagenes_vacia():
    lista2.delete(0, tk.END)
    visor.configure(image="", text="Usa el botón para cargar una imagen")
    titulo.configure(text="Selecciona una imagen")

def al_seleccionar_empleado(event):
    seleccion = lista.curselection()
    if not seleccion:
        return
    texto_seleccionado = lista.get(seleccion[0])
    try:
        t_dni = texto_seleccionado.split(" - DNI: ")[1].strip()
    except IndexError:
        return
    entrada.delete(0, tk.END)
    entrada.insert(0, t_dni)
    cursor.execute("SELECT id FROM empleados WHERE dni = ?", (t_dni,))
    fila = cursor.fetchone()
    if not fila:
        return
    id_empleado = fila[0]
    lista2.delete(0, tk.END)
    filas = conexion.execute(
        "SELECT id, nombre FROM imagenes WHERE id_empleado = ? ORDER BY id DESC",
        (id_empleado,),
    ).fetchall()
    for id_imagen, nombre in filas:
        lista2.insert(tk.END, f"{id_imagen} - {nombre}")

def guardar_imagen_bd(ruta_origen, empleado_id, dni_usuario):
    try:
        with open(ruta_origen, "rb") as archivo:
            contenido = archivo.read()
        nombre = ruta_origen.replace("\\", "/").split("/")[-1]
        formato = nombre.rsplit(".", 1)[-1].lower()
        cursor.execute(
            "INSERT INTO imagenes (nombre, formato, contenido, id_empleado) VALUES (?, ?, ?, ?)",
            (nombre, formato, sqlite3.Binary(contenido), empleado_id),
        )
        conexion.commit()
        nombre_copia = f"dni_{dni_usuario}_{nombre}"
        ruta_destino = os.path.join(CARPETA_COPIAS, nombre_copia)
        shutil.copy(ruta_origen, ruta_destino)
        messagebox.showinfo(
            "Éxito",
            f"Imagen guardada y copiada como: {nombre_copia}",
        )
    except (OSError, sqlite3.Error) as error:
        messagebox.showerror("Error", str(error))
    cursor.execute("SELECT id FROM empleados WHERE dni = ?", (dni_usuario,))
    fila = cursor.fetchone()
    if fila:
        lista2.delete(0, tk.END)
        filas = conexion.execute(
            "SELECT id, nombre FROM imagenes WHERE id_empleado = ? ORDER BY id DESC",
            (fila[0],),
        ).fetchall()
        for id_imagen, nombre_i in filas:
            lista2.insert(tk.END, f"{id_imagen} - {nombre_i}")

def agregar_foto():
    t_dni = entrada.get().strip()
    if not t_dni:
        print("Por favor introduce el DNI del empleado en el primer campo.")
        return
    cursor.execute("SELECT id FROM empleados WHERE dni = ?", (t_dni,))
    fila = cursor.fetchone()
    if not fila:
        messagebox.showerror(
            "Error", "No existe ningún empleado registrado con ese DNI."
        )
        return
    id_empleado = fila[0]
    ruta_origen = filedialog.askopenfilename(
        parent=ventana,
        title="Seleccionar imagen de origen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"),
            ("Todos los archivos", "*.*"),
        ],
    )
    if not ruta_origen:
        return
    guardar_imagen_bd(ruta_origen, id_empleado, t_dni)

def borrar_imagen():
    seleccion = lista2.curselection()
    if not seleccion:
        messagebox.showwarning(
            "Atencion",
            "Por favor, selecciona una imagen de la lista para borrar.",
        )
        return
    texto = lista2.get(seleccion[0])
    id_imagen = int(texto.split(" - ", 1)[0])
    try:
        conexion.execute("DELETE FROM imagenes WHERE id = ?", (id_imagen,))
        conexion.commit()
        visor.configure(image="", text="Usa el boton para cargar una imagen")
        titulo.configure(text="Selecciona una imagen")
        messagebox.showinfo("Exito", "Imagen eliminada correctamente de la BD.")
        t_dni = entrada.get().strip()
        cursor.execute("SELECT id FROM empleados WHERE dni = ?", (t_dni,))
        fila = cursor.fetchone()
        if fila:
            lista2.delete(0, tk.END)
            filas = conexion.execute(
                "SELECT id, nombre FROM imagenes WHERE id_empleado = ? ORDER BY id DESC",
                (fila[0],),
            ).fetchall()
            for id_img, nom_img in filas:
                lista2.insert(tk.END, f"{id_img} - {nom_img}")
    except Exception as error:
        messagebox.showerror("Error", "No se pudo borrar la imagen")

def mostrar_imagen(event=None):
    seleccion = lista2.curselection()
    if not seleccion:
        return
    texto = lista2.get(seleccion[0])
    id_imagen = int(texto.split(" - ", 1)[0])
    fila = conexion.execute(
        "SELECT nombre, contenido FROM imagenes WHERE id = ?", (id_imagen,)
    ).fetchone()
    if fila is None:
        return
    nombre, contenido = fila
    try:
        imagen = Image.open(BytesIO(contenido))
        ventana.update_idletasks()
        ancho_max = visor.winfo_width()
        alto_max = visor.winfo_height()
        if ancho_max < 50:
            ancho_max = 600
        if alto_max < 50:
            alto_max = 450
        imagen.thumbnail((ancho_max, alto_max))
        foto = ImageTk.PhotoImage(imagen)
        visor.configure(image=foto, text="")
        visor.image = foto
        titulo.configure(text=nombre)
    except Exception as error:
        messagebox.showerror("Error al mostrar", str(error))

# --- INTERFAZ GRAFICA ---
ventana = tk.Tk()
ventana.title("Control de Empleados")
ventana.geometry("900x800")

conectar_base_de_datos()
crear_tablas()

resultado = tk.Label(ventana, text="DNI del empleado a modificar, borrar o asociar foto")
resultado.pack()

entrada = tk.Entry(ventana)
entrada.pack()

resultado = tk.Label(ventana, text="nombre")
resultado.pack()

entrada1 = tk.Entry(ventana)
entrada1.pack()

resultado = tk.Label(ventana, text="apellido")
resultado.pack()

entrada2 = tk.Entry(ventana)
entrada2.pack()

resultado = tk.Label(ventana, text="dni")
resultado.pack()

entrada3 = tk.Entry(ventana)
entrada3.pack()

tk.Button(ventana, text="agregar empleado", command=agragar_data).pack()
tk.Button(ventana, text="modificar nombre de empleado", command=modificar_nombre).pack()
tk.Button(ventana, text="modificar apellido de empleado", command=modificar_apellido).pack()
tk.Button(ventana, text="borrar a un empleado", command=borrar).pack()
tk.Button(ventana, text="buscar a un empleado", command=buscar).pack()
tk.Button(ventana, text="Agregar imagen", command=agregar_foto).pack()

boton_borrar_imagen = tk.Button(ventana, text="Borrar imagen seleccionada", command=borrar_imagen, fg="red")
boton_borrar_imagen.pack(pady=5, fill="x")
busca = tk.Label(ventana, text="")
busca.pack()

lista = tk.Listbox(ventana)
lista.pack()

lista.bind("<<ListboxSelect>>", al_seleccionar_empleado)

ver_lista()

titulo = tk.Label(ventana, text="Selecciona una imagen")
titulo.pack(pady=5)
lista2 = tk.Listbox(ventana, height=8)
lista2.pack(fill="x", padx=10)
lista2.bind("<<ListboxSelect>>", mostrar_imagen)

visor = tk.Label(ventana,text="Usa el boton para aÃ±adir una imagen",bg="#e1e1e1",relief="groove",)
visor.pack(expand=True, fill="both", padx=10, pady=10)

if __name__ == "__main__":
    ventana.mainloop()
