import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO
from PIL import Image

conexion=sqlite3.connect("base de datos trabajo final.db")
cursor=conexion.cursor()
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
def agragar_data():
    t1=entrada1.get()
    t2=entrada2.get()
    t3=entrada3.get()
    if t1=="" or t2=="" or t3=="":
        print("Por favor complete los campos")
        return
    cursor.execute(          
    "INSERT INTO empleados (nombre,apellido,dni) VALUES (?,?,?)",(t1,t2,t3)           
    )
    conexion.commit()   
    ver_lista() 
       
def ver_lista():
    lista.delete(0, tk.END)
    cursor.execute("SELECT * FROM empleados")
    for u in cursor.fetchall():
        lista.insert(tk.END, u)
        print("222")


def modificar_empleado():
    dni_actual = entrada.get().strip()
    if not dni_actual:
            print("Introduce el DNI actual del empleado.")
            return
    # Buscar al empleado por su DNI actual
    cursor.execute(
        "SELECT id FROM empleados WHERE dni = ?",
        (dni_actual,)
    )
    empleados = cursor.fetchall()
    if len(empleados) == 0:
        print("Empleado no encontrado.")
        return
    if len(empleados) > 1:
           print("Hay varios empleados con ese DNI.")
           return
    # Obtener solamente los datos que se quiere modificar
    nombre = entrada1.get().strip()
    apellido = entrada2.get().strip()
    dni_nuevo = entrada3.get().strip()
    campos = []
    valores = []
    if nombre:
        campos.append("nombre = ?")
        valores.append(nombre)
    if apellido:
        campos.append("apellido = ?")
        valores.append(apellido)
    if dni_nuevo:
        if not dni_nuevo.isdigit():
                print("El nuevo DNI debe contener solo numeros.")
                return
        campos.append("dni = ?")
        valores.append(int(dni_nuevo))
    if not campos:
        print("Completa al menos un campo para modificar.")
        return
    id_empleado = empleados[0][0]
    consulta = (
        "UPDATE empleados SET "
        + ", ".join(campos)
        + " WHERE id = ?"
    )
    valores.append(id_empleado)
    cursor.execute(consulta, valores)
    conexion.commit()
    ver_lista()
    print("Datos del empleado actualizados correctamente.")

def borrar():
    dni = entrada.get().strip()
    if not dni:
        print("Introduce el DNI del empleado.")
        return
    cursor.execute(
        "SELECT id FROM empleados WHERE dni = ?",
        (dni,)
    )
    empleados = cursor.fetchall()
    if len(empleados) == 0:
        print("Resultado", "No se encontro ningun empleado.")
        return
    if len(empleados) > 1:
        print("Hay varios empleados con ese DNI.")
        return
    cursor.execute(
        "DELETE FROM empleados WHERE id = ?",
        (empleados[0][0],)
    )
    conexion.commit()
    ver_lista()
    print("Empleado eliminado correctamente.")

def buscar():    
    et=int(entrada.get())
    print("holaaaaa1")
    cursor.execute("SELECT * FROM empleados WHERE dni = ?", (et,))
    print("holaaaaa2")
    idbusca=cursor.fetchall()
    for i in idbusca:
        print("holaaaaa")
        print("paa")
        if et in i:
            busca.config(text=i) 
            print("sssssssss")
        else:
            busca.config(text="contacto no encontrado")
            print("nnnnnnnnnn")    

def agregar_imagen():
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"),
            ("Todos los archivos", ".")
        ]
    )
    if not ruta:
        return
    try:
        with open(ruta, "rb") as archivo:
            contenido = archivo.read()
        nombre = ruta.replace("\\", "/").split("/")[-1]
        formato = nombre.rsplit(".", 1)[-1].lower()  
        et=int(entrada1.get())
        cursor.execute("SELECT * FROM empleados WHERE id = ?", (et,))
        conexion.execute(
            "INSERT INTO imagenes (nombre, formato, contenido) "
            "VALUES (?, ?, ?)",
            (nombre, formato, sqlite3.Binary(contenido), et)
        )
        conexion.commit()
        messagebox.showinfo("Éxito", f"Imagen guardada: {nombre}")
    except (OSError, sqlite3.Error) as error:
        messagebox.showerror("Error", str(error))
     
ventana = tk.Tk()
ventana.title("Prueba Multiprocessing")
ventana.geometry("600x650")

resultado=tk.Label(ventana, text="DNI actual para modificar o borrar")
resultado.pack()
entrada=tk.Entry(ventana)
entrada.pack()

resultado=tk.Label(ventana, text="nombre")
resultado.pack()
entrada1=tk.Entry(ventana)
entrada1.pack()

resultado=tk.Label(ventana, text="apellido")
resultado.pack()
entrada2=tk.Entry(ventana)
entrada2.pack()

resultado=tk.Label(ventana, text="dni")
resultado.pack()
entrada3=tk.Entry(ventana)
entrada3.pack()

tk.Button(ventana,text="agregar empleado",command=agragar_data).pack()
tk.Button(ventana,text="Modificar datos del empleado",command=modificar_empleado).pack()
tk.Button(ventana,text="Borrar empleado por DNI",command=borrar).pack()
tk.Button(ventana,text="buscar a un empleado",command=buscar).pack()
tk.Button(ventana,text="Agregar imagen",command=agregar_imagen).pack()

busca=tk.Label(ventana, text="")
busca.pack()

lista=tk.Listbox(ventana, width=30, height=30)
lista.pack()
ver_lista()

visor = tk.Label(ventana, text="Tu imagen aparecerá aquí")
visor.pack(expand=True, fill="both", padx=10, pady=10)

ventana.mainloop()
