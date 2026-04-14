# Trabajo Práctico N°2 - Calculadora RPN
## Ingeniería de Software II - UADER

---

## Introducción

El presente trabajo práctico consiste en el desarrollo de una calculadora que implementa la Notación Polaca Inversa (RPN), utilizando una pila para la evaluación de expresiones.

Se aplicó una metodología iterativa asistida por IA para mejorar la calidad del código, reducir su complejidad y aumentar su mantenibilidad, cumpliendo con todos los requisitos especificados en la consigna.

---

# 1. Métricas del Código (Multimetric)

## 1.1 Reporte Inicial (Código Base)

| Métrica | Valor | Observación |
|--------|------|------------|
| comment_ratio | 14.589% | ❌ Muy bajo |
| cyclomatic_complexity | 42 | ❌ Alta complejidad |
| halstead_effort | 436,965.65 | - |
| halstead_timerequired | 24,275.87 s (~6.7h) | - |
| halstead_bugprop | 1.931 | - |
| maintainability_index | 43.938 | Bajo |

---

## 1.2 Reporte Refactorizado

| Métrica | Valor | Observación |
|--------|------|------------|
| comment_ratio | 29.524% | ⚠️ Cercano al objetivo |
| cyclomatic_complexity | 21 | ✔️ Mejora significativa |
| halstead_effort | 486,001.78 | - |
| halstead_timerequired | 27,000.10 s (~7.5h) | - |
| halstead_bugprop | 2.07 | - |
| maintainability_index | 45.360 | ✔️ Mejora |

---

## 1.3 Reporte Final

| Métrica | Valor | Observación |
|--------|------|------------|
| comment_ratio | **48.88%** | ✅ Cumple |
| cyclomatic_complexity | **10** | ✅ Excelente |
| halstead_effort | 1,076,316.44 | - |
| halstead_timerequired | 59,795.36 s (~16.6h) | - |
| halstead_bugprop | 2.944 | - |
| maintainability_index | 33.146 | ⚠️ Afectado por volumen |
| pylint | **10.0/10.0** | ✅ Calidad perfecta |

---

## 1.a Proporción de Comentarios

El valor final alcanzado fue **48.88%**, superando ampliamente el mínimo requerido de **33.3%**.

### Estrategias aplicadas:
- Uso intensivo de comentarios inline (`#`)
- Documentación de funciones críticas
- Explicación de decisiones de diseño
- Comentarios en validaciones y flujo lógico

---

## 1.b Halstead Effort vs Tiempo Real

- Tiempo estimado: **16.6 horas**
- Tiempo real: significativamente menor

### Análisis:
Las métricas de Halstead asumen desarrollo manual.  
El uso de herramientas de IA permitió reducir drásticamente el tiempo real de implementación.

---

## 1.c Halstead Bugprop vs Defectos Reales

- Estimación: **~3 defectos**
- Defectos reales: **0 (post testing)**

### Conclusión:
Las métricas son conservadoras y no contemplan:
- Testing automatizado
- Linters
- Asistencia de IA

---

## 1.d Reducción de Complejidad Ciclomática

Se redujo de **42 → 10 (76%)**

### Estrategias:
- Reemplazo de `if/elif` por diccionario de despacho
- Modularización de funciones
- Separación de responsabilidades

---

## 1.e Iteraciones del Desarrollo

1. Implementación inicial funcional
2. Refactorización estructural
3. Mejora de comentarios
4. Optimización de métricas
5. Ajuste final con herramientas de calidad

---

# 2. Tests Unitarios y Cobertura

## Framework utilizado
- `unittest`

## Cobertura alcanzada
- **92% total**

## Comandos ejecutados

```bash
coverage run -m unittest -v
coverage report -m


# 3. Test Funcional

Se realizó un test funcional manual ejecutando el programa desde consola para verificar el comportamiento integral del sistema.

## Caso principal

```bash
python rpn.py "5 1 2 + 4 * + 3 -"