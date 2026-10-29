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
    nombre = entrada_nombre.get().strip()
    anios = entrada_anios.get().strip()
    dni = entrada_dni.get().strip()
    justificadas = entrada_justificadas.get().strip()
    
    if nombre and anios and dni and justificadas:
        

        registro = (f"Nombre: {nombre} | Apellido: {anios} | DNI: {dni} | "
                    f"Fecha de ingreso: {justificadas} ")
        
        lista_empleados.insert(tk.END, registro)
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
        
     
        limpiar_formulario()
        
       
        partes = [p.split(": ")[1] for p in texto_registro.split(" | ")]
        
       
        entrada_nombre.insert(0, partes[0])
        entrada_anios.insert(0, partes[1])
        entrada_dni.insert(0, partes[2])
        entrada_justificadas.insert(0, partes[4])
    except IndexError:
        pass 


def guardar_edicion():
    global indice_edicion
    if indice_edicion is not None:
        nombre = entrada_nombre.get().strip()
        anios = entrada_anios.get().strip()
        dni = entrada_dni.get().strip()
        justificadas = entrada_justificadas.get().strip()
        
        if nombre and anios and dni and justificadas:
            
            registro_actualizado = (f"Nombre: {nombre} | Apellido: {anios} | DNI: {dni} | "
                                    f"Fecha de ingreso: {justificadas} ")
            

            lista_empleados.delete(indice_edicion)
            lista_empleados.insert(indice_edicion, registro_actualizado)
            
            indice_edicion = None
            limpiar_formulario()


def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    entrada_anios.delete(0, tk.END)
    entrada_dni.delete(0, tk.END)
    entrada_justificadas.delete(0, tk.END)



indice_edicion = None


ventana = tk.Tk()
ventana.title("Datos")
ventana.geometry("920x880") 
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
entrada_anios = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_anios.pack(pady=3)

tk.Label(ventana, text="DNI:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_dni = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_dni.pack(pady=3)


tk.Label(ventana, text="Fecha de Ingreso:", font=("Consolas", 11, "bold"), bg=VERDE_AZULADO, fg="white").pack(pady=(5, 0))
entrada_justificadas = tk.Entry(ventana, font=("Consolas", 11), width=45)
entrada_justificadas.pack(pady=3)


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
    ("Kenny", "Galindo", "44555666", "21/6/2026"),
    ("Juancho", "Tazo", "11222333", "13/10/2026"),
    ("Solomeo", "Paredes", "77888999", "1/1/2026")
]

for nombre, anios, dni, justificadas in empleados_iniciales:
    registro = (f"Nombre: {nombre} | Apellido: {anios} | DNI: {dni} | "
                f"Fecha de ingreso: {justificadas}")
    lista_empleados.insert(tk.END, registro)

ventana.mainloop()

import re
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from io import BytesIO
from PIL import Image, ImageTk

# ===========================================================
# BASE DE DATOS
# ===========================================================
conexion = sqlite3.connect("Trabajo_FINAL.db")
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("""
CREATE TABLE IF NOT EXISTS personas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    dni INTEGER UNIQUE NOT NULL,
    foto BLOB
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entrevistas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni_persona INTEGER NOT NULL,
    entrevistador TEXT NOT NULL,
    fecha TEXT NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (dni_persona) REFERENCES personas(dni)
)""")
conexion.commit()

# ===========================================================
# PALETA
# ===========================================================
ROJO = "#E3000F"
AMARILLO = "#FCAF17"
NEGRO = "#0a0a0a"
VERDE = "#00FF00"
GRIS = "#222222"
AZUL_PETROLEO = "#006080"
BLANCO_HUESO = "#F5F5DC"
VERDE_AZULADO = "#008080"
VERDE_TERMINAL = "#00FF00"

# ===========================================================
# VENTANA PRINCIPAL
# ===========================================================
ventana = tk.Tk()
ventana.title("APP:GESTOR DE DATOS")
ventana.geometry("900x650")
ventana.config(bg=NEGRO)
# --- Banner ---
banner = tk.Frame(ventana,bg=AZUL_PETROLEO, height=70)
banner.pack(fill="x")
banner.pack_propagate(False)
tk.Label(banner, text="GESTOR DE DATOS", bg=AZUL_PETROLEO, fg=BLANCO_HUESO,font=("Courier", 20, "bold")).pack(pady=18)
# --- Cuerpo principal (foto + lista) ---
cuerpo = tk.Frame(ventana,bg = NEGRO)
cuerpo.pack(fill="both", expand=True, padx=15, pady=10)
# Izquierda: visor de foto
frame_foto = tk.Frame(cuerpo, bg=AZUL_PETROLEO, width=320, height=320)
frame_foto.pack(side="left", padx=10)
frame_foto.pack_propagate(False)
visor_foto = tk.Label(frame_foto, text="Sin foto", bg=VERDE_AZULADO, fg=BLANCO_HUESO)
visor_foto.pack(expand=True, fill="both")
# Derecha: lista de personas
frame_lista = tk.Frame(cuerpo, bg=NEGRO)
frame_lista.pack(side="left", fill="both", expand=True, padx=10)
tk.Label(frame_lista, text="Personas registradas", bg=NEGRO, fg=BLANCO_HUESO,font=("Courier", 12, "bold")).pack(anchor="w")
scroll = tk.Scrollbar(frame_lista, orient="vertical")
scroll.pack(side="right", fill="y")

def detalles_persona(event=None):
    seleccion=lista_personas.curselection()
    if seleccion:
        dato=lista_personas.get(seleccion)
        datos=re.split(r",\s*|\s*—\s*DNI\s*",dato)
        
        ventana_detalles_persona=tk.Toplevel(ventana)
        ventana_detalles_persona.title("detalles_persona")
        ventana_detalles_persona.geometry("300x200")
        
        label_dato_apellido=tk.Label(ventana_detalles_persona,text=f"Apellido: {datos[0]}")
        label_dato_apellido.grid()
        label_dato_nombre=tk.Label(ventana_detalles_persona,text=f"Nombre: {datos[1]}")
        label_dato_nombre.grid()
        label_dato_dni=tk.Label(ventana_detalles_persona,text=f"DNI: {datos[2]}")
        label_dato_dni.grid()
        mostrar_foto(datos[2])
        
lista_personas = tk.Listbox(frame_lista, yscrollcommand=scroll.set,font=("Consolas", 11), bg=VERDE_AZULADO, fg=NEGRO,selectbackground=AMARILLO, selectforeground=BLANCO_HUESO)
lista_personas.pack(side="left", fill="both", expand=True)
lista_personas.bind("<Double-1>",detalles_persona)
scroll.config(command=lista_personas.yview)

# --- Formulario (entries) ---
frame_form = tk.Frame(ventana, bg=NEGRO)
frame_form.pack(fill="x", padx=15, pady=10)
tk.Label(frame_form, text="Nombre:", bg=NEGRO, fg=BLANCO_HUESO).grid(row=0, column=0, sticky="e", padx=5)
entry_nombre = tk.Entry(frame_form, width=22)
entry_nombre.grid(row=0, column=1, padx=5, pady=3)
tk.Label(frame_form, text="Apellido:", bg=NEGRO, fg = BLANCO_HUESO).grid(row=0, column=2, sticky="e", padx=5)
entry_apellido = tk.Entry(frame_form, width=22)
entry_apellido.grid(row=0, column=3, padx=5, pady=3)
tk.Label(frame_form, text="DNI:", bg=NEGRO, fg=BLANCO_HUESO).grid(row=0, column=4, sticky="e", padx=5)
entry_dni = tk.Entry(frame_form, width=15)
entry_dni.grid(row=0, column=5, padx=5, pady=3)
# --- Botonera ---
frame_btn = tk.Frame(ventana, bg=NEGRO)
frame_btn.pack(pady=10)    

def refrescar_lista():
    lista_personas.delete(0, tk.END)
    cursor.execute("SELECT nombre, apellido, dni FROM personas ORDER BY apellido, nombre")
    for nombre, apellido, dni in cursor.fetchall():
        lista_personas.insert(tk.END, f"{apellido}, {nombre} — DNI {dni}")
        
def mostrar_foto(dni):
    cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if fila and fila[0]:
        try:
            img = Image.open(BytesIO(fila[0]))
            img.thumbnail((300, 300))
            foto = ImageTk.PhotoImage(img)
            visor_foto.configure(image=foto, text="")
            visor_foto.image = foto
            return
        except Exception:
            pass
    visor_foto.configure(image="", text="Sin foto")
def al_seleccionar(event=None):
    sel = lista_personas.curselection()
    if not sel: return
    texto = lista_personas.get(sel[0])
    dni = int(texto.split("DNI ")[1])
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni,))
    fila = cursor.fetchone()
    if not fila: return
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    entry_dni.delete(0, tk.END); entry_dni.insert(0, fila[2])
    mostrar_foto(dni)
lista_personas.bind("<<ListboxSelect>>", al_seleccionar)

def agregar():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni_txt = entry_dni.get().strip()
    if not (nombre and apellido and dni_txt):
        messagebox.showwarning("Faltan datos", "Completa nombre, apellido y DNI.")
        return
    try:
        dni = int(dni_txt)
    except ValueError:
        messagebox.showerror("DNI invalido", "El DNI debe ser numerico.")
        return
    ruta = filedialog.askopenfilename(title="Foto (opcional)",
        filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.webp")])
    contenido = None
    if ruta:
        with open(ruta, "rb") as f:
            contenido = sqlite3.Binary(f.read())
    try:
        cursor.execute("INSERT INTO personas (nombre, apellido, dni, foto) VALUES (?,?,?,?)",
                       (nombre, apellido, dni, contenido))
        conexion.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Ya existe una persona con ese DNI.")
        return
    refrescar_lista()
    limpiar()
    messagebox.showinfo("OK", "Persona agregada.")

def eliminar():
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atención", "Selecciona o escribi un DNI.")
        return
    if not messagebox.askyesno("Confirmar", f"¿Eliminar DNI {dni_txt}?"):
        return
    cursor.execute("DELETE FROM entrevistas WHERE dni_persona = ?", (dni_txt,))
    cursor.execute("DELETE FROM personas WHERE dni = ?", (dni_txt,))
    conexion.commit()
    refrescar_lista()
    limpiar()
    visor_foto.configure(image="", text="Sin foto")

def buscar():
    dni_txt = entry_dni.get().strip()
    if not dni_txt:
        messagebox.showwarning("Atencion", "Escribi de forma numerica un DNI para buscar.")
        return
    cursor.execute("SELECT nombre, apellido, dni FROM personas WHERE dni = ?", (dni_txt,))
    fila = cursor.fetchone()
    if not fila:
        messagebox.showinfo("Sin resultados", "No existe esa persona.")
        return
    entry_nombre.delete(0, tk.END); entry_nombre.insert(0, fila[0])
    entry_apellido.delete(0, tk.END); entry_apellido.insert(0, fila[1])
    mostrar_foto(fila[2])
    # resaltar en lista
    for i in range(lista_personas.size()):
        if f"DNI {fila[2]}" in lista_personas.get(i):
            lista_personas.selection_clear(0, tk.END)
            lista_personas.selection_set(i)
            lista_personas.see(i)
            break

def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)

tk.Button(frame_btn, text="Agregar", command=agregar, bg=VERDE_AZULADO,fg="white",width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar", command=eliminar, bg=VERDE_AZULADO, fg="white", width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", command=buscar, bg=VERDE_AZULADO, fg="white",width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar", command=limpiar, bg=VERDE_AZULADO, fg="white",width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)

# ===========================================================
# VENTANA ENTREVISTAS
# ===========================================================
def abrir_entrevistas():
    v = tk.Toplevel(ventana)
    v.title("Entrevistas")
    v.geometry("600x560")
    v.config(bg=VERDE_AZULADO)

    # ===== FORMULARIO =====
    # Frame contenedor del formulario (arriba, ocupa todo el ancho)
    form = tk.Frame(v, bg=VERDE_AZULADO)
    form.pack(side="top", fill="x", padx=15, pady=(15, 5))

    # --- Fila 1: DNI ---
    fila1 = tk.Frame(form, bg=VERDE_AZULADO)
    fila1.pack(side="top", fill="x", pady=3)
    tk.Label(fila1, text="DNI:", bg=VERDE_AZULADO, fg=BLANCO_HUESO, width=18, anchor="w").pack(side="left")
    e_dni = tk.Entry(fila1, width=20)
    e_dni.pack(side="left", padx=(0, 10))

    # --- Fila 2: Entrevistador ---
    fila2 = tk.Frame(form, bg=VERDE_AZULADO)
    fila2.pack(side="top", fill="x", pady=3)
    tk.Label(fila2, text="Entrevistador:", bg=VERDE_AZULADO, fg=BLANCO_HUESO,width=18, anchor="w").pack(side="left")
    e_entrev = tk.Entry(fila2, width=40)
    e_entrev.pack(side="left", padx=(0, 10))

    # --- Fila 3: Fecha ---
    fila3 = tk.Frame(form, bg=VERDE_AZULADO)
    fila3.pack(side="top", fill="x", pady=3)
    tk.Label(fila3, text="Fecha (DD/MM/AAAA):", bg=VERDE_AZULADO, fg=BLANCO_HUESO,width=18, anchor="w").pack(side="left")
    e_fecha = tk.Entry(fila3, width=20)
    e_fecha.pack(side="left", padx=(0, 10))

    # --- Fila 4: Observaciones ---
    fila4 = tk.Frame(form, bg=VERDE_AZULADO)
    fila4.pack(side="top", fill="x", pady=3)
    tk.Label(fila4, text="Observaciones:", bg=VERDE_AZULADO, fg=BLANCO_HUESO,width=18, anchor="w").pack(side="left")
    e_obs = tk.Entry(fila4, width=50)
    e_obs.pack(side="left", padx=(0, 10))

    # ===== LISTBOX (lo que queda, ocupa todo el resto) =====
    frame_lb = tk.Frame(v, bg=VERDE_AZULADO)
    frame_lb.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 15))

    scroll = tk.Scrollbar(frame_lb, orient="vertical")
    scroll.pack(side="right", fill="y")
    lb = tk.Listbox(frame_lb, height=10, font=("Consolas", 10),
                    bg=AZUL_PETROLEO, fg="white",
                    selectbackground=AMARILLO, selectforeground=NEGRO,
                    yscrollcommand=scroll.set)
    lb.pack(side="left", fill="both", expand=True)
    scroll.config(command=lb.yview)



    def refrescar():
        lb.delete(0, tk.END)
        cursor.execute("""SELECT id, dni_persona, entrevistador, fecha, observaciones FROM entrevistas ORDER BY fecha DESC""")
        for i, dni, ent, fec, obs in cursor.fetchall():
            lb.insert(tk.END, f"[{i}] DNI {dni} | {ent} | {fec} | {obs or ''}")

    def agregar_ent():
        dni = e_dni.get().strip()
        ent = e_entrev.get().strip()
        fec = e_fecha.get().strip()
        if not (dni and ent and fec):
            messagebox.showwarning("Faltan datos", "DNI, entrevistador y fecha son obligatorios.")
            return
        cursor.execute("SELECT 1 FROM personas WHERE dni = ?", (dni,))
        if not cursor.fetchone():
            messagebox.showerror("Error", "No existe persona con ese DNI.")
            return
        cursor.execute("INSERT INTO entrevistas (dni_persona, entrevistador, fecha, observaciones) VALUES (?,?,?,?)",dni, ent, fec, e_obs.get().strip())
        conexion.commit()
        refrescar()

    def eliminar_ent():
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("Atencion","Selecciona una entrevista.")
            return
        texto = lb.get(sel[0])
        id_ent = int(texto.split("]")[0].replace("[", ""))
        cursor.execute("DELETE FROM entrevistas WHERE id = ?", (id_ent,))
        conexion.commit()
        refrescar()

    frame_btns = tk.Frame(v, bg=VERDE_AZULADO); frame_btns.pack(pady=5)
    tk.Button(frame_btns, text="Agregar entrevista", command=agregar_ent,bg=AZUL_PETROLEO, fg=BLANCO_HUESO).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Eliminar seleccionada", command=eliminar_ent,bg=AZUL_PETROLEO, fg=BLANCO_HUESO).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Cerrar", command=v.destroy,bg=AZUL_PETROLEO, fg=BLANCO_HUESO).pack(side="left", padx=5)
    refrescar()
tk.Button(frame_btn, text="Entrevistas", command=abrir_entrevistas,bg="#008080", fg="white", width=12).pack(side="left", padx=5)

# ===========================================================
refrescar_lista()
ventana.mainloop()
