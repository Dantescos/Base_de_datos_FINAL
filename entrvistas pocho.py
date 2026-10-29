#plantilla de admision, dni foto y foto de ambos lados, buscar por nombre y apellido, recuadros de lista: nombre, apellido, dni, fecha de ingreso

#codigo de agregar imagenes
#formulario

import tkinter as tk
from tkinter import ttk,font

AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_AZULADO = "#008080"
VERDE_TERMINAL = "#00FF00"


def agregar_empleado():
    datos = obtener_datos_empleado()
    if all(datos[:4]):
        lista_empleados.insert(tk.END, formatear_empleado(datos))
        limpiar_formulario()


def eliminar_empleado():
    try:
        indice_seleccionado = lista_empleados.curselection()[0]
        lista_empleados.delete(indice_seleccionado)
    except IndexError:
        pass


def cargar_empleado_a_editar():
    global indice_edicion
    try:
        indice_edicion = lista_empleados.curselection()[0]
        texto_registro = lista_empleados.get(indice_edicion)
    except IndexError:
        return

    partes = [parte.split(": ", 1)[1] for parte in texto_registro.split(" | ")]
    if len(partes) != len(entradas_formulario):
        return

    limpiar_formulario()
    for entrada, valor in zip(entradas_formulario, partes):
        entrada.insert(0, valor)


def guardar_edicion():
    global indice_edicion
    if indice_edicion is not None:
        datos = obtener_datos_empleado()
        if all(datos[:4]):
            registro_actualizado = formatear_empleado(datos)
            lista_empleados.delete(indice_edicion)
            lista_empleados.insert(indice_edicion, registro_actualizado)
            indice_edicion = None
            limpiar_formulario()


def limpiar_formulario():
    for entrada in entradas_formulario:
        entrada.delete(0, tk.END)


def obtener_datos_empleado():
    return tuple(entrada.get().strip() for entrada in entradas_formulario)


def formatear_empleado(datos):
    etiquetas = (
        "Nombre", "Apellido", "DNI", "Fecha de ingreso",
        "Fecha entrevista", "Resultado", "Observaciones",
    )
    return " | ".join(
        f"{etiqueta}: {valor}" for etiqueta, valor in zip(etiquetas, datos)
    )



indice_edicion = None


ventana = tk.Tk()
ventana.title("Datos")
ventana.geometry("920x980")
ventana.configure(bg=VERDE_AZULADO)


encabezado = tk.Frame(ventana, height=105, bg=AZUL_PETROLEO)
encabezado.pack(fill="x")
encabezado.pack_propagate(False)

tk.Label(
    encabezado,
    text="BASE DE DATOS",
    font=("Consolas", 25, "bold"),
    bg=AZUL_PETROLEO,
    fg="black",
).pack(anchor="center", pady=(28, 0))

marco_titulo = tk.Frame(ventana, bg=BLANCO_HUESO, height=20)
marco_titulo.pack(fill="x", side="top")

estilo = ttk.Style()
estilo.theme_use("clam")


marco_lista = tk.Frame(ventana, bg=AZUL_PETROLEO)
marco_lista.pack(pady=20, fill="both", expand=True, padx=50)

scrollbar = tk.Scrollbar(marco_lista, orient="vertical")
scrollbar.pack(side="right", fill="y")
scrollbar.config(bg=AZUL_PETROLEO)
lista_empleados = tk.Listbox(
    marco_lista, 
    font=("Consolas", 10), 
    bg=VERDE_AZULADO, 
    fg="white", 
    selectbackground="#fffefe", 
    selectforeground="black",
    yscrollcommand=scrollbar.set
)
lista_empleados.pack(side="left", fill="both", expand=True)
scrollbar.config(command=lista_empleados.yview)




tk.Label(ventana, text="Nombre:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_nombre = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_nombre.pack(pady=3)

tk.Label(ventana, text="Apellido:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_apellido = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_apellido.pack(pady=3)

tk.Label(ventana, text="DNI:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_dni = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_dni.pack(pady=3)


tk.Label(ventana, text="Fecha de Ingreso:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_fecha_ingreso = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_fecha_ingreso.pack(pady=3)

tk.Label(ventana, text="Fecha de entrevista:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_fecha_entrevista = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_fecha_entrevista.pack(pady=3)

tk.Label(ventana, text="Resultado:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_resultado = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_resultado.pack(pady=3)

tk.Label(ventana, text="Observaciones:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_observaciones = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_observaciones.pack(pady=3)

entradas_formulario = (
    entrada_nombre,
    entrada_apellido,
    entrada_dni,
    entrada_fecha_ingreso,
    entrada_fecha_entrevista,
    entrada_resultado,
    entrada_observaciones,
)

marco_botones = tk.Frame(ventana, bg=VERDE_AZULADO)
marco_botones.pack(pady=15)

boton_crear = tk.Button(
    marco_botones, text="Agregar Perfil", font=("Consolas", 11, "bold"),
    bg=AZUL_PETROLEO, fg="white", command=agregar_empleado, padx=8, pady=4
)
boton_crear.pack(side="left", padx=5)


boton_cargar = tk.Button(
    marco_botones, text="Seleccionar para editar", font=("Consolas", 11, "bold"),
    bg=BLANCO_HUESO, fg="black", command=cargar_empleado_a_editar, padx=8, pady=4
)
boton_cargar.pack(side="left", padx=5)

boton_actualizar = tk.Button(
    marco_botones, text="Confirmar edicion de cambios", font=("Consolas", 11, "bold"),
    bg=AZUL_PETROLEO, fg="white", command=guardar_edicion, padx=8, pady=4
)
boton_actualizar.pack(side="left", padx=5)

boton_eliminar = tk.Button(
    marco_botones, text="Eliminar Perfil", font=("Consolas", 11, "bold"),
    bg=BLANCO_HUESO, fg="black", command=eliminar_empleado, padx=8, pady=4
)
boton_eliminar.pack(side="left", padx=5)

empleados_iniciales = [
    ("Kenny", "Galindo", "44555666", "21/6/2026", "23/6/2026", "Aprobado", "Buena actitud"),
    ("Juancho", "Tazo", "11222333", "13/10/2026", "15/10/2026", "Pendiente", "Revisar documentos"),
    ("Solomeo", "Paredes", "77888999", "1/1/2026", "3/1/2026", "Aprobado", "Cumple requisitos"),
]

for empleado in empleados_iniciales:
    lista_empleados.insert(tk.END, formatear_empleado(empleado))

ventana.mainloop()


