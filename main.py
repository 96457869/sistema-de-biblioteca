from biblioteca import Biblioteca

def main():
    mi_biblioteca = Biblioteca()
    
    print("SISTEMA DE BIBLIOTECA SIMPLE")
    print("============================")
    
    # entonces Se agrega el año como tercer dato al llamar la función
    mi_biblioteca.agregar_libro("El Principito", "Antoine de Saint-Exupery", 1943)
    mi_biblioteca.agregar_libro("1984", "George Orwell", 1949)
    mi_biblioteca.agregar_libro("Cien anos de soledad", "Gabriel Garcia Marquez", 1967)
    
    mi_biblioteca.registrar_usuario("Ana Garcia", "U001")
    mi_biblioteca.registrar_usuario("Luis Martinez", "U002")
    
    mi_biblioteca.mostrar_libros()
    mi_biblioteca.mostrar_usuarios()
    
    print("\n--- REALIZANDO PRESTAMOS ---")
    mi_biblioteca.prestar_libro("El Principito", "U001")
    mi_biblioteca.prestar_libro("1984", "U002")
    
    print("\n--- DESPUES DE PRESTAMOS ---")
    mi_biblioteca.mostrar_libros()
    mi_biblioteca.mostrar_usuarios()
    
    print("\n--- DEVOLVIENDO LIBRO ---")
    mi_biblioteca.devolver_libro("El Principito", "U001")
    
    print("\n--- ESTADO FINAL ---")
    mi_biblioteca.mostrar_libros()
    mi_biblioteca.mostrar_usuarios()

if __name__ == "__main__":
    main()