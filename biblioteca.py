from libro import Libro
from usuario import Estudiante, Profesor
from prestamo import Prestamo
from database import DBConector
import datetime
import logging
import bcrypt

class Biblioteca:
    def __init__(self):
        # (Tu __init__ no cambia)
        self.db = DBConector()
        self.prestamos_activos = []
        self.logger = logging.getLogger(__name__)
        try:
            if not self.db.connect():
                self.logger.error("No se pudo conectar a la base de datos al inicializar")
                raise ConnectionError("Fallo en la conexión inicial a la BD")
        except Exception as e:
            self.logger.critical(f"Error fatal de conexión: {e}")
            raise

    # --- MÉTODO DE LOGIN (CORREGIDO) ---
    def login(self, id_usuario: str, password_ingresada: str):
        """
        Verifica el login de un usuario contra la base de datos.
        Usa bcrypt para comparar contraseñas de forma segura.
        """
        try:
            query = "SELECT password FROM usuarios WHERE id_usuario = %s"
            resultado = self.db.fetch_one(query, (id_usuario,))
            
            if resultado:
                # --- ¡CAMBIO IMPORTANTE AQUÍ! ---
                # resultado[0] YA es 'bytes' porque la columna es BINARY.
                # No necesitamos .encode('utf-8')
                password_guardada_hash = resultado[0] 
                # ---------------------------------

                password_ingresada_bytes = password_ingresada.encode('utf-8')
                
                # bcrypt comprueba si la contraseña ingresada coincide con la guardada
                if bcrypt.checkpw(password_ingresada_bytes, password_guardada_hash):
                    print(f"\n¡Bienvenido, {id_usuario}!")
                    return True
                else:
                    print("Contraseña incorrecta.")
                    return False
            else:
                print("Usuario no encontrado.")
                return False
        except Exception as e:
            print(f"Error durante el login: {e}")
            return False

    # --- (EL RESTO DEL ARCHIVO ES IDÉNTICO) ---

    def agregar_libro(self, libro: Libro):
        # (Tu código de agregar_libro)
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
        # (Tu código de registrar_estudiante)
        query = "INSERT INTO usuarios (id_usuario, nombre, password, tipo, carrera_depto) VALUES (%s, %s, %s, %s, %s)"
        hashed_pw = bcrypt.hashpw(estudiante.password.encode('utf-8'), bcrypt.gensalt())
        valores = (estudiante.id_usuario, estudiante.nombre, hashed_pw, 'Estudiante', estudiante.carrera)
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

    def registrar_profesor(self, profesor: Profesor):
        # (Tu código de registrar_profesor)
        query = "INSERT INTO usuarios (id_usuario, nombre, password, tipo, carrera_depto) VALUES (%s, %s, %s, %s, %s)"
        hashed_pw = bcrypt.hashpw(profesor.password.encode('utf-8'), bcrypt.gensalt())
        valores = (profesor.id_usuario, profesor.nombre, hashed_pw, 'Profesor', profesor.departamento)
        try:
            success = self.db.execute_query(query, valores)
            if success:
                print(f"Profesor '{profesor.nombre}' registrado en la base de datos.")
                return True
            else:
                print("Error al registrar al profesor en la base de datos.")
                return False
        except Exception as e:
            print(f"Error al registrar al profesor: {e}")
            return False

    def prestar_libro(self, id_libro: int, id_usuario: str):
        # (Tu código de prestar_libro)
        try:
            libro_disponible_query = "SELECT disponible FROM libros WHERE id_libro = %s"
            resultado = self.db.fetch_one(libro_disponible_query, (id_libro,))
            if resultado and resultado[0]:
                update_libro_query = "UPDATE libros SET disponible = FALSE WHERE id_libro = %s"
                success_update = self.db.execute_query(update_libro_query, (id_libro,))
                if success_update:
                    nuevo_prestamo = Prestamo(id_libro, id_usuario, datetime.date.today())
                    insert_prestamo_query = "INSERT INTO prestamos (id_libro, id_usuario, fecha_prestamo, devuelto) VALUES (%s, %s, %s, %s)"
                    valores_prestamo = (nuevo_prestamo.id_libro, nuevo_prestamo.id_usuario, nuevo_prestamo.fecha_prestamo, False)
                    success_insert = self.db.execute_query(insert_prestamo_query, valores_prestamo)
                    if success_insert:
                        print(f"Préstamo del libro ID {id_libro} al usuario {id_usuario} registrado con éxito.")
                        return True
                    else:
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
        # (Tu código de devolver_libro)
        try:
            update_libro_query = "UPDATE libros SET disponible = TRUE WHERE id_libro = %s"
            success_libro = self.db.execute_query(update_libro_query, (id_libro,))
            if success_libro:
                update_prestamo_query = "UPDATE prestamos SET fecha_devolucion = %s, devuelto = TRUE WHERE id_libro = %s AND id_usuario = %s AND devuelto = FALSE"
                success_prestamo = self.db.execute_query(update_prestamo_query, (datetime.date.today(), id_libro, id_usuario))
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
        # (Tu código de mostrar_libros)
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
        # (Tu código de buscar_libro_por_titulo)
        try:
            query = "SELECT id_libro, titulo, autor, disponible FROM libros WHERE titulo LIKE %s"
            resultados = self.db.fetch_all(query, (f"%{titulo}%",))
            return resultados
        except Exception as e:
            print(f"Error al buscar libro: {e}")
            return []

    # --- ¡NUEVOS MÉTODOS CRUD AÑADIDOS! ---

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados."""
        try:
            query = "SELECT id_usuario, nombre, tipo, carrera_depto FROM usuarios"
            resultados = self.db.fetch_all(query)
            print("\n--- Lista de Usuarios ---")
            for id_usuario, nombre, tipo, carrera_depto in resultados:
                print(f"ID: {id_usuario} | Nombre: {nombre} | Tipo: {tipo} | Depto/Carrera: {carrera_depto}")
            return resultados
        except Exception as e:
            print(f"Error al mostrar los usuarios: {e}")
            return []

    def eliminar_libro(self, id_libro: int):
        """Elimina un libro si no tiene préstamos activos."""
        try:
            query_prestamos = "SELECT 1 FROM prestamos WHERE id_libro = %s AND devuelto = FALSE"
            prestamo_activo = self.db.fetch_one(query_prestamos, (id_libro,))
            
            if prestamo_activo:
                print(f"Error: No se puede eliminar el libro ID {id_libro} porque tiene un préstamo activo.")
                return False
                
            # Si no hay préstamos, borramos primero de préstamos (historial) y luego de libros
            query_delete_prestamos = "DELETE FROM prestamos WHERE id_libro = %s"
            self.db.execute_query(query_delete_prestamos, (id_libro,))
            
            query_delete_libro = "DELETE FROM libros WHERE id_libro = %s"
            success = self.db.execute_query(query_delete_libro, (id_libro,))
            
            if success:
                print(f"Libro ID {id_libro} eliminado correctamente.")
                return True
            else:
                print("Error al eliminar el libro (no se encontró o ya fue eliminado).")
                return False
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            return False

    def eliminar_usuario(self, id_usuario: str):
        """Elimina un usuario si no tiene préstamos activos."""
        try:
            query_prestamos = "SELECT 1 FROM prestamos WHERE id_usuario = %s AND devuelto = FALSE"
            prestamo_activo = self.db.fetch_one(query_prestamos, (id_usuario,))
            
            if prestamo_activo:
                print(f"Error: No se puede eliminar el usuario {id_usuario} porque tiene préstamos activos.")
                return False

            # Borramos historial de préstamos y luego el usuario
            query_delete_prestamos = "DELETE FROM prestamos WHERE id_usuario = %s"
            self.db.execute_query(query_delete_prestamos, (id_usuario,))
            
            query_delete_usuario = "DELETE FROM usuarios WHERE id_usuario = %s"
            success = self.db.execute_query(query_delete_usuario, (id_usuario,))
            
            if success:
                print(f"Usuario {id_usuario} eliminado correctamente.")
                return True
            else:
                print("Error al eliminar el usuario (no se encontró o ya fue eliminado).")
                return False
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False

    # --- MÉTODO FINAL (No cambia) ---
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.db.close()