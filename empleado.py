from persona import Persona
from datetime import date

class Empleado(Persona):

    def __init__(self, nombre: str, direccion: str, telefono: str, email: str, 
                 fecha_inicio: date, salario: float, id_departamento: int):
                   
        super().__init__(nombre, direccion, telefono, email)
        
        self._id_empleado = None  
        self._fecha_inicio = fecha_inicio
        self._salario = salario
        self._id_departamento = id_departamento

    @property
    def id_empleado(self):
        return self._id_empleado

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @property
    def salario(self):
        return self._salario

    @property
    def id_departamento(self):
        return self._id_departamento
    
    @id_empleado.setter
    def id_empleado(self, id_empleado):
        self._id_empleado = id_empleado

    @salario.setter
    def salario(self, nuevo_salario):
        if nuevo_salario > 0:
            self._salario = nuevo_salario
        else:
            print("Error: El salario debe ser un valor positivo.")
    
    @id_departamento.setter
    def id_departamento(self, id_departamento):
        self._id_departamento = id_departamento

    
    def mostrar_info(self):
      
        info_persona = f"Nombre: {self._nombre}, Email: {self._email}"
        info_empleado = f"ID: {self._id_empleado}, Salario: ${self._salario:,.2f}"
        return f"Empleado [{info_empleado}] - Contacto [{info_persona}]"
    def __str__(self):
        return self.mostrar_info()
