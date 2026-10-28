import sqlite3
import tkinter as tk
from tkinter import Label, Button, Entry, Frame, Toplevel

conexion = sqlite3.connect("Trabajo_FINAL.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(""" CREATE TABLE IF NOT EXISTS personas(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre_persona TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS persona(
id INTEGER PRIMARY KEY AUTOINCREMENT, 
nombre TEXT NOT NULL, 
apellido TEXT NOT NULL,
dni INTEGER, 
FOREIGN KEY (nombre) REFERENCES personas(nombre_persona))""")
conexion.commit()
# ESTO LO HACE IGNACIO

def abrir_ventana_personas_datos():
    ventana_persona_datos = Toplevel(ventana)
    ventana_persona_datos.title('Visor de datos de personas')
    ventana_persona_datos.geometry('500x550')
    ventana_persona_datos.config(bg="#ffffff") # Fondo terminal

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
        if nombre_persona== "":
            mensaje.config(text="Escriba un ID para buscar", fg="red")
            return
        cursor.execute("SELECT  nombre, apellido,dni FROM persona WHERE nombre = ?", (nombre_persona,))
        resultado = cursor.fetchone()
        
        if resultado:
            persona_encontrada = f"Nombre: {resultado[0]} Apellido: {resultado[1]} DNI: {resultado[2]}"
            mensaje.config(text=persona_encontrada, fg="#00FF00")
        else:
            mensaje.config(text="No existe sucursal con ese ID", fg="red")

    def eliminar_todas_los_datos():
        cursor.execute("DROP TABLE IF EXISTS personas")
        conexion.commit()
        mensaje.config(text="Tabla de los datos de personas eliminada.", fg="red")
    def crear_nueva_base_de_datos_sucursales():
        cursor.execute(""" CREATE TABLE IF NOT EXISTS personas(id INTEGER PRIMARY KEY AUTOINCREMENT,nombre_persona TEXT NOT NULL)""")
        conexion.commit()
        mensaje.config(text="Tabla de sucursales creada de nuevo.", fg="#00FF00")
    
    Button(ventana_persona_datos, text="Mostrar Datos", command=mostrar_persona_seleccionada, bg="#FCAF17").grid(row=2, column=0, columnspan=2, pady=10)
    Button(ventana_persona_datos, text='Cerrar', command=ventana_persona_datos.destroy, fg="#ffffff", bg="#000000").grid(row=3, column=0, columnspan=2, pady=10)

# ===========================================================
# VENTANA EMPLEADOS (me encargo yo)
# ===========================================================
def abrir_ventana_CRUD():
    ventana_persona = tk.Toplevel(ventana)
    ventana_persona.title('Gestor de datos')
    ventana_persona.geometry('500x500')
    ventana_persona.config(bg="#000000")
    mensaje = Label(ventana_persona, text="", fg="#00FF00", bg="#0a0a0a", justify="left")
    mensaje.grid(row=6, column=0, columnspan=7, pady=10)
    #ACA ESCRIBO LAS ENTRADAS ASI ME FUNCIONA LAS FUNCIONES Y OBTIENEN LOS DATOS
    Label(ventana_persona, text="Escriba el nombre de la persona", fg="#FCAF17", bg="#0a0a0a").grid(row= 0,column=1,pady=5)
    persona_nombre = tk.Entry(ventana_persona)
    persona_nombre.grid(row=1,column=1,pady=5) 
    Label(ventana_persona, text="Escriba el apellido de la persona", fg="#FCAF17", bg="#0a0a0a").grid(row=0,column=2,pady=5)
    persona_apellido = tk.Entry(ventana_persona)
    persona_apellido.grid(row=1,column=2,pady=5)   
    Label(ventana_persona, text="Escriba el DNI de la persona", fg="#FCAF17", bg="#0a0a0a").grid(row=0,column=3,pady=5)
    persona_DNI = tk.Entry(ventana_persona)
    persona_DNI.grid(row=1,column=3,pady=5)    
    def agregar_nueva_persona():
        nombre = persona_nombre.get()
        apellido = persona_apellido.get()
        dni = persona_DNI.get()
        dni = int(dni)
        cursor.execute("INSERT INTO persona(nombre, apellido, dni) VALUES (?,?,?)",(nombre, apellido, dni))
        conexion.commit()
        mensaje.config(text='Nuevo expediente agregado.', fg="#00FF00")
        # Limpiamos
        persona_nombre.delete(0, tk.END)
        persona_apellido.delete(0,tk.END)
        persona_DNI.delete(0, tk.END)
        
    def mostrar_persona():
        nombre_buscar = persona_nombre.get() 
        if nombre_buscar == "":
            mensaje.config(text="No se encuentra el nombre de la persona que busca", fg="red")
            return
        cursor.execute("SELECT nombre,apellido,dni FROM persona WHERE nombre = ?", (nombre_buscar,))
        resultado = cursor.fetchone()
        
        if resultado:
            empleado_encontrado = f"Nombre :{resultado[0]}"+f"Apellido:{ resultado[1]}"+f"DNI:{resultado[2]}"
            mensaje.config(text= empleado_encontrado, fg="#00FF00")
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
        persona_id INTEGER, 
        FOREIGN KEY (nombre) REFERENCES personas(nombre_persona))""")
        conexion.commit()
        mensaje.config(text="Base de datos creada de nuevo.", fg="#00FF00")
    # Botones de persona
    Button(ventana_persona, text="Mostrar datos", command=mostrar_persona, bg="#FCAF17").grid(row=4, column=1, columnspan=1, pady=5)
    Button(ventana_persona, text="Añadir datos de persona", command=agregar_nueva_persona, bg="#E3000F", fg="white").grid(row=4,column=2, columnspan=1, pady=5)
    Button(ventana_persona, text="Crear base de datos nueva de persona", command=crear_nueva_base_de_datos_persona, fg="#ffffff",bg="#000000").grid(row=4, column=3,columnspan=2, pady=5)
    Button(ventana_persona, text="Vaciar base de datos", command=eliminar_todos_los_archivos_persona, fg="#ffffff",bg="#000000").grid(row=4, column=6, columnspan=2, pady=5)
    Button(ventana_persona, text='Cerrar', command=ventana_persona.destroy,fg="#ffffff",bg="#000000").grid(row=5, column=2, columnspan=2, pady=10)
    
# ===========================================================
# VENTANA PRINCIPAL
# ===========================================================
# --- PALETA DE COLORES ---
ROJO_ROCKSTAR = "#E3000F"
AMARILLO_ROCKSTAR = "#FCAF17"
NEGRO_TERMINAL = "#0a0a0a"
VERDE_TERMINAL = "#00FF00"

ventana = tk.Tk()
ventana.title("Gestor")
ventana.geometry("600x450")
ventana.config(bg=NEGRO_TERMINAL) # Fondo general negro
mensaje = Label(ventana,text="")


# Configuramos las columnas para que el centro se estire
ventana.grid_columnconfigure(1, weight=1)

# --- 1. BANNER ROJO ARRIBA (Fila 0) ---
# Usamos columnspan=3 para que ocupe todo el ancho
banner_rojo = Frame(ventana, bg=ROJO_ROCKSTAR, height=80)  # dar otro color 
banner_rojo.grid(row=0, column=0, columnspan=3, sticky="ew")
Label(banner_rojo, text="ROCKSTAR MANAGER", bg=ROJO_ROCKSTAR, fg=AMARILLO_ROCKSTAR, font=("Courier", 20, "bold")).pack(pady=20)

# --- 2. COSTADOS AMARILLOS (Fila 1) ---
# Margen Izquierdo
frame_izq = Frame(ventana, bg=AMARILLO_ROCKSTAR, width=40)
frame_izq.grid(row=1, column=0, sticky="ns")
# Margen Derecho
frame_der = Frame(ventana, bg=AMARILLO_ROCKSTAR, width=40)
frame_der.grid(row=1, column=2, sticky="ns")

# --- 3. CENTRO (Fila 1) - Estilo Consola ---
frame_centro = Frame(ventana, bg=NEGRO_TERMINAL)
frame_centro.grid(row=1, column=1, sticky="nsew")
Label(frame_centro, text=" Seleccione una opcion abajo.", 
      bg=NEGRO_TERMINAL, fg=VERDE_TERMINAL, font=("Courier", 12), justify="left").pack(pady=40)

# --- 4. BOTONES ABAJO (Fila 2) ---
frame_botones = Frame(ventana, bg=NEGRO_TERMINAL)
# Ocupa las 3 columnas para que quede centrado abajo
frame_botones.grid(row=2, column=0, columnspan=3, pady=20)

# Usamos grid para poner los botones uno al lado del otro
btn_sucursales = Button(frame_botones, text="VER ARCHIVOS",command= abrir_ventana_personas_datos,bg=ROJO_ROCKSTAR, fg="white", font=("Arial", 10, "bold"), width=15)
btn_sucursales.grid(row=0, column=0, padx=10)

btn_empleados = Button(frame_botones, text="GESTIONAR PERSONAS", command= abrir_ventana_CRUD,bg=AMARILLO_ROCKSTAR, fg="black", font=("Arial", 10, "bold"), width=15)
btn_empleados.grid(row=0, column=1,padx=10)

btn_cerrar = Button(frame_botones, text="CERRAR", command=ventana.destroy, bg="gray", fg="white", font=("Arial", 10, "bold"), width=10)
btn_cerrar.grid(row=0, column=2, padx=10)

ventana.mainloop()
