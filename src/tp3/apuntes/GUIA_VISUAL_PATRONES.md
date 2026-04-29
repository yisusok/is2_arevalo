# GUÍA VISUAL DE PATRONES DE DISEÑO
## Referencia Rápida - Python

---

## 1. PATRÓN SINGLETON ✓

### Estructura
```
┌──────────────────────────────┐
│   FactorialCalculator        │
│   TaxCalculator              │
├──────────────────────────────┤
│ - _instance: static          │
├──────────────────────────────┤
│ + __new__(): instance única  │
│ + calcular(n): resultado     │
└──────────────────────────────┘
         ↓
    Una única instancia
    compartida globalmente
```

### Casos de Uso
- ✓ Calculadora de factoriales
- ✓ Cálculo centralizado de impuestos
- ✓ Logger global
- ✓ Pool de conexiones a BD
- ✓ Caché compartido

### Ventajas
- Instancia única garantizada
- Acceso global centralizado
- Control de recursos únicos

### Desventajas
- Dificulta pruebas unitarias
- Oculta dependencias
- Complica concurrencia

### Ejemplo Mínimo
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True
```

---

## 2. PATRÓN STRATEGY ✓

### Estructura
```
┌─────────────────────────┐
│   Context/Cliente       │
│  (Hamburguesa/Factura)  │
├─────────────────────────┤
│ - estrategia            │
├─────────────────────────┤
│ + set_estrategia()      │
│ + ejecutar()            │
└─────────────────────────┘
           ▲
           │ usa
           │
      ┌────┴────────────────────┐
      │                         │
┌─────┴──────┐          ┌──────┴────┐
│ Estrategia │          │ Estrategia │
│    A       │          │     B      │
├────────────┤          ├────────────┤
│ execute()  │          │ execute()  │
└────────────┘          └────────────┘
```

### Casos de Uso
- ✓ Métodos de entrega (mostrador, retiro, delivery)
- ✓ Cálculo de impuestos por condición impositiva
- ✓ Algoritmos de ordenamiento intercambiables
- ✓ Estrategias de pago
- ✓ Validación de datos con reglas diferentes

### Ventajas
- Encapsula algoritmos intercambiables
- Elimina condicionales complejos
- Facilita agregar nuevas estrategias
- Permite elegir estrategia en tiempo de ejecución

### Desventajas
- Puede crear muchas clases
- Overhead para algoritmos simples

### Ejemplo Mínimo
```python
class Estrategia(ABC):
    @abstractmethod
    def ejecutar(self):
        pass

class EstrategiaA(Estrategia):
    def ejecutar(self):
        return "A"

cliente = Cliente()
cliente.set_estrategia(EstrategiaA())
print(cliente.ejecutar())  # A
```

---

## 3. PATRÓN BUILDER ✓

### Estructura
```
┌────────────────────────┐
│ DirectorConstruccion   │
├────────────────────────┤
│ - constructor          │
├────────────────────────┤
│ + construir()          │
└────────────┬───────────┘
             │
       usa   │
             ▼
┌────────────────────────┐
│ ConstructorAbstracto   │
├────────────────────────┤
│ + crear_vehiculo()     │
│ + construir_partes()   │
│ + obtener_vehiculo()   │
└────────────┬───────────┘
             △
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
ConstructorAuto  ConstructorAvion
    │                 │
    └────┬────────────┘
         │ producen
         ▼
    ┌─────────────┐
    │  Producto   │
    │ (Vehículo)  │
    └─────────────┘
```

### Casos de Uso
- ✓ Construcción de automóviles
- ✓ Construcción de aviones (extendido)
- ✓ Creación de objetos complejos (casas, comidas)
- ✓ Construcción de reportes
- ✓ Configuración de aplicaciones

### Ventajas
- Separa construcción de representación
- Facilita crear variantes de productos
- Código más legible (construcción paso a paso)
- Reutilizable para diferentes productos

### Desventajas
- Complejidad adicional para objetos simples
- Múltiples clases necesarias

### Ejemplo Mínimo
```python
class Director:
    def __init__(self, constructor):
        self.constructor = constructor
    
    def construir(self):
        self.constructor.paso1()
        self.constructor.paso2()
        return self.constructor.obtener()
```

---

## 4. PATRÓN PROTOTYPE ✓

### Estructura
```
┌──────────────────────────┐
│  Prototipo (Original)    │
├──────────────────────────┤
│ + titulo                 │
│ + contenido              │
│ + autor                  │
├──────────────────────────┤
│ + clonar()               │
│ + modificar()            │
└──────┬───────────────────┘
       │
   clonar deepcopy
       │
   ┌───┴────┬─────────┐
   ▼        ▼         ▼
Copia1   Copia2   Copia3
(Independiente, puede clonar más)
```

### Casos de Uso
- ✓ Clonar documentos
- ✓ Versioning de objetos
- ✓ Copiar configuraciones
- ✓ Deshacer/Rehacer (undo/redo)
- ✓ Creación rápida de múltiples instancias

### Ventajas
- Copia eficiente de objetos complejos
- Evita recalcular datos existentes
- Las copias son completamente independientes
- Genera cadenas de clonación

### Desventajas
- Requiere implementar clonación profunda
- Puede ser costoso en memoria
- Copia de referencias no deseadas

### Ejemplo Mínimo
```python
from copy import deepcopy

class Prototipo:
    def clonar(self):
        return deepcopy(self)

