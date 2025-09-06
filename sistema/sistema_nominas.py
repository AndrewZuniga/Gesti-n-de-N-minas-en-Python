from typing import List, Dict, Optional
from functools import reduce

from modelos import Empleado, Nomina, DetalleNomina
from repositorios import RepositorioEmpleadosJSON, RepositorioNominasJSON
from utils import (
    log_operacion, 
    manejar_errores,
    calcular_total_neto,
    generar_estadisticas_avanzadas,
    calcular_metricas_departamento
)
class SistemaNominas:
    """
    Sistema principal que coordina todas las operaciones de nómina
    Usa lambdas, map, filter, reduce y comprehensions para cumplir con los requisitos
    """
    
    def __init__(self):
        self.repo_empleados = RepositorioEmpleadosJSON()
        self.repo_nominas = RepositorioNominasJSON()
    
    # --- CRUD EMPLEADOS ---

    def obtener_empleado(self, cedula: str) -> Optional[Empleado]:
        """
        Obtiene un empleado por cédula
        """
        return self.repo_empleados.obtener(cedula)
    
    def listar_empleados(self) -> List[Empleado]:
        """
        Obtiene todos los empleados
        """
        return self.repo_empleados.obtener_todos()
    
    def actualizar_empleado(self, cedula: str, **kwargs) -> Optional[Empleado]:
        """
        Actualiza los datos de un empleado
        """
        empleado = self.repo_empleados.obtener(cedula)
        if empleado:
            for key, value in kwargs.items():
                if hasattr(empleado, key):
                    setattr(empleado, key, value)
            self.repo_empleados.guardar(empleado)
            return empleado
        return None
    
    def eliminar_empleado(self, cedula: str) -> bool:
        """
        Elimina un empleado
        """
        return self.repo_empleados.eliminar(cedula)

        # Crear nómina
        nomina = Nomina(self._obtener_proximo_id(), aniomes)
        
        # Generar detalles para cada empleado usando enumerate
        for i, empleado in enumerate(empleados, 1):
            detalle = DetalleNomina(
                id=i,
                empleado=empleado,
                sueldo=empleado.sueldo,
                bono=Nomina.BONO,
                prestamo=Nomina.PRESTAMO
            )
            nomina.agregar_detalle(detalle)
        
        # Guardar nómina
        self.repo_nominas.guardar(nomina)
        return nomina
    
    def _obtener_proximo_id(self) -> int:
        """
        Obtiene el próximo ID para una nómina
        """
        nominas_existentes = self.repo_nominas.listar_nominas()
        return len(nominas_existentes) + 1
    
    # --- CONSULTAS Y ESTADÍSTICAS ---
    def obtener_nomina(self, aniomes: str) -> Optional[Nomina]:
        """
        Obtiene una nómina por mes-año
        """
        return self.repo_nominas.obtener(aniomes)
    
    def listar_nominas(self) -> List[str]:
        """
        Lista todas las nóminas disponibles
        """
        return self.repo_nominas.listar_nominas()
    
    def generar_estadisticas_nomina(self, aniomes: str) -> Dict:
        """
        Genera estadísticas detalladas de una nómina usando funciones de orden superior
        """
        nomina = self.repo_nominas.obtener(aniomes)
        if not nomina:
            return {}
        
        # Usando LAMBDAS, MAP, FILTER, REDUCE y COMPREHENSIONS
        detalles = nomina.detalles
        
        # Comprehensions para listas básicas
        netos = [d.neto for d in detalles]
        sueldos = [d.sueldo for d in detalles]
        
        # Usando map para transformaciones
        nombres_empleados = list(map(lambda d: d.empleado.nombre, detalles))
        
        # Usando filter para filtros
        empleados_altos_sueldos = list(filter(lambda d: d.sueldo > 1000, detalles))
        empleados_bajos_sueldos = list(filter(lambda d: d.sueldo <= 1000, detalles))
        
        # Usando reduce para agregaciones
        total_iess = reduce(lambda acc, d: acc + d.iess, detalles, 0.0)
        total_bonos = reduce(lambda acc, d: acc + d.bono, detalles, 0.0)
        
        return {
            'periodo': aniomes,
            'total_empleados': len(detalles),
            'total_neto': reduce(lambda a, b: a + b, netos, 0.0),
            'promedio_sueldo': reduce(lambda a, b: a + b, sueldos, 0.0) / len(sueldos) if sueldos else 0,
            'promedio_neto': reduce(lambda a, b: a + b, netos, 0.0) / len(netos) if netos else 0,
            'empleado_mayor_neto': max(detalles, key=lambda d: d.neto) if detalles else None,
            'empleado_menor_neto': min(detalles, key=lambda d: d.neto) if detalles else None,
            'empleado_mayor_sueldo': max(detalles, key=lambda d: d.sueldo) if detalles else None,
            'total_aporte_iess': total_iess,
            'total_bonos': total_bonos,
            'empleados_alto_sueldo': empleados_altos_sueldos,
            'empleados_bajo_sueldo': empleados_bajos_sueldos,
            'nombres_empleados': nombres_empleados
        }
    
    def generar_reporte_completo(self, aniomes: str) -> str:
        """
        Genera un reporte completo en formato texto
        """
        stats = self.generar_estadisticas_nomina(aniomes)
        if not stats:
            return f"No se encontró nómina para el período {aniomes}"
        
        reporte = f"""
        📊 REPORTE COMPLETO DE NÓMINA - {aniomes}
        {'=' * 50}
        
        👥 EMPLEADOS:
        • Total: {stats['total_empleados']}
        • Nómina neta total: ${stats['total_neto']:,.2f}
        • Promedio sueldo: ${stats['promedio_sueldo']:,.2f}
        • Promedio neto: ${stats['promedio_neto']:,.2f}
        
        💰 INGRESOS Y DESCUENTOS:
        • Total bonos: ${stats['total_bonos']:,.2f}
        • Total aporte IESS: ${stats['total_aporte_iess']:,.2f}
        
        🏆 DESTACADOS:
        • Empleado mayor neto: {stats['empleado_mayor_neto'].empleado.nombre if stats['empleado_mayor_neto'] else 'N/A'} (${stats['empleado_mayor_neto'].neto:,.2f if stats['empleado_mayor_neto'] else 0})
        • Empleado menor neto: {stats['empleado_menor_neto'].empleado.nombre if stats['empleado_menor_neto'] else 'N/A'} (${stats['empleado_menor_neto'].neto:,.2f if stats['empleado_menor_neto'] else 0})
        • Empleado mayor sueldo: {stats['empleado_mayor_sueldo'].empleado.nombre if stats['empleado_mayor_sueldo'] else 'N/A'} (${stats['empleado_mayor_sueldo'].sueldo:,.2f if stats['empleado_mayor_sueldo'] else 0})
        
        📈 DISTRIBUCIÓN:
        • Empleados con sueldo > $1000: {len(stats['empleados_alto_sueldo'])}
        • Empleados con sueldo ≤ $1000: {len(stats['empleados_bajo_sueldo'])}
        """
        
        return reporte
    
    # --- MÉTODOS CON LAMBDAS AVANZADAS ---
    def buscar_empleados_por(self, condicion) -> List[Empleado]:
        """
        Busca empleados usando una condición lambda
        Ejemplo: sistema.buscar_empleados_por(lambda emp: emp.sueldo > 1000)
        """
        empleados = self.repo_empleados.obtener_todos()
        return list(filter(condicion, empleados))
    
    def calcular_total_nominas(self) -> float:
        """
        Calcula el total de todas las nóminas usando reduce
        """
        nominas = self.listar_nominas()
        total = reduce(lambda acc, aniomes: acc + (self.obtener_nomina(aniomes).neto if self.obtener_nomina(aniomes) else 0), 
                      nominas, 0.0)
        return total
    
    @manejar_errores
    @log_operacion
    def crear_empleado(self, cedula: str, nombre: str, sueldo: float, 
                      departamento: str, cargo: str) -> Optional[Empleado]:
        """
        Crea un nuevo empleado con validación y logging
        """
        empleado = Empleado(cedula, nombre, sueldo, departamento, cargo)
        self.repo_empleados.guardar(empleado)
        return empleado
    
    @manejar_errores
    def generar_nomina_mensual(self, aniomes: str) -> Optional[Nomina]:
        """
        Genera una nómina mensual con manejo de errores
        """
        empleados = self.repo_empleados.obtener_todos()
        
        if not empleados:
            print("⚠️ No hay empleados para generar nómina")
            return None
        
        # Crear nómina
        nomina = Nomina(self._obtener_proximo_id(), aniomes)
        
        # Generar detalles para cada empleado
        for i, empleado in enumerate(empleados, 1):
            detalle = DetalleNomina(
                id=i,
                empleado=empleado,
                sueldo=empleado.sueldo,
                bono=Nomina.BONO,
                prestamo=Nomina.PRESTAMO
            )
            nomina.agregar_detalle(detalle)
        
        # Guardar nómina
        self.repo_nominas.guardar(nomina)
        print(f"✅ Nómina {aniomes} generada con {len(empleados)} empleados")
        return nomina
    
    def generar_estadisticas_avanzadas(self, aniomes: str) -> Dict:
        """
        Genera estadísticas avanzadas usando las nuevas utilidades
        """
        nomina = self.repo_nominas.obtener(aniomes)
        if not nomina or not nomina.detalles:
            return {}
        
        return generar_estadisticas_avanzadas(nomina.detalles)
    
    def generar_metricas_departamento(self, aniomes: str) -> Dict:
        """
        Genera métricas por departamento
        """
        nomina = self.repo_nominas.obtener(aniomes)
        if not nomina or not nomina.detalles:
            return {}
        
        return calcular_metricas_departamento(nomina.detalles)