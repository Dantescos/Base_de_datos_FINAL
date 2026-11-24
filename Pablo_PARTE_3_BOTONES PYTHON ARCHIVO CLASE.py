import tkinter as tk
from tkinter import messagebox, ttk

# --- 1. FUNCIONES (ACCIONES DE LOS BOTONES) ---

contador = 0


def accion_simple():
    """Muestra una ventana emergente al hacer clic."""
    messagebox.showinfo("Aviso", "¡Hiciste clic en el botón simple!")


def contar_clics():
    """Actualiza el texto de una etiqueta cada vez que se presiona."""
    global contador
    contador += 1
    etiqueta_estado.config(text=f"Clics realizados: {contador}")


def alternar_estado():
    """Activa o desactiva el botón objetivo."""
    if boton_objetivo["state"] == tk.NORMAL:
        boton_objetivo.config(state=tk.DISABLED, text="Estoy deshabilitado")
    else:
        boton_objetivo.config(state=tk.NORMAL, text="Estoy habilitado")


def accion_con_parametro(nombre):
    """Recibe un argumento usando una función lambda."""
    etiqueta_estado.config(text=f"Hola, {nombre}. ¡Botón presionado!")


# --- 2. CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---

ventana = tk.Tk()
ventana.title("Ejemplos de Botones en Python")
ventana.geometry("400x420")
ventana.config(padx=20, pady=20)

# Etiqueta superior para mostrar resultados
etiqueta_estado = tk.Label(
    ventana,
    text="Presiona cualquier botón para probar",
    font=("Arial", 12, "bold"),
    fg="#333333",
)
etiqueta_estado.pack(pady=(0, 20))


# --- 3. CREACIÓN DE DISTINTOS TIPOS DE BOTONES ---

# A. Botón básico con ventana emergente
btn_basico = tk.Button(
    ventana, text="1. Botón Básico (Alerta)", command=accion_simple, width=30
)
btn_basico.pack(pady=5)

# B. Botón personalizado (colores, fuente, relieve y cursor)
btn_personalizado = tk.Button(
    ventana,
    text="2. Sumar Clic (+1)",
    command=contar_clics,
    bg="#4CAF50",  # Color de fondo
    fg="white",  # Color del texto
    activebackground="#45a049",  # Color al mantener presionado
    activeforeground="white",
    font=("Arial", 11, "bold"),
    relief=tk.RAISED,  # Estilo de borde (FLAT, RAISED, SUNKEN, GROOVE, RIDGE)
    bd=3,  # Grosor del borde
    cursor="hand2",  # Cambia el cursor a una mano
    width=28,
)
btn_personalizado.pack(pady=10)

# C. Botón que envía parámetros (usando lambda)
btn_parametro = tk.Button(
    ventana,
    text="3. Saludar a Usuario",
    command=lambda: accion_con_parametro("Usuario"),
    bg="#2196F3",
    fg="white",
    font=("Arial", 10),
    width=30,
)
btn_parametro.pack(pady=5)

# D. Botón moderno usando el módulo ttk (adapta el estilo al sistema operativo)
btn_moderno = ttk.Button(
    ventana,
    text="4. Botón Moderno (ttk)",
    command=lambda: etiqueta_estado.config(text="Usaste un botón ttk"),
    width=32,
)
btn_moderno.pack(pady=10)

# E. Control de estados (Habilitado / Deshabilitado)
frame_estados = tk.Frame(ventana)
frame_estados.pack(pady=15)

boton_objetivo = tk.Button(
    frame_estados,
    text="Estoy habilitado",
    command=lambda: messagebox.showinfo("Estado", "¡El botón funciona!"),
    width=18,
)
boton_objetivo.pack(side=tk.LEFT, padx=5)

btn_interruptor = tk.Button(
    frame_estados,
    text="Bloquear / Activar",
    command=alternar_estado,
    bg="#FF9800",
    fg="white",
    width=15,
)
btn_interruptor.pack(side=tk.LEFT, padx=5)

# F. Botón para cerrar la aplicación
btn_salir = tk.Button(
    ventana,
    text="Salir del programa",
    command=ventana.destroy,
    bg="#f44336",
    fg="white",
    width=30,
)
btn_salir.pack(side=tk.BOTTOM, pady=10)


# --- 4. INICIAR EL BUCLE DE LA APLICACIÓN ---
ventana.mainloop()
