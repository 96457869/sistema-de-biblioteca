import datetime

class Prestamo:
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = datetime.date.today()
        self.fecha_devolucion = None
        self.devuelto = False
    
    def calcular_dias_retraso(self):
        if self.devuelto and self.fecha_devolucion:
            dias_transcurridos = (self.fecha_devolucion - self.fecha_prestamo).days
        else:
            dias_transcurridos = (datetime.date.today() - self.fecha_prestamo).days
        
        dias_permitidos = self.usuario.get_dias_prestamo()
        return max(0, dias_transcurridos - dias_permitidos)
    
    def calcular_multa(self):
        dias_retraso = self.calcular_dias_retraso()
        return dias_retraso * 100  
