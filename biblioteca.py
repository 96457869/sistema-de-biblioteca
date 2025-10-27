from libro import Libro
from usuario import Estudiante, Profesor
from prestamo import Prestamo
from database import DBConector
import datetime
import logging

class Biblioteca:
    def __init__(self):
        # Inicializamos el conector real
        self.db = DBConector()
        self.prestamos_activos = []
        self.logger = logging.getLogger(__name__)
        
        # Conectar automáticamente al inicializar
        if not self.db.connect():
            self.logger.error("No se pudo conectar a la base de datos al inicializar")

    def agregar_libro(self, libro: Libro):
        query = "INSERT INTO libros (titulo, autor, fecha_publicacion, disponible) VALUES (%s, %s, %s, %s)"
        valores = (libro.titulo, libro.autor, libro.fecha_publicacion, libro.disponible)
        try:
            success = self.db.execute_query(query, valores)
            if success:
                print(f"Libro '{libro.titulo}' agregado a la base de datos.")
                return True
            else:
                print("Error al agregar el libro a la base de datos.")
                return False
        except Exception as e:
            print(f"Error al agregar el libro: {e}")
            return False

    def registrar_estudiante(self, estudiante: Estudiante):
        query = "INSERT INTO usuarios (id_usuario, nombre, tipo, carrera_depto) VALUES (%s, %s, %s, %s)"
        valores = (estudiante.id_usuario, estudiante.nombre, 'Estudiante', estudiante.carrera)
        try:
            success = self.db.execute_query(query, valores)
            if success:
                print(f"Estudiante '{estudiante.nombre}' registrado en la base de datos.")
                return True
            else:
                print("Error al registrar al estudiante en la base de datos.")
                return False
        except Exception as e:
            print(f"Error al registrar al estudiante: {e}")
            return False

    def prestar_libro(self, id_libro: int, id_usuario: str):
        try:
            # Verificar si el libro existe y está disponible
            libro_disponible_query = "SELECT disponible FROM libros WHERE id_libro = %s"
            resultado = self.db.fetch_one(libro_disponible_query, (id_libro,))
            
            if resultado and resultado[0]:  # Si existe y está disponible
                # Actualizar libro a no disponible
                update_libro_query = "UPDATE libros SET disponible = FALSE WHERE id_libro = %s"
                success_update = self.db.execute_query(update_libro_query, (id_libro,))
                
                if success_update:
                    # Registrar préstamo
                    nuevo_prestamo = Prestamo(id_libro, id_usuario, datetime.date.today())
                    insert_prestamo_query = """
                    INSERT INTO prestamos (id_libro, id_usuario, fecha_prestamo, devuelto) 
                    VALUES (%s, %s, %s, %s)
                    """
                    valores_prestamo = (nuevo_prestamo.id_libro, nuevo_prestamo.id_usuario, 
                                      nuevo_prestamo.fecha_prestamo, False)
                    
                    success_insert = self.db.execute_query(insert_prestamo_query, valores_prestamo)
                    
                    if success_insert:
                        print(f"Préstamo del libro ID {id_libro} al usuario {id_usuario} registrado con éxito.")
                        return True
                    else:
                        # Revertir cambio en libro si falla el préstamo
                        self.db.execute_query("UPDATE libros SET disponible = TRUE WHERE id_libro = %s", (id_libro,))
                        print("Error al registrar el préstamo.")
                        return False
                else:
                    print("Error al actualizar el estado del libro.")
                    return False
            else:
                print("El libro no está disponible para préstamo o no existe.")
                return False
                
        except Exception as e:
            print(f"Error al realizar el préstamo: {e}")
            return False

    def devolver_libro(self, id_libro: int, id_usuario: str):
        try:
            # Actualizar libro a disponible
            update_libro_query = "UPDATE libros SET disponible = TRUE WHERE id_libro = %s"
            success_libro = self.db.execute_query(update_libro_query, (id_libro,))
            
            if success_libro:
                # Actualizar préstamo como devuelto
                update_prestamo_query = """
                UPDATE prestamos 
                SET fecha_devolucion = %s, devuelto = TRUE 
                WHERE id_libro = %s AND id_usuario = %s AND devuelto = FALSE
                """
                success_prestamo = self.db.execute_query(update_prestamo_query, 
                                                       (datetime.date.today(), id_libro, id_usuario))
                
                if success_prestamo:
                    print(f"Devolución del libro ID {id_libro} registrada con éxito.")
                    return True
                else:
                    print("Error al actualizar el registro de préstamo.")
                    return False
            else:
                print("Error al actualizar el estado del libro.")
                return False
                
        except Exception as e:
            print(f"Error al devolver el libro: {e}")
            return False
            
    def mostrar_libros(self):
        try:
            query = "SELECT id_libro, titulo, autor, fecha_publicacion, disponible FROM libros"
            resultados = self.db.fetch_all(query)
            print("\n--- Catálogo de Libros ---")
            for id_libro, titulo, autor, fecha_publicacion, disponible in resultados:
                estado = "Disponible" if disponible else "Prestado"
                print(f"ID: {id_libro} | Título: {titulo} | Autor: {autor} | Año: {fecha_publicacion} | Estado: {estado}")
            return resultados
        except Exception as e:
            print(f"Error al mostrar los libros: {e}")
            return []

    def buscar_libro_por_titulo(self, titulo):
        """Método adicional para buscar libros por título"""
        try:
            query = "SELECT id_libro, titulo, autor, disponible FROM libros WHERE titulo LIKE %s"
            resultados = self.db.fetch_all(query, (f"%{titulo}%",))
            return resultados
        except Exception as e:
            print(f"Error al buscar libro: {e}")
            return []

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.db.close()