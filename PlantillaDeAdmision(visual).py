#plantilla de admision, dni foto y foto de ambos lados, buscar por nombre y apellido, recuadros de lista: nombre, apellido, dni, fecha de ingreso

#codigo de agregar imagenes
#formulario


#AZUL PETROLEO Y BLANCO HUESO

import sqlite3
import tkinter as tk
from tkinter import Label, Button, Entry, Frame, Toplevel

# ===========================================================
# CONEXION A BASE DE DATOS
# ===========================================================
conexion = sqlite3.connect("Tabla_sucursales.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(""" CREATE TABLE IF NOT EXISTS sucursales(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
direccion TEXT NOT NULL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS empleados(
id INTEGER PRIMARY KEY AUTOINCREMENT, 
nombre TEXT NOT NULL, 
año_inicio INTEGER,
asistencia INTEGER, 
dni INTEGER,
sucursal_id INTEGER, 
FOREIGN KEY (sucursal_id) REFERENCES sucursales(id))""")
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
class Empleado:
    def __init__(self,nombre,año_inicio,asistencia,dni,sucursal_id):
        self.nombre= nombre
        self.año_inicio = año_inicio
        self.asistencia = asistencia
        self.dni = dni
        self.sucursal_id = sucursal_id #aca lo hago composicion , es un intento a ver si me sale
    def mostrar_informacion(self):
        return f"El empleado es {self.nombre},cuyo DNI es: {self.dni}, emepezo a trabajar en la sucursal {self.sucursal_id} en el {self.año_inicio} año, lleva {self.asistencia} dias trabajando"
# ===========================================================
# VENTANA SUCURSALES
# ===========================================================
def abrir_ventana_sucursales():
    ventana_sucursales = Toplevel(ventana)
    ventana_sucursales.title('Mostrar informacion')
    ventana_sucursales.geometry('800x850')
    ventana_sucursales.config(bg=VERDE_AZULADO) # Fondo terminal

    mensaje = Label(ventana_sucursales, text="", fg="#00FF00", bg=VERDE_AZULADO, justify="left")
    mensaje.grid(row=0, column=0, columnspan=2, pady=10)

    cursor.execute("SELECT nombre FROM sucursales")
    nombres = [fila[0] for fila in cursor.fetchall()]
    if not nombres: nombres = ["No hay ningun nombre registrado"]

    seleccion = tk.StringVar(ventana_sucursales)
    seleccion.set(nombres[0])

    Label(ventana_sucursales, text="Seleccione a la persona:", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=1, column=0, pady=5)
    tk.OptionMenu(ventana_sucursales, seleccion, *nombres).grid(row=1, column=1, pady=5)

    Label(ventana_sucursales, text="Escriba el nombre", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=2, column=0, pady=5)
    nombre_sucursal = Entry(ventana_sucursales)
    nombre_sucursal.grid(row=2, column=1, pady=5)

    Label(ventana_sucursales, text="Escriba el apellido", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=3, column=0, pady=5)
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
            mensaje.config(text="Escriba un ID para buscar", fg="red",bg=VERDE_AZULADO)
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
    Button(ventana_sucursales, text="Mostrar persona", command=mostrar_sucursal_y_empleados, bg=AZUL_PETROLEO, fg="white" ).grid(row=4, column=0, columnspan=2, pady=5)
    Button(ventana_sucursales, text="Añadir persona", command=agregar_nueva_sucursal, bg=BLANCO_HUESO, fg="black").grid(row=4, column=3, columnspan=2, pady=5)
    Button(ventana_sucursales, text="Crear base de datos nueva", command=crear_nueva_base_de_datos_sucursales,fg="#ffffff",bg="#000000").grid(row=5, column=0, columnspan=2, pady=5)
    Button(ventana_sucursales, text="Vaciar base de datos", command=eliminar_todas_las_sucursales,fg="#ffffff",bg="#000000").grid(row=5, column=4, columnspan=2, pady=5)
    Button(ventana_sucursales, text='Cerrar', command=ventana_sucursales.destroy,fg="#ffffff",bg="#000000").grid(row=8, column=1, columnspan=2, pady=10)

# ===========================================================
# VENTANA EMPLEADOS
# ===========================================================
def abrir_ventana_empleados():
    ventana_empleados = tk.Toplevel(ventana)
    ventana_empleados.title('CRUD')
    ventana_empleados.geometry('800x800')
    ventana_empleados.config(bg=VERDE_AZULADO)
    mensaje = Label(ventana_empleados, text="", fg="#00FF00", bg="#0a0a0a", justify="left")
    mensaje.grid(row=6, column=0, columnspan=7, pady=10)
    #ACA ESCRIBO LAS ENTRADAS ASI ME FUNCIONA LAS FUNCIONES Y OBTIENEN LOS DATOS
    Label(ventana_empleados,text="Escriba el ID del empleado", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row = 0,column=0,pady=5)
    empleado_id = tk.Entry(ventana_empleados)
    empleado_id.grid(row = 1,column=0,pady=5)
    Label(ventana_empleados, text="Escriba el nombre", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row= 0,column=1,pady=5)
    empleado_nombre = tk.Entry(ventana_empleados)
    empleado_nombre.grid(row=1,column=1,pady=5)   
    Label(ventana_empleados, text="Fecha de ingreso", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=0,column=3,pady=5)
    empleado_DNI = tk.Entry(ventana_empleados)
    empleado_DNI.grid(row=1,column=3,pady=5)    
    Label(ventana_empleados, text="Escriba los dias trabajados", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=0,column=4,pady=5)
    empleado_dias = tk.Entry(ventana_empleados)
    empleado_dias.grid(row=1,column=4,pady=5)   
    Label(ventana_empleados, text="Escriba las asistencias", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=0,column=5,pady=5)
    empleado_asistencia = tk.Entry(ventana_empleados)
    empleado_asistencia.grid(row=1,column=5,pady=5) 
    Label(ventana_empleados, text="Escriba el ID de la sucursal", fg=BLANCO_HUESO, bg=VERDE_AZULADO).grid(row=0, column=6, pady=5)
    empleado_sucursal_id = tk.Entry(ventana_empleados)
    empleado_sucursal_id.grid(row=1, column=6, pady=5)
    def agregar_nuevo_empleado():
        nombre = empleado_nombre.get()
        dni = empleado_DNI.get()
        años = empleado_dias.get()
        asistencia = empleado_asistencia.get()
        sucursal_id = empleado_sucursal_id.get()
        nuevo_empleado = Empleado(nombre, años, asistencia, dni, sucursal_id)
        cursor.execute("INSERT INTO empleados(nombre, año_inicio, asistencia, dni, sucursal_id) VALUES (?,?,?,?,?)",(nuevo_empleado.nombre, nuevo_empleado.año_inicio, nuevo_empleado.asistencia, nuevo_empleado.dni, nuevo_empleado.sucursal_id))
        conexion.commit()
        mensaje.config(text=f"Nuevo empleado {nuevo_empleado.nombre} agregado.", fg="#00FF00")
        # Limpiamos
        empleado_nombre.delete(0, tk.END)
        empleado_DNI.delete(0, tk.END)
        empleado_dias.delete(0,tk.END)
        empleado_asistencia.delete(0,tk.END)
        empleado_sucursal_id.delete(0,tk.END)
    def mostrar_empleados():
        id_buscar = empleado_id.get() 
        if id_buscar == "":
            mensaje.config(text="Escriba un nombre para buscar", fg="red",bg=VERDE_AZULADO)
            return
        cursor.execute("SELECT id, nombre,año_inicio,asistencia,dni,sucursal_id FROM empleados WHERE id = ?", (id_buscar,))
        resultado = cursor.fetchone()
        
        if resultado:
            empleado_encontrado = Empleado(resultado[0], resultado[1], resultado[2],resultado[3],resultado[4],resultado[5])
            texto_final = empleado_encontrado.mostrar_informacion() 
            mensaje.config(text=texto_final, fg="#00FF00")
        else:
            mensaje.config(text="No existe el empleado solicitado con ese ID", fg="red",bg=VERDE_AZULADO)
    def eliminar_todos_los_archivos_empleados():
        cursor.execute("DROP TABLE IF EXISTS empleados")
        conexion.commit()
        mensaje.config(text="Tabla de personas eliminadas.", fg="red",bg=VERDE_AZULADO)
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
        mensaje.config(text="Tabla de empleados creada de nuevo.", fg="#00FF00",bg=VERDE_AZULADO)
    # Botones de Sucursales
    Button(ventana_empleados, text="Mostrar persona", command=mostrar_empleados, bg=AZUL_PETROLEO, fg="white").grid(row=4, column=0, columnspan=1, pady=5)
    Button(ventana_empleados, text="Añadir persona", command=agregar_nuevo_empleado, bg=BLANCO_HUESO, fg="black").grid(row=4,column=1, columnspan=1, pady=5)
    Button(ventana_empleados, text="Crear base de datos nueva de empleados", command=crear_nueva_base_de_datos_empleados,fg="#ffffff",bg="#000000").grid(row=4, column=2,columnspan=2, pady=5)
    Button(ventana_empleados, text="Vaciar base de datos", command=eliminar_todos_los_archivos_empleados,fg="#ffffff",bg="#000000").grid(row=4, column=4, columnspan=2, pady=5)
    Button(ventana_empleados, text='Cerrar', command=ventana_empleados.destroy,fg="#ffffff",bg="#000000").grid(row=5, column=2, columnspan=2, pady=10)
# ===========================================================
# VENTANA PRINCIPAL (DISEÑO ROCKSTAR TERMINAL)
# ===========================================================
# --- PALETA DE COLORES ---
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_AZULADO = "#008080"
VERDE_TERMINAL = "#00FF00"

ventana = tk.Tk()
ventana.title("Inicio")
ventana.geometry("800x850")
ventana.config(bg=VERDE_AZULADO) # Fondo general negro
mensaje = Label(ventana,text="")


# Configuramos las columnas para que el centro se estire
ventana.grid_columnconfigure(1, weight=1)

# --- 1. BANNER ROJO ARRIBA (Fila 0) ---
# Usamos columnspan=3 para que ocupe todo el ancho
banner_rojo = Frame(ventana, bg=AZUL_PETROLEO, height=80)
banner_rojo.grid(row=0, column=0, columnspan=3, sticky="ew")
Label(banner_rojo, text="MANAGER DE DATOS", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Courier", 20, "bold")).pack(pady=20)

# --- 2. COSTADOS AMARILLOS (Fila 1) ---
# Margen Izquierdo
frame_izq = Frame(ventana, bg=BLANCO_HUESO, width=40)
frame_izq.grid(row=1, column=0, sticky="ns")
# Margen Derecho
frame_der = Frame(ventana, bg=BLANCO_HUESO, width=40)
frame_der.grid(row=1, column=2, sticky="ns")

# --- 3. CENTRO (Fila 1) - Estilo Consola ---
frame_centro = Frame(ventana, bg=VERDE_AZULADO)
frame_centro.grid(row=1, column=1, sticky="nsew")
Label(frame_centro, text=" Seleccione una opcion abajo.", 
      bg=VERDE_AZULADO, fg=BLANCO_HUESO, font=("Courier", 12), justify="left").pack(pady=40)

# --- 4. BOTONES ABAJO (Fila 2) ---
frame_botones = Frame(ventana, bg=VERDE_AZULADO)
# Ocupa las 3 columnas para que quede centrado abajo
frame_botones.grid(row=2, column=0, columnspan=3, pady=20)

# Usamos grid para poner los botones uno al lado del otro
btn_sucursales = Button(frame_botones, text="Nombres", command=abrir_ventana_sucursales, bg=AZUL_PETROLEO, fg="white", font=("Arial", 10, "bold"), width=15)
btn_sucursales.grid(row=0, column=0, padx=10)

btn_empleados = Button(frame_botones, text="CRUD", command=abrir_ventana_empleados, bg=BLANCO_HUESO, fg="black", font=("Arial", 10, "bold"), width=15)
btn_empleados.grid(row=0, column=1, padx=10)

btn_cerrar = Button(frame_botones, text="CERRAR", command=ventana.destroy, bg="gray", fg="white", font=("Arial", 10, "bold"), width=10)
btn_cerrar.grid(row=0, column=2, padx=10)

ventana.mainloop()


