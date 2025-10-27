from biblioteca import Biblioteca
from libro import Libro
from usuario import Estudiante, Profesor
import sys
import getpass  # Para ocultar la contraseña al escribirla

# --- FUNCIÓN PARA EL MENÚ PRINCIPAL (DESPUÉS DEL LOGIN) ---
def mostrar_menu_principal():
    print("\n--- MENÚ DE LA BIBLIOTECA ---")
    print("1. Agregar un nuevo libro")
    print("2. Prestar un libro")
    print("3. Devolver un libro")
    print("4. Mostrar todos los libros")
    print("5. Mostrar todos los usuarios")
    print("6. Eliminar un libro")
    print("7. Eliminar un usuario")
    print("8. Salir")

# --- FUNCIÓN PARA EL BUCLE PRINCIPAL (DESPUÉS DEL LOGIN) ---
def iniciar_aplicacion(mi_biblioteca: Biblioteca):
    while True:
        mostrar_menu_principal()
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
            # --- PRESTAR LIBRO ---
            print("\n[Prestando libro]")
            try:
                id_libro = int(input("ID del libro a prestar: "))
                id_usuario = input("ID del usuario que lo pide: ")
                mi_biblioteca.prestar_libro(id_libro, id_usuario)
            except ValueError:
                print("Error: El ID del libro debe ser un número.")

        elif opcion == '3':
            # --- DEVOLVER LIBRO ---
            print("\n[Devolviendo libro]")
            try:
                id_libro = int(input("ID del libro a devolver: "))
                id_usuario = input("ID del usuario que lo devuelve: ")
                mi_biblioteca.devolver_libro(id_libro, id_usuario)
            except ValueError:
                print("Error: El ID del libro debe ser un número.")

        elif opcion == '4':
            # --- MOSTRAR LIBROS ---
            mi_biblioteca.mostrar_libros()

        elif opcion == '5':
            # --- (NUEVO) MOSTRAR USUARIOS ---
            mi_biblioteca.mostrar_usuarios()

        elif opcion == '6':
            # --- (NUEVO) ELIMINAR LIBRO ---
            print("\n[Eliminando libro]")
            try:
                id_libro = int(input("ID del libro a eliminar: "))
                mi_biblioteca.eliminar_libro(id_libro)
            except ValueError:
                print("Error: El ID del libro debe ser un número.")
                
        elif opcion == '7':
            # --- (NUEVO) ELIMINAR USUARIO ---
            print("\n[Eliminando usuario]")
            id_usuario = input("ID del usuario a eliminar: ")
            mi_biblioteca.eliminar_usuario(id_usuario)

        elif opcion == '8':
            # --- SALIR ---
            print("Cerrando conexión y saliendo...")
            mi_biblioteca.cerrar_conexion()
            sys.exit()
            
        else:
            print("Opción no válida. Intente de nuevo.")

# --- FUNCIÓN PARA REGISTRAR (AHORA SEPARADA) ---
def registrar_nuevo_usuario(mi_biblioteca: Biblioteca):
    print("\n[Registrando nuevo usuario]")
    id_usuario = input("ID de usuario (ej: EST002 o PROF002): ")
    nombre = input("Nombre completo: ")
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
            mi_biblioteca.registrar_profesor(nuevo_usuario)
        
        else:
            print("Tipo no válido.")
    except Exception as e:
        print(f"Error al registrar: {e}")

# --- FUNCIÓN DE INICIO (LA PRINCIPAL) ---
def main():
    try:
        # 1. Conectar a la BD
        mi_biblioteca = Biblioteca()
    except Exception as e:
        print(f"Error fatal al conectar con la BD. Revisa tus credenciales o el servicio MySQL.")
        print(f"Detalle: {e}")
        sys.exit(1)

    # --- 2. NUEVO MENÚ DE BIENVENIDA (TU IDEA) ---
    while True:
        print("\n--- BIENVENIDO AL SISTEMA DE BIBLIOTECA ---")
        print("1. Iniciar Sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir")
        opcion_inicio = input("Seleccione una opción: ")

        if opcion_inicio == '1':
            # --- BUCLE DE LOGIN ---
            autenticado = False
            intentos = 0
            while not autenticado and intentos < 3:
                print("\n--- INICIO DE SESIÓN ---")
                id_usuario = input("ID de Usuario: ")
                password = getpass.getpass("Contraseña: ") 
                
                autenticado = mi_biblioteca.login(id_usuario, password)
                if not autenticado:
                    intentos += 1
                    print(f"Acceso denegado. Quedan {3 - intentos} intentos.")
            
            if autenticado:
                # Si el login es exitoso, inicia la app principal
                iniciar_aplicacion(mi_biblioteca)
            else:
                print("\nDemasiados intentos fallidos.")

        elif opcion_inicio == '2':
            # --- REGISTRAR USUARIO ---
            registrar_nuevo_usuario(mi_biblioteca)
            print("Registro completado. Ahora puede iniciar sesión.")

        elif opcion_inicio == '3':
            # --- SALIR ---
            print("Cerrando conexión y saliendo...")
            mi_biblioteca.cerrar_conexion()
            sys.exit()
            
        else:
            print("Opción no válida. Intente de nuevo.")

# --- Punto de entrada del programa (MODIFICADO PARA .EXE) ---
if __name__ == "__main__":
    try:
        main()
        
    except SystemExit:
        # Esto captura el sys.exit() cuando el usuario elige "Salir"
        # y permite que el script continúe al 'finally'
        pass 
        
    except Exception as e:
        # Esto captura cualquier error inesperado que crashee el programa
        print("\n\n--- HA OCURRIDO UN ERROR INESPERADO ---")
        print(f"ERROR: {e}")
        
    finally:
        # Esto SIEMPRE se ejecutará
        print("\n\nPresiona ENTER para cerrar esta ventana.")
        input() # <-- Esta es la línea que pausa la ventana