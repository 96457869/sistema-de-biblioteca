class Libro:
    # le agregue 'fecha_publicacion' para guardar el año del libro
    def __init__(self, titulo, autor, fecha_publicacion):
        self.titulo = titulo
        self.autor = autor
        self.fecha_publicacion = fecha_publicacion
        self.disponible = True
    
    def mostrar_info(self):
        estado = "Disponible" if self.disponible else "Prestado"
        # esto lo agregue porque lo que hace actualiza para mostrar también el año de publicación de los libros eso pense
        return f"'{self.titulo}' por {self.autor} ({self.fecha_publicacion}) - {estado}"