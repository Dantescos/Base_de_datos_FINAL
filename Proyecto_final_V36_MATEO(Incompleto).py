# ============================================================================
# BLOQUE 14: FUNCIONES AUXILIARES
# ============================================================================
def comprobar_fecha(entry_fecha):
    # Reemplaza signos de puntuacion por "/"
    fecha = entry_fecha.get()
    for i in string.punctuation:
        fecha = fecha.replace(i, "/")
    return str(fecha)

def ver_list_entrevist(lista_widget):
    # Llena el Listbox de entrevistas
    lista_widget.delete(0, tk.END)
    cursor.execute("""SELECT id, fecha_entrevista, hora_entrevista, dni_paciente,nombre_profecional, apellido_profecional, tipo_entrevista FROM entrevistas ORDER BY id""")
    for i in cursor.fetchall():
        dato = f"ID: {i[0]} // Fecha: {i[1]} {i[2] or ''} // DNI pac: {i[3]} // Prof: {i[4]} {i[5] or ''} // Tipo: {i[6] or '-'}"
        lista_widget.insert(tk.END, dato)

# ============================================================================
# BLOQUE 15: VENTANA PARA EDITAR ENTREVISTA
# ============================================================================
def pantalla_edit_entrevista(ventana_padre):
    ventana_editar = tk.Toplevel(ventana_padre)
    ventana_editar.title("Editar datos de entrevista")
    ventana_editar.geometry("800x900")
    ventana_editar.config(bg=GRIS_NIEBLA)

    frame_editar_superior = tk.Frame(ventana_editar, bg=AZUL_PETROLEO, relief="solid", bd=1)
    frame_editar_superior.pack(side="top", padx=20, pady=20, fill="x")


    # PARA VISUAL: arreglar el Label y el Entry de ID
    Label(frame_editar_superior, text="ID de la entrevista a editar:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).grid(row=0, column=12)
    entry_id = tk.Entry(frame_editar_superior, width=30, relief="solid", bd=1, font=("Segoe UI", 12))
    entry_id.grid(row=0, column=13)



    # ---FILA 0: Datos del Paciente, Fecha y Hora---
    Label(frame_editar_superior, text="DNI Paciente:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="e", padx=10, pady=8)
    entry_dni_entrevista = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_dni_entrevista.grid(row=0, column=1, sticky="w", padx=5)

    Label(frame_editar_superior, text="Fecha:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=2, sticky="e", padx=10, pady=8)
    entry_fecha = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_fecha.grid(row=0, column=3, sticky="w", padx=5)

    Label(frame_editar_superior, text="Hora:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=4, sticky="e", padx=10, pady=8)
    entry_hora_entrevista = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_hora_entrevista.grid(row=0, column=5, sticky="w", padx=5)

    # ---FILA 1: Datos del Profesional e Identificacion---
    Label(frame_editar_superior, text="Nombre del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky="e", padx=10, pady=8)
    entry_nombre_profecional = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_nombre_profecional.grid(row=1, column=1, sticky="w", padx=5)

    Label(frame_editar_superior, text="Apellido del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=2, sticky="e", padx=10, pady=8)
    entry_apellido_profecional = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_apellido_profecional.grid(row=1, column=3, sticky="w", padx=5)

    Label(frame_editar_superior, text="DNI del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=4, sticky="e", padx=10, pady=8)
    entry_dni_profesional = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_dni_profesional.grid(row=1, column=5, sticky="w", padx=5)

    # ---FILA 2: Datos adicionales---
    Label(frame_editar_superior, text="Matricula:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="e", padx=10, pady=8)
    entry_matricula = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_matricula.grid(row=2, column=1, sticky="w", padx=5)

    Label(frame_editar_superior, text="Especialidad:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=2, sticky="e", padx=10, pady=8)
    entry_especialidad = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_especialidad.grid(row=2, column=3, sticky="w", padx=5)

    Label(frame_editar_superior, text="Proxima Sesión:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=4, sticky="e", padx=10, pady=8)
    entry_proxima_sesion = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_proxima_sesion.grid(row=2, column=5, sticky="w", padx=5)

    # ---FILA 3: Datos adicionales---
    Label(frame_editar_superior, text="Tipo de visita:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=4, column=0, sticky="e", padx=10, pady=8)
    var_tipo_d_visita = tk.StringVar(value="")
    menu_tipo_d_visita = tk.OptionMenu(frame_editar_superior, var_tipo_d_visita, "individual", "grupal", "familiar")
    menu_tipo_d_visita.config(font=("Segoe UI", 10), width=12)
    menu_tipo_d_visita.grid(row=4, column=1, sticky="w", padx=5)

    # Telefono del profesional
    Label(frame_editar_superior, text="Telefono del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=6, sticky="e", padx=10, pady=8)
    entry_telefono_del_profesional = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_telefono_del_profesional.grid(row=0, column=7, sticky="w", padx=5)

    # Mail del profesional
    Label(frame_editar_superior, text="Mail del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=6, sticky="e", padx=10, pady=8)
    entry_mail_del_profesional = Entry(frame_editar_superior, font=("Segoe UI", 11), width=15)
    entry_mail_del_profesional.grid(row=2, column=7, sticky="w", padx=5)

    # Estado del profesional
    Label(frame_editar_superior, text="Estado:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=6, sticky="e", padx=10, pady=8)
    var_estado_d_profesional = tk.StringVar(value="")
    menu_estado_d_profesional= tk.OptionMenu(frame_editar_superior, var_estado_d_profesional, "Activo","No activo")
    menu_estado_d_profesional.config(font=("Segoe UI", 10), width=12)
    menu_estado_d_profesional.grid(row=1, column=7, sticky="w", padx=5)

    # Entrevista
    frame_editar_medio = tk.Frame(ventana_editar, bg=GRIS_NIEBLA, relief="solid", bd=1)
    frame_editar_medio.pack(fill="both", expand=True, padx=20, pady=10)
    Label(frame_editar_medio, text="Texto de la entrevista:", bg=AZUL_PETROLEO, fg=BLANCO_HUESO, font=("Segoe UI", 12)).pack(fill="x", side="top", padx=20, pady=5)
    text_entrevista_edit = tk.Text(frame_editar_medio, bg=GRIS_NIEBLA, relief="solid", bd=1, font=("Segoe UI", 12))
    text_entrevista_edit.pack(fill="both", expand=True, padx=15, pady=15)

    # Funcion para precargar los datos de la entrevista a partir del ID
    def cargar_entrevista():
        p_id = entry_id.get().strip()
        if not p_id:
            return
        cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (p_id,))
        e = cursor.fetchone()
        if not e:
            messagebox.showinfo("Error", "No existe esa entrevista.")
            return
        entry_nombre_profecional.delete(0, tk.END); entry_nombre_profecional.insert(0, e[1] or "")
        entry_apellido_profecional.delete(0, tk.END); entry_apellido_profecional.insert(0, e[2] or "")
        entry_dni_profesional.delete(0, tk.END); entry_dni_profesional.insert(0, e[3] or "")
        entry_matricula.delete(0, tk.END); entry_matricula.insert(0, e[4] or "")
        entry_especialidad.delete(0, tk.END); entry_especialidad.insert(0, e[5] or "")
        entry_telefono_del_profesional.delete(0, tk.END); entry_telefono_del_profesional.insert(0, e[6] or "")
        entry_mail_del_profesional.delete(0, tk.END); entry_mail_del_profesional.insert(0, e[7] or "")
        var_estado_d_profesional.set(e[8])
        text_entrevista_edit.delete("1.0", tk.END)
        text_entrevista_edit.insert("1.0", e[9] or "")
        entry_dni_entrevista.delete(0, tk.END); entry_dni_entrevista.insert(0, e[10] or "")
        entry_fecha.delete(0, tk.END); entry_fecha.insert(0, e[11] or "")
        entry_hora_entrevista.delete(0, tk.END); entry_hora_entrevista.insert(0, e[12] or "")
        var_tipo_d_visita.set(e[13])
        entry_proxima_sesion.delete(0, tk.END); entry_proxima_sesion.insert(0, e[14] or "")

    boton_cargar = RoundedButton(frame_editar_superior, 150, 30, 20,VERDE_AZULADO, BLANCO,text="Cargar datos", command=cargar_entrevista)
    boton_cargar.grid(row=0, column=2, padx=10, sticky="ew")

    def guardar_entrevista():
        p_id = entry_id.get()
        if p_id == "":
            return
        cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (p_id,))
        entrevista = cursor.fetchone()
        if not entrevista:
            messagebox.showinfo("Error", "No existe esa entrevista.")
            return
        texto_nuevo = text_entrevista_edit.get("1.0", tk.END).strip()
        if texto_nuevo == "":
            texto_nuevo = entrevista[9]
        prof_nombre_nuevo = entry_nombre_profecional.get().strip() or entrevista[1]
        prof_apellido_nuevo = entry_apellido_profecional.get().strip() or entrevista[2]
        dni_profesional_nuevo = entry_dni_profesional.get().strip() or entrevista[3]
        matricula_nuevo = entry_matricula.get().strip() or entrevista[4]
        especialidad_nuevo = entry_especialidad.get().strip() or entrevista[5]
        telefono_del_profesional_nuevo = entry_telefono_del_profesional.get().strip() or entrevista[6]
        mail_del_profesional_nuevo = entry_mail_del_profesional.get().strip() or entrevista[7]
        estado_d_profesional_nuevo = var_estado_d_profesional.get().strip() or entrevista[8]
        dni_nuevo = entry_dni_entrevista.get().strip() or entrevista[10]
        hora_nuevo = entry_hora_entrevista.get().strip() or entrevista[12]
        tipo_d_visita_nuevo = var_tipo_d_visita.get().strip() or entrevista[13]
        proxima_sesion_nuevo = entry_proxima_sesion.get().strip() or entrevista[14]
        fecha_nueva = entry_fecha.get().strip()
        if fecha_nueva == "":
            fecha_nueva = entrevista[11]
        else:
            fecha_nueva = comprobar_fecha(entry_fecha)
        conexion.execute("""UPDATE entrevistas SET nombre_profecional = ?, apellido_profecional = ?, dni_profecional = ?, matricula = ?, especialidad = ?, telefono_profecional = ?, email_profecional = ?, activo_profecional = ?, entrevista = ?, dni_paciente = ?, fecha_entrevista = ?, hora_entrevista = ?, tipo_entrevista = ?, proxima_sesion_entrevista = ? WHERE id = ?""",
                         (prof_nombre_nuevo, prof_apellido_nuevo, dni_profesional_nuevo, matricula_nuevo, especialidad_nuevo, telefono_del_profesional_nuevo, mail_del_profesional_nuevo, estado_d_profesional_nuevo, texto_nuevo, dni_nuevo, fecha_nueva, hora_nuevo, tipo_d_visita_nuevo, proxima_sesion_nuevo, p_id))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)
        ventana_editar.destroy()

    frame_editar_inferior = tk.Frame(ventana_editar, bg=GRIS_NIEBLA)
    frame_editar_inferior.pack(fill="x", expand=True)
    boton_cargar = RoundedButton(frame_editar_superior, 150, 30, 20,VERDE_AZULADO, BLANCO,text="Guardar cambios",command=guardar_entrevista)
    boton_cargar.grid(row=0, column=10, padx=5, sticky="ew")
    agregar_boton_luna(ventana_editar)

# ============================================================================
# BLOQUE 16: VENTANA EMERGENTE DE ENTREVISTAS
# ============================================================================
def abrir_ventana_entrevistas(ventana_padre):
    ventana_entrevistas = tk.Toplevel(ventana_padre)
    ventana_entrevistas.title("ENTREVISTAS")
    ventana_entrevistas.geometry("1150x800")
    ventana_entrevistas.config(bg=GRIS_NIEBLA)

    frame_superior = Frame(ventana_entrevistas, bg=GRIS_AZULADO)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)
    frame_superior = Frame(ventana_entrevistas, bg=GRIS_AZULADO)
    frame_superior.pack(side="top", fill="x", padx=20, pady=10)

    global entry_nombre_profecional, entry_apellido_profecional, entry_dni_profesional, entry_matricula
    global entry_especialidad, entry_telefono_del_profesional, entry_mail_del_profesional, var_estado_d_profesional
    global text_entrevista, entry_dni_entrevista, entry_fecha, entry_hora_entrevista, var_tipo_d_visita
    global entry_proxima_sesion, lista_entrevistas

    # ---FILA 0: Datos del Paciente, Fecha y Hora---
    Label(frame_superior, text="DNI Paciente:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="e", padx=10, pady=8)
    entry_dni_entrevista = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_dni_entrevista.grid(row=0, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Fecha:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=2, sticky="e", padx=10, pady=8)
    entry_fecha = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_fecha.grid(row=0, column=3, sticky="w", padx=5)

    Label(frame_superior, text="Hora:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=4, sticky="e", padx=10, pady=8)
    entry_hora_entrevista = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_hora_entrevista.grid(row=0, column=5, sticky="w", padx=5)

    # ---FILA 1: Datos del Profesional e Identificacion---
    Label(frame_superior, text="Nombre del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky="e", padx=10, pady=8)
    entry_nombre_profecional = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_nombre_profecional.grid(row=1, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Apellido del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=2, sticky="e", padx=10, pady=8)
    entry_apellido_profecional = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_apellido_profecional.grid(row=1, column=3, sticky="w", padx=5)

    Label(frame_superior, text="DNI del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=4, sticky="e", padx=10, pady=8)
    entry_dni_profesional = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_dni_profesional.grid(row=1, column=5, sticky="w", padx=5)

    # ---FILA 2: Datos adicionales---
    Label(frame_superior, text="Matricula:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="e", padx=10, pady=8)
    entry_matricula = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_matricula.grid(row=2, column=1, sticky="w", padx=5)

    Label(frame_superior, text="Especialidad:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=2, sticky="e", padx=10, pady=8)
    entry_especialidad = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_especialidad.grid(row=2, column=3, sticky="w", padx=5)

    Label(frame_superior, text="Proxima Sesión:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=4, sticky="e", padx=10, pady=8)
    entry_proxima_sesion = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_proxima_sesion.grid(row=2, column=5, sticky="w", padx=5)

    # ---FILA 4: Datos adicionales---
    Label(frame_superior, text="Tipo de visita:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=4, column=0, sticky="e", padx=10, pady=8)
    var_tipo_d_visita = tk.StringVar(value="")
    menu_tipo_d_visita = tk.OptionMenu(frame_superior, var_tipo_d_visita, "individual", "grupal", "familiar")
    menu_tipo_d_visita.config(font=("Segoe UI", 10), width=12)
    menu_tipo_d_visita.grid(row=4, column=1, sticky="w", padx=5)

    # Telefono del profesional
    Label(frame_superior, text="Telefono del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=0, column=6, sticky="e", padx=10, pady=8)
    entry_telefono_del_profesional = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_telefono_del_profesional.grid(row=0, column=7, sticky="w", padx=5)

    # Mail del profesional
    Label(frame_superior, text="Mail del profesional:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=2, column=6, sticky="e", padx=10, pady=8)
    entry_mail_del_profesional = Entry(frame_superior, font=("Segoe UI", 11), width=15)
    entry_mail_del_profesional.grid(row=2, column=7, sticky="w", padx=5)

    # Estado del profesional
    Label(frame_superior, text="Estado:", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 11, "bold")).grid(row=1, column=6, sticky="e", padx=10, pady=8)
    var_estado_d_profesional = tk.StringVar(value="")
    menu_estado_d_profesional= tk.OptionMenu(frame_superior, var_estado_d_profesional, "Activo","No activo")
    menu_estado_d_profesional.config(font=("Segoe UI", 10), width=12)
    menu_estado_d_profesional.grid(row=1, column=7, sticky="w", padx=5)

    # ---CUERPO MEDIO (Lista e Historial)---
    frame_medio_cuerpo = Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_medio_cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

    # LADO IZQUIERDO: lista
    frame_lista_medio = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_lista_medio.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    Label(frame_lista_medio, text="Historial de Entrevistas", bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    
    lista_entrevistas = Listbox(frame_lista_medio, bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO, bd=0, font=("Segoe UI", 10))
    lista_entrevistas.pack(fill="both", expand=True, padx=5, pady=5)
    lista_entrevistas.bind("<Double-Button-1>", detalles_entrevsit)
    
    ver_list_entrevist(lista_entrevistas)

    # LADO DERECHO: texto
    frame_texto = Frame(frame_medio_cuerpo, bg=BLANCO, relief="solid", bd=1)
    frame_texto.pack(side="left", fill="both", expand=True, padx=(10, 0))
    Label(frame_texto, text="Anotaciones de la entrevista", bg=BLANCO, fg=GRIS_AZULADO, font=("Segoe UI", 13, "bold")).pack(pady=5)
    text_entrevista = tk.Text(frame_texto, relief="solid", bd=1, bg=GRIS_NIEBLA, font=("Segoe UI", 12))
    text_entrevista.pack(fill="both", expand=True, padx=5, pady=5)

    frame_inferior = Frame(ventana_entrevistas, bg=GRIS_NIEBLA)
    frame_inferior.pack(side="bottom", fill="x", padx=20, pady=20)

    frame_inferior.grid_columnconfigure(0, weight=1)
    frame_inferior.grid_columnconfigure(4, weight=1)

    frame_inferior.columnconfigure(1, weight=1)
    frame_inferior.columnconfigure(2, weight=1)
    frame_inferior.columnconfigure(3, weight=1)


    RoundedButton(frame_inferior, 150, 40, 20,VERDE_AZULADO, BLANCO,  text="Nueva entrevista", command=new_entrevista).grid(row=0, column=1, padx=10, sticky="ew")
    RoundedButton(frame_inferior, 160, 40, 20, VERDE_AZULADO, BLANCO, text="Eliminar entrevista", command=eliminar_entrevista).grid(row=0, column=2, padx=10, sticky="ew")
   
    def abrir_editar():
        pantalla_edit_entrevista(ventana_entrevistas)
    RoundedButton(frame_inferior,  180, 40, 20,VERDE_AZULADO, BLANCO, text="Editar entrevista", command=abrir_editar).grid(row=0, column=3, padx=10, sticky="ew")
    RoundedButton(frame_inferior,  150, 40, 20,VERDE_AZULADO, BLANCO, text="Generar PDF", command=exportar_entrevistas_pdf).grid(row=0, column=4, padx=10, sticky="ew")

    agregar_boton_luna(ventana_entrevistas)


# ============================================================================
# BLOQUE 17: FUNCIONES DE LA VENTANA DE ENTREVISTAS
# ============================================================================

def new_entrevista():
    nom_profecional = entry_nombre_profecional.get().strip()
    apellido_profecional = entry_apellido_profecional.get().strip()
    dni_profesional = entry_dni_profesional.get().strip()
    matricula = entry_matricula.get().strip()
    especialidad = entry_especialidad.get().strip()
    telefono_profecional = entry_telefono_del_profesional.get().strip()
    email_profecional = entry_mail_del_profesional.get().strip()
    activo_profecional = var_estado_d_profesional.get()
    entrevista = text_entrevista.get("1.0", tk.END).strip()
    dni = entry_dni_entrevista.get().strip()
    fecha = comprobar_fecha(entry_fecha)
    hora = entry_hora_entrevista.get().strip()
    tipo = var_tipo_d_visita.get()
    proxima_sesion = entry_proxima_sesion.get().strip()

    if not(nom_profecional and apellido_profecional and dni_profesional and matricula and especialidad and telefono_profecional and email_profecional and activo_profecional and entrevista and dni and fecha and hora and tipo and proxima_sesion):
        messagebox.showwarning("Faltan datos", "Complete: nombre del profesional, apellido del profesional, DNI del profesional, matricula, especialidad, telefono del profesional, email del profesional, activo, entrevista, DNI del paciente, fecha, hora, tipo de visita y proxima sesion.")
        return

    try:
        # ACA ESTA LA CORRECCION: dice dni_profecional (con C)
        cursor.execute("""INSERT INTO entrevistas 
            (nombre_profecional, apellido_profecional, dni_profecional, matricula, especialidad, telefono_profecional, email_profecional, activo_profecional, entrevista, dni_paciente, fecha_entrevista, hora_entrevista, tipo_entrevista, proxima_sesion_entrevista) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (nom_profecional, apellido_profecional, dni_profesional, matricula, especialidad, telefono_profecional, email_profecional, activo_profecional, entrevista, dni, fecha, hora, tipo, proxima_sesion))
        conexion.commit()

    except Exception as e:
        # ACA ESTA LA CORRECCION: mostramos el error real
        messagebox.showerror("Error", f'No se pudo guardar la entrevista:\n{e}')
        return

    ver_list_entrevist(lista_entrevistas)
    text_entrevista.delete("1.0", tk.END)

def eliminar_entrevista():
    seleccion = lista_entrevistas.curselection()
    if seleccion:
        dato = lista_entrevistas.get(seleccion[0])
        id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()
        cursor.execute("DELETE FROM entrevistas WHERE id = ?", (id_entrevista,))
        conexion.commit()
        ver_list_entrevist(lista_entrevistas)

def detalles_entrevsit(event=None):
    seleccion = lista_entrevistas.curselection()
    if not seleccion:
        return
    dato = lista_entrevistas.get(seleccion[0])
    id_entrevista = dato.split("//")[0].replace("ID: ", "").strip()

    cursor.execute("""SELECT nombre_profecional, apellido_profecional, dni_profecional, matricula, especialidad, telefono_profecional, email_profecional, activo_profecional, entrevista, dni_paciente, fecha_entrevista, hora_entrevista, tipo_entrevista, proxima_sesion_entrevista FROM entrevistas WHERE id = ?""", (id_entrevista,))    
    e = cursor.fetchone()
    if not e:
        return
    ventana_detalle = Toplevel()
    ventana_detalle.title(f"Detalle de entrevista #{id_entrevista}")
    ventana_detalle.geometry("600x550")
    ventana_detalle.config(bg=GRIS_NIEBLA)

    frame_detalle = Frame(ventana_detalle, bg=BLANCO, relief="solid", bd=1)
    frame_detalle.pack(padx=20, pady=20, fill="both", expand=True)

    info = [
        ("ID", id_entrevista),
        ("Profesional", f"{e[0]} {e[1] or "-"}"),
        ("DNI profesional", e[2] or "-"),
        ("Matricula", e[3] or "-"),
        ("Especialidad", e[4] or "-"),
        ("Telefono profesional", e[5] or "-"),
        ("Email profesional", e[6] or "-"),
        ("Activo profecional", e[7] or "-"),
        ("DNI paciente", e[9] or "-"),
        ("Fecha", e[10] or "-"),
        ("Hora", e[11] or "-"),
        ("Tipo", e[12] or "-"),
        ("Proxima sesion", e[13] or "-"),
    ]
    for etiqueta, valor in info:
        fila = Frame(frame_detalle, bg=BLANCO)
        fila.pack(fill="x", padx=10, pady=2)
        Label(fila, text=f"{etiqueta}:", bg=BLANCO, fg=GRIS_AZULADO,font=("Segoe UI", 11, "bold"), width=16, anchor="e").pack(side="left")
        Label(fila, text=valor, bg=BLANCO, fg=GRIS_AZULADO,font=("Segoe UI", 11), anchor="w").pack(side="left", padx=5)

    Label(frame_detalle, text="Anotaciones:", bg=BLANCO, fg=GRIS_AZULADO,font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", padx=10, pady=(10, 2))
    text_dato = tk.Text(frame_detalle, height=8, font=("Segoe UI", 11), relief="solid", bd=1)
    text_dato.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    text_dato.insert("1.0", e[8] or "-")
    text_dato.config(state=tk.DISABLED)
    agregar_boton_luna(ventana_detalle)


# ============================================================================
# BLOQUE 18: VENTANA DE PERFIL
# ============================================================================
def abrir_ventana_perfil():
    ventana_perfil = Toplevel(ventana)
    ventana_perfil.title("PERFIL")
    ventana_perfil.geometry("1000x800")
    ventana_perfil.config(bg=GRIS_NIEBLA)
    ventana_perfil.resizable(False, False)

    # Foto pendiente (dict para poder mutarlo desde funciones anidadas)
    foto_pendiente = {"bytes": None}

    frame_izquierdo = Frame(ventana_perfil, bg=GRIS_NIEBLA)
    frame_izquierdo.pack(side="left", fill="y", padx=15, pady=15)

    # Nombre
    Label(frame_izquierdo, text=" Nombre:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_nombre_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_nombre_perfil.grid(row=0, column=1, padx=5, pady=3)
    entry_nombre_perfil.insert(0, entry_nombre.get())

    # Apellido
    Label(frame_izquierdo, text=" Apellido:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", padx=5)
    entry_apellido_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_apellido_perfil.grid(row=1, column=1, padx=5, pady=3)
    entry_apellido_perfil.insert(0, entry_apellido.get())

    #Edad
    Label(frame_izquierdo, text="Edad:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", padx=5)
    entry_edad_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_edad_perfil.grid(row=2, column=1, padx=5, pady=3)

    # DNI
    Label(frame_izquierdo, text=" DNI:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", padx=5)
    entry_dni_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_dni_perfil.grid(row=3, column=1, padx=5, pady=3)
    entry_dni_perfil.insert(0, entry_dni.get())

    # Direccion
    Label(frame_izquierdo, text=" Domicilio:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", padx=5)
    entry_direccion_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_direccion_perfil.grid(row=4, column=1, padx=5, pady=3)

    # F. Nacimiento
    Label(frame_izquierdo, text=" Fecha de nacimiento:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=5, column=0, sticky="e", padx=5)
    entry_f_nacimiento_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_f_nacimiento_perfil.grid(row=5, column=1, padx=5, pady=3)

    # F. Ingreso a institucion
    Label(frame_izquierdo, text=" Fecha de ingreso al instituto:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=6, column=0, sticky="e", padx=5)
    entry_f_ingreso_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_f_ingreso_perfil.grid(row=6, column=1, padx=5, pady=3)

    #Numero de telefono del paciente
    Label(frame_izquierdo, text="Telefono:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=7, column=0, sticky="e", padx=5)
    entry_telefono_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_telefono_perfil.grid(row=7, column=1, padx=5, pady=3)

    #Nombre del contacto de emergencia
    Label(frame_izquierdo, text="Nombre del contacto de emergencia:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=8, column=0, sticky="e", padx=5)
    entry_nombre_contacto_emergencia_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_nombre_contacto_emergencia_perfil.grid(row=8, column=1, padx=5, pady=3)

    #Telefono del contacto de emergencia
    Label(frame_izquierdo, text="Telefono del contacto de emergencia:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=9, column=0, sticky="e", padx=5)
    entry_telefono_contacto_emergencia_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_telefono_contacto_emergencia_perfil.grid(row=9, column=1, padx=5, pady=3)

    #Obra social
    Label(frame_izquierdo, text="Obra social:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=10, column=0, sticky="e", padx=5)
    entry_obra_social_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_obra_social_perfil.grid(row=10, column=1, padx=5, pady=3)

    #Estado del paciente, si es ACTIVO, ABANDONO o alguna cosa de ese mambo
    Label(frame_izquierdo, text="Estado:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=11, column=0, sticky="e", padx=5)
    var_estado_paciente_perfil = tk.StringVar(value="")
    menu_estado_paciente_perfil = tk.OptionMenu(frame_izquierdo,var_estado_paciente_perfil,"Activo","Inactivo")
    menu_estado_paciente_perfil.grid(row=11, column=1, padx=5, pady=3)

    # Consentimiento
    Label(frame_izquierdo, text="Consentimiento:", bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 12)).grid(row=12, column=0, sticky="e", padx=5)
    entry_consentimiento_perfil = Entry(frame_izquierdo, width=22, font=("Segoe UI", 12))
    entry_consentimiento_perfil.grid(row=12, column=1, padx=5, pady=3)

    def mostrar_foto_en_perfil():
        # Poblar galeria con fotos del editor
        lista_fotos_galeria.delete(0, tk.END)
        for ruta in imagenes_cargadas:
            lista_fotos_galeria.insert(tk.END, os.path.basename(ruta))
        # Si la foto pendiente es b"" significa "quitar foto", mostrar el placeholder
        if foto_pendiente["bytes"] == b"":
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return

        # Si hay foto pendiente nueva, mostrarla
        if foto_pendiente["bytes"] is not None:
            try:
                img = Image.open(BytesIO(foto_pendiente["bytes"]))
                img.thumbnail((300, 300))
                foto_tk = ImageTk.PhotoImage(img)
                visor_foto_perfil.configure(image=foto_tk, text="")
                visor_foto_perfil.image = foto_tk
                return
            except Exception:
                pass

        # Si no, mostrar la de la base
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None
            return
        cursor.execute("SELECT foto FROM personas WHERE dni = ?", (dni_txt,))
        fila = cursor.fetchone()
        if fila and fila[0]:
            img = Image.open(BytesIO(fila[0]))
            img.thumbnail((300, 300))
            foto = ImageTk.PhotoImage(img)
            visor_foto_perfil.configure(image=foto, text="")
            visor_foto_perfil.image = foto
        else:
            visor_foto_perfil.configure(image="", text="👤\nClic para subir foto")
            visor_foto_perfil.image = None

    def subir_foto_perfil(event=None):
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not ruta:
            return
        try:
            with open(ruta, "rb") as f:
                foto_pendiente["bytes"] = f.read()
            mostrar_foto_en_perfil()
        except Exception:
            messagebox.showerror("Error", 'No se pudo cargar la foto')

    def asignar_foto_galeria(event=None):
        sel = lista_fotos_galeria.curselection()
        if not sel:
            return
        ruta = imagenes_cargadas[sel[0]]
        try:
            with open(ruta, "rb") as f:
                foto_pendiente["bytes"] = f.read()
            mostrar_foto_en_perfil()
        except Exception:
            messagebox.showerror("Error", 'No se pudo asignar la foto')
    
    def quitar_foto_perfil():
        foto_pendiente["bytes"] = b""  # b"" = "borrar foto al guardar"
        mostrar_foto_en_perfil()


    def guardar_cambios_perfil():
        nombre = entry_nombre_perfil.get().strip()
        apellido = entry_apellido_perfil.get().strip()
        dni_txt = entry_dni_perfil.get().strip()
        edad = entry_edad_perfil.get().strip()
        fecha_nacimiento = comprobar_fecha(entry_f_nacimiento_perfil)
        fecha_ingreso = comprobar_fecha(entry_f_ingreso_perfil)
        telefono = entry_telefono_perfil.get().strip()
        direccion = entry_direccion_perfil.get().strip()
        contacto_emergencia = entry_nombre_contacto_emergencia_perfil.get().strip()
        telefono_emergencia = entry_telefono_contacto_emergencia_perfil.get().strip()
        obra_social = entry_obra_social_perfil.get().strip()
        estado = var_estado_paciente_perfil.get()
        consentimiento = entry_consentimiento_perfil.get().strip()
        if not (nombre and apellido and dni_txt and edad and fecha_nacimiento and fecha_ingreso and telefono and direccion and contacto_emergencia and telefono_emergencia and obra_social and estado and consentimiento):
            messagebox.showwarning("Faltan datos", "Completa nombre, apellido, DNI, edad, fecha de nacimiento, fecha de ingreso, telefono, direccion, contacto de emergencia, telefono de emergencia, obra social, estado y consentimiento.")
            return
        try:
            dni = int(dni_txt)
        except ValueError:
            messagebox.showerror("Error", "El DNI debe ser numérico.")
            return
        cursor.execute("SELECT id FROM personas WHERE dni = ?", (dni,))
        existe = cursor.fetchone()
        if existe:
            # Tres casos: foto nueva, quitar foto, o no tocar
            if foto_pendiente["bytes"] == b"":
                cursor.execute("""UPDATE personas SET nombre = ?, apellido = ?, edad = ?, fecha_nacimiento = ?, fecha_ingreso = ?, telefono = ?, direccion = ?, contacto_emergencia = ?, telefono_emergencia = ?, obra_social = ?, estado = ?, consentimiento = ?, foto = NULL WHERE dni = ?""",(nombre, apellido, edad, fecha_nacimiento, fecha_ingreso, telefono, direccion, contacto_emergencia, telefono_emergencia, obra_social, estado, consentimiento,dni))
            elif foto_pendiente["bytes"] is not None:
                cursor.execute("""UPDATE personas SET nombre = ?, apellido = ?, edad = ?, fecha_nacimiento = ?, fecha_ingreso = ?, telefono = ?, direccion = ?, contacto_emergencia = ?, telefono_emergencia = ?, obra_social = ?, estado = ?, consentimiento = ?, foto = ?  WHERE dni = ?""",(nombre, apellido, edad, fecha_nacimiento, fecha_ingreso, telefono, direccion, contacto_emergencia, telefono_emergencia, obra_social, estado, consentimiento, sqlite3.Binary(foto_pendiente["bytes"]),dni))
            else:
                cursor.execute("""UPDATE personas SET nombre = ?, apellido = ?, edad = ?, fecha_nacimiento = ?, fecha_ingreso = ?, telefono = ?, direccion = ?, contacto_emergencia = ?, telefono_emergencia = ?, obra_social = ?, estado = ?, consentimiento = ? WHERE dni = ?""", (nombre, apellido, edad, fecha_nacimiento, fecha_ingreso, telefono, direccion, contacto_emergencia, telefono_emergencia, obra_social, estado, consentimiento, dni))
        else:
            if foto_pendiente["bytes"] == b"":
                contenido = None
            elif foto_pendiente["bytes"] is not None:
                contenido = sqlite3.Binary(foto_pendiente["bytes"])
            else:
                contenido = None
            try:
                cursor.execute("""INSERT INTO personas (nombre, apellido, dni, edad, fecha_nacimiento, fecha_ingreso, telefono,  direccion, contacto_emergencia, telefono_emergencia, obra_social, estado, consentimiento, foto) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (nombre, apellido, dni, edad, fecha_nacimiento, fecha_ingreso, telefono, direccion, contacto_emergencia, telefono_emergencia, obra_social, estado, consentimiento))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ya existe una persona con ese DNI.")
                return
        conexion.commit()
        refrescar_lista()
        foto_pendiente["bytes"] = None
        messagebox.showinfo("OK", "Datos guardados.")

    def cargar_perfil():
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            messagebox.showwarning("Atencion", "Escriba un DNI")
            return
        lista_personas_perfil.delete(0, tk.END)
        foto_pendiente["bytes"] = None
        cursor.execute("""SELECT nombre, apellido, edad, fecha_nacimiento, fecha_ingreso, telefono,  direccion, contacto_emergencia, telefono_emergencia, obra_social, estado, consentimiento
                        FROM personas WHERE dni = ?""", (dni_txt,))
        fila = cursor.fetchone()
        if fila:
            entry_nombre_perfil.delete(0, tk.END); entry_nombre_perfil.insert(0, fila[0] or "")
            entry_apellido_perfil.delete(0, tk.END); entry_apellido_perfil.insert(0, fila[1] or "")
            entry_edad_perfil.delete(0, tk.END); entry_edad_perfil.insert(0, fila[2] or "")
            entry_f_nacimiento_perfil.delete(0, tk.END); entry_f_nacimiento_perfil.insert(0, fila[3] or "")
            entry_f_ingreso_perfil.delete(0, tk.END); entry_f_ingreso_perfil.insert(0, fila[4] or "")
            entry_telefono_perfil.delete(0, tk.END); entry_telefono_perfil.insert(0, fila[5] or "")
            entry_direccion_perfil.delete(0, tk.END); entry_direccion_perfil.insert(0, fila[6] or "")
            entry_nombre_contacto_emergencia_perfil.delete(0, tk.END); entry_nombre_contacto_emergencia_perfil.insert(0, fila[7] or "")
            entry_telefono_contacto_emergencia_perfil.delete(0, tk.END); entry_telefono_contacto_emergencia_perfil.insert(0, fila[8] or "")
            entry_obra_social_perfil.delete(0, tk.END); entry_obra_social_perfil.insert(0, fila[9] or "")
            var_estado_paciente_perfil.set(fila[10])
            entry_consentimiento_perfil.delete(0, tk.END); entry_consentimiento_perfil.insert(0, fila[11] or "")
            mostrar_foto_en_perfil()

            cursor.execute("""SELECT id, fecha_entrevista, nombre_profecional, apellido_profecional
                              FROM entrevistas WHERE dni_paciente = ? ORDER BY fecha_entrevista""", (dni_txt,))
            for e in cursor.fetchall():
                lista_personas_perfil.insert(tk.END, f"ID {e[0]} — {e[1]} — {e[2]} {e[3] or ''}")
        else:
            messagebox.showinfo("Error", "No existe ese DNI.")


    def exportar_pdf_paciente():
        dni_txt = entry_dni_perfil.get().strip()
        if not dni_txt:
            messagebox.showwarning("Atención", "Escribí un DNI primero.")
            return
        exportar_entrevistas_pdf(dni_paciente=dni_txt)

    # Botones
    boton_cargar_perfil = RoundedButton(frame_izquierdo, 80, 40, 20, VERDE_AZULADO,BLANCO,text="⟳", command=cargar_perfil)
    boton_cargar_perfil.grid(row=2, column=2, padx=10, sticky="ew")
    boton_entrevistas   = RoundedButton(frame_izquierdo, 100, 40, 20, VERDE_AZULADO,BLANCO,text="Entrevista", command=abrir_desde_principal)
    boton_entrevistas.grid(row=13, column=2, padx=10, sticky="ew")
    boton_editor_fotos  = RoundedButton(frame_izquierdo, 100, 40, 20, VERDE_AZULADO,BLANCO,text="Editar fotos", command=abrir_ventana_editor_fotos)
    boton_editor_fotos.grid(row=13, column=1, padx=10, sticky="ew")
    boton_guardar_perfil= RoundedButton(frame_izquierdo, 140, 40, 20, VERDE_AZULADO,BLANCO,text="Guardar cambios", command=guardar_cambios_perfil)
    boton_guardar_perfil.grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="ew") # Ocupa 2 columnas
    boton_pdf_paciente =  RoundedButton(frame_izquierdo, 180, 40, 20, VERDE_AZULADO,BLANCO,text="PDF de este paciente", command=exportar_pdf_paciente)
    boton_pdf_paciente.grid(row=15, column=1, padx=10, sticky="ew")

    # --- FRAME DERECHO ---
    frame_derecha = tk.Frame(ventana_perfil, bg=GRIS_NIEBLA)
    frame_derecha.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

    # Foto grande clickeable
    frame_foto_perfil = Frame(frame_derecha, bg=BLANCO, relief="solid", bd=1, height=280)
    frame_foto_perfil.pack(side="top", fill="x", pady=(0, 10))
    frame_foto_perfil.pack_propagate(False)
    visor_foto_perfil = tk.Label(frame_foto_perfil, text="👤\nClic para subir foto",bg=BLANCO, fg=GRIS_MEDIO, font=("Segoe UI", 20), cursor="hand2")
    visor_foto_perfil.pack(fill="both", expand=True, padx=10, pady=10)
    visor_foto_perfil.bind("<Button-1>", subir_foto_perfil)

    boton_quitar_foto =  RoundedButton(frame_derecha, 100, 40, 20, VERDE_AZULADO,BLANCO,text="Quitar foto", command=quitar_foto_perfil)
    boton_quitar_foto.pack(side="top",padx=10,pady=5)

    # Galeria con fotos del editor
    frame_galeria = Frame(frame_derecha, bg=GRIS_NIEBLA)
    frame_galeria.pack(side="top", fill="x", pady=(0, 10))
    Label(frame_galeria, text="Fotos del editor:",bg=GRIS_NIEBLA, fg=GRIS_AZULADO, font=("Segoe UI", 10, "bold")).pack(anchor="w")

    frame_galeria_inner = Frame(frame_galeria, bg=GRIS_NIEBLA, height=120)
    frame_galeria_inner.pack(fill="x")
    frame_galeria_inner.pack_propagate(False)

    scroll_galeria = tk.Scrollbar(frame_galeria_inner, orient="vertical")
    scroll_galeria.pack(side="right", fill="y")
    lista_fotos_galeria = tk.Listbox(frame_galeria_inner, font=("Segoe UI", 10), yscrollcommand=scroll_galeria.set,selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_fotos_galeria.pack(side="left", fill="both", expand=True)
    scroll_galeria.config(command=lista_fotos_galeria.yview)
    lista_fotos_galeria.bind("<<ListboxSelect>>", asignar_foto_galeria)

    # Entrevistas del paciente
    frame_lista_perfil = Frame(frame_derecha, bg=GRIS_AZULADO, relief="solid", bd=1)
    frame_lista_perfil.pack(side="top", fill="both", expand=True, pady=(0, 20))
    Label(frame_lista_perfil, text="Entrevistas del paciente", bg=GRIS_AZULADO, fg=BLANCO, font=("Segoe UI", 15, "bold")).pack(side="top", padx=10, pady=10)
    scroll_perfil = tk.Scrollbar(frame_lista_perfil, orient="vertical")
    scroll_perfil.pack(side="right", fill="y")
    lista_personas_perfil = Listbox(frame_lista_perfil, yscrollcommand=scroll_perfil.set, font=("Segoe UI", 12), bg=BLANCO, fg=GRIS_AZULADO, selectbackground=AZUL_SERENO, selectforeground=BLANCO)
    lista_personas_perfil.pack(side="left", fill="both", expand=True)
    scroll_perfil.config(command=lista_personas_perfil.yview)

    mostrar_foto_en_perfil()
    agregar_boton_luna(ventana_perfil)
