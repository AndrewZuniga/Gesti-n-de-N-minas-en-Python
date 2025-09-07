from typing import Dict

class DetalleNomina:
    def __init__(self, id: int, empleado, sueldo: float, bono: float, prestamo: float):
        self.id = id
        self.empleado = empleado  
        self.sueldo = sueldo
        self.bono = bono
        self.tot_ing = sueldo + bono
        self.iess = round(sueldo * 0.0945, 2)
        self.prestamo = prestamo
        self.tot_des = self.iess + prestamo
        self.neto = self.tot_ing - self.tot_des
    
    def to_dict(self) -> Dict:
        """
        Convierte el detalle a diccionario para serialización JSON
        DEBE guardar TODOS los datos del empleado, no solo el nombre
        """
        return {
            'id': self.id,
            'empleado': {
                'cedula': self.empleado.cedula,
                'nombre': self.empleado.nombre,
                'sueldo': self.empleado.sueldo,
                'departamento': self.empleado.departamento,
                'cargo': self.empleado.cargo
            },
            'sueldo': self.sueldo,
            'bono': self.bono,
            'tot_ing': self.tot_ing,
            'iess': self.iess,
            'prestamo': self.prestamo,
            'tot_des': self.tot_des,
            'neto': self.neto
        }
    
    def __str__(self):
        return (f"Detalle {self.id}: {self.empleado.nombre} - "
                f"Sueldo: ${self.sueldo} + Bono: ${self.bono} - "
                f"IESS: ${self.iess} - Préstamo: ${self.prestamo} = "
                f"Neto: ${self.neto}")
    
    def __repr__(self):
        return f"DetalleNomina(id={self.id}, empleado='{self.empleado.nombre}', neto={self.neto})"