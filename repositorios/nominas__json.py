import json
import os
from typing import Optional, List
from modelos.nomina import Nomina
from modelos.detalle_nomina import DetalleNomina
from modelos.empleado import Empleado

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
        Obtiene una nómina por año-mes con todos sus detalles
        Returns: Nomina completa o None si no existe
        """
        archivo = f"{self.directorio}nomina_{aniomes}.json"
        try:
            if not os.path.exists(archivo):
                print(f"⚠️ Archivo no encontrado: {archivo}")
                return None
                
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Reconstruir la nómina completa
                nomina = Nomina(data['id'], data['aniomes'])
                nomina.tot_ing = data['tot_ing']
                nomina.tot_des = data['tot_des']
                nomina.neto = data['neto']
                
                # Reconstruir los detalles de la nómina
                for detalle_data in data['detalles']:
                    try:
                        # Reconstruir el empleado
                        emp_data = detalle_data['empleado']
                        empleado = Empleado(
                            emp_data['cedula'],
                            emp_data['nombre'],
                            emp_data['sueldo'],
                            emp_data['departamento'],
                            emp_data['cargo']
                        )
                        
                        # Reconstruir el detalle
                        detalle = DetalleNomina(
                            detalle_data['id'],
                            empleado,
                            detalle_data['sueldo'],
                            detalle_data['bono'],
                            detalle_data['prestamo']
                        )
                        
                        # Agregar el detalle a la nómina
                        nomina.agregar_detalle(detalle)
                        
                    except KeyError as e:
                        print(f"❌ Error en estructura de detalle: {e}")
                        continue
                        
                print(f"✅ Nómina {aniomes} cargada con {len(nomina.detalles)} empleados")
                return nomina
                
        except FileNotFoundError:
            print(f"❌ Nómina {aniomes} no encontrada")
            return None
        except json.JSONDecodeError:
            print(f"❌ Error decodificando JSON de nómina {aniomes}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado cargando nómina {aniomes}: {e}")
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
    
    def verificar_nomina(self, aniomes: str) -> bool:
        """
        Verifica si una nómina existe y tiene la estructura correcta
        """
        archivo = f"{self.directorio}nomina_{aniomes}.json"
        if not os.path.exists(archivo):
            print(f"❌ Archivo no existe: {archivo}")
            return False
    
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📋 Estructura de nómina {aniomes}:")
                print(f"   ID: {data.get('id')}")
                print(f"   Período: {data.get('aniomes')}")
                print(f"   Total detalles: {len(data.get('detalles', []))}")
            
                if data.get('detalles'):
                    primer_detalle = data['detalles'][0]
                    print(f"   Primer detalle - Empleado: {primer_detalle.get('empleado', {})}")
                
                return True
            
        except Exception as e:
            print(f"❌ Error verificando nómina: {e}")
            return False