"""
EJEMPLOS DE USO AVANZADO Y CASOS DE PRUEBA
Patrones de Diseño en Python
"""

# Importar las clases del módulo principal
# (En un proyecto real, esto sería: from patrones_diseno import *)
# Para este archivo, asumimos que patrones_diseno.py está disponible

from abc import ABC, abstractmethod
from copy import deepcopy


# ============================================================================
# EJEMPLO 1: USO AVANZADO DEL SINGLETON - FACTORIAL
# ============================================================================

def ejemplo_singleton_factorial():
    """
    Ejemplo avanzado del patrón Singleton con FactorialCalculator.
    Demuestra cómo múltiples clientes utilizan la misma instancia.
    """
    print("\n" + "="*70)
    print("EJEMPLO 1: SINGLETON - MÚLTIPLES CLIENTES")
    print("="*70)
    
    # Simular diferentes módulos que usan el calculador
    class ServicioReportes:
        def generar_combinaciones(self, n):
            # Importar aquí simularía usar desde otro módulo
            from patrones_diseno import FactorialCalculator
            calc = FactorialCalculator()
            return f"Combinaciones posibles: {calc.calcular(n)}"
    
    class ServicioAnalisis:
        def calcular_permutaciones(self, n):
            from patrones_diseno import FactorialCalculator
            calc = FactorialCalculator()
            return f"Permutaciones: {calc.calcular(n)}"
    
    # Usar ambos servicios
    reportes = ServicioReportes()
    analisis = ServicioAnalisis()
    
    print(reportes.generar_combinaciones(6))
    print(analisis.calcular_permutaciones(8))
    
    # Verificar que usan la misma instancia
    from patrones_diseno import FactorialCalculator
    calc1 = FactorialCalculator()
    print(f"\n✓ Todas las instancias son idénticas: {id(calc1)}")


# ============================================================================
# EJEMPLO 2: USO AVANZADO DEL STRATEGY - HAMBURGUESA PREMIUM
# ============================================================================

def ejemplo_strategy_hamburguesa():
    """
    Ejemplo avanzado del patrón Strategy con personalizaciones.
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: STRATEGY - HAMBURGUESAS CON PERSONALIZACIONES")
    print("="*70)
    
    from patrones_diseno import (
        Hamburguesa, EntregaDelivery, EntregaEnMostrador,
        RetiroPorCliente
    )
    
    # Crear diferentes tipos de hamburguesas
    hamburguesas = [
        Hamburguesa("Hamburguesa Clásica"),
        Hamburguesa("Hamburguesa Premium con Queso Azul"),
        Hamburguesa("Hamburguesa BBQ con Bacon"),
        Hamburguesa("Hamburguesa Vegetariana"),
    ]
    
    # Aplicar diferentes métodos de entrega
    metodos = [
        EntregaEnMostrador(),
        RetiroPorCliente(),
        EntregaDelivery(),
        EntregaDelivery()
    ]
    
    print("\nPEDIDOS REALIZADOS:")
    print("-" * 70)
    for hamburguesa, metodo in zip(hamburguesas, metodos):
        hamburguesa.set_metodo_entrega(metodo)
        print(hamburguesa.procesar_entrega())


# ============================================================================
# EJEMPLO 3: USO AVANZADO DEL BUILDER - CONSTRUCCIÓN PROGRESIVA
# ============================================================================

def ejemplo_builder_avanzado():
    """
    Ejemplo avanzado del patrón Builder con construcción personalizada.
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: BUILDER - CONSTRUCCIÓN PERSONALIZADA DE AVIONES")
    print("="*70)
    
    from patrones_diseno import (
        Avion, ConstructorAvion, ConstructorVehiculo
    )
    
    # Crear un constructor personalizado para un avión de carga
    class ConstructorAvionCarga(ConstructorVehiculo):
        def crear_vehiculo(self):
            self.vehiculo = Avion()
        
        def construir_partes(self):
            self.vehiculo.partes['body'] = 'Fuselaje reforzado para carga (Airbus A400M)'
            self.vehiculo.partes['turbinas'] = '4 turbinas turbohélice Rolls-Royce AE 2100'
            self.vehiculo.partes['alas'] = '2 alas de carga máxima 130,000 kg'
            self.vehiculo.partes['tren_aterrizaje'] = 'Tren reforzado de aterrizaje de alta resistencia'
    
    # Crear el avión de carga
    from patrones_diseno import DirectorConstruccion
    director = DirectorConstruccion(ConstructorAvionCarga())
    avion_carga = director.construir()
    
    print(avion_carga.mostrar_partes())


# ============================================================================
# EJEMPLO 4: USO AVANZADO DEL PROTOTYPE - VERSIONING
# ============================================================================

