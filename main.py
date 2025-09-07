from sistema import SistemaNominas 

def mostrar_menu():
    """
    Muestra el menú principal
    """
    print("\n" + "=" * 50)
    print("🏢 SISTEMA DE GESTIÓN DE NÓMINAS")
    print("=" * 50)
    print("1. Gestión de Empleados")
    print("2. Generar Nómina Mensual")
    print("3. Consultar Nóminas")
    print("4. Estadísticas y Reportes")
    print("5. Salir")
    print("=" * 50)

def input_solo_numeros(mensaje: str, longitud: int = None) -> str:
    """
    Valida que el input solo contenga números
    """
    while True:
        entrada = input(mensaje).strip()
        
        if not entrada:
            print("❌ Este campo no puede estar vacío")
            continue
            
        if not entrada.isdigit():
            print("❌ Solo se permiten números. Intente nuevamente.")
            continue
        
        if longitud and len(entrada) != longitud:
            print(f"❌ Debe tener {longitud} dígitos. Intente nuevamente.")
            continue
        
        return entrada

def input_sueldo():
    """
    Solicita sueldo con validación
    """
    while True:
        try:
            sueldo_str = input("Sueldo: ").strip()
            if not sueldo_str:
                print("❌ El sueldo no puede estar vacío")
                continue
                
            sueldo = float(sueldo_str)
            if sueldo <= 0:
                print("❌ El sueldo debe ser positivo")
                continue
            return sueldo
        except ValueError:
            print("❌ Ingrese un valor numérico válido")

def menu_empleados(sistema: SistemaNominas):
    """
    Submenú completo para gestión de empleados
    """
    while True:
        print("\n👥 GESTIÓN DE EMPLEADOS")
        print("1. Crear empleado")
        print("2. Lista empleados")
        print("3. Buscar empleado")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n➕ CREAR NUEVO EMPLEADO")
            try:
                cedula = input_solo_numeros("Cédula (10 dígitos): ", 10)
                nombre = input("Nombre: ").strip()
                if not nombre:
                    print("❌ El nombre no puede estar vacío")
                    continue
                    
                sueldo = input_sueldo()
                departamento = input("Departamento: ").strip()
                if not departamento:
                    print("❌ El departamento no puede estar vacío")
                    continue
                    
                cargo = input("Cargo: ").strip()
                if not cargo:
                    print("❌ El cargo no puede estar vacío")
                    continue
                
                empleado = sistema.crear_empleado(cedula, nombre, sueldo, departamento, cargo)
                print(f"✅ Empleado creado: {empleado}")
                
            except ValueError as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
        
        elif opcion == "2":
            print("\n📋 LISTA DE EMPLEADOS")
            empleados = sistema.listar_empleados()
            if not empleados:
                print("No hay empleados registrados")
            else:
                for i, emp in enumerate(empleados, 1):
                    print(f"{i}. {emp.nombre} - {emp.cedula} - ${emp.sueldo:.2f} - {emp.departamento} - {emp.cargo}")
        
        elif opcion == "3":
            print("\n🔍 BUSCAR EMPLEADO")
            try:
                cedula = input_solo_numeros("Cédula a buscar (10 dígitos): ", 10)
                empleado = sistema.obtener_empleado(cedula)
                if empleado:
                    print(f"✅ Empleado encontrado:")
                    print(f"   Cédula: {empleado.cedula}")
                    print(f"   Nombre: {empleado.nombre}")
                    print(f"   Sueldo: ${empleado.sueldo:.2f}")
                    print(f"   Departamento: {empleado.departamento}")
                    print(f"   Cargo: {empleado.cargo}")
                else:
                    print("❌ Empleado no encontrado")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "4":
            print("\n✏️ ACTUALIZAR EMPLEADO")
            try:
                cedula = input_solo_numeros("Cédula del empleado a actualizar (10 dígitos): ", 10)
                empleado = sistema.obtener_empleado(cedula)
                
                if not empleado:
                    print("❌ Empleado no encontrado")
                    continue
                
                print(f"Empleado actual: {empleado}")
                print("\nDeje en blanco los campos que no desea cambiar:")
                
                nombre = input(f"Nuevo nombre [{empleado.nombre}]: ").strip()
                nombre = nombre if nombre else empleado.nombre
                
                sueldo_str = input(f"Nuevo sueldo [{empleado.sueldo}]: ").strip()
                sueldo = float(sueldo_str) if sueldo_str else empleado.sueldo
                
                departamento = input(f"Nuevo departamento [{empleado.departamento}]: ").strip()
                departamento = departamento if departamento else empleado.departamento
                
                cargo = input(f"Nuevo cargo [{empleado.cargo}]: ").strip()
                cargo = cargo if cargo else empleado.cargo
                
                empleado_actualizado = sistema.actualizar_empleado(
                    cedula, 
                    nombre=nombre, 
                    sueldo=sueldo, 
                    departamento=departamento, 
                    cargo=cargo
                )
                
                if empleado_actualizado:
                    print(f"✅ Empleado actualizado: {empleado_actualizado}")
                else:
                    print("❌ Error al actualizar empleado")
                    
            except ValueError as e:
                print(f"❌ Error de validación: {e}")
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
        
        elif opcion == "5":
            print("\n🗑️ ELIMINAR EMPLEADO")
            try:
                cedula = input_solo_numeros("Cédula del empleado a eliminar (10 dígitos): ", 10)
                
                # Confirmación de eliminación
                confirmacion = input("¿Está seguro que desea eliminar este empleado? (s/n): ").lower()
                if confirmacion != 's':
                    print("❌ Eliminación cancelada")
                    continue
                
                eliminado = sistema.eliminar_empleado(cedula)
                if eliminado:
                    print("✅ Empleado eliminado exitosamente")
                else:
                    print("❌ Empleado no encontrado")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "6":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("❌ Opción no válida")

