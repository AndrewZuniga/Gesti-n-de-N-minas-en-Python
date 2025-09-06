import json
import os
from typing import Optional, List
from modelos.nomina import Nomina

class RepositorioNominasJSON:
    """
    Repositorio para guardar y cargar nóminas en archivos JSON
    """
    
    def __init__(self, directorio: str = "archivos/nominas/"):
        self.directorio = directorio
        self._crear_directorio_si_no_existe()
    
    def _crear_directorio_si_no_existe(self) -> None:
        """Crea el directorio de nóminas si no existe"""
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
    
    def guardar(self, nomina: Nomina) -> None:
        """
        Guarda una nómina en un archivo JSON
        El archivo se nombra: nomina_YYYYMM.json
        """
        archivo = f"{self.directorio}nomina_{nomina.aniomes}.json"
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(nomina.to_dict(), f, indent=2, ensure_ascii=False)
    
    def obtener(self, aniomes: str) -> Optional[Nomina]:
        """
        Obtiene una nómina por año-mes
        Returns: Nomina o None si no existe
        """
        archivo = f"{self.directorio}nomina_{aniomes}.json"
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Reconstruir la nómina básica (los detalles se pierden sin empleados)
                nomina = Nomina(data['id'], data['aniomes'])
                nomina.tot_ing = data['tot_ing']
                nomina.tot_des = data['tot_des']
                nomina.neto = data['neto']
                
                return nomina
                
        except FileNotFoundError:
            return None
    
    def listar_nominas(self) -> List[str]:
        """
        Lista todas las nóminas disponibles
        Returns: Lista de strings aniomes (YYYYMM)
        """
        if not os.path.exists(self.directorio):
            return []
        
        nominas = []
        for archivo in os.listdir(self.directorio):
            if archivo.startswith("nomina_") and archivo.endswith(".json"):
                aniomes = archivo.replace("nomina_", "").replace(".json", "")
                nominas.append(aniomes)
        
        return sorted(nominas)