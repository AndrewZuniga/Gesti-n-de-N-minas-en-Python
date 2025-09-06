from typing import List, Dict, TYPE_CHECKING
from functools import reduce
from modelos.detalle_nomina import DetalleNomina

if TYPE_CHECKING:
    from modelos.detalle_nomina import DetalleNomina

def generar_estadisticas_avanzadas(detalles: List['DetalleNomina']) -> Dict:
    """
    Genera estadísticas avanzadas usando funciones de orden superior
    """
    # Usando comprehensions para listas básicas
    netos = [d.neto for d in detalles]
    sueldos = [d.sueldo for d in detalles]
    bonos = [d.bono for d in detalles]
    
    # Usando reduce para cálculos agregados
    total_neto = reduce(lambda a, b: a + b, netos, 0.0)
    total_sueldos = reduce(lambda a, b: a + b, sueldos, 0.0)
    total_bonos = reduce(lambda a, b: a + b, bonos, 0.0)
    
    # Usando map para transformaciones
    nombres = list(map(lambda d: d.empleado.nombre, detalles))
    
    # Usando filter para segmentación
    altos_sueldos = list(filter(lambda d: d.sueldo > 1000, detalles))
    bajos_sueldos = list(filter(lambda d: d.sueldo <= 1000, detalles))
    
    # Encontrar extremos con lambda
    mayor_neto = max(detalles, key=lambda d: d.neto) if detalles else None
    menor_neto = min(detalles, key=lambda d: d.neto) if detalles else None
    
    return {
        'totales': {
            'neto': total_neto,
            'sueldos': total_sueldos,
            'bonos': total_bonos,
            'empleados': len(detalles)
        },
        'promedios': {
            'neto': total_neto / len(netos) if netos else 0,
            'sueldo': total_sueldos / len(sueldos) if sueldos else 0
        },
        'distribucion': {
            'altos_sueldos': len(altos_sueldos),
            'bajos_sueldos': len(bajos_sueldos)
        },
        'extremes': {
            'mayor_neto': mayor_neto,
            'menor_neto': menor_neto
        },
        'nombres': nombres
    }

def calcular_metricas_departamento(detalles: List['DetalleNomina']) -> Dict[str, Dict]:
    """
    Calcula métricas por departamento usando reduce y comprehensions
    """
    # Agrupar por departamento
    departamentos = {}
    for detalle in detalles:
        depto = detalle.empleado.departamento
        if depto not in departamentos:
            departamentos[depto] = []
        departamentos[depto].append(detalle)
    
    # Calcular métricas por departamento
    metricas = {}
    for depto, depto_detalles in departamentos.items():
        netos = [d.neto for d in depto_detalles]
        metricas[depto] = {
            'empleados': len(depto_detalles),
            'total_neto': reduce(lambda a, b: a + b, netos, 0.0),
            'promedio_neto': reduce(lambda a, b: a + b, netos, 0.0) / len(netos) if netos else 0,
            'empleado_mayor_neto': max(depto_detalles, key=lambda d: d.neto) if depto_detalles else None
        }
    
    return metricas