from .base import Repositorio
from .empleados__json import RepositorioEmpleadosJSON
from .nominas__json import RepositorioNominasJSON

__all__ = [
    'Repositorio',
    'RepositorioEmpleadosJSON',
    'RepositorioNominasJSON'
]