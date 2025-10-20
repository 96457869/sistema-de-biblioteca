from libro import Libro
from usuario import Estudiante, Profesor
from prestamo import Prestamo
import datetime

class Biblioteca:
    def __init__(self, db_conector):
        self.db = db_conector
        self.prestamos_activos = []

    def agregar_libro(self, libro: Libro):
        query = "INSERT INTO libros (titulo, autor, fecha_publicacion, disponible) VALUES (%s, %s, %s, %s)"
        valores = (libro.titulo, libro.autor, libro.fecha_publicacion, libro.disponible)
        try:
            self.db.execute_query(query, valores)
            print(f"Libro '{libro.titulo}' agregado a la base de datos.")
        except Exception as e:
            print(f"Error al agregar el libro: {e}")

    def registrar_estudiante(self, estudiante: Estudiante):
        query = "INSERT INTO usuarios (id_usuario, nombre, tipo, carrera_depto) VALUES (%s, %s, %s, %s)"
        valores = (estudiante.id_usuario, estudiante.nombre, 'Estudiante', estudiante.carrera)
        try:
            self.db.execute_query(query, valores)
            print(f"Estudiante '{estudiante.nombre}' registrado en la base de datos.")
        except Exception as e:
            print(f"Error al registrar al estudiante: {e}")

    def prestar_libro(self, id_libro: int, id_usuario: str):
        try:
            libro_disponible_query = "SELECT disponible FROM libros WHERE id_libro = %s"
            resultado = self.db.fetch_one(libro_disponible_query, (id_libro,))
            
            if resultado and resultado[0]:
                update_libro_query = "UPDATE libros SET disponible = FALSE WHERE id_libro = %s"
                self.db.execute_query(update_libro_query, (id_libro,))

                nuevo_prestamo = Prestamo(id_libro, id_usuario, datetime.date.today())
                insert_prestamo_query = "INSERT INTO prestamos (id_libro, id_usuario, fecha_prestamo) VALUES (%s, %s, %s)"
                valores_prestamo = (nuevo_prestamo.id_libro, nuevo_prestamo.id_usuario, nuevo_prestamo.fecha_prestamo)
                self.db.execute_query(insert_prestamo_query, valores_prestamo)
                
                print(f"Préstamo del libro ID {id_libro} al usuario {id_usuario} registrado con éxito.")
            else:
                print("El libro no está disponible para préstamo o no existe.")
        except Exception as e:
            print(f"Error al realizar el préstamo: {e}")

    def devolver_libro(self, id_libro: int, id_usuario: str):
        try:
            update_libro_query = "UPDATE libros SET disponible = TRUE WHERE id_libro = %s"
            self.db.execute_query(update_libro_query, (id_libro,))
            
            update_prestamo_query = """
            UPDATE prestamos 
            SET fecha_devolucion = %s, devuelto = TRUE 
            WHERE id_libro = %s AND id_usuario = %s AND devuelto = FALSE
            """
            self.db.execute_query(update_prestamo_query, (datetime.date.today(), id_libro, id_usuario))
            
            print(f"Devolución del libro ID {id_libro} registrada con éxito.")
        except Exception as e:
            print(f"Error al devolver el libro: {e}")
            
    def mostrar_libros(self):
        try:
            query = "SELECT id_libro, titulo, autor, disponible FROM libros"
            resultados = self.db.fetch_all(query)
            print("\n--- Catálogo de Libros ---")
            for id_libro, titulo, autor, disponible in resultados:
                estado = "Disponible" if disponible else "Prestado"
                print(f"ID: {id_libro} | Título: {titulo} | Autor: {autor} | Estado: {estado}")
        except Exception as e:
            print(f"Error al mostrar los libros: {e}")
