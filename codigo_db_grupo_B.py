import sqlite3
conexion=sqlite3.connect("Base_negocio.db")
cursor=conexion.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS productos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre_producto TEXT NOT NULL,
stock_disponible INTEGER,
precio INTEGER
)
""")
conexion.commit()

class Producto:
    def __init__(self,nombre_producto,stock_disponible,precio):
        self.nombre_producto   = nombre_producto
        self.stock_disponible = stock_disponible
        self.precio     = precio
    def mostrar_datos(self):
        return f"El producto es {self.nombre_producto}, Quedan {self.stock_disponible} copias del producto, cuesta ${self.precio} pesos"

def mostrar_lista():
    cursor.execute("SELECT * FROM productos")
    productos= cursor.fetchall()
    if not productos:
        print("No hay productos")
        return
    texto = "--- Productos ---\n"
    for producto in productos:
        # producto = (id, nombre_producto, stock_disponible, precio)
        texto += f"ID: {producto[0]} "+f"Nombre: {producto[1]} " +f"Stock disponible: {producto[2]} " + f"Precio: {producto[3]} "
        print(texto)

def agregar_nuevo_producto(nombre_producto,stock_disponible,precio):
    # Valido que no esten vacios
    if nombre_producto == "" or stock_disponible == "" or precio == "":
        print("Complete todos los campos")
        return
    stock_disponible = int(stock_disponible)
    precio = int(precio)
    producto = Producto(nombre_producto,stock_disponible,precio)
    cursor.execute("INSERT INTO productos(nombre_producto,stock_disponible,precio) VALUES (?,?,?)",(producto.nombre_producto,producto.stock_disponible,producto.precio))
    conexion.commit()
    print(f"Producto agregado: {producto.mostrar_datos()}")

def eliminar_producto(nombre_producto):
    if nombre_producto =="":
        print("Campo vacio. Escriba un nombre de producto")
        return
    nombre_producto = nombre_producto
    cursor.execute("SELECT * FROM productos WHERE nombre_producto = ?",(nombre_producto,))
    producto = cursor.fetchone()

    if not producto:
        print("No hay registro para ese producto")
        return
    cursor.execute("DELETE FROM productos WHERE nombre_producto = ?",(nombre_producto,))
    conexion.commit()
    print("Producto eliminado correctamente")

#Prueba interna- Puede eliminarse luego
while True:
    print("MENU")
    print("0. Salir")
    print("1. Agregar")
    print("2. Eliminar")
    print("3. Mostrar lista")
    op=input("Seleccione opcion\n")
    if op=="0":
        conexion.close()
        break
    elif op=="1":
        print("Ingrese los datos de su producto")
        nombre_producto=input("Nombre del producto\n")
        stock_disponible=int(input("Stock disponible\n"))
        precio=int(input("Precio\n"))
        agregar_nuevo_producto(nombre_producto,stock_disponible,precio)
    elif op=="2":
        print("Ingrese el nombre de su producto")
        nombre_producto=input("Nombre del producto\n")
        eliminar_producto(nombre_producto)
    elif op=="3":
        mostrar_lista()
    else:
        print("opcion invalida")
