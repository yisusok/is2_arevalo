"""
Soluciones de Patrones de Diseño en Python
Todos los ejemplos solicitados implementados correctamente
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
import math


# ============================================================================
# 1. PATRÓN SINGLETON - Clase para calcular factoriales
# ============================================================================

class FactorialCalculator:
    """
    Clase Singleton que asegura una única instancia para calcular factoriales.
    Cualquier clase que lo invoque utilizará la misma instancia.
    """
    _instance = None
    
    def __new__(cls):
        """Implementa el patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(FactorialCalculator, cls).__new__(cls)
            cls._instance._inicializado = False
        return cls._instance
    
    def __init__(self):
        """Inicializa solo una vez."""
        if self._inicializado:
            return
        self._inicializado = True
        self.cache = {}
    
    def calcular(self, n):
        """
        Calcula el factorial de n.
        
        Args:
            n (int): Número entero no negativo
            
        Returns:
            int: El factorial de n
            
        Raises:
            ValueError: Si n es negativo
            TypeError: Si n no es un entero
        """
        if not isinstance(n, int):
            raise TypeError(f"El argumento debe ser un entero, se recibió {type(n).__name__}")
        
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos")
        
        # Buscar en caché
        if n in self.cache:
            return self.cache[n]
        
        # Calcular
        if n == 0 or n == 1:
            resultado = 1
        else:
            resultado = n * self.calcular(n - 1)
        
        # Guardar en caché
        self.cache[n] = resultado
        return resultado


# ============================================================================
# 2. PATRÓN SINGLETON - Clase para calcular impuestos
# ============================================================================

class TaxCalculator:
    """
    Clase Singleton que calcula impuestos de manera centralizada.
    IVA (21%), IIBB (5%) y Contribuciones municipales (1.2%)
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaxCalculator, cls).__new__(cls)
            cls._instance._inicializado = False
        return cls._instance
    
    def __init__(self):
        if self._inicializado:
            return
        self._inicializado = True
        self.iva_rate = 0.21        # 21%
        self.iibb_rate = 0.05       # 5%
        self.municipal_rate = 0.012 # 1.2%
    
    def calcular(self, importe_base):
        """
        Calcula los impuestos totales sobre un importe base.
        
        Args:
            importe_base (float): Valor base imponible
            
        Returns:
            dict: Diccionario con desglose de impuestos y total
        """
        if not isinstance(importe_base, (int, float)) or importe_base < 0:
            raise ValueError("El importe base debe ser un número positivo")
        
        iva = importe_base * self.iva_rate
        iibb = importe_base * self.iibb_rate
        municipal = importe_base * self.municipal_rate
        total_impuestos = iva + iibb + municipal
        
        return {
            'base_imponible': importe_base,
            'iva': round(iva, 2),
            'iibb': round(iibb, 2),
            'municipal': round(municipal, 2),
            'total_impuestos': round(total_impuestos, 2),
            'total_con_impuestos': round(importe_base + total_impuestos, 2)
        }


# ============================================================================
# 3. PATRÓN STRATEGY - Entregas de comida rápida (Hamburguesa)
# ============================================================================

class MetodoEntrega(ABC):
    """Interfaz abstracta para métodos de entrega."""
    
    @abstractmethod
    def entregar(self, producto):
        pass


class EntregaEnMostrador(MetodoEntrega):
    """Entrega en mostrador."""
    
    def entregar(self, producto):
        return f"🍔 {producto} será entregada en mostrador"


class RetiroPorCliente(MetodoEntrega):
    """Retiro por el cliente."""
    
    def entregar(self, producto):
        return f"🍔 {producto} está lista para retirar por el cliente"


class EntregaDelivery(MetodoEntrega):
    """Entrega por delivery."""
    
    def entregar(self, producto):
        return f"🍔 {producto} será entregada por delivery"


class Hamburguesa:
    """
    Clase Hamburguesa que puede ser entregada de diferentes formas.
    Utiliza el patrón Strategy para seleccionar el método de entrega.
    """
    
    def __init__(self, descripcion="Hamburguesa clásica"):
        self.descripcion = descripcion
        self.metodo_entrega = None
    
    def set_metodo_entrega(self, metodo_entrega):
        """Define el método de entrega."""
        self.metodo_entrega = metodo_entrega
    
    def procesar_entrega(self):
        """Procesa la entrega según el método configurado."""
        if self.metodo_entrega is None:
            return "⚠️ No se ha especificado método de entrega"
        return self.metodo_entrega.entregar(self.descripcion)


# ============================================================================
# 4. PATRÓN STRATEGY - Facturación según condición impositiva
# ============================================================================

class CondicionImpositiva(ABC):
    """Interfaz para diferentes condiciones impositivas."""
    
    @abstractmethod
    def aplicar_impuestos(self, monto):
        pass
    
    @abstractmethod
    def obtener_condicion(self):
        pass


class IVAResponsable(CondicionImpositiva):
    """Cliente IVA Responsable - Se le aplican impuestos completos."""
    
    def aplicar_impuestos(self, monto):
        tax_calc = TaxCalculator()
        return tax_calc.calcular(monto)
    
    def obtener_condicion(self):
        return "IVA Responsable"


class IVANoInscripto(CondicionImpositiva):
    """Cliente IVA No Inscripto - Se aplica IVA únicamente."""
    
    def aplicar_impuestos(self, monto):
        iva = monto * 0.21
        return {
            'base_imponible': monto,
            'iva': round(iva, 2),
            'iibb': 0,
            'municipal': 0,
            'total_impuestos': round(iva, 2),
            'total_con_impuestos': round(monto + iva, 2)
        }
    
    def obtener_condicion(self):
        return "IVA No Inscripto"


class IVAExento(CondicionImpositiva):
    """Cliente IVA Exento - No se aplican impuestos."""
    
    def aplicar_impuestos(self, monto):
        return {
            'base_imponible': monto,
            'iva': 0,
            'iibb': 0,
            'municipal': 0,
            'total_impuestos': 0,
            'total_con_impuestos': monto
        }
    
    def obtener_condicion(self):
        return "IVA Exento"


class Factura:
    """
    Clase Factura que genera facturas según la condición impositiva del cliente.
    """
    
    def __init__(self, numero, cliente, monto_base, condicion_impositiva):
        self.numero = numero
        self.cliente = cliente
        self.monto_base = monto_base
        self.condicion = condicion_impositiva
    
    def generar_factura(self):
        """Genera el detalle de la factura."""
        impuestos = self.condicion.aplicar_impuestos(self.monto_base)
        
        factura_text = f"""
