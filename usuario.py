class Usuario:

    def __init__(self, id_usuario: str, nombre: str):
        
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._libros_prestados = []
        
    @property
    def nombre(self):
        return self._nombre

    @property
    def id_usuario(self):
        return self._id_usuario

    def mostrar_info(self):
  
        return f"ID: {self._id_usuario}, Nombre: {self._nombre}"

    def __str__(self):
        return self.mostrar_info()

class Estudiante(Usuario):

    def __init__(self, id_usuario: str, nombre: str, carrera: str):
        super().__init__(id_usuario, nombre)
        self._carrera = carrera

    def mostrar_info(self):

        info_padre = super().mostrar_info()
        return f"Estudiante [{info_padre}, Carrera: {self._carrera}]"

class Profesor(Usuario):

    def __init__(self, id_usuario: str, nombre: str, departamento: str):
        super().__init__(id_usuario, nombre)

        self._departamento = departamento

    def mostrar_info(self):
       
        info_padre = super().mostrar_info()
        return f"Profesor [{info_padre}, Departamento: {self._departamento}]"
