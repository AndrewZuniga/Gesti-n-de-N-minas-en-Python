from .decoradores import (
    validar_cedula,
    validar_sueldo_positivo,
    validar_nombre,
    validar_departamento,
    validar_empleado_completo,
    log_operacion,
    manejar_errores
)

from .calculos import (
    calcular_total_neto,
    calcular_promedio_sueldos,
    filtrar_empleados_por_sueldo,
    obtener_top_empleados,
    calcular_distribucion_sueldos
)

from .estadisticas import (
    generar_estadisticas_avanzadas,
    calcular_metricas_departamento
)

__all__ = [
    'validar_cedula',
    'validar_sueldo_positivo',
    'validar_nombre',
    'validar_departamento',
    'validar_empleado_completo',
    'log_operacion',
    'manejar_errores',
    'calcular_total_neto',
    'calcular_promedio_sueldos',
    'filtrar_empleados_por_sueldo',
    'obtener_top_empleados',
    'calcular_distribucion_sueldos',
    'generar_estadisticas_avanzadas',
    'calcular_metricas_departamento',
    'input_numero'
]