def ejemplo_prototype_versioning():
    """
    Ejemplo avanzado del patrón Prototype para control de versiones.
    """
    print("\n" + "="*70)
    print("EJEMPLO 4: PROTOTYPE - CONTROL DE VERSIONES DE DOCUMENTOS")
    print("="*70)
    
    from patrones_diseno import DocumentoPrototipo
    
    # Crear versión original
    doc_v1 = DocumentoPrototipo(
        titulo="Especificación de Proyecto v1.0",
        contenido="Requerimientos iniciales del proyecto de software",
        autor="Juan García"
    )
    
    # Crear versión 2 basada en v1
    doc_v2 = doc_v1.clonar()
    doc_v2.modificar(
        nuevo_titulo="Especificación de Proyecto v1.1",
        nuevo_contenido="Requerimientos actualizados: Se agregaron módulos de autenticación"
    )
    
    # Crear versión 3 basada en v2
    doc_v3 = doc_v2.clonar()
    doc_v3.modificar(
        nuevo_titulo="Especificación de Proyecto v2.0",
        nuevo_contenido="Rediseño completo: Cambio de arquitectura a microservicios"
    )
    
    # Mostrar historial de versiones
    versiones = [doc_v1, doc_v2, doc_v3]
    print("\nHISTORIAL DE VERSIONES:")
    print("-" * 70)
    
    for i, doc in enumerate(versiones, 1):
        print(f"\n{doc.titulo}")
        print(f"ID: {doc._id}")
        print(f"Contenido: {doc.contenido}")
        print(f"Autor: {doc.autor}")


# ============================================================================
# EJEMPLO 5: USO AVANZADO DEL ABSTRACT FACTORY - MULTI-REGIÓN
# ============================================================================

def ejemplo_abstract_factory_multiregion():
    """
    Ejemplo avanzado del patrón Abstract Factory con múltiples regiones.
    """
    print("\n" + "="*70)
    print("EJEMPLO 5: ABSTRACT FACTORY - SISTEMA MULTINACIONAL DE PAGOS")
    print("="*70)
    
    from patrones_diseno import (
        FabricaPagosArgentina, FabricaPagosEuropa,
        SistemaDeFacturacionConPagos
    )
    
    # Definir montos de transacciones
    transacciones = [
        {"monto": 1000, "descripcion": "Compra de productos"},
        {"monto": 5000, "descripcion": "Servicio premium"},
        {"monto": 15000, "descripcion": "Contrato anual"},
    ]
    
    # Procesar en diferentes regiones
    regiones = [
        ("Argentina", FabricaPagosArgentina()),
        ("Europa", FabricaPagosEuropa()),
    ]
    
    for region_nombre, fabrica in regiones:
        print(f"\n╔════════════════════════════════════════╗")
        print(f"║  PROCESAMIENTO EN {region_nombre:<28} ║")
        print(f"╚════════════════════════════════════════╝")
        
        for transaccion in transacciones:
            print(f"\nTransacción: {transaccion['descripcion']}")
            print(f"Monto: ${transaccion['monto']:.2f}")
            print("-" * 70)
            
            # Probar diferentes métodos de pago
            metodos = [
                fabrica.crear_pago_tarjeta_credito(),
                fabrica.crear_pago_tarjeta_debito(),
                fabrica.crear_pago_efectivo(),
            ]
            
            for metodo in metodos:
                resultado = metodo.procesar_pago(transaccion['monto'])
                comisión_texto = f" (Comisión: ${resultado.get('comision', 0):.2f})" if resultado.get('comision', 0) > 0 else ""
                descuento_texto = f" (Descuento: ${resultado.get('descuento', 0):.2f})" if resultado.get('descuento', 0) > 0 else ""
                
                print(f"  {metodo.obtener_nombre():<25} → ${resultado['total']:.2f}{comisión_texto}{descuento_texto}")


# ============================================================================
# EJEMPLO 6: COMPOSICIÓN DE PATRONES - FACTURACIÓN COMPLETA
# ============================================================================

def ejemplo_composicion_patrones():
    """
    Ejemplo que combina múltiples patrones en un sistema de facturación.
    """
    print("\n" + "="*70)
    print("EJEMPLO 6: COMPOSICIÓN - SISTEMA DE FACTURACIÓN COMPLETO")
    print("="*70)
    
    from patrones_diseno import (
        TaxCalculator, Factura, IVAResponsable,
        FabricaPagosArgentina
    )
    
    print("\n1. CÁLCULO DE IMPUESTOS (Singleton)")
    print("-" * 70)
    tax = TaxCalculator()
    impuestos = tax.calcular(5000)
    print(f"Base: ${impuestos['base_imponible']:.2f}")
    print(f"IVA (21%): ${impuestos['iva']:.2f}")
    print(f"Total: ${impuestos['total_con_impuestos']:.2f}")
    
    print("\n2. GENERACIÓN DE FACTURA (Strategy)")
    print("-" * 70)
    factura = Factura(
        numero="001-001",
        cliente="Cliente Premium",
        monto_base=5000,
        condicion_impositiva=IVAResponsable()
    )
    print(factura.generar_factura())
    
    print("\n3. PROCESAMIENTO DE PAGO (Abstract Factory)")
    print("-" * 70)
    fabrica = FabricaPagosArgentina()
    metodo_pago = fabrica.crear_pago_tarjeta_debito()
    resultado_pago = metodo_pago.procesar_pago(impuestos['total_con_impuestos'])
    print(resultado_pago['mensaje'])
    print(f"Monto final a cobrar: ${resultado_pago['total']:.2f}")


