from typing import Dict
#from utils.decoradores import validar_empleado_completo

class Empleado:
    #@validar_empleado_completo
    def __init__(self, cedula: str, nombre: str, sueldo: float, 
                 departamento: str, cargo: str):
        self.cedula = cedula
        self.nombre = nombre
        self.sueldo = sueldo
        self.departamento = departamento
        self.cargo = cargo
    
    def to_dict(self) -> Dict:
        """
        Convierte el empleado a diccionario para JSON
        """
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'sueldo': self.sueldo,
            'departamento': self.departamento,
            'cargo': self.cargo
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Empleado':
        """
        Crea un empleado desde un diccionario
        """
        return cls(
            data['cedula'],
            data['nombre'],
            data['sueldo'],
            data['departamento'],
            data['cargo']
        )
    
    def __str__(self):
        return f"{self.nombre} ({self.cedula}) - ${self.sueldo:.2f} - {self.cargo}"
    
    def __repr__(self):
        return f"Empleado(cedula='{self.cedula}', nombre='{self.nombre}', sueldo={self.sueldo})"