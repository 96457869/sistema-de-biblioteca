class Libro:
    def __init__(self, titulo: str, autor: str, fecha_publicacion: int):
        self._id_libro = None
        self._titulo = titulo
        self._autor = autor
        self._fecha_publicacion = fecha_publicacion
        self._disponible = True

    @property
    def id_libro(self):
        return self._id_libro

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor
    
    @property
    def fecha_publicacion(self):
        return self._fecha_publicacion

    @property
    def disponible(self):
        return self._disponible
    
    @id_libro.setter
    def id_libro(self, id_libro):
        self._id_libro = id_libro

    def cambiar_estado(self, nuevo_estado: bool):
        self._disponible = nuevo_estado

    def mostrar_info(self):
        estado = "Disponible" if self._disponible else "Prestado"
        return f"ID: {self._id_libro} | '{self._titulo}' por {self._autor} ({self._fecha_publicacion}) - {estado}"

    def __str__(self):
        return self.mostrar_info()