original = Prototipo()
copia = original.clonar()
print(original is copia)  # False
```

---

## 5. PATRÓN ABSTRACT FACTORY ✓

### Estructura
```
┌─────────────────────────────────────────┐
│    AbstractFactory                      │
│  (FabricaPagos)                         │
├─────────────────────────────────────────┤
│ + crear_tarjeta_credito()               │
│ + crear_tarjeta_debito()                │
│ + crear_efectivo()                      │
│ + crear_transferencia()                 │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
  FabricaArgentina   FabricaEuropa
        │                 │
        └────┬────────────┘
             │ producen
             │
    ┌────────┴──────────────┐
    │                       │
    ▼                       ▼
 MedioPago             MedioPago
 (Familia 1)           (Familia 2)
 ├─ TarjetaCredito    ├─ TarjetaCredito
 ├─ TarjetaDebito     ├─ TarjetaDebito
 ├─ Efectivo          ├─ Efectivo
 └─ Transferencia     └─ Transferencia
```

### Casos de Uso
- ✓ Métodos de pago por región
- ✓ Temas UI (claro/oscuro con componentes relacionados)
- ✓ Sistemas operativos (Mac/Windows/Linux UI)
- ✓ Sabores de base de datos (SQL/NoSQL)
- ✓ Proveedores de servicios (AWS/Azure/GCP)

### Ventajas
- Asegura familias de objetos compatibles
- Aísla código de creación
- Facilita cambiar familias completas
- Favorece consistencia entre productos

### Desventajas
- Complejidad adicional
- Difícil agregar nuevos tipos de productos
- Muchas clases necesarias

### Ejemplo Mínimo
```python
class AbstractFactory(ABC):
    @abstractmethod
    def crear_producto_a(self):
        pass

class ConcreteFactory1(AbstractFactory):
    def crear_producto_a(self):
        return ProductoA1()

factory = ConcreteFactory1()
producto = factory.crear_producto_a()
```

---

## MATRIZ COMPARATIVA

| Aspecto | Singleton | Strategy | Builder | Prototype | Abstract Factory |
|---------|-----------|----------|---------|-----------|------------------|
| **Complejidad** | Baja | Media | Media | Media | Alta |
| **Instancias** | 1 | Múltiples | 1/tipo | Múltiples | Múltiples |
| **Flexibilidad** | Baja | Alta | Media | Media | Alta |
| **Cambio runtime** | No | Sí | No | Sí | Sí |
| **Curva aprendizaje** | Baja | Media | Media | Baja | Alta |

---

## CUÁNDO USAR CADA PATRÓN

### SINGLETON
```
¿Necesitas una instancia única?
└─ SÍ → SINGLETON
└─ NO → Otros patrones
```

### STRATEGY
```
¿Múltiples algoritmos intercambiables?
└─ SÍ → STRATEGY
└─ NO → Otros patrones
```

### BUILDER
```
¿Objeto complejo con muchas partes?
├─ SÍ + construcción paso a paso
│  └─ BUILDER
└─ NO → Otros patrones
```

### PROTOTYPE
```
¿Necesitas clonar objetos?
└─ SÍ → PROTOTYPE
└─ NO → Otros patrones
```

### ABSTRACT FACTORY
```
¿Familias de objetos relacionados?
├─ SÍ + múltiples variantes
│  └─ ABSTRACT FACTORY
└─ NO → Otros patrones
```

---

## ANTI-PATRONES A EVITAR

### ❌ Singleton en TODAS partes
```python
# MAL - Singleton para todo
class TiempoGlobal:
    _instance = None
    # ...

# BIEN - Inyección de dependencias
def procesar(tiempo):
    # usa el tiempo pasado
    pass
```

### ❌ Strategy para algoritmos simples
```python
# MAL - 10 clases para 2 líneas de código
class SumarStrategy(Strategy):
    def ejecutar(self, a, b):
        return a + b

# BIEN - Lambda o función simple
operaciones = {
    'suma': lambda a, b: a + b,
    'resta': lambda a, b: a - b
}
```

### ❌ Builder sin beneficios reales
```python
# MAL - Builder para objeto simple
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

# BIEN - Constructor normal
persona = Persona("Juan", 30)
```

---

## FLUJO DE DECISIÓN

```
                    ┌─ ¿Una instancia? → SINGLETON
                    │
¿Cuál patrón usar?──┼─ ¿Algoritmos intercambiables? → STRATEGY
                    │
                    ├─ ¿Objeto complejo? → BUILDER
                    │
                    ├─ ¿Clonar objetos? → PROTOTYPE
                    │
                    └─ ¿Familias de objetos? → ABSTRACT FACTORY
```

---

## RESUMEN DE IMPLEMENTACIÓN

### Lo que hicimos:

1. **FactorialCalculator** - Singleton
   - Garantiza instancia única
   - Caché de resultados

2. **TaxCalculator** - Singleton
   - Cálculo centralizado de impuestos
   - Acceso global

3. **MetodoEntrega** (y estrategias) - Strategy
   - Intercambiar métodos de entrega
   - Polimorfismo en acción

4. **CondicionImpositiva** (y estrategias) - Strategy
   - Diferentes cálculos según condición
   - Dinámico y extensible

5. **Builder + Director** - Builder
   - Construcción de autos y aviones
   - Separación de responsabilidades

6. **DocumentoPrototipo** - Prototype
   - Clonación profunda
   - Cadena de clonación

7. **FabricaPagos** (y familias) - Abstract Factory
   - Métodos de pago por región
   - Familias de objetos coherentes

---

## REFERENCIAS Y LECTURAS

- Gang of Four (GoF) - Design Patterns
- Design Patterns in Python
- Refactoring Guru - Design Patterns
- Python Documentation - abc module

---

Elaborado en Python 3.7+
Uso de módulos estándar: abc, copy, enum
Sin dependencias externas requeridas.
