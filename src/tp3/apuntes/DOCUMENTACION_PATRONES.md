# Patrones de Diseño en Python - Documentación Completa

## Índice
1. [Patrón Singleton](#patrón-singleton)
2. [Patrón Strategy](#patrón-strategy)
3. [Patrón Builder](#patrón-builder)
4. [Patrón Prototype](#patrón-prototype)
5. [Patrón Abstract Factory](#patrón-abstract-factory)

---

## Patrón Singleton

### Descripción
El patrón Singleton garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella.

### Implementación 1: FactorialCalculator

```python
class FactorialCalculator:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FactorialCalculator, cls).__new__(cls)
        return cls._instance
```

**Características:**
- Una única instancia compartida por toda la aplicación
- Caché de resultados para evitar recálculos
- Validación de entrada (solo números positivos)

**Uso:**
```python
calc1 = FactorialCalculator()
calc2 = FactorialCalculator()
print(calc1 is calc2)  # True - misma instancia
print(calc1.calcular(5))  # 120
```

### Implementación 2: TaxCalculator

```python
class TaxCalculator:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaxCalculator, cls).__new__(cls)
        return cls._instance
```

**Características:**
- Centraliza el cálculo de impuestos
- Tasas consistentes en toda la aplicación
- Fácil de actualizar tasas globalmente

**Tasas implementadas:**
- IVA: 21%
- IIBB: 5%
- Contribuciones municipales: 1.2%

**Uso:**
```python
tax = TaxCalculator()
resultado = tax.calcular(1000)
# Retorna diccionario con desglose detallado
```

---

## Patrón Strategy

### Descripción
El patrón Strategy define una familia de algoritmos, encapsula cada uno y los hace intercambiables.

### Caso 1: Entregas de Hamburguesa

**Interfaz:**
```python
class MetodoEntrega(ABC):
    @abstractmethod
    def entregar(self, producto):
        pass
```

**Implementaciones:**
- `EntregaEnMostrador`: Retira en el local
- `RetiroPorCliente`: Cliente se acerca a retirar
- `EntregaDelivery`: Entrega a domicilio

**Uso:**
```python
hamburgesa = Hamburguesa("Hamburguesa con queso")
hamburgesa.set_metodo_entrega(EntregaDelivery())
print(hamburgesa.procesar_entrega())
```

### Caso 2: Facturación según Condición Impositiva

**Interfaz:**
```python
class CondicionImpositiva(ABC):
    @abstractmethod
    def aplicar_impuestos(self, monto):
        pass
```

**Implementaciones:**
- `IVAResponsable`: Aplica todos los impuestos (IVA 21%, IIBB 5%, Municipal 1.2%)
- `IVANoInscripto`: Solo aplica IVA (21%)
- `IVAExento`: No aplica ningún impuesto

**Ejemplo de factura:**
```python
factura = Factura(
    numero="001-001",
    cliente="Empresa ABC",
    monto_base=1000,
    condicion_impositiva=IVAResponsable()
)
print(factura.generar_factura())
```

---

## Patrón Builder

### Descripción
El patrón Builder separa la construcción de un objeto complejo de su representación, permitiendo construir diferentes variantes.

### Estructura

```
DirectorConstruccion
        ↓
ConstructorVehiculo (ABC)
        ↓
    ├─ ConstructorAuto
    └─ ConstructorAvion
        ↓
    Vehiculo (ABC)
    ├─ Auto
    └─ Avion
```

### Clase Base

```python
class Vehiculo(ABC):
    def __init__(self):
        self.partes = {}
```

### Constructores

**ConstructorAuto:**
```python
class ConstructorAuto(ConstructorVehiculo):
    def crear_vehiculo(self):
        self.vehiculo = Auto()
    
    def construir_partes(self):
        self.vehiculo.partes['motor'] = 'Motor V8 - 300HP'
        self.vehiculo.partes['ruedas'] = '4 ruedas de aluminio'
        # ... más partes
```

**ConstructorAvion (EXTENDIDO):**
```python
class ConstructorAvion(ConstructorVehiculo):
    def crear_vehiculo(self):
        self.vehiculo = Avion()
    
    def construir_partes(self):
        self.vehiculo.partes['body'] = 'Fuselaje de aluminio'
        self.vehiculo.partes['turbinas'] = '2 turbinas Rolls-Royce'
        self.vehiculo.partes['alas'] = '2 alas de fibra de carbono'
        self.vehiculo.partes['tren_aterrizaje'] = 'Tren retráctil triple'
```

### Director

```python
class DirectorConstruccion:
    def __init__(self, constructor):
        self.constructor = constructor
    
    def construir(self):
        self.constructor.crear_vehiculo()
        self.constructor.construir_partes()
        return self.constructor.obtener_vehiculo()
```

### Uso

```python
# Construir un automóvil
director = DirectorConstruccion(ConstructorAuto())
auto = director.construir()
print(auto.mostrar_partes())

# Construir un avión
director = DirectorConstruccion(ConstructorAvion())
avion = director.construir()
print(avion.mostrar_partes())
```

---

## Patrón Prototype

### Descripción
El patrón Prototype crea nuevos objetos copiando un objeto existente (prototipo) en lugar de crear uno desde cero.

### Implementación

```python
class Prototipo(ABC):
    @abstractmethod
    def clonar(self):
        pass

class DocumentoPrototipo(Prototipo):
    def clonar(self):
        """Crea una copia profunda del documento."""
        return deepcopy(self)
    
    def obtener_copia_de_copia(self):
        """Permite que la copia genere sus propias copias."""
        return self.clonar()
```

### Características Principales

1. **Clonación profunda**: Usa `deepcopy()` para crear copias independientes
2. **IDs únicos**: Cada copia tiene su propio ID de objeto
3. **Cadena de clonación**: Las copias pueden generar sus propias copias

### Uso

```python
# Crear documento original
doc_original = DocumentoPrototipo(
    titulo="Informe Anual",
    contenido="Contenido detallado...",
    autor="María López"
)

# Clonar el documento
doc_copia1 = doc_original.clonar()
doc_copia1.modificar(nuevo_titulo="Informe - Copia")

# La copia puede generar sus propias copias
doc_copia2 = doc_copia1.obtener_copia_de_copia()
doc_copia2.modificar(nuevo_titulo="Informe - Copia de Copia")

# Verificar independencia
print(doc_original._id)  # ID diferente
print(doc_copia1._id)    # ID diferente
print(doc_copia2._id)    # ID diferente
```

### Ventajas

- Copia eficiente de objetos complejos
- Evita recalcular datos de un objeto existente
- Permite crear jerarquías de clonación
- Objetos completamente independientes tras la clonación

---

## Patrón Abstract Factory

### Descripción
El patrón Abstract Factory proporciona una interfaz para crear familias de objetos relacionados sin especificar sus clases concretas.

### Caso de Uso: Sistema Multinacional de Pagos

**Problema:**
Una empresa opera en Argentina y Europa. Cada región tiene diferentes métodos de pago disponibles con tasas distintas.

**Solución:**
Usar Abstract Factory para crear métodos de pago según la región.

### Jerarquía de Clases

```
MedioPago (ABC)
├─ TarjetaCredito
├─ TarjetaDebito
├─ Efectivo
└─ TransferenciaBancaria

FabricaPagos (ABC)
├─ FabricaPagosArgentina
└─ FabricaPagosEuropa
```

### Interfaz Abstract Factory

```python
class FabricaPagos(ABC):
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
```

### Implementaciones Concretas

**FabricaPagosArgentina:**
```python
class FabricaPagosArgentina(FabricaPagos):
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
```

### Métodos de Pago

**TarjetaCredito:**
- Comisión: 3%
- Ejemplo: $5000 → $5150

**TarjetaDebito:**
- Comisión: 0%
- Ejemplo: $5000 → $5000

**Efectivo:**
- Descuento: 5%
- Ejemplo: $5000 → $4750

**TransferenciaBancaria:**
- Comisión: 0%
- Ejemplo: $5000 → $5000

### Uso

```python
# Sistema para Argentina
fabrica_arg = FabricaPagosArgentina()
sistema_arg = SistemaDeFacturacionConPagos(fabrica_arg)
sistema_arg.inicializar_metodos()

# Procesar pago con tarjeta de crédito
metodo = fabrica_arg.crear_pago_tarjeta_credito()
resultado = metodo.procesar_pago(5000)
print(resultado['mensaje'])  # "Pago de $5000.00 procesado..."

# Sistema para Europa
fabrica_eu = FabricaPagosEuropa()
# ... mismo flujo
```

### Ventajas del Patrón

1. **Flexibilidad regional**: Fácil agregar nuevas regiones
2. **Coherencia**: Todos los métodos de una región son compatibles
3. **Mantenibilidad**: Cambios regionales aislados
4. **Extensibilidad**: Agregar nuevos métodos de pago es simple

---

## Resumen Comparativo de Patrones

| Patrón | Propósito | Instancias | Flexibilidad |
|--------|-----------|-----------|--------------|
| **Singleton** | Una instancia global única | 1 | Baja |
| **Strategy** | Intercambiar algoritmos | Múltiples | Alta |
| **Builder** | Construir objetos complejos | 1 por tipo | Media |
| **Prototype** | Clonar objetos | Múltiples | Media |
| **Abstract Factory** | Crear familias de objetos | Múltiples por familia | Alta |

---

## Ejecución del Programa

```bash
python patrones_diseno.py
```

El programa genera una demostración completa de todos los patrones con ejemplos prácticos y visualización formateada.

---

## Requisitos

- Python 3.7+
- Módulos estándar: `abc`, `copy`, `enum`

---

## Conclusión

Estos patrones de diseño son fundamentales en Python para crear código:
- **Mantenible**: Fácil de actualizar y modificar
- **Escalable**: Soporta crecimiento de funcionalidad
- **Reutilizable**: Componentes intercambiables
- **Limpio**: Sigue principios SOLID
