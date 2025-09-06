from typing import List, Dict, TYPE_CHECKING  
from functools import reduce

if TYPE_CHECKING:
    from modelos.detalle_nomina import DetalleNomina

def calcular_total_neto(detalles: List['DetalleNomina']) -> float:  
    """
    Calcula el total neto usando reduce y lambda
    """
    return reduce(lambda acc, detalle: acc + detalle.neto, detalles, 0.0)

def calcular_promedio_sueldos(detalles: List['DetalleNomina']) -> float:  
    """
    Calcula el promedio de sueldos usando map y reduce
    """
    sueldos = list(map(lambda d: d.sueldo, detalles))
    return reduce(lambda a, b: a + b, sueldos, 0.0) / len(sueldos) if sueldos else 0

def filtrar_empleados_por_sueldo(detalles: List['DetalleNomina'], min_sueldo: float = 0) -> List['DetalleNomina']:  
    """
    Filtra empleados por sueldo mínimo usando filter y lambda
    """
    return list(filter(lambda d: d.sueldo >= min_sueldo, detalles))

def obtener_top_empleados(detalles: List['DetalleNomina'], top_n: int = 5, por: str = 'neto') -> List['DetalleNomina']:  
    """
    Obtiene los top N empleados por neto o sueldo
    """
    key_func = lambda d: getattr(d, por)
    return sorted(detalles, key=key_func, reverse=True)[:top_n]

def calcular_distribucion_sueldos(detalles: List['DetalleNomina']) -> Dict[str, int]:  
    """
    Calcula distribución de sueldos usando comprehensions
    """
    rangos = {
        '0-500': 0,
        '501-1000': 0,
        '1001-1500': 0,
        '1501-2000': 0,
        '2000+': 0
    }
    
    for detalle in detalles:
        sueldo = detalle.sueldo
        if sueldo <= 500:
            rangos['0-500'] += 1
        elif sueldo <= 1000:
            rangos['501-1000'] += 1
        elif sueldo <= 1500:
            rangos['1001-1500'] += 1
        elif sueldo <= 2000:
            rangos['1501-2000'] += 1
        else:
            rangos['2000+'] += 1
    
    return rangos