╔════════════════════════════════════════════════╗
║                   FACTURA                       ║
╠════════════════════════════════════════════════╣
║ Número: {self.numero:<34} ║
║ Cliente: {self.cliente:<33} ║
║ Condición: {self.condicion.obtener_condicion():<29} ║
╠════════════════════════════════════════════════╣
║ Monto Base:           ${self.monto_base:>10.2f}      ║
║ IVA (21%):            ${impuestos['iva']:>10.2f}      ║
║ IIBB (5%):            ${impuestos['iibb']:>10.2f}      ║
║ Municipal (1.2%):     ${impuestos['municipal']:>10.2f}      ║
║ ─────────────────────────────────────────────  ║
║ Total Impuestos:      ${impuestos['total_impuestos']:>10.2f}      ║
║ ═════════════════════════════════════════════  ║
║ TOTAL A PAGAR:        ${impuestos['total_con_impuestos']:>10.2f}      ║
╚════════════════════════════════════════════════╝
"""
        return factura_text


# ============================================================================
# 5. PATRÓN BUILDER - Construcción de vehículos (extendido a aviones)
# ============================================================================

class Vehiculo(ABC):
    """Clase abstracta para vehículos."""
    
    def __init__(self):
        self.partes = {}
    
    @abstractmethod
    def mostrar_partes(self):
        pass


class Auto(Vehiculo):
    """Clase para representar un automóvil."""
    
    def mostrar_partes(self):
        return f"""
