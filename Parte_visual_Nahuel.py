import sqlite3
import tkinter as tk
from tkinter import Label, Button, Entry, Frame, Toplevel

# ===========================================================
# CONEXION A BASE DE DATOS
# ===========================================================
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
persona_id INTEGER, 
FOREIGN KEY (persona_id) REFERENCES personas(id))""")
conexion.commit()


class Sucursal:
    def __init__(self, id_sucursal, nombre, direccion):
        self.id_sucursal = id_sucursal
        self.nombre = nombre
        self.direccion = direccion

    def mostrar_datos(self):
        return f"ID: {self.id_sucursal} | {self.nombre} - {self.direccion}."
        
    def ver_empleados(self):
        cursor.execute("SELECT nombre FROM empleados WHERE sucursal_id = ?", (self.id_sucursal,))
        empleados = cursor.fetchall()
        if not empleados:   
            return 'No hay empleados'
        else:
            texto = f"\nEmpleados en {self.nombre}:\n"
            for empleado in empleados:
                texto += f"- {empleado[0]}\n"
            return texto
        
class Persona:
    def __init__(self,nombre,apellido,dni):
        self.nombre= nombre
        self.apellido = apellido
        self.dni = dni
    def mostrar_informacion(self):
        return f"El empleado es {self.nombre},cuyo DNI es: {self.dni}, emepezo a trabajar en la sucursal {self.sucursal_id} en el {self.año_inicio} año, lleva {self.asistencia} dias trabajando"
# ===========================================================
# VENTANA SUCURSALES (ignacio)
# ===========================================================
def abrir_ventana_nombre():
    ventana_sucursales = Toplevel(ventana)
    ventana_sucursales.title('Gestor de sucursales')
    ventana_sucursales.geometry('500x550')
    ventana_sucursales.config(bg="#0a0a0a") # Fondo terminal

    mensaje = Label(ventana_sucursales, text="", fg="#00FF00", bg="#0a0a0a", justify="left")
    mensaje.grid(row=0, column=0, columnspan=2, pady=10)

    cursor.execute("SELECT nombre FROM sucursales")
    nombres = [fila[0] for fila in cursor.fetchall()]
    if not nombres: nombres = ["No hay sucursales"]

    seleccion = tk.StringVar(ventana_sucursales)
    seleccion.set(nombres[0])

    Label(ventana_sucursales, text="Seleccione sucursal:", fg="#FCAF17", bg="#0a0a0a").grid(row=1, column=0, pady=5)
    tk.OptionMenu(ventana_sucursales, seleccion, *nombres).grid(row=1, column=1, pady=5)

    Label(ventana_sucursales, text="Escriba el nombre de la sucursal", fg="#FCAF17", bg="#0a0a0a").grid(row=2, column=0, pady=5)
    nombre_sucursal = Entry(ventana_sucursales)
    nombre_sucursal.grid(row=2, column=1, pady=5)

    Label(ventana_sucursales, text="Escriba la direccion", fg="#FCAF17", bg="#0a0a0a").grid(row=3, column=0, pady=5)
    direccion_sucursal = Entry(ventana_sucursales)
    direccion_sucursal.grid(row=3, column=1, pady=5)

    def agregar_nueva_sucursal():
        nombre = nombre_sucursal.get()
        direccion = direccion_sucursal.get()
        if nombre == "" or direccion == "":
            mensaje.config(text="Complete todos los campos", fg="red") 
            return          
        nueva_sucursal = Sucursal(None, nombre, direccion)
        cursor.execute("INSERT INTO sucursales(nombre,direccion) VALUES (?,?)", (nueva_sucursal.nombre, nueva_sucursal.direccion))
        conexion.commit()
        mensaje.config(text=f"Sucursal '{nueva_sucursal.nombre}' agregada.", fg="#00FF00")
        nombre_sucursal.delete(0, tk.END)
        direccion_sucursal.delete(0, tk.END)
    def mostrar_sucursal_y_empleados():
        id_buscar = seleccion.get()
        if id_buscar == "":
            mensaje.config(text="Escriba un ID para buscar", fg="red")
            return
        cursor.execute("SELECT id, nombre, direccion FROM sucursales WHERE id = ?", (id_buscar,))
        resultado = cursor.fetchone()
        
        if resultado:
            sucursal_encontrada = Sucursal(resultado[0], resultado[1], resultado[2])
            texto_final = sucursal_encontrada.mostrar_datos() + sucursal_encontrada.ver_empleados()
            mensaje.config(text=texto_final, fg="#00FF00")
        else:
            mensaje.config(text="No existe sucursal con ese ID", fg="red")
            
    def eliminar_todas_las_sucursales():
        cursor.execute("DROP TABLE IF EXISTS sucursales")
        conexion.commit()
        mensaje.config(text="Tabla de sucursales eliminada.", fg="red")
    def crear_nueva_base_de_datos_sucursales():
        cursor.execute(""" CREATE TABLE IF NOT EXISTS sucursales(id INTEGER PRIMARY KEY AUTOINCREMENT,nombre TEXT NOT NULL,direccion TEXT NOT NULL)""")
        conexion.commit()
        mensaje.config(text="Tabla de sucursales creada de nuevo.", fg="#00FF00")

    # Botones de Sucursales
    Button(ventana_sucursales, text="Mostrar sucursal", command=mostrar_sucursal_y_empleados, bg="#FCAF17").grid(row=4, column=0, columnspan=2, pady=5)
    Button(ventana_sucursales, text="Añadir sucursal", command=agregar_nueva_sucursal, bg="#E3000F").grid(row=4, column=3, columnspan=2, pady=5)
    Button(ventana_sucursales, text="Crear base de datos nueva", command=crear_nueva_base_de_datos_sucursales,fg="#ffffff",bg="#000000").grid(row=5, column=0, columnspan=2, pady=5)
    Button(ventana_sucursales, text="Vaciar base de datos", command=eliminar_todas_las_sucursales,fg="#ffffff",bg="#000000").grid(row=5, column=4, columnspan=2, pady=5)
    Button(ventana_sucursales, text='Cerrar', command=ventana_sucursales.destroy,fg="#ffffff",bg="#000000").grid(row=8, column=1, columnspan=2, pady=10)

# ===========================================================
# VENTANA EMPLEADOS (me encargo yo)
# ===========================================================
def abrir_ventana_nombre():
    ventana_persona = tk.Toplevel(ventana)
    ventana_persona.title('Gestor de persona')
    ventana_persona.geometry('500x500')
    ventana_persona.config()
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
    def agregar_nuevo_empleado():
        nombre = persona_nombre.get()
        apellido = persona_apellido.get()
        dni = persona_DNI.get()
        nuevo_persona = Persona(nombre,apellido, dni,) # no se uso objeto, arreglar!
        cursor.execute("INSERT INTO empleados(nombre, año_inicio, asistencia, dni, sucursal_id) VALUES (?,?,?,?,?)",(nuevo_persona.nombre, nuevo_persona.apellido, nuevo_persona.dni))
        conexion.commit()
        mensaje.config(text=f"Nuevo empleado {nuevo_persona.nombre} agregado.", fg="#00FF00")
        # Limpiamos
        persona_nombre.delete(0, tk.END)
        persona_apellido.delete(0,tk.END)
        persona_DNI.delete(0, tk.END)
        
    def mostrar_persona():
        nombre_buscar = persona_nombre.get() 
        if nombre_buscar == "":
            mensaje.config(text="No se encuentra la persona que busca", fg="red")
            return
        cursor.execute("SELECT id, nombre,año_inicio,asistencia,dni,sucursal_id FROM empleados WHERE id = ?", (nombre_buscar,))
        resultado = cursor.fetchone()
        
        if resultado:
            empleado_encontrado = Persona(resultado[0], resultado[1], resultado[2],resultado[3],resultado[4],resultado[5])
            texto_final = empleado_encontrado.mostrar_informacion() 
            mensaje.config(text=texto_final, fg="#00FF00")
        else:
            mensaje.config(text="No existe el empleado solicitado con ese ID", fg="red")
    def eliminar_todos_los_archivos_empleados():
        cursor.execute("DROP TABLE IF EXISTS empleados")
        conexion.commit()
        mensaje.config(text="Tabla de empleados eliminada.", fg="red")
    def crear_nueva_base_de_datos_empleados():
        cursor.execute("""CREATE TABLE IF NOT EXISTS empleados(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre TEXT NOT NULL, 
        año_inicio INTEGER,
        asistencia INTEGER, 
        dni INTEGER,
        sucursal_id INTEGER, 
        FOREIGN KEY (sucursal_id) REFERENCES sucursales(id))""")
        conexion.commit()
        mensaje.config(text="Tabla de empleados creada de nuevo.", fg="#00FF00")
    # Botones de Sucursales
    Button(ventana_persona, text="Mostrar empleados",  bg="#FCAF17").grid(row=4, column=0, columnspan=1, pady=5)
    Button(ventana_persona, text="Añadir empleados",  bg="#E3000F", fg="white").grid(row=4,column=1, columnspan=1, pady=5)
    Button(ventana_persona, text="Crear base de datos nueva de empleados", fg="#ffffff",bg="#000000").grid(row=4, column=2,columnspan=2, pady=5)
    Button(ventana_persona, text="Vaciar base de datos", fg="#ffffff",bg="#000000").grid(row=4, column=4, columnspan=2, pady=5)
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
btn_sucursales = Button(frame_botones, text="VER ARCHIVOS",command= abrir_ventana_nombre,bg=ROJO_ROCKSTAR, fg="white", font=("Arial", 10, "bold"), width=15)
btn_sucursales.grid(row=0, column=0, padx=10)

btn_empleados = Button(frame_botones, text="GESTIONAR PERSONAS", command= abrir_ventana_nombre,bg=AMARILLO_ROCKSTAR, fg="black", font=("Arial", 10, "bold"), width=15)
btn_empleados.grid(row=0, column=1, padx=10)

btn_cerrar = Button(frame_botones, text="CERRAR", command=ventana.destroy, bg="gray", fg="white", font=("Arial", 10, "bold"), width=10)
btn_cerrar.grid(row=0, column=2, padx=10)

ventana.mainloop()