from biblioteca import Biblioteca
from libro import Libro
from usuario import Estudiante, Profesor
import sys
import getpass  # Para ocultar la contraseña al escribirla

def mostrar_menu():
    print("\n--- MENÚ DE LA BIBLICA ---")
    print("1. Agregar un nuevo libro")
    print("2. Registrar un nuevo usuario (Estudiante/Profesor)")
    print("3. Prestar un libro")
    print("4. Devolver un libro")
    print("5. Mostrar todos los libros")
    print("6. Salir")

def main():
    try:
        # 1. Conectar a la BD
        mi_biblioteca = Biblioteca()
    except Exception as e:
        print(f"Error fatal al conectar con la BD. Revisa tus credenciales o el servicio MySQL.")
        print(f"Detalle: {e}")
        sys.exit(1) # Salir del programa si no hay BD

    # --- 2. BUCLE DE LOGIN (ACTIVADO) ---
    autenticado = False
    intentos = 0
    while not autenticado and intentos < 3:
        print("\n--- INICIO DE SESIÓN ---")
        id_usuario = input("ID de Usuario: ")
        # Usamos getpass para que la contraseña no se vea al escribir
        password = getpass.getpass("Contraseña: ") 
        
        autenticado = mi_biblioteca.login(id_usuario, password)
        if not autenticado:
            intentos += 1
            print(f"Acceso denegado. Quedan {3 - intentos} intentos.")
            
    # --- 3. MENÚ PRINCIPAL (SI ESTÁ AUTENTICADO) ---
    if autenticado:
        while True:
            mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                # --- AGREGAR LIBRO ---
                print("\n[Agregando nuevo libro]")
                titulo = input("Título: ")
                autor = input("Autor: ")
                try:
                    fecha = int(input("Año de publicación: "))
                    nuevo_libro = Libro(titulo, autor, fecha)
                    mi_biblioteca.agregar_libro(nuevo_libro)
                except ValueError:
                    print("Error: El año debe ser un número.")

            elif opcion == '2':
                # --- REGISTRAR USUARIO ---
                print("\n[Registrando nuevo usuario]")
                id_usuario = input("ID de usuario (ej: EST002 o PROF002): ")
                nombre = input("Nombre completo: ")
                # Pedimos la contraseña para el NUEVO usuario
                password = getpass.getpass("Contraseña para el nuevo usuario: ")
                tipo = input("Tipo (1: Estudiante, 2: Profesor): ")

                try:
                    if tipo == '1':
                        carrera = input("Carrera: ")
                        nuevo_usuario = Estudiante(id_usuario, nombre, password, carrera)
                        mi_biblioteca.registrar_estudiante(nuevo_usuario)
                    
                    elif tipo == '2':
                        depto = input("Departamento: ")
                        nuevo_usuario = Profesor(id_usuario, nombre, password, depto)
                        mi_biblioteca.registrar_profesor(nuevo_usuario) # Usamos el nuevo método
                    
                    else:
                        print("Tipo no válido.")
                except Exception as e:
                    print(f"Error al registrar: {e}")

            elif opcion == '3':
                # --- PRESTAR LIBRO ---
                print("\n[Prestando libro]")
                try:
                    id_libro = int(input("ID del libro a prestar: "))
                    id_usuario = input("ID del usuario que lo pide: ")
                    mi_biblioteca.prestar_libro(id_libro, id_usuario)
                except ValueError:
                    print("Error: El ID del libro debe ser un número.")

            elif opcion == '4':
                # --- DEVOLVER LIBRO ---
                print("\n[Devolviendo libro]")
                try:
                    id_libro = int(input("ID del libro a devolver: "))
                    id_usuario = input("ID del usuario que lo devuelve: ")
                    mi_biblioteca.devolver_libro(id_libro, id_usuario)
                except ValueError:
                    print("Error: El ID del libro debe ser un número.")

            elif opcion == '5':
                # --- MOSTRAR LIBROS ---
                mi_biblioteca.mostrar_libros()

            elif opcion == '6':
                # --- SALIR ---
                print("Cerrando conexión y saliendo...")
                mi_biblioteca.cerrar_conexion()
                sys.exit()
                
            else:
                print("Opción no válida. Intente de nuevo.")
                
    else:
        # --- SI FALLA EL LOGIN 3 VECES ---
        print("\nDemasiados intentos fallidos. El programa se cerrará.")
        mi_biblioteca.cerrar_conexion()
        sys.exit()

# --- Punto de entrada del programa ---
if __name__ == "__main__":
    main()