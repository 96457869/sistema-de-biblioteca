from biblioteca import Biblioteca
from libro import Libro
from usuario import Estudiante, Profesor
import mysql.connector

def mostrar_menu():
    print("\n--- MENÚ DE LA BIBLIOTECA ---")
    print("1. Agregar un nuevo libro")
    print("2. Registrar un nuevo usuario (Estudiante/Profesor)")
    print("3. Prestar un libro")
    print("4. Devolver un libro")
    print("5