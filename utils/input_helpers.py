def input_numero(mensaje: str, longitud: int = None) -> str:
    """
    Solicita input al usuario y valida que solo contenga números
    con la longitud especificada.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            
            # Validar que solo sean dígitos
            if not entrada.isdigit():
                print("❌ Error: Solo se permiten números. Intente nuevamente.")
                continue
            
            # Validar longitud si se especificó
            if longitud is not None and len(entrada) != longitud:
                print(f"❌ Error: Debe tener exactamente {longitud} dígitos. Intente nuevamente.")
                continue
            
            return entrada
            
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario")
            exit()
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            continue