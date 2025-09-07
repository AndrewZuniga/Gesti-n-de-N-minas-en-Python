from typing import Callable, Any
import re

def validar_cedula(func: Callable) -> Callable:
    """
    Decorador para validar que la cédula tenga 10 dígitos y no esté vacía
    """
    def wrapper(*args, **kwargs):
        # Extraer cédula de args o kwargs
        cedula = None
        
        # Buscar en kwargs
        if 'cedula' in kwargs:
            cedula = kwargs['cedula']
        # Buscar en args (generalmente es el segundo argumento después de self)
        elif len(args) > 1:
            cedula = args[1]
        
        # Validar que no esté vacía
        if not cedula or cedula.strip() == "":
            raise ValueError("❌ La cédula no puede estar vacía")
        
        # Validar que tenga exactamente 10 dígitos numéricos
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValueError("❌ La cédula debe tener exactamente 10 dígitos numéricos")
        
        return func(*args, **kwargs)
    return wrapper

def validar_sueldo_positivo(func: Callable) -> Callable:
    """
    Decorador para validar que el sueldo sea positivo
    """
    def wrapper(*args, **kwargs):
        # Extraer sueldo de args o kwargs
        sueldo = None
        
        # Buscar en kwargs
        if 'sueldo' in kwargs:
            sueldo = kwargs['sueldo']
        # Buscar en args 
        elif len(args) > 3:  # sueldo es usualmente el cuarto argumento
            sueldo = args[3]
        
        # Validar que no sea None o vacío
        if sueldo is None:
            raise ValueError("❌ El sueldo no puede estar vacío")
        
        if sueldo <= 0:
            raise ValueError("❌ El sueldo debe ser un valor positivo")
        
        return func(*args, **kwargs)
    return wrapper

def validar_nombre(func: Callable) -> Callable:
    """
    Decorador para validar que el nombre sea válido y no esté vacío
    """
    def wrapper(*args, **kwargs):
        nombre = None
        
        print(f"🔍 DEBUG validar_nombre: args={args}")  # ← AGREGA ESTO
        print(f"🔍 DEBUG validar_nombre: kwargs={kwargs}")  # ← AGREGA ESTO
        
        if 'nombre' in kwargs:
            nombre = kwargs['nombre']
        elif len(args) > 2:  # nombre es usualmente el tercer argumento
            nombre = args[2]
        
        print(f"🔍 DEBUG validar_nombre: nombre='{nombre}'")  # ← AGREGA ESTO
        
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
    Decorador para validar el departamento y que no esté vacío
    """
    def wrapper(*args, **kwargs):
        departamento = None
        
        if 'departamento' in kwargs:
            departamento = kwargs['departamento']
        elif len(args) > 4:  # departamento es usualmente el quinto argumento
            departamento = args[4]
        
        # Validar que no esté vacío
        if not departamento or departamento.strip() == "":
            raise ValueError("❌ El departamento no puede estar vacío")
        
        if len(departamento.strip()) < 2:
            raise ValueError("❌ El departamento debe tener al menos 2 caracteres")
        
        return func(*args, **kwargs)
    return wrapper

def validar_cargo(func: Callable) -> Callable:
    """
    Decorador para validar el cargo y que no esté vacío
    """
    def wrapper(*args, **kwargs):
        cargo = None
        
        if 'cargo' in kwargs:
            cargo = kwargs['cargo']
        elif len(args) > 5:  # cargo es usualmente el sexto argumento
            cargo = args[5]
        
        # Validar que no esté vacío
        if not cargo or cargo.strip() == "":
            raise ValueError("❌ El cargo no puede estar vacío")
        
        if len(cargo.strip()) < 2:
            raise ValueError("❌ El cargo debe tener al menos 2 caracteres")
        
        return func(*args, **kwargs)
    return wrapper

def validar_empleado_completo(func: Callable) -> Callable:
    """
    Decorador compuesto que aplica todas las validaciones de empleado
    """
    def wrapper(*args, **kwargs):
        # Aplicar todas las validaciones en orden
        wrapper_validado = validar_cedula(
            validar_sueldo_positivo(
                validar_nombre(
                    validar_departamento(
                        validar_cargo(func)
                    )
                )
            )
        )
        return wrapper_validado(*args, **kwargs)
    return wrapper

def log_operacion(func: Callable) -> Callable:
    """
    Decorador para loggear operaciones importantes
    """
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"📝 Operación '{func.__name__}' ejecutada exitosamente")
        return resultado
    return wrapper

def manejar_errores(func: Callable) -> Callable:
    """
    Decorador para manejar errores gracefully
    """
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