╔════════════════════════════════════════╗
║         AUTOMÓVIL CONSTRUIDO            ║
╠════════════════════════════════════════╣
║ Motor: {self.partes.get('motor', 'No instalado'):<30} ║
║ Ruedas: {self.partes.get('ruedas', 'No instalado'):<29} ║
║ Transmisión: {self.partes.get('transmision', 'No instalado'):<23} ║
║ Asientos: {self.partes.get('asientos', 'No instalado'):<28} ║
║ Techo: {self.partes.get('techo', 'No instalado'):<32} ║
╚════════════════════════════════════════╝
"""


class Avion(Vehiculo):
    """Clase para representar un avión."""
    
    def mostrar_partes(self):
        return f"""
╔════════════════════════════════════════╗
║          AVIÓN CONSTRUIDO               ║
╠════════════════════════════════════════╣
║ Body: {self.partes.get('body', 'No instalado'):<31} ║
║ Turbinas (2): {self.partes.get('turbinas', 'No instalado'):<24} ║
║ Alas (2): {self.partes.get('alas', 'No instalado'):<27} ║
║ Tren de aterrizaje: {self.partes.get('tren_aterrizaje', 'No instalado'):<18} ║
╚════════════════════════════════════════╝
"""


class ConstructorVehiculo(ABC):
    """Clase abstracta para constructores de vehículos."""
    
    def __init__(self):
        self.vehiculo = None
    
    @abstractmethod
    def crear_vehiculo(self):
        pass
    
    @abstractmethod
    def construir_partes(self):
        pass
    
    def obtener_vehiculo(self):
        return self.vehiculo


class ConstructorAuto(ConstructorVehiculo):
    """Constructor de automóviles."""
    
    def crear_vehiculo(self):
        self.vehiculo = Auto()
    
    def construir_partes(self):
        self.vehiculo.partes['motor'] = 'Motor V8 - 300HP'
        self.vehiculo.partes['ruedas'] = '4 ruedas de aluminio'
        self.vehiculo.partes['transmision'] = 'Transmisión automática 6 marchas'
        self.vehiculo.partes['asientos'] = '5 asientos de cuero'
        self.vehiculo.partes['techo'] = 'Techo panorámico'


class ConstructorAvion(ConstructorVehiculo):
    """Constructor de aviones."""
    
    def crear_vehiculo(self):
        self.vehiculo = Avion()
    
    def construir_partes(self):
        self.vehiculo.partes['body'] = 'Fuselaje de aluminio reforzado'
        self.vehiculo.partes['turbinas'] = '2 turbinas Rolls-Royce de 50,000 lbs'
        self.vehiculo.partes['alas'] = '2 alas de fibra de carbono con winglets'
        self.vehiculo.partes['tren_aterrizaje'] = 'Tren retráctil de triple rueda'


class DirectorConstruccion:
    """Director que orquesta la construcción de vehículos."""
    
    def __init__(self, constructor):
        self.constructor = constructor
    
    def construir(self):
        """Ejecuta los pasos de construcción."""
        self.constructor.crear_vehiculo()
        self.constructor.construir_partes()
        return self.constructor.obtener_vehiculo()


# ============================================================================
# 6. PATRÓN PROTOTYPE - Clonación de objetos
# ============================================================================

class Prototipo(ABC):
    """Clase abstracta que define la interfaz de clonación."""
    
    @abstractmethod
    def clonar(self):
        pass
    
    @abstractmethod
    def mostrar_info(self):
        pass


class DocumentoPrototipo(Prototipo):
    """
    Implementa el patrón Prototype.
    Permite crear copias de documentos.
    """
    
    def __init__(self, titulo, contenido, autor):
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor
        self.fecha_creacion = "2024"
        self._id = id(self)
    
    def clonar(self):
        """Crea una copia profunda del documento."""
        copia = deepcopy(self)
        copia._id = id(copia)
        return copia
    
    def obtener_copia_de_copia(self):
        """
        Permite que una copia obtenga también copias de sí misma.
        Verifica que el prototipo puede generar nuevas instancias a partir de copias.
        """
        return self.clonar()
    
    def mostrar_info(self):
        return f"""