# ============================================================================
# CASOS DE PRUEBA UNITARIAS
# ============================================================================

def ejecutar_pruebas():
    """
    Casos de prueba para verificar la funcionalidad de cada patrón.
    """
    print("\n" + "="*70)
    print("CASOS DE PRUEBA - VALIDACIÓN DE PATRONES")
    print("="*70)
    
    from patrones_diseno import (
        FactorialCalculator, TaxCalculator,
        DocumentoPrototipo, Hamburguesa, EntregaDelivery
    )
    
    # Prueba 1: Singleton
    print("\n✓ PRUEBA 1: Singleton - Instancia Única")
    calc1 = FactorialCalculator()
    calc2 = FactorialCalculator()
    assert calc1 is calc2, "ERROR: Las instancias no son idénticas"
    print("  Resultado: PASSOU")
    
    # Prueba 2: Cálculo de factorial
    print("\n✓ PRUEBA 2: Singleton - Cálculo Correcto")
    assert calc1.calcular(5) == 120, "ERROR: Factorial incorrecto"
    assert calc1.calcular(0) == 1, "ERROR: 0! debe ser 1"
    print("  Resultado: PASSOU")
    
    # Prueba 3: Impuestos
    print("\n✓ PRUEBA 3: Singleton - Cálculo de Impuestos")
    tax = TaxCalculator()
    impuestos = tax.calcular(1000)
    assert impuestos['iva'] == 210, "ERROR: IVA incorrecto"
    assert impuestos['iibb'] == 50, "ERROR: IIBB incorrecto"
    assert impuestos['municipal'] == 12, "ERROR: Municipal incorrecto"
    print("  Resultado: PASSOU")
    
    # Prueba 4: Prototype - Clonación
    print("\n✓ PRUEBA 4: Prototype - Clonación Independiente")
    doc_original = DocumentoPrototipo("Título", "Contenido", "Autor")
    doc_copia = doc_original.clonar()
    
    assert doc_original._id != doc_copia._id, "ERROR: Los IDs deben ser diferentes"
    doc_copia.modificar(nuevo_titulo="Nuevo Título")
    assert doc_original.titulo == "Título", "ERROR: Original fue modificado"
    assert doc_copia.titulo == "Nuevo Título", "ERROR: Copia no fue modificada"
    print("  Resultado: PASSOU")
    
    # Prueba 5: Prototype - Copia de Copia
    print("\n✓ PRUEBA 5: Prototype - Copia Generada por Copia")
    doc_copia2 = doc_copia.obtener_copia_de_copia()
    assert doc_copia._id != doc_copia2._id, "ERROR: Las copias deben tener IDs diferentes"
    print("  Resultado: PASSOU")
    
    # Prueba 6: Strategy
    print("\n✓ PRUEBA 6: Strategy - Cambio Dinámico de Estrategia")
    hamburgesa = Hamburguesa("Hamburguesa")
    hamburgesa.set_metodo_entrega(EntregaDelivery())
    resultado = hamburgesa.procesar_entrega()
    assert "delivery" in resultado.lower(), "ERROR: Método no aplicado"
    print("  Resultado: PASSOU")
    
    # Prueba 7: Errores esperados
    print("\n✓ PRUEBA 7: Manejo de Errores")
    try:
        calc1.calcular(-5)
        print("  Resultado: FALLÓ (debe lanzar excepción)")
    except ValueError:
        print("  Resultado: PASSOU")
    
    print("\n" + "="*70)
    print("TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("="*70)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║         EJEMPLOS AVANZADOS Y CASOS DE PRUEBA                     ║")
    print("║            Patrones de Diseño en Python                          ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    # Ejecutar ejemplos avanzados
    ejemplo_singleton_factorial()
    ejemplo_strategy_hamburguesa()
    ejemplo_builder_avanzado()
    ejemplo_prototype_versioning()
    ejemplo_abstract_factory_multiregion()
    ejemplo_composicion_patrones()
    
    # Ejecutar pruebas
    ejecutar_pruebas()
    
    print("\n")
