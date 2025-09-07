from typing import Callable, Any
from functools import wraps
import re

# Decoradores de Validación
#
# Estos decoradores verifican que los datos del empleado sean correctos.
# Usan functools.wraps para preservar los metadatos de la función original
# y buscan los argumentos por su nombre para ser más flexibles.

def validar_cedula(func: Callable) -> Callable:
    """
    Decorador para validar que la cédula tenga 10 dígitos y no esté vacía.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cedula = kwargs.get('cedula', None)
        if cedula is None and len(args) > 1:
            cedula = args[1]
        
        if not cedula or not isinstance(cedula, str) or cedula.strip() == "":
            raise ValueError("❌ La cédula no puede estar vacía")
        
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValueError("❌ La cédula debe tener exactamente 10 dígitos numéricos")
        
        return func(*args, **kwargs)
    return wrapper

def validar_sueldo_positivo(func: Callable) -> Callable:
    """
    Decorador para validar que el sueldo sea un valor numérico positivo.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        sueldo = kwargs.get('sueldo', None)
        if sueldo is None and len(args) > 3:
            sueldo = args[3]
        
        if not sueldo or not isinstance(sueldo, (int, float)):
            raise ValueError("❌ El sueldo debe ser un valor numérico")
            
        if sueldo <= 0:
            raise ValueError("❌ El sueldo debe ser un valor positivo")
        
        return func(*args, **kwargs)
    return wrapper

def validar_nombre(func: Callable) -> Callable:
    """
    Decorador para validar que el nombre no esté vacío y solo contenga letras.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        nombre = None
        
        if 'nombre' in kwargs:
            nombre = kwargs['nombre']
        elif len(args) > 2:  # nombre es usualmente el tercer argumento
            nombre = args[2]
        
        # Validar que no esté vacío
        if not nombre or nombre.strip() == "":
            raise ValueError("❌ El nombre no puede estar vacío")
        
        if nombre:
            # Validar que el nombre solo contenga letras y espacios
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise ValueError("❌ El nombre solo puede contener letras y espacios")
            
            # Validar longitud mínima
            if len(nombre.strip()) < 2:
                raise ValueError("❌ El nombre debe tener al menos 2 caracteres")
        
        return func(*args, **kwargs)
    return wrapper

def validar_departamento(func: Callable) -> Callable:
    """
    Decorador para validar que el departamento no esté vacío y tenga al menos 2 caracteres.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        departamento = kwargs.get('departamento', None)
        if departamento is None and len(args) > 4:
            departamento = args[4]

        if not departamento or departamento.strip() == "":
            raise ValueError("❌ El departamento no puede estar vacío")
        
        if len(departamento.strip()) < 2:
            raise ValueError("❌ El departamento debe tener al menos 2 caracteres")
        
        return func(*args, **kwargs)
    return wrapper

def validar_cargo(func: Callable) -> Callable:
    """
    Decorador para validar que el cargo no esté vacío y tenga al menos 2 caracteres.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cargo = kwargs.get('cargo', None)
        if cargo is None and len(args) > 5:
            cargo = args[5]

        if not cargo or cargo.strip() == "":
            raise ValueError("❌ El cargo no puede estar vacío")
        
        if len(cargo.strip()) < 2:
            raise ValueError("❌ El cargo debe tener al menos 2 caracteres")
        
        return func(*args, **kwargs)
    return wrapper

def validar_empleado_completo(func: Callable) -> Callable:
    """
    Decorador compuesto que aplica todas las validaciones de empleado
    en una cadena ordenada and robusta.
    """
    # Se aplican los decoradores de manera anidada, de adentro hacia afuera,
    # y finalmente se devuelve la función decorada.
    @wraps(func)
    @validar_cedula
    @validar_sueldo_positivo
    @validar_nombre
    @validar_departamento
    @validar_cargo
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Decoradores de Manejo de Lógica del Sistema
#
# Estos decoradores no validan datos, sino que se encargan de la lógica
# de la aplicación, como el registro de operaciones y el manejo de errores.

def log_operacion(func: Callable) -> Callable:
    """
    Decorador para registrar una operación exitosa en la consola.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"📝 Operación '{func.__name__}' ejecutada exitosamente")
        return resultado
    return wrapper

def manejar_errores(func: Callable) -> Callable:
    """
    Decorador para manejar errores comunes de manera controlada.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return None
        except FileNotFoundError as e:
            print(f"❌ Error de archivo: {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None
    return wrapper