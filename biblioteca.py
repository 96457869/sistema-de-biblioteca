from libro import Libro  
from usuario import Usuario  

class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
    
    # le modifique esta función para que reciba la fecha de publicación
    def agregar_libro(self, titulo, autor, fecha_publicacion):
        # Se pasa la fecha al crear el nuevo libro aunque no estoy seguro de si lo hice bien
        nuevo_libro = Libro(titulo, autor, fecha_publicacion)
        self.libros.append(nuevo_libro)
        print(f"Libro agregado: {titulo}")
    
    def registrar_usuario(self, nombre, id_usuario):
        nuevo_usuario = Usuario(nombre, id_usuario)
        self.usuarios.append(nuevo_usuario)
        print(f"Usuario registrado: {nombre}")
    
    def prestar_libro(self, titulo_libro, id_usuario):
        libro_encontrado = None
        for libro in self.libros:
            if libro.titulo.lower() == titulo_libro.lower() and libro.disponible:
                libro_encontrado = libro
                break
        
        usuario_encontrado = None
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                usuario_encontrado = usuario
                break
        
        if libro_encontrado and usuario_encontrado:
            libro_encontrado.disponible = False
            usuario_encontrado.libros_prestados.append(libro_encontrado.titulo)
            print(f"Prestamo exitoso: {libro_encontrado.titulo} -> {usuario_encontrado.nombre}")
        else:
            print("Error: Libro no disponible o usuario no encontrado")
    
    def devolver_libro(self, titulo_libro, id_usuario):
        for libro in self.libros:
            if libro.titulo.lower() == titulo_libro.lower() and not libro.disponible:
                for usuario in self.usuarios:
                    if usuario.id_usuario == id_usuario and titulo_libro in usuario.libros_prestados:
                        libro.disponible = True
                        usuario.libros_prestados.remove(titulo_libro)
                        print(f"Devolucion exitosa: {libro.titulo} <- {usuario.nombre}")
                        return
        print("Error: No se pudo completar la devolucion")
    
    def mostrar_libros(self):
        print("\n--- LIBROS EN BIBLIOTECA ---")
        for libro in self.libros:
            print(libro.mostrar_info())
    
    def mostrar_usuarios(self):
        print("\n--- USUARIOS REGISTRADOS ---")
        for usuario in self.usuarios:
            print(usuario.mostrar_info())