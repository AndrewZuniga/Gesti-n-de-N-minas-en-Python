from typing import List, Dict
from functools import reduce
from modelos.detalle_nomina import DetalleNomina

class Nomina:
    """
    Representa una nómina mensual con todos los detalles de empleados
    y totales consolidados.
    """
    
    # Constantes de clase (valores fijos)
    BONO = 50.0
    PRESTAMO = 20.0
    
    def __init__(self, id: int, aniomes: str):
        self.id = id
        self.aniomes = aniomes
        self.detalles: List[DetalleNomina] = []
        self.tot_ing = 0.0
        self.tot_des = 0.0
        self.neto = 0.0
    
    def agregar_detalle(self, detalle: DetalleNomina) -> None:
        """
        Agrega un detalle a la nómina y actualiza los totales
        """
        self.detalles.append(detalle)
        self._actualizar_totales()
    
    def _actualizar_totales(self) -> None:
        """
        Actualiza los totales usando reduce y lambdas (como requiere el proyecto)
        """
        # Usando REDUCE y LAMBDAS para cumplir con el requerimiento
        self.tot_ing = reduce(lambda acumulado, detalle: acumulado + detalle.tot_ing, 
                            self.detalles, 0.0)
        
        self.tot_des = reduce(lambda acumulado, detalle: acumulado + detalle.tot_des, 
                            self.detalles, 0.0)
        
        self.neto = reduce(lambda acumulado, detalle: acumulado + detalle.neto, 
                         self.detalles, 0.0)
    
    def to_dict(self) -> Dict:
        """
        Convierte la nómina completa a diccionario para JSON
        """
        return {
            'id': self.id,
            'aniomes': self.aniomes,
            'tot_ing': self.tot_ing,
            'tot_des': self.tot_des,
            'neto': self.neto,
            'detalles': [detalle.to_dict() for detalle in self.detalles]
        }
    
    def generar_estadisticas(self) -> Dict:
        """
        Genera estadísticas usando funciones de orden superior
        """
        # Usando LAMBDAS, MAP, FILTER y REDUCE como requiere el proyecto
        
        # Lista de netos usando comprehension
        netos = [detalle.neto for detalle in self.detalles]
        
        # Lista de sueldos usando map
        sueldos = list(map(lambda d: d.sueldo, self.detalles))
        
        return {
            'total_empleados': len(self.detalles),
            'total_neto': reduce(lambda a, b: a + b, netos, 0.0),
            'promedio_sueldos': reduce(lambda a, b: a + b, sueldos, 0.0) / len(sueldos) if sueldos else 0,
            'empleados_alto_sueldo': list(filter(lambda d: d.sueldo > 1000, self.detalles)),
            'empleado_mayor_neto': max(self.detalles, key=lambda d: d.neto) if self.detalles else None,
            'empleado_menor_neto': min(self.detalles, key=lambda d: d.neto) if self.detalles else None,
            'total_aporte_iess': reduce(lambda a, b: a + b.iess, self.detalles, 0.0)
        }
    
    def __str__(self):
        return (f"Nómina {self.aniomes}: {len(self.detalles)} empleados - "
                f"Ingresos: ${self.tot_ing} - Descuentos: ${self.tot_des} - "
                f"Neto: ${self.neto}")