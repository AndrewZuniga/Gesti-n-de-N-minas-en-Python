from abc import ABC, abstractmethod
from typing import List, Optional
from modelos.empleado import Empleado

class Repositorio(ABC):
    """
    Clase abstracta que define la interfaz para todos los repositorios.
    Usa el principio de inversión de dependencias.
    """
    
    @abstractmethod
    def guardar(self, empleado: Empleado) -> None:
        """
        Guarda o actualiza un empleado en la persistencia
        """
        pass
    
    @abstractmethod
    def obtener(self, cedula: str) -> Optional[Empleado]:
        """
        Obtiene un empleado por su cédula
        Returns: Empleado o None si no existe
        """
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Empleado]:
        """
        Obtiene todos los empleados
        Returns: Lista de empleados
        """
        pass
    
    @abstractmethod
    def eliminar(self, cedula: str) -> bool:
        """
        Elimina un empleado por su cédula
        Returns: True si se eliminó, False si no existía
        """
        pass