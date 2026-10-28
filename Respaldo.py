import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import Label, Button, Entry, Frame, Toplevel

# ===========================================================
# BASE DE DATOS Y TABLAS
# ===========================================================
conexion = sqlite3.connect("Trabajo_FINAL.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Crear tablas principales
cursor.execute(""" CREATE TABLE IF NOT EXISTS personas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre_persona TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS persona(
id INTEGER PRIMARY KEY AUTOINCREMENT, 
nombre TEXT NOT NULL, 
apellido TEXT NOT NULL,
dni INTEGER, 
FOREIGN KEY (nombre) REFERENCES personas(nombre_persona))""")

# Crear tablas de empleados e imágenes que faltaban en la inicialización
cursor.execute("""CREATE TABLE IF NOT EXISTS empleados(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
apellido TEXT NOT NULL,
dni INTEGER UNIQUE)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS imagenes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
formato TEXT NOT NULL,
contenido BLOB NOT NULL,
id_empleado INTEGER)""")

conexion.commit()

# ===========================================================
# VENTANA PERSONAS DATOS
# ===========================================================
def abrir_ventana_personas_datos():
    ventana_persona_datos = Toplevel(ventana)
    ventana_persona_datos.title('Visor de datos de personas')
    ventana_persona_datos.geometry('500x550')
    ventana_persona_datos.config(bg="#ffffff") 

    mensaje = Label(ventana_persona_datos, text="", fg="#00FF00", bg="#0a0a0a", justify="left")
    mensaje.grid(row=0, column=0, columnspan=2, pady=10)

    cursor.execute("SELECT nombre_persona FROM personas")
    nombres = [fila[0] for fila in cursor.fetchall()]
    if not nombres: nombres = ["No hay datos de esa persona"]

    seleccion = tk.StringVar(ventana_persona_datos)
    seleccion.set(nombres[0])

    Label(ventana_persona_datos, text="Seleccione el nombre de la persona que busca:", fg="#FCAF17", bg="#0a0a0a").grid(row=1, column=0, pady=5)
    tk.OptionMenu(ventana_persona_datos, seleccion, *nombres).grid(row=1, column=1, pady=5)

    def mostrar_persona_seleccionada():
        nombre_persona = seleccion.get()
        if nombre_persona == "":
            mensaje.config(text="Escriba un ID para buscar", fg="red")
            return
        cursor.execute("SELECT nombre, apellido, dni FROM persona WHERE nombre = ?", (nombre_persona,))
        resultado = cursor.fetchone()
        
        if resultado:
            persona_encontrada = f"Nombre: {resultado[0]} Apellido: {resultado[1]} DNI: {resultado[2]}"
            mensaje.config(text=persona_encontrada, fg="#00FF00")
        else:
            mensaje.config(text="No existe sucursal con ese ID", fg="red")

    Button(ventana_persona_datos, text="Mostrar Datos", command=mostrar_persona_seleccionada, bg="#FCAF17").grid(row=2, column=0, columnspan=2, pady=10)
    Button(ventana_persona_datos, text='Cerrar', command=ventana_persona_datos.destroy, fg="#ffffff", bg="#000000").grid(row=3, column=0, columnspan=2, pady=10)

# ===========================================================
# GESTOR DE PERSONAS CRUD
# ===========================================================
def abrir_ventana_CRUD():
    ventana_persona = tk.Toplevel(ventana)
    ventana_persona.title('Gestor de datos')
    ventana_persona.geometry('500x500')
    ventana_persona.config(bg="#000000")
    mensaje = Label(ventana_persona, text="", fg="#00FF00", bg="#0a0a0a", justify="left")
    mensaje.grid(row=6, column=0, columnspan=7, pady=10)
    
    Label(ventana_persona, text="Escriba el nombre de la persona", fg="#FCAF17", bg="#0a0a0a").grid(row=0, column=1, pady=5)
    persona_nombre = tk.Entry(ventana_persona)
    persona_nombre.grid(row=1, column=1, pady=5) 
    Label(ventana_persona, text="Escriba el apellido de la persona", fg="#FCAF17", bg="#0a0a0a").grid(row=0, column=2, pady=5)
    persona_apellido = tk.Entry(ventana_persona)
    persona_apellido.grid(row=1, column=2, pady=5)   
    Label(ventana_persona, text="Escriba el DNI de la persona", fg="#FCAF17", bg="#0a0a0a").grid(row=0, column=3, pady=5)
    persona_DNI = tk.Entry(ventana_persona)
    persona_DNI.grid(row=1, column=3, pady=5)    
    
    def agregar_nueva_persona():
        nombre = persona_nombre.get()
        apellido = persona_apellido.get()
        dni = persona_DNI.get()
        dni = int(dni)
        cursor.execute("INSERT INTO persona(nombre, apellido, dni) VALUES (?,?,?)", (nombre, apellido, dni))
        conexion.commit()
        mensaje.config(text='Nuevo expediente agregado.', fg="#00FF00")
        persona_nombre.delete(0, tk.END)
        persona_apellido.delete(0, tk.END)
        persona_DNI.delete(0, tk.END)
        
    def mostrar_persona():
        nombre_buscar = persona_nombre.get() 
        if nombre_buscar == "":
            mensaje.config(text="No se encuentra el nombre de la persona que busca", fg="red")
            return
        cursor.execute("SELECT nombre, apellido, dni FROM persona WHERE nombre = ?", (nombre_buscar,))
        resultado = cursor.fetchone()
        
        if resultado:
            empleado_encontrado = f"Nombre: {resultado[0]} Apellido: {resultado[1]} DNI: {resultado[2]}"
            mensaje.config(text=empleado_encontrado, fg="#00FF00")
        else:
            mensaje.config(text="No existe la persona que busca", fg="red")
            
    def eliminar_todos_los_archivos_persona():
        cursor.execute("DROP TABLE IF EXISTS persona")
        conexion.commit()
        mensaje.config(text="Base de datos persona eliminada.", fg="red")
        
    def crear_nueva_base_de_datos_persona():
        cursor.execute("""CREATE TABLE IF NOT EXISTS persona(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre TEXT NOT NULL, 
        apellido TEXT NOT NULL,
        dni INTEGER, 
        FOREIGN KEY (nombre) REFERENCES personas(nombre_persona))""")
        conexion.commit()
        mensaje.config(text="Base de datos creada de nuevo.", fg="#00FF00")

    Button(ventana_persona, text="Mostrar datos", command=mostrar_persona, bg="#FCAF17").grid(row=4, column=1, columnspan=1, pady=5)
    Button(ventana_persona, text="Añadir datos", command=agregar_nueva_persona, bg="#E3000F", fg="white").grid(row=4, column=2, columnspan=1, pady=5)
    Button(ventana_persona, text="Crear BD nueva", command=crear_nueva_base_de_datos_persona, fg="#ffffff", bg="#000000").grid(row=4, column=3, columnspan=2, pady=5)
    Button(ventana_persona, text="Vaciar BD", command=eliminar_todos_los_archivos_persona, fg="#ffffff", bg="#000000").grid(row=4, column=6, columnspan=2, pady=5)
    Button(ventana_persona, text='Cerrar', command=ventana_persona.destroy, fg="#ffffff", bg="#000000").grid(row=5, column=2, columnspan=2, pady=10)

# ===========================================================
# VENTANA MULTIPROCESSING / EMPLEADOS & IMÁGENES
# ===========================================================
def abrir_ventana_multiprocessing():
    ventana_multi = Toplevel(ventana)
    ventana_multi.title("Prueba Multiprocessing")
    ventana_multi.geometry("420x720")
    ventana_multi.config(bg="#0a0a0a")

    Label(ventana_multi, text="nombre del empleado a modificar o borrar", fg="#FCAF17", bg="#0a0a0a").pack()
    entrada = Entry(ventana_multi)
    entrada.pack(pady=2)

    Label(ventana_multi, text="nombre", fg="#FCAF17", bg="#0a0a0a").pack()
    entrada1 = Entry(ventana_multi)
    entrada1.pack(pady=2)

    Label(ventana_multi, text="apellido", fg="#FCAF17", bg="#0a0a0a").pack()
    entrada2 = Entry(ventana_multi)
    entrada2.pack(pady=2)

    Label(ventana_multi, text="dni", fg="#FCAF17", bg="#0a0a0a").pack()
    entrada3 = Entry(ventana_multi)
    entrada3.pack(pady=2)

    busca = Label(ventana_multi, text="", fg="#00FF00", bg="#0a0a0a")
    lista = tk.Listbox(ventana_multi, height=5)
    lista2 = tk.Listbox(ventana_multi, height=5)
    visor = Label(ventana_multi, text="Tu imagen aparecerá aquí", fg="white", bg="#222222")
    titulo_imagen = Label(ventana_multi, text="Seleccioná una imagen", fg="#FCAF17", bg="#0a0a0a")

    def ver_lista():
        lista.delete(0, tk.END)
        cursor.execute("SELECT * FROM empleados")
        for u in cursor.fetchall():
            lista.insert(tk.END, u)

    def agragar_data():
        t1 = entrada1.get()
        t2 = entrada2.get()
        t3 = entrada3.get()
        cursor.execute("INSERT INTO empleados (nombre,apellido,dni) VALUES (?,?,?)", (t1, t2, t3))
        conexion.commit()
        ver_lista()

    def modificar_nombre():
        t1 = entrada.get()
        t2 = entrada2.get()  
        cursor.execute("UPDATE empleados SET nombre = ? WHERE dni = ?", (t2, t1))
        conexion.commit()
        ver_lista()

    def modificar_apellido():
        t1 = entrada.get()
        t2 = entrada3.get()  
        cursor.execute("UPDATE empleados SET apellido = ? WHERE dni = ?", (t2, t1))
        conexion.commit()
        ver_lista()

    def borrar():
        t1 = entrada.get()
        cursor.execute("DELETE FROM empleados WHERE dni=?", (t1,))
        conexion.commit()
        ver_lista()

    def buscar():    
        try:
            et = int(entrada.get())
            cursor.execute("SELECT * FROM empleados WHERE dni = ?", (et,))
            idbusca = cursor.fetchall()
            if idbusca:
                busca.config(text=str(idbusca[0]), fg="#00FF00")
            else:
                busca.config(text="contacto no encontrado", fg="red")
        except ValueError:
            busca.config(text="Ingresa un DNI numérico válido", fg="red")

    def actualizar_lista():
        lista2.delete(0, tk.END)
        filas = conexion.execute("SELECT id, nombre FROM imagenes ORDER BY id DESC").fetchall()
        for id_imagen, nombre in filas:
            lista2.insert(tk.END, f"{id_imagen} - {nombre}")

    def agregar_imagen():
        et = entrada.get()
        if not et:
            messagebox.showerror("Error", "Escribe el ID del empleado para asociar la imagen")
            return
        
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"), ("Todos los archivos", ".")]
        )
        if not ruta: return

        try:
            with open(ruta, "rb") as archivo:
                contenido = archivo.read()
            nombre_archivo = ruta.replace("\\", "/").split("/")[-1]
            formato = nombre_archivo.rsplit(".", 1)[-1].lower()
            
            conexion.execute(
                "INSERT INTO imagenes (nombre, formato, contenido, id_empleado) VALUES (?, ?, ?, ?)",
                (nombre_archivo, formato, sqlite3.Binary(contenido), et)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", f"Imagen guardada: {nombre_archivo}")
        except Exception as error:
            messagebox.showerror("Error", str(error))
        actualizar_lista()

    def mostrar_imagen(event=None):
        seleccion = lista2.curselection()
        if not seleccion: return
        texto = lista2.get(seleccion[0])
        id_imagen = int(texto.split(" - ", 1)[0])
        fila = conexion.execute("SELECT nombre, contenido FROM imagenes WHERE id = ?", (id_imagen,)).fetchone()
        if fila is None: return
        
        nombre, contenido = fila
        try:
            imagen = Image.open(BytesIO(contenido))
            imagen.thumbnail((300, 200))
            foto = ImageTk.PhotoImage(imagen)
            visor.configure(image=foto, text="")
            visor.image = foto
            titulo_imagen.configure(text=nombre)
        except Exception as error:
            messagebox.showerror("Error al mostrar", str(error))

    # Botonera de Multiprocessing
    Button(ventana_multi, text="Agregar empleado", command=agragar_data, bg="#E3000F", fg="white").pack(pady=2)
    Button(ventana_multi, text="Modificar nombre", command=modificar_nombre, bg="#FCAF17").pack(pady=2)
    Button(ventana_multi, text="Modificar apellido", command=modificar_apellido, bg="#FCAF17").pack(pady=2)
    Button(ventana_multi, text="Borrar empleado", command=borrar, bg="gray", fg="white").pack(pady=2)
    Button(ventana_multi, text="Buscar por DNI", command=buscar, bg="gray", fg="white").pack(pady=2)
    Button(ventana_multi, text="Asociar imagen", command=agregar_imagen, bg="#00FF00", fg="black").pack(pady=5)
    
    busca.pack()
    lista.pack(fill="x", padx=10, pady=2)
    titulo_imagen.pack(pady=2)
    lista2.pack(fill="x", padx=10, pady=2)
    lista2.bind("<<ListboxSelect>>", mostrar_imagen)
    visor.pack(expand=True, fill="both", padx=10, pady=5)
    
    ver_lista()
    actualizar_lista()

# ===========================================================
# VENTANA PRINCIPAL (ROCKSTAR MANAGER)
# ===========================================================
ROJO_ROCKSTAR = "#E3000F"
AMARILLO_ROCKSTAR = "#FCAF17"
NEGRO_TERMINAL = "#0a0a0a"
VERDE_TERMINAL = "#00FF00"

ventana = tk.Tk()
ventana.title("Rockstar Manager")
ventana.geometry("650x480")
ventana.config(bg=NEGRO_TERMINAL)

ventana.grid_columnconfigure(1, weight=1)

# --- Banner Superior ---
banner_rojo = Frame(ventana, bg=ROJO_ROCKSTAR, height=80)
banner_rojo.grid(row=0, column=0, columnspan=3, sticky="ew")
Label(banner_rojo, text="ROCKSTAR MANAGER", bg=ROJO_ROCKSTAR, fg=AMARILLO_ROCKSTAR, font=("Courier", 20, "bold")).pack(pady=20)

# --- Márgenes Laterales ---
frame_izq = Frame(ventana, bg=AMARILLO_ROCKSTAR, width=40)
frame_izq.grid(row=1, column=0, sticky="ns")
frame_der = Frame(ventana, bg=AMARILLO_ROCKSTAR, width=40)
frame_der.grid(row=1, column=2, sticky="ns")

# --- Cuerpo Central ---
frame_centro = Frame(ventana, bg=NEGRO_TERMINAL)
frame_centro.grid(row=1, column=1, sticky="nsew")
Label(frame_centro, text="Seleccione una opción de gestión abajo.", 
      bg=NEGRO_TERMINAL, fg=VERDE_TERMINAL, font=("Courier", 12)).pack(pady=40)

# --- Panel de Botones ---
frame_botones = Frame(ventana, bg=NEGRO_TERMINAL)
frame_botones.grid(row=2, column=0, columnspan=3, pady=20)

btn_sucursales = Button(frame_botones, text="VER ARCHIVOS", command=abrir_ventana_personas_datos, bg=ROJO_ROCKSTAR, fg="white", font=("Arial", 9, "bold"), width=15)
btn_sucursales.grid(row=0, column=0, padx=5)

btn_empleados = Button(frame_botones, text="GESTIONAR PERSONAS", command=abrir_ventana_CRUD, bg=AMARILLO_ROCKSTAR, fg="black", font=("Arial", 9, "bold"), width=18)
btn_empleados.grid(row=0, column=1, padx=5)

btn_multi = Button(frame_botones, text="MULTIPROCESSING", command=abrir_ventana_multiprocessing, bg="#00FF00", fg="black", font=("Arial", 9, "bold"), width=18)
btn_multi.grid(row=0, column=2, padx=5)

btn_cerrar = Button(frame_botones, text="CERRAR", command=ventana.destroy, bg="gray", fg="white", font=("Arial", 9, "bold"), width=10)
btn_cerrar.grid(row=0, column=3, padx=5)

ventana.mainloop()