def menu_nominas(sistema: SistemaNominas):
    """
    Submenú para gestión de nóminas
    """
    while True:
        print("\n💰 GESTIÓN DE NÓMINAS")
        print("1. Generar nómina mensual")
        print("2. Consultar nóminas disponibles")
        print("3. Ver detalle de nómina")
        print("4. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n💰 GENERAR NÓMINA MENSUAL")
            try:
                aniomes = input_solo_numeros("Ingrese el período (YYYYMM): ", 6)
                nomina = sistema.generar_nomina_mensual(aniomes)
                if nomina:
                    print(f"✅ Nómina generada exitosamente")
                    print(f"   Período: {nomina.aniomes}")
                    print(f"   Total empleados: {len(nomina.detalles)}")
                    print(f"   Total neto: ${nomina.neto:.2f}")
                else:
                    print("❌ No se pudo generar la nómina")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            print("\n📊 NÓMINAS DISPONIBLES")
            nominas = sistema.listar_nominas()
            if not nominas:
                print("No hay nóminas generadas")
            else:
                print("Nóminas disponibles:")
                for i, aniomes in enumerate(nominas, 1):
                    print(f"{i}. {aniomes}")
        
        elif opcion == "3":
            print("\n📋 DETALLE DE NÓMINA")
            try:
                aniomes = input_solo_numeros("Período a consultar (YYYYMM): ", 6)
                nomina = sistema.obtener_nomina(aniomes)
                
                if nomina:
                    print(f"\n📊 DETALLE DE NÓMINA {aniomes}")
                    print("=" * 60)
                    for detalle in nomina.detalles:
                        print(f"{detalle.empleado.nombre:20} | "
                              f"Sueldo: ${detalle.sueldo:7.2f} | "
                              f"Neto: ${detalle.neto:7.2f}")
                    print("=" * 60)
                    print(f"TOTAL: ${nomina.neto:.2f}")
                else:
                    print("❌ Nómina no encontrada")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "4":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("❌ Opción no válida")

def menu_estadisticas(sistema: SistemaNominas):
    """
    Submenú para estadísticas y reportes
    """
    while True:
        print("\n📈 ESTADÍSTICAS Y REPORTES")
        print("1. Reporte completo de nómina")
        print("2. Estadísticas avanzadas")
        print("3. Métricas por departamento")
        print("4. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n📊 REPORTE COMPLETO")
            try:
                aniomes = input_solo_numeros("Período a consultar (YYYYMM): ", 6)
                reporte = sistema.generar_reporte_completo(aniomes)
                print(reporte)
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            print("\n📈 ESTADÍSTICAS AVANZADAS")
            try:
                aniomes = input_solo_numeros("Período a consultar (YYYYMM): ", 6)
                stats = sistema.generar_estadisticas_avanzadas(aniomes)
                
                if stats:
                    print(f"\n📊 ESTADÍSTICAS AVANZADAS - {aniomes}")
                    print("=" * 50)
                    print(f"Total empleados: {stats['totales']['empleados']}")
                    print(f"Total neto pagado: ${stats['totales']['neto']:,.2f}")
                    print(f"Promedio sueldo: ${stats['promedios']['sueldo']:,.2f}")
                    print(f"Promedio neto: ${stats['promedios']['neto']:,.2f}")
                    print(f"Empleados alto sueldo: {stats['distribucion']['altos_sueldos']}")
                    print(f"Empleados bajo sueldo: {stats['distribucion']['bajos_sueldos']}")
                else:
                    print("❌ No hay estadísticas disponibles")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "3":
            print("\n🏢 MÉTRICAS POR DEPARTAMENTO")
            try:
                aniomes = input_solo_numeros("Período a consultar (YYYYMM): ", 6)
                metricas = sistema.generar_metricas_departamento(aniomes)
                
                if metricas:
                    print(f"\n📊 MÉTRICAS POR DEPARTAMENTO - {aniomes}")
                    print("=" * 60)
                    for depto, data in metricas.items():
                        print(f"{depto:15}: {data['empleados']} empleados | "
                              f"Total: ${data['total_neto']:,.2f} | "
                              f"Promedio: ${data['promedio_neto']:,.2f}")
                else:
                    print("❌ No hay métricas disponibles")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "4":
            print("Volviendo al menú principal...")
            break
        
        else:
            print("❌ Opción no válida")

def main():
    """
    Función principal del sistema
    """
    sistema = SistemaNominas()
    
    print("🚀 Iniciando Sistema de Gestión de Nóminas...")
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                menu_empleados(sistema)
            elif opcion == "2":
                menu_nominas(sistema)
            elif opcion == "3":
                menu_nominas(sistema)  # Para consultar nóminas
            elif opcion == "4":
                menu_estadisticas(sistema)  # Para estadísticas
            elif opcion == "5":
                print("\n👋 ¡Hasta pronto!")
                break
            else:
                print("❌ Opción no válida. Intente nuevamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta pronto!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()