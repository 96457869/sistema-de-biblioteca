import datetime

class Prestamo:
    def __init__(self, id_libro: int, id_usuario: str, fecha_prestamo: datetime.date):
        self._id_prestamo = None
        self._id_libro = id_libro
        self._id_usuario = id_usuario
        self._fecha_prestamo = fecha_prestamo
        self._fecha_devolucion = None
        self._devuelto = False

    @property
    def id_prestamo(self):
        return self._id_prestamo

    @property
    def id_libro(self):
        return self._id_libro

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def fecha_prestamo(self):
        return self._fecha_prestamo

    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion

    def marcar_devolucion(self):
        self._devuelto = True
        self._fecha_devolucion = datetime.date.today()

    def calcular_dias_retraso(self, dias_permitidos: int):
        if self._devuelto and self._fecha_devolucion:
            dias_transcurridos = (self._fecha_devolucion - self._fecha_prestamo).days
        else:
            dias_transcurridos = (datetime.date.today() - self._fecha_prestamo).days
        
        return max(0, dias_transcurridos - dias_permitidos)

    def calcular_multa(self, dias_permitidos: int, costo_por_dia: float):
        dias_retraso = self.calcular_dias_retraso(dias_permitidos)
        return dias_retraso * costo_por_dia
