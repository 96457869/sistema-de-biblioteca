class Usuario:

    def __init__(self, id_usuario: str, nombre: str, password: str):  # <-- CAMBIO AQUÍ
        
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._password = password  # <-- CAMBIO AQUÍ
        self._libros_prestados = []
        
    @property
    def nombre(self):
        return self._nombre

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def password(self):  # <-- AÑADIDO ESTO
        return self._password

    def mostrar_info(self):
  
        return f"ID: {self._id_usuario}, Nombre: {self._nombre}"

    def __str__(self):
        return self.mostrar_info()

class Estudiante(Usuario):

    # <-- CAMBIO EN LOS PARÁMETROS:
    def __init__(self, id_usuario: str, nombre: str, password: str, carrera: str):
        super().__init__(id_usuario, nombre, password) # <-- CAMBIO AQUÍ (pasa la pass al padre)
        self._carrera = carrera

    @property
    def carrera(self): # <-- Añadido para que biblioteca.py pueda usarlo
        return self._carrera

    def mostrar_info(self):
        info_padre = super().mostrar_info()
        return f"Estudiante [{info_padre}, Carrera: {self._carrera}]"

class Profesor(Usuario):

    # <-- CAMBIO EN LOS PARÁMETROS:
    def __init__(self, id_usuario: str, nombre: str, password: str, departamento: str):
        super().__init__(id_usuario, nombre, password) # <-- CAMBIO AQUÍ (pasa la pass al padre)
        self._departamento = departamento

    @property
    def departamento(self): # <-- Añadido para que biblioteca.py pueda usarlo
        return self._departamento

    def mostrar_info(self):
        info_padre = super().mostrar_info()
        return f"Profesor [{info_padre}, Departamento: {self._departamento}]"