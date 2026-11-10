from datetime import datetime

# Diccionario para almacenar los trabajadores registrados
# Estructura: { "ID": {"nombre": str, "puesto": str, "estado": str} }
trabajadores = {
    "101": {"nombre": "Ana García", "puesto": "Desarrolladora", "estado": "Fuera"},
    "102": {"nombre": "Carlos López", "puesto": "Diseñador", "estado": "Fuera"}
}

# Lista para guardar el historial de movimientos (entradas y salidas)
historial_asistencia = []


def registrar_trabajador():
    print("\n--- REGISTRO DE NUEVO TRABAJADOR ---")
    id_emp = input("Ingrese el ID del trabajador: ").strip()
    
    if id_emp in trabajadores:
        print("Error: Ya existe un trabajador con ese ID.")
        return

    nombre = input("Ingrese el nombre completo: ").strip()
    puesto = input("Ingrese el puesto o cargo: ").strip()

    trabajadores[id_emp] = {
        "nombre": nombre,
        "puesto": puesto,
        "estado": "Fuera"
    }
    print(f"Trabajador '{nombre}' registrado con éxito.")


def marcar_entrada():
    print("\n--- MARCAR ENTRADA ---")
    id_emp = input("Ingrese el ID del trabajador: ").strip()

    if id_emp not in trabajadores:
        print("Error: ID no encontrado. Registre al trabajador primero.")
        return

    if trabajadores[id_emp]["estado"] == "Dentro":
        print(f"Aviso: {trabajadores[id_emp]['nombre']} ya registró su entrada previamente.")
        return

    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trabajadores[id_emp]["estado"] = "Dentro"
    
    historial_asistencia.append({
        "id": id_emp,
        "nombre": trabajadores[id_emp]["nombre"],
        "tipo": "ENTRADA",
        "fecha_hora": hora_actual
    })
    print(f"Entrada registrada para {trabajadores[id_emp]['nombre']} a las {hora_actual}.")


def marcar_salida():
    print("\n--- MARCAR SALIDA ---")
    id_emp = input("Ingrese el ID del trabajador: ").strip()

    if id_emp not in trabajadores:
        print("Error: ID no encontrado.")
        return

    if trabajadores[id_emp]["estado"] == "Fuera":
        print(f"Aviso: {trabajadores[id_emp]['nombre']} no ha marcado entrada o ya salió.")
        return

    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trabajadores[id_emp]["estado"] = "Fuera"

    historial_asistencia.append({
        "id": id_emp,
        "nombre": trabajadores[id_emp]["nombre"],
        "tipo": "SALIDA",
        "fecha_hora": hora_actual
    })
    print(f"Salida registrada para {trabajadores[id_emp]['nombre']} a las {hora_actual}.")


def ver_estado_actual():
    print("\n--- ESTADO ACTUAL DEL PERSONAL ---")
    if not trabajadores:
        print("No hay trabajadores registrados.")
        return

    print(f"{'ID':<10} {'NOMBRE':<25} {'PUESTO':<20} {'ESTADO':<10}")
    print("-" * 65)
    for id_emp, datos in trabajadores.items():
        print(f"{id_emp:<10} {datos['nombre']:<25} {datos['puesto']:<20} {datos['estado']:<10}")


def ver_historial():
    print("\n--- HISTORIAL DE ENTRADAS Y SALIDAS ---")
    if not historial_asistencia:
        print("Aún no hay registros de entrada o salida.")
        return

    print(f"{'FECHA Y HORA':<22} {'TIPO':<10} {'ID':<8} {'NOMBRE':<25}")
    print("-" * 65)
    for registro in historial_asistencia:
        print(f"{registro['fecha_hora']:<22} {registro['tipo']:<10} {registro['id']:<8} {registro['nombre']:<25}")


def menu():
    while True:
        print("\n=========================================")
        print("   CONTROL DE ASISTENCIA DE PERSONAL")
        print("=========================================")
        print("1. Registrar nuevo trabajador")
        print("2. Marcar ENTRADA")
        print("3. Marcar SALIDA")
        print("4. Ver estado actual de trabajadores")
        print("5. Ver historial completo de movimientos")
        print("6. Salir del sistema")
        
        opcion = input("\nSeleccione una opción (1-6): ").strip()

        if opcion == "1":
            registrar_trabajador()
        elif opcion == "2":
            marcar_entrada()
        elif opcion == "3":
            marcar_salida()
        elif opcion == "4":
            ver_estado_actual()
        elif opcion == "5":
            ver_historial()
        elif opcion == "6":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


# Ejecutar el programa
if __name__ == "__main__":
    menu()

