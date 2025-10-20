from biblioteca import Biblioteca
from libro import Libro
from usuario import Estudiante, Profesor

def mostrar_menu():
    print("\n--- MENÚ DE LA BIBLIoteca ---")
    print("1. Agregar un nuevo libro")
    print("2. Registrar un nuevo usuario (Estudiante/Profesor)")
    print("3. Prestar un libro")
    print("4. Devolver un libro")
    print("5. Mostrar todos los libros")
    print("6. Salir del programa")
    return input("Seleccione una opción: ")

def main():
    mi_biblioteca = None 
    print("¡Bienvenido al Sistema de Gestión de la Biblioteca!")
    print("ADVERTENCIA: El sistema aún no está conectado a una base de datos.")
    
    continuar_ejecucion = True
    
    while continuar_ejecucion:
        opcion = mostrar_menu()
        
        if opcion == '1':
            print("\n--- Agregar Nuevo Libro ---")
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            fecha = int(input("Ingrese el año de publicación: "))
            nuevo_libro = Libro(titulo, autor, fecha)
            print(f"Libro '{titulo}' listo para ser agregado.")

        elif opcion == '2':
            print("\n--- Registrar Nuevo Usuario ---")
            tipo = input("¿Es 'estudiante' o 'profesor'?: ").lower()
            id_usuario = input("Ingrese el ID del usuario: ")
            nombre = input("Ingrese el nombre completo: ")
            
            if tipo == 'estudiante':
                carrera = input("Ingrese la carrera del estudiante: ")
                estudiante = Estudiante(id_usuario, nombre, carrera)
                print(f"Estudiante '{nombre}' listo para ser registrado.")
            elif tipo == 'profesor':
                depto = input("Ingrese el departamento del profesor: ")
                profesor = Profesor(id_usuario, nombre, depto)
                print(f"Profesor '{nombre}' listo para ser registrado.")
            else:
                print("Tipo de usuario no válido.")

        elif opcion == '3':
            print("\n--- Prestar Libro ---")
            id_libro = int(input("Ingrese el ID del libro a prestar: "))
            id_usuario = input("Ingrese el ID del usuario que solicita el préstamo: ")
            print(f"Préstamo del libro {id_libro} al usuario {id_usuario} listo para procesar.")

        elif opcion == '4':
            print("\n--- Devolver Libro ---")
            id_libro = int(input("Ingrese el ID del libro a devolver: "))
            id_usuario = input("Ingrese el ID del usuario que devuelve: ")
            print(f"Devolución del libro {id_libro} lista para procesar.")

        elif opcion == '5':
            print("Función 'Mostrar Libros' se activará con la base de datos.")

        elif opcion == '6':
            print("Gracias por usar el sistema. ¡Hasta luego!")
            continuar_ejecucion = False
            
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
