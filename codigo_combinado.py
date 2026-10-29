import sqlite3
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO
from PIL import Image, ImageTk

conexion = None
cursor = None

def conectar_base_de_datos():
    global conexion, cursor
    nombre_defecto = "base de datos trabajo final.db"
    if os.path.exists(nombre_defecto):
        conexion = sqlite3.connect(nombre_defecto)
        cursor = conexion.cursor()
        return
    messagebox.showinfo("Configuracion Inicial", "Por favor, selecciona donde deseas guardar el archivo de la Base de Datos.", parent=ventana)
    ruta_personalizada = filedialog.asksaveasfilename(
        parent=ventana,
        title="Crear o Seleccionar archivo de Base de Datos",
        initialfile=nombre_defecto,
        filetypes=[("Base de Datos", "*.db"), ("Todos los archivos", "*.*")]
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
        dni INTEGER
    )            
    """)

    conexion.execute("""
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

# --- FUNCIONES ---
def agragar_data():
    t1 = entrada1.get().strip()
    t2 = entrada2.get().strip()
    t3 = entrada3.get().strip()
    if t1 == "" or t2 == "" or t3 == "":
        print("Por favor complete los campos")
        return   
    cursor.execute(
        "INSERT INTO empleados (nombre, apellido, dni) VALUES (?, ?, ?)", (t1, t2, t3)
    )
    conexion.commit()   
    ver_lista() 

def ver_lista():
    lista.delete(0, tk.END)
    cursor.execute("SELECT * FROM empleados")
    for u in cursor.fetchall():
        lista.insert(tk.END, u)

def modificar_nombre():
    t1 = entrada.get().strip()
    t2 = entrada2.get().strip()  
    if not t1 or not t2:
        print("Complete el DNI en el primer campo y el nuevo nombre en el campo 'apellido'")
        return
    cursor.execute("UPDATE empleados SET nombre = ? WHERE dni = ?", (t2, t1))
    conexion.commit()
    ver_lista()

def modificar_apellido():
    t1 = entrada.get().strip()
    t2 = entrada3.get().strip()  
    if not t1 or not t2:
        print("Complete el DNI en el primer campo y el nuevo apellido en el campo 'dni'")
        return
    cursor.execute("UPDATE empleados SET apellido = ? WHERE dni = ?", (t2, t1))
    conexion.commit()
    ver_lista()

def borrar():
    t1 = entrada.get().strip()
    if not t1:
        print("Introduce el DNI del empleado en el primer campo.")
        return
    cursor.execute("DELETE FROM empleados WHERE dni = ?", (t1,))
    conexion.commit()
    ver_lista()

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
    cursor.execute("SELECT * FROM empleados WHERE dni = ?", (et,))
    idbusca = cursor.fetchall()
    if idbusca:
        for i in idbusca:
            if et in i:
                busca.config(text=str(i)) 
            else:
                busca.config(text="contacto no encontrado")
    else:
        busca.config(text="contacto no encontrado")

def actualizar_lista():
    lista2.delete(0, tk.END)
    filas = conexion.execute(
        "SELECT id, nombre FROM imagenes ORDER BY id DESC"
    ).fetchall()
    for id_imagen, nombre in filas:
        lista2.insert(tk.END, f"{id_imagen} - {nombre}")

def al_seleccionar_empleado(event):
    seleccion = lista.curselection()
    if not seleccion:
        return
    datos_empleado = lista.get(seleccion[0])
    id_empleado = datos_empleado[0]
    entrada.delete(0, tk.END)
    entrada.insert(0, str(id_empleado))
    lista2.delete(0, tk.END)
    filas = conexion.execute(
        "SELECT id, nombre FROM imagenes WHERE id_empleado = ? ORDER BY id DESC", (id_empleado,)
    ).fetchall()
    for id_imagen, nombre in filas:
        lista2.insert(tk.END, f"{id_imagen} - {nombre}")

def guardar_imagen_bd(ruta_origen, empleado_id):
    try:
        with open(ruta_origen, "rb") as archivo:
            contenido = archivo.read()
        nombre = ruta_origen.replace("\\", "/").split("/")[-1]
        formato = nombre.rsplit(".", 1)[-1].lower()
        conexion.execute(
            "INSERT INTO imagenes (nombre, formato, contenido, id_empleado) "
            "VALUES (?, ?, ?, ?)",
            (nombre, formato, sqlite3.Binary(contenido), empleado_id)
        )
        conexion.commit()
        messagebox.showinfo("Éxito", f"Imagen guardada: {nombre}")
    except (OSError, sqlite3.Error) as error:
        messagebox.showerror("Error", str(error))
    actualizar_lista()

def agregar_foto():
    et = entrada.get().strip()
    if not et:
        print("Por favor introduce el ID del empleado en el primer campo.")
        return   
    ruta_origen = filedialog.askopenfilename(
        parent=ventana,
        title="Seleccionar imagen de origen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"),
            ("Todos los archivos", "*.*")
        ]
    )
    if not ruta_origen:
        return
    guardar_imagen_bd(ruta_origen, et)

def borrar_imagen():
    seleccion = lista2.curselection()
    if not seleccion:
        messagebox.showwarning("Atencion", "Por favor, selecciona una imagen de la lista para borrar.")
        return
    texto = lista2.get(seleccion[0])
    id_imagen = int(texto.split(" - ", 1)[0])   
    try:
        conexion.execute("DELETE FROM imagenes WHERE id = ?", (id_imagen,))
        conexion.commit()
        visor.configure(image="", text="Usa el botón para cargar una imagen")
        titulo.configure(text="Selecciona una imagen")
        messagebox.showinfo("Exito", "Imagen eliminada correctamente de la BD.")
        actualizar_lista()
    except Exception as error:
        messagebox.showerror("Error", "No se pudo borrar la imagen")

def mostrar_imagen(event=None):
    seleccion = lista2.curselection()
    if not seleccion:
        return
    texto = lista2.get(seleccion[0])
    id_imagen = int(texto.split(" - ", 1)[0])
    fila = conexion.execute(
        "SELECT nombre, contenido FROM imagenes WHERE id = ?",
        (id_imagen,)
    ).fetchone()
    if fila is None:
        return
    nombre, contenido = fila
    try:
        imagen = Image.open(BytesIO(contenido))
        ventana.update_idletasks()  
        ancho_max = visor.winfo_width()
        alto_max = visor.winfo_height()
        if ancho_max < 50: ancho_max = 600
        if alto_max < 50: alto_max = 450
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

visor = tk.Label(ventana, text="Usa el boton para añadir una imagen", bg="#e1e1e1", relief="groove")
visor.pack(expand=True, fill="both", padx=10, pady=10)

actualizar_lista()

if __name__ == "__main__":
    ventana.mainloop()