╔════════════════════════════════════════╗
║          DOCUMENTO PROTOTIPO             ║
╠════════════════════════════════════════╣
║ ID de objeto: {self._id:<28} ║
║ Título: {self.titulo:<31} ║
║ Autor: {self.autor:<32} ║
║ Fecha: {self.fecha_creacion:<31} ║
║ Contenido: {self.contenido[:30]:<28}... ║
╚════════════════════════════════════════╝
"""
    
    def modificar(self, nuevo_titulo=None, nuevo_contenido=None):
        """Permite modificar la copia sin afectar el original."""
        if nuevo_titulo:
            self.titulo = nuevo_titulo
        if nuevo_contenido:
            self.contenido = nuevo_contenido


# ============================================================================
# 7. PATRÓN ABSTRACT FACTORY - Fábrica de sistemas de pago
# ============================================================================

class MedioPago(ABC):
    """Interfaz abstracta para medios de pago."""
    
    @abstractmethod
    def procesar_pago(self, monto):
        pass
    
    @abstractmethod
    def obtener_nombre(self):
        pass


class TarjetaCredito(MedioPago):
    """Implementación de pago con tarjeta de crédito."""
    
    def procesar_pago(self, monto):
        comision = monto * 0.03
        return {
            'metodo': 'Tarjeta de Crédito',
            'monto_original': monto,
            'comision': round(comision, 2),
            'total': round(monto + comision, 2),
            'mensaje': f'Pago de ${monto:.2f} procesado con comisión del 3%'
        }
    
    def obtener_nombre(self):
        return "Tarjeta de Crédito"


class TarjetaDebito(MedioPago):
    """Implementación de pago con tarjeta de débito."""
    
    def procesar_pago(self, monto):
        return {
            'metodo': 'Tarjeta de Débito',
            'monto_original': monto,
            'comision': 0,
            'total': monto,
            'mensaje': f'Pago de ${monto:.2f} procesado sin comisión'
        }
    
    def obtener_nombre(self):
        return "Tarjeta de Débito"


class Efectivo(MedioPago):
    """Implementación de pago en efectivo."""
    
    def procesar_pago(self, monto):
        descuento = monto * 0.05
        return {
            'metodo': 'Efectivo',
            'monto_original': monto,
            'descuento': round(descuento, 2),
            'total': round(monto - descuento, 2),
            'mensaje': f'Pago de ${monto:.2f} procesado con 5% de descuento'
        }
    
    def obtener_nombre(self):
        return "Efectivo"


class TransferenciaBancaria(MedioPago):
    """Implementación de pago por transferencia bancaria."""
    
    def procesar_pago(self, monto):
        return {
            'metodo': 'Transferencia Bancaria',
            'monto_original': monto,
            'comision': 0,
            'total': monto,
            'mensaje': f'Pago de ${monto:.2f} transferido exitosamente'
        }
    
    def obtener_nombre(self):
        return "Transferencia Bancaria"


class FabricaPagos(ABC):
    """Abstract Factory para crear diferentes medios de pago por región."""
    
    @abstractmethod
    def crear_pago_tarjeta_credito(self):
        pass
    
    @abstractmethod
    def crear_pago_tarjeta_debito(self):
        pass
    
    @abstractmethod
    def crear_pago_efectivo(self):
        pass
    
    @abstractmethod
    def crear_pago_transferencia(self):
        pass
    
    @abstractmethod
    def obtener_nombre_region(self):
        pass


class FabricaPagosArgentina(FabricaPagos):
    """Factory para métodos de pago comunes en Argentina."""
    
    def crear_pago_tarjeta_credito(self):
        return TarjetaCredito()
    
    def crear_pago_tarjeta_debito(self):
        return TarjetaDebito()
    
    def crear_pago_efectivo(self):
        return Efectivo()
    
    def crear_pago_transferencia(self):
        return TransferenciaBancaria()
    
    def obtener_nombre_region(self):
        return "Argentina"


class FabricaPagosEuropa(FabricaPagos):
    """Factory para métodos de pago comunes en Europa."""
    
    def crear_pago_tarjeta_credito(self):
        return TarjetaCredito()
    
    def crear_pago_tarjeta_debito(self):
        return TarjetaDebito()
    
    def crear_pago_efectivo(self):
        return Efectivo()
    
    def crear_pago_transferencia(self):
        return TransferenciaBancaria()
    
    def obtener_nombre_region(self):
        return "Europa"


class SistemaDeFacturacionConPagos:
    """
    Sistema que utiliza la Abstract Factory para gestionar pagos.
    Ejemplo de uso práctico del patrón.
    """
    
    def __init__(self, fabrica_pagos):
        self.fabrica = fabrica_pagos
        self.metodos_disponibles = []
    
    def inicializar_metodos(self):
        """Crea todos los métodos de pago disponibles."""
        self.metodos_disponibles = [
            self.fabrica.crear_pago_tarjeta_credito(),
            self.fabrica.crear_pago_tarjeta_debito(),
            self.fabrica.crear_pago_efectivo(),
            self.fabrica.crear_pago_transferencia()
        ]
    
    def mostrar_metodos_disponibles(self):
        """Muestra los métodos de pago disponibles en la región."""
        info = f"\n╔════════════════════════════════════════╗\n"
        info += f"║  Métodos de pago en {self.fabrica.obtener_nombre_region():<23} ║\n"
        info += f"╠════════════════════════════════════════╣\n"
        for metodo in self.metodos_disponibles:
            info += f"║ ✓ {metodo.obtener_nombre():<35} ║\n"
        info += f"╚════════════════════════════════════════╝\n"
        return info


# ============================================================================
# PROGRAMA PRINCIPAL - DEMOSTRACIONES
# ============================================================================

def main():
    print("\n" + "="*70)
    print("PATRONES DE DISEÑO EN PYTHON - DEMOSTRACIONES COMPLETAS")
    print("="*70)
    
    # ========================================================================
    # 1. SINGLETON - FACTORIAL
    # ========================================================================
    print("\n1. PATRÓN SINGLETON - CÁLCULO DE FACTORIALES")
    print("-" * 70)
    
    calc1 = FactorialCalculator()
    calc2 = FactorialCalculator()
    
    print(f"¿calc1 es calc2? {calc1 is calc2}")  # True - misma instancia
    print(f"Factorial de 5: {calc1.calcular(5)}")
    print(f"Factorial de 10: {calc2.calcular(10)}")
    print(f"Caché actual: {calc1.cache}")
    
    # ========================================================================
    # 2. SINGLETON - CÁLCULO DE IMPUESTOS
    # ========================================================================
    print("\n2. PATRÓN SINGLETON - CÁLCULO DE IMPUESTOS")
    print("-" * 70)
    
    tax1 = TaxCalculator()
    tax2 = TaxCalculator()
    
    print(f"¿tax1 es tax2? {tax1 is tax2}")  # True - misma instancia
    
    resultado = tax1.calcular(1000)
    for clave, valor in resultado.items():
        print(f"  {clave}: ${valor:.2f}" if clave != 'base_imponible' else f"  {clave}: ${valor:.2f}")
    
    # ========================================================================
    # 3. STRATEGY - HAMBURGUESA CON DIFERENTES ENTREGAS
    # ========================================================================
    print("\n3. PATRÓN STRATEGY - ENTREGAS DE HAMBURGUESA")
    print("-" * 70)
    
    hamburgesa = Hamburguesa("Hamburguesa con queso")
    
    # Entrega en mostrador
    hamburgesa.set_metodo_entrega(EntregaEnMostrador())
    print(hamburgesa.procesar_entrega())
    
    # Retiro por cliente
    hamburgesa.set_metodo_entrega(RetiroPorCliente())
    print(hamburgesa.procesar_entrega())
    
    # Delivery
    hamburgesa.set_metodo_entrega(EntregaDelivery())
    print(hamburgesa.procesar_entrega())
    
    # ========================================================================
    # 4. STRATEGY - FACTURAS SEGÚN CONDICIÓN IMPOSITIVA
    # ========================================================================
    print("\n4. PATRÓN STRATEGY - FACTURACIÓN CON DIFERENTES CONDICIONES")
    print("-" * 70)
    
    monto_base = 1000
    
    # Factura para IVA Responsable
    factura1 = Factura(
        numero="001-001",
        cliente="Empresa ABC",
        monto_base=monto_base,
        condicion_impositiva=IVAResponsable()
    )
    print(factura1.generar_factura())
    
    # Factura para IVA No Inscripto
    factura2 = Factura(
        numero="001-002",
        cliente="Juan Pérez",
        monto_base=monto_base,
        condicion_impositiva=IVANoInscripto()
    )
    print(factura2.generar_factura())
    
    # Factura para IVA Exento
    factura3 = Factura(
        numero="001-003",
        cliente="Institución Educativa",
        monto_base=monto_base,
        condicion_impositiva=IVAExento()
    )
    print(factura3.generar_factura())
    
    # ========================================================================
    # 5. BUILDER - CONSTRUCCIÓN DE AUTOS Y AVIONES
    # ========================================================================
    print("\n5. PATRÓN BUILDER - CONSTRUCCIÓN DE VEHÍCULOS")
    print("-" * 70)
    
    # Construcción de un automóvil
    director = DirectorConstruccion(ConstructorAuto())
    auto = director.construir()
    print(auto.mostrar_partes())
    
    # Construcción de un avión
    director = DirectorConstruccion(ConstructorAvion())
    avion = director.construir()
    print(avion.mostrar_partes())
    
    # ========================================================================
    # 6. PROTOTYPE - CLONACIÓN DE OBJETOS
    # ========================================================================
    print("\n6. PATRÓN PROTOTYPE - CLONACIÓN DE DOCUMENTOS")
    print("-" * 70)
    
    # Crear documento original
    doc_original = DocumentoPrototipo(
        titulo="Informe Anual",
        contenido="Este es un informe detallado de las actividades realizadas",
        autor="María López"
    )
    
    print("DOCUMENTO ORIGINAL:")
    print(doc_original.mostrar_info())
    
    # Clonar el documento
    doc_copia1 = doc_original.clonar()
    doc_copia1.modificar(
        nuevo_titulo="Informe Anual - Copia",
        nuevo_contenido="Versión modificada del informe"
    )
    
    print("PRIMERA COPIA (modificada):")
    print(doc_copia1.mostrar_info())
    
    # Verificar que la copia puede generar sus propias copias
    doc_copia2 = doc_copia1.obtener_copia_de_copia()
    doc_copia2.modificar(nuevo_titulo="Informe Anual - Copia de Copia")
    
    print("COPIA DE LA COPIA (segunda generación):")
    print(doc_copia2.mostrar_info())
    
    print("\n✓ Verificación: Los IDs de objeto son diferentes")
    print(f"  ID Original: {doc_original._id}")
    print(f"  ID Copia 1: {doc_copia1._id}")
    print(f"  ID Copia 2: {doc_copia2._id}")
    
    # ========================================================================
    # 7. ABSTRACT FACTORY - SISTEMAS DE PAGO
    # ========================================================================
    print("\n7. PATRÓN ABSTRACT FACTORY - SISTEMAS DE PAGO")
    print("-" * 70)
    
    print("\nSCENARIO: Sistema de facturación multinacional")
    print("Necesidad: Diferentes métodos de pago según la región\n")
    
    # Sistema para Argentina
    fabrica_arg = FabricaPagosArgentina()
    sistema_arg = SistemaDeFacturacionConPagos(fabrica_arg)
    sistema_arg.inicializar_metodos()
    print(sistema_arg.mostrar_metodos_disponibles())
    
    # Procesar algunos pagos
    print("EJEMPLOS DE TRANSACCIONES EN ARGENTINA:")
    print("-" * 70)
    
    metodo_credito = fabrica_arg.crear_pago_tarjeta_credito()
    resultado = metodo_credito.procesar_pago(5000)
    print(f"  {resultado['mensaje']}")
    print(f"  Total a cobrar: ${resultado['total']:.2f}")
    
    metodo_efectivo = fabrica_arg.crear_pago_efectivo()
    resultado = metodo_efectivo.procesar_pago(5000)
    print(f"  {resultado['mensaje']}")
    print(f"  Total a cobrar: ${resultado['total']:.2f}")
    
    # Sistema para Europa
    fabrica_eu = FabricaPagosEuropa()
    sistema_eu = SistemaDeFacturacionConPagos(fabrica_eu)
    sistema_eu.inicializar_metodos()
    print(sistema_eu.mostrar_metodos_disponibles())
    
    print("\n" + "="*70)
    print("FIN DE LAS DEMOSTRACIONES")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
