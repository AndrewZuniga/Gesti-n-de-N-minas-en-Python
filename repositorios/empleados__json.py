import json
import os
from typing import List, Optional
from modelos.empleado import Empleado
from repositorios.base import Repositorio

class RepositorioEmpleadosJSON(Repositorio):
    """
    Implementación concreta del repositorio usando JSON como persistencia
    """
    
    def __init__(self, archivo: str = "archivos/empleados.json"):
        self.archivo = archivo
        self._crear_directorio_si_no_existe()
    
    def _crear_directorio_si_no_existe(self) -> None:
        """Crea el directorio de archivos si no existe"""
        directorio = os.path.dirname(self.archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
    
    def _leer_datos(self) -> List[dict]:
        """
        Lee todos los datos del archivo JSON
        Returns: Lista de diccionarios con datos de empleados
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _escribir_datos(self, datos: List[dict]) -> None:
        """
        Escribe datos al archivo JSON
        """
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def guardar(self, empleado: Empleado) -> None:
        """
        Guarda o actualiza un empleado en el archivo JSON
        """
        datos = self._leer_datos()
        empleado_encontrado = False
        
        # Buscar si el empleado ya existe
        for i, emp_data in enumerate(datos):
            if emp_data['cedula'] == empleado.cedula:
                datos[i] = empleado.to_dict()
                empleado_encontrado = True
                break
        
        # Si no existe, agregarlo
        if not empleado_encontrado:
            datos.append(empleado.to_dict())
        
        self._escribir_datos(datos)
    
    def obtener(self, cedula: str) -> Optional[Empleado]:
        """
        Obtiene un empleado por su cédula
        """
        datos = self._leer_datos()
        for emp_data in datos:
            if emp_data['cedula'] == cedula:
                return Empleado.from_dict(emp_data)
        return None
    
    def obtener_todos(self) -> List[Empleado]:
        """
        Obtiene todos los empleados del archivo JSON
        """
        datos = self._leer_datos()
        return [Empleado.from_dict(emp_data) for emp_data in datos]
    
    def eliminar(self, cedula: str) -> bool:
        """
        Elimina un empleado por su cédula
        Returns: True si se eliminó, False si no existía
        """
        datos = self._leer_datos()
        nuevos_datos = [emp for emp in datos if emp['cedula'] != cedula]
        
        # Verificar si se eliminó algún elemento
        if len(nuevos_datos) < len(datos):
            self._escribir_datos(nuevos_datos)
            return True
        return False