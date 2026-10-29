import string
#
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from io import BytesIO
#from PIL import Image, ImageTk
from tkinter import Label, Button, Entry, Frame, Toplevel

# ===========================================================
# BASE DE DATOS
# ===========================================================
conexion = sqlite3.connect("Trabajo_FIN.db")
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
# ===========================================================================================================
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
# BOTONES
tk.Button(frame_btn, text="Agregar", command=agregar, bg=VERDE_AZULADO,fg="white",width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)
tk.Button(frame_btn, text="Eliminar", command=eliminar, bg=VERDE_AZULADO, fg="white", width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)
tk.Button(frame_btn, text="Buscar", command=buscar, bg=VERDE_AZULADO, fg="white",width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)
tk.Button(frame_btn, text="Limpiar", command=limpiar, bg=VERDE_AZULADO, fg="white",width=12,activebackground=AMARILLO, activeforeground="white").pack(side="left", padx=5)

# ======================================================================================================
def comprobar(i_del_for,entry_,orden):
    variable=entry_.get()
    if variable=="":
        return i_del_for[orden]
    else:
        return variable

def comprobar_fecha(entry_fecha):
    fecha=entry_fecha.get()
    for i in string.punctuation:
        fecha=fecha.replace(i,"/")
    return str(fecha)
# =====================================================================================================
#CRUD entrevistas
def new_entrevista():
    entrevista=text_entrevista.get("1.0",tk.END)
    dni=entry_dni.get()
    nom_profecional=entry_nombre_profecional.get()
    fecha=comprobar_fecha(entry_fecha)
    cursor.execute("INSERT INTO entrevistas (entrevista,dni,nombre_profecional,fecha) VALUES (?,?,?,?)",(entrevista,dni,nom_profecional,fecha))
    conexion.commit()
    ver_list_entrevist()
    
def pantalla_edit_entrevista():
    ventana_editar=tk.Toplevel(ventana)
    ventana_editar.title("edit_entrevista")
    ventana_editar.geometry("300x200")
    label_id=tk.Label(ventana_editar,text="ingrese el ID de la entrevista que desea editar")
    label_id.pack()
    entry_id=tk.Entry(ventana_editar)
    entry_id.pack()

    label_entrevista=tk.Label(ventana_editar, text="entrevista")
    label_entrevista.pack()
    text_entrevista=tk.Text(ventana_editar)
    text_entrevista.pack()

    label_dni=tk.Label(ventana_editar, text="dni")
    label_dni.pack()
    entry_dni=tk.Entry(ventana_editar)
    entry_dni.pack()

    label_nombre_profecional=tk.Label(ventana_editar, text="nombre_profecional")
    label_nombre_profecional.pack()
    entry_nombre_profecional=tk.Entry(ventana_editar)
    entry_nombre_profecional.pack()

    label_fecha=tk.Label(ventana_editar, text="fecha")
    label_fecha.pack()
    entry_fecha=tk.Entry(ventana_editar)
    entry_fecha.pack()

    def edit_entrevista(): #ventana nueva
        p_id=entry_id.get()
        cursor.execute("SELECT * FROM entrevistas")
        entrevistas=cursor.fetchall()
        for entrevista in entrevistas:
            if int(p_id)==entrevista[0]:
                entrevist=text_entrevista.get("1.0",tk.END)
                if entrevist.strip()=="":
                    entrevist=entrevista[1]
                dni=comprobar(entrevista,entry_dni,2)
                nom_profecional=comprobar(entrevista,entry_nombre_profecional,3)
                fecha=entry_fecha.get()
                if fecha=="":
                    fecha=entrevista[4]
                else:
                    fecha=comprobar_fecha(entry_fecha)
                conexion.execute("UPDATE entrevistas SET entrevista = ?, dni = ?, nombre_profecional = ?, fecha = ? WHERE id = ?",(entrevist,dni,nom_profecional,fecha,p_id))
                conexion.commit()
                break
        ver_list_entrevist()
    boton_edit_entrevista=tk.Button(ventana_editar,text="editar_entrevista",command=edit_entrevista)
    boton_edit_entrevista.pack()
    
def eliminar_entrevista():
    p_dni=entry_dni.get()
    cursor.execute("DELETE FROM entrevistas WHERE dni = ?",(p_dni,))
    conexion.commit()
    ver_list_entrevist()

def ver_list_entrevist():
    lista_entrevistas.delete(0, tk.END)
    cursor.execute("SELECT * FROM entrevistas")
    for i in cursor.fetchall():
        dato=f"ID: {i[0]} // Fecha: {i[4]} // DNI: {i[2]} // Profecional: {i[3]} // Entrevista: {i[1]}"
        lista_entrevistas.insert(tk.END, dato)
# ===================================================================================================
def detalles_entrevsit(event=None):
    seleccion=lista_entrevistas.curselection()
    if seleccion:
        dato=lista_entrevistas.get(seleccion)
        datos=dato.split("//")

        ventana_entrevista=tk.Toplevel(ventana)
        ventana_entrevista.title("entrevista")
        ventana_entrevista.geometry("300x200")

        label_dato_fecha=tk.Label(ventana_entrevista,text=datos[1])
        label_dato_fecha.pack()
        label_dato_dni=tk.Label(ventana_entrevista,text=datos[2])
        label_dato_dni.pack()
        label_dato_profecional=tk.Label(ventana_entrevista,text=datos[3])
        label_dato_profecional.pack()

        text_dato_entrevista=tk.Text(ventana_entrevista)
        text_dato_entrevista.pack()
        text_dato_entrevista.insert("1.0",datos[4])
        text_dato_entrevista.config(state=tk.DISABLED)


ventana_entrevista = tk.Toplevel(ventana) 
lista_entrevistas=tk.Listbox(ventana_entrevista)
lista_entrevistas.pack()

lista_entrevistas.bind("<<ListboxSelect>>",detalles_entrevsit)

ver_list_entrevist()

label_entrevista=tk.Label(ventana_entrevista, text="entrevista")
label_entrevista.pack()
text_entrevista=tk.Text(ventana_entrevista)
text_entrevista.pack()

label_dni=tk.Label(ventana_entrevista, text="dni")
label_dni.pack()
entry_dni=tk.Entry(ventana_entrevista)
entry_dni.pack()

label_nombre_profecional=tk.Label(ventana_entrevista, text="nombre_profecional")
label_nombre_profecional.pack()
entry_nombre_profecional=tk.Entry(ventana_entrevista)
entry_nombre_profecional.pack()

label_fecha=tk.Label(ventana_entrevista, text="fecha")
label_fecha.pack()
entry_fecha=tk.Entry(ventana_entrevista)
entry_fecha.pack()

boton_new_entrevista=tk.Button(ventana_entrevista,text="new_entrevista",command=new_entrevista)
boton_new_entrevista.pack()

boton_ventana_edit_entrevista=tk.Button(ventana,text="pantalla_edit_entrevista",command=pantalla_edit_entrevista)
boton_ventana_edit_entrevista.pack()
boton_eliminar_entrevista=tk.Button(ventana,text="eliminar_entrevista",command=eliminar_entrevista)
boton_eliminar_entrevista.pack()

tk.Button(frame_btn, text="Entrevistas", command= ventana_entrevista,bg=AZUL_PETROLEO, fg="white",activebackground=AMARILLO, activeforeground="white", width=12).pack(side="left", padx=5)

ventana.mainloop()
