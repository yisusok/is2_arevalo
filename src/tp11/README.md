# TP11: Gestión de Calidad, Validación & Verificación

**Asignatura:** Ingeniería de Software II  
**Docente:** Dr. Pedro E. Colla  
**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  
**Alumno:** Jesús Arévalo  
**Ubicación de Resolución y Documentación:** `src/tp11/`  

> **Nota de Alineación Académica:** Las respuestas, derivaciones matemáticas, modelos de confiabilidad y desarrollos de software presentados en este documento han sido elaborados en estricta conformidad con el marco teórico, modelos sistémicos, formulaciones y láminas de las clases dictadas por el **Dr. Pedro E. Colla** (*"Gestión de Calidad, Validación & Verificación"*, *"Procesos de Calidad"*, *"Garantía"* y el taller *"Taller_Defectos.ipynb"*), así como el tutorial de referencia *"Kanban para uso genérico"* del **Ing. Álvaro Ruiz de Mendarozqueta**.

---

## Tabla de Contenidos

1. [Archivos de Código, Pruebas y Notebook Asociados](#archivos-de-código-pruebas-y-notebook-asociados)
2. [Ejercicio 1: Conjetura de Collatz: Requerimientos, Trazabilidad e Inspección](#ejercicio-1-conjetura-de-collatz-requerimientos-trazabilidad-e-inspección)
3. [Ejercicio 2: Métricas de Fase, Contención (PCE) y Densidad de Defectos](#ejercicio-2-métricas-de-fase-contención-pce-y-densidad-de-defectos)
4. [Ejercicio 3: Metodología Kanban y el Parámetro TEP (Álvaro Ruiz de Mendarozqueta)](#ejercicio-3-metodología-kanban-y-el-parámetro-tep-álvaro-ruiz-de-mendarozqueta)
5. [Ejercicio 4: Modelos Dinámicos de Confiabilidad y Proyección de Defectos (Modelo de Musa)](#ejercicio-4-modelos-dinámicos-de-confiabilidad-y-proyección-de-defectos-modelo-de-musa)
6. [Ejercicio 5: Marco para Evaluar Garantía y Efecto de Multas Contractuales](#ejercicio-5-marco-para-evaluar-garantía-y-efecto-de-multas-contractuales)
7. [Ejercicio 6: Línea de Base Organizacional y Dimensionamiento de V&V](#ejercicio-6-línea-de-base-organizacional-y-dimensionamiento-de-vv)
8. [Ejercicio 7: Herramienta CLI `json2csv.py` y Marco de Integración Continua (CI/CD)](#ejercicio-7-herramienta-cli-json2csvpy-y-marco-de-integración-continua-cicd)
9. [Ejercicio 8: Deuda Técnica y Calidad en Ciclos Ágiles](#ejercicio-8-deuda-técnica-y-calidad-en-ciclos-ágiles)

---

## Archivos de Código, Pruebas y Notebook Asociados

Para la resolución automatizada, verificación de calidad, simulación numérica y validación de software de este trabajo práctico, se desarrollaron los siguientes componentes dentro de `src/tp11/` y en la raíz del repositorio:

- [collatz.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/collatz.py): Implementación refactorizada, robusta y con manejo de excepciones de la conjetura de Collatz.
- [test_collatz.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/test_collatz.py): Suite de pruebas unitarias (caja blanca) y funcionales (caja negra) con Pytest para Collatz (cobertura del 90%).
- [taller_defectos_collatz.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/taller_defectos_collatz.py): Script en Python que implementa los algoritmos de regresión del Modelo de Confiabilidad de Musa / Goel-Okumoto para la tabla dada y para las sesiones de Collatz.
- [ejercicio_garantia_vyv.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/ejercicio_garantia_vyv.py): Script de resolución analítica del ejercicio de línea de base organizacional de V&V (PCE=89%, $\delta_r=0.12$ def/FP, $S=100$ FP).
- [json2csv.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/json2csv.py): Herramienta utilitaria de filtro CLI para conversión de archivos JSON a CSV (`-i`, `-o`, `-d`).
- [test_json2csv.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/test_json2csv.py): Suite de 20 pruebas unitarias e integración para `json2csv.py` con cobertura del 99%.
- [create_notebook.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/create_notebook.py): Script generador programático del cuaderno Jupyter Notebook.
- [TP11_Gestion_Calidad.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/TP11_Gestion_Calidad.ipynb): Jupyter Notebook interactivo con modelos ejecutables, simulaciones y visualizaciones.
- [CONTEXT.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/CONTEXT.md): Registro formal de requerimientos y directivas de asistencia IA.
- [CHANGELOG.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/CHANGELOG.md): Historial de versiones y modificaciones bajo estándar Keep a Changelog.
- [REQUIREMENTS.TXT](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/REQUIREMENTS.TXT): Lista de dependencias del entorno de ejecución.
- [VERSION](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/VERSION) y [BUILD](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/BUILD): Registro estático de versión y build.
- [LICENSE](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/LICENSE): Licencia de software MIT.
- [.github/workflows/ci.yml](file:///c:/Users/Usuario/Desktop/is2_arevalo/.github/workflows/ci.yml): Workflow de CI/CD para GitHub Actions integrando linters, análisis de tipos, seguridad y tests con cobertura.

---

## Ejercicio 1: Conjetura de Collatz: Requerimientos, Trazabilidad e Inspección

### 1.1. Estructura de Requerimientos

#### Requerimientos Funcionales $R = \{R_1, R_2, R_3, R_4\}$:
- **$R_1$:** El sistema debe solicitar y aceptar un número entero positivo cualquiera por teclado ($n \in \mathbb{Z}^+$).
- **$R_2$:** El sistema debe comprobar la conjetura de Collatz aplicando recursiva/iterativamente la regla:
  $$\text{Si } n \text{ es par} \implies n = \frac{n}{2}$$
  $$\text{Si } n \text{ es impar} \implies n = 3n + 1$$
  deteniéndose cuando se alcanza el valor $1$.
- **$R_3$:** El sistema debe calcular el número exacto de iteraciones necesarias para que el número de partida alcance el valor 1.
- **$R_4$:** El sistema debe imprimir en pantalla el número de partida y el número total de iteraciones calculadas.

#### Requerimientos No Funcionales $F = \{F_1, F_2, F_3, F_4\}$:
- **$F_1$ (Restricción de Dominio / Capacidad):** Por cuestiones prácticas, el sistema debe limitar a 1999 el entero máximo a validar ($1 \le n \le 1999$). Ante un valor superior o inferior a este rango, se debe rechazar o solicitar reingreso.
- **$F_2$ (Calidad de Código / Tasa de Comentarios):** La tasa de comentarios del código fuente debe mantenerse dentro de los estándares de mantenibilidad de la cátedra (se considera defecto una tasa mayor a 12).
- **$F_3$ (Robustez y Manejo de Excepciones):** El programa debe interceptar y manejar amigablemente condiciones de error en tiempo de ejecución (entradas no numéricas, flotantes, cadenas, interrupciones de teclado).
- **$F_4$ (Estándares de Codificación):** Cumplimiento de convenciones sintácticas de Python (PEP8) y documentación mediante docstrings (PEP257).

---

### 1.2. Formulación de Casos de Prueba $T = \{T_1, \dots, T_{12}\}$

| ID | Tipo de Test | Entrada ($n$) | Salida / Comportamiento Esperado | Criterio de Selección |
|---|---|---|---|---|
| **$T_1$** | Unitario (Caja Blanca) | $n = 1$ | `iteraciones = 0` | Cobertura de rama: condición de parada inmediata (`num != 1` es falso al ingreso). |
| **$T_2$** | Unitario (Caja Blanca) | $n = 2$ | `iteraciones = 1` | Cobertura de rama par simple (`num % 2 == 0`). |
| **$T_3$** | Unitario (Caja Blanca) | $n = 3$ | `iteraciones = 7` | Cobertura de rama impar (`num = 3n + 1`) y alternancia de ramas ($3 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1$). |
| **$T_4$** | Unitario (Caja Blanca) | $n = 4$ | `iteraciones = 2` | Cobertura de múltiples ramas pares sucesivas ($4 \to 2 \to 1$). |
| **$T_{11}$** | Unitario (Caja Blanca) | $n = 0$ | Dispara `ValueError` | Cobertura de control defensivo interno. |
| **$T_{12}$** | Unitario (Caja Blanca) | $n = -5$ | Dispara `ValueError` | Cobertura de valores no positivos. |
| **$T_5$** | Funcional (Caja Negra) | $n = 20$ | Partida: 20, Iteraciones: 7 | Caso nominal solicitado en el snippet de prueba de la guía. |
| **$T_6$** | Funcional (Caja Negra) | $n = 1$ | Partida: 1, Iteraciones: 0 | Valor límite inferior válido del dominio de entrada. |
| **$T_7$** | Funcional (Caja Negra) | $n = 1999$ | Partida: 1999, Iteraciones: 50 | Valor límite superior válido permitido ($F_1$). |
| **$T_8$** | Funcional (Caja Negra) | $n = 2000$ | Mensaje de error / Rechazo | Prueba de frontera: valor inmediatamente superior al máximo admisible ($F_1$). |
| **$T_9$** | Funcional (Caja Negra) | $n \le 0$ (ej: -10) | Mensaje de error / Rechazo | Caso de excepción funcional: rechazo de enteros no positivos ($R_1$). |
| **$T_{10}$** | Funcional (Caja Negra) | `"abc"`, `12.5` | Mensaje de error / Reintento | Robustez de interfaz: entrada no numérica o con formato inválido ($F_3$). |

---

### 1.3. Matriz de Trazabilidad RTMX ($R \cup F \iff T$)

La matriz de trazabilidad bidireccional valida la integridad del conjunto de pruebas, asegurando que cada requerimiento esté cubierto por al menos un caso de prueba y que no existan pruebas desvinculadas de los requerimientos:

| Requerimiento | $T_1$ | $T_2$ | $T_3$ | $T_4$ | $T_5$ | $T_6$ | $T_7$ | $T_8$ | $T_9$ | $T_{10}$ | $T_{11}$ | $T_{12}$ | Cobertura |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$R_1$ (Entrada teclado)** | | | | | **X** | **X** | **X** | **X** | **X** | **X** | | | **100%** |
| **$R_2$ (Algoritmo Collatz)** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | | | | | | **100%** |
| **$R_3$ (Cálculo iteraciones)**| **X** | **X** | **X** | **X** | **X** | **X** | **X** | | | | | | **100%** |
| **$R_4$ (Salida en pantalla)** | | | | | **X** | **X** | **X** | | | | | | **100%** |
| **$F_1$ (Límite $\le 1999$)**   | | | | | | | **X** | **X** | | | | | **100%** |
| **$F_2$ (Tasa comentarios)**   | | | | | | | | | | | | | *Inspección* |
| **$F_3$ (Robustez/Excepciones)**| | | | | | | | **X** | **X** | **X** | **X** | **X** | **100%** |
| **$F_4$ (Convenciones/Calidad)**| | | | | | | | | | | | | *Linters/CI* |

**Validación de Integridad:** Se comprueba que $\forall r \in R \cup F, \exists t \in T$ tal que $r \mapsto t$, y recíprocamente $\forall t \in T, \exists r \in R \cup F$ tal que $t \mapsto r$. No existen requerimientos huérfanos ni casos de prueba espurios.

---

### 1.4. Sesión 1: Inspección Estática del Código Original (Sin Ejecutar)

El fragmento original provisto en la guía es:

```python
#Calculando el número de iteraciones del algoritmo de Collatz
def collatz(num):
 iteraciones = 0
 while num != 1:
 if num % 2 == 0:
 num = num // 2
 else:
 num = 3*num + 1
 iteraciones += 1
 return iter 
#Comprobando los resultados
i=20
print("El número de iteraciones para %d es %d\n" % (i,collatz(j))
```

#### Defectos Detectados en la Sesión 1 (Inspección):
1. **Defecto Sintáctico 1 (Indentación):** Las líneas dentro del bloque `while` y de las estructuras `if/else` carecen de indentación obligatoria en Python (`IndentationError`).
2. **Defecto Sintáctico 2 (Paréntesis no cerrado):** La última línea `print("..." % (i, collatz(j))` no cierra el paréntesis de la función `print` (`SyntaxError: '(' was never closed`).
3. **Defecto Semántico 1 (Variable de retorno no definida / Built-in):** `return iter` intenta retornar `iter` (función integrada del lenguaje) en lugar de la variable de estado local `iteraciones`.
4. **Defecto Semántico 2 (Variable no definida en invocación):** La llamada `collatz(j)` utiliza la variable `j`, la cual nunca fue definida ni inicializada (la variable asignada previamente es `i = 20`), provocando `NameError`.
5. **Defecto de Requerimiento 1 (Ausencia de entrada por teclado):** El código contiene un valor hardcodeado `i = 20`, incumpliendo el requerimiento $R_1$ que exige solicitar y aceptar el dato por teclado.
6. **Defecto de Requerimiento 2 (Ausencia de límite superior $n \le 1999$):** No existe ningún control sobre la cota máxima establecida en $F_1$.
7. **Defecto de Requerimiento 3 (Ausencia de validación de positividad):** No se valida que el entero sea estrictamente positivo ($n \ge 1$); un valor $n \le 0$ produciría un bucle infinito en tiempo de ejecución.
8. **Defecto No Funcional (Tasa de comentarios):** El programa original consta de 14 líneas netas y posee 2 comentarios. Si la tasa se calcula como $\frac{\text{Líneas de código}}{\text{Comentarios}} = \frac{14}{2} = 7$, o bien como porcentaje ($\approx 14.3\%$), se detecta la ausencia de docstring normativo del módulo.

*Total de defectos detectados en Sesión 1:* **4 defectos críticos de código (sintácticos y semánticos) + 3 defectos de requerimiento.**

---

### 1.5. Sesión 2: Inspección y Validación del Conjunto de Casos de Prueba

En la Sesión 2 se procedió a revisar la suficiencia de los casos de prueba formulados originalmente:
- **Defecto en pruebas 1:** Se constató la omisión de casos de prueba para entradas fuera de límite superior ($n = 2000$).
- **Defecto en pruebas 2:** Se constató la omisión de casos para entradas no numéricas o con caracteres especiales.
- **Acción:** Se incorporaron formalmente $T_8, T_9, T_{10}, T_{11}, T_{12}$ y se actualizó la matriz de trazabilidad RTMX.

*Total de defectos detectados en Sesión 2:* **2 defectos de cobertura de prueba.**

---

### 1.6. Ejecución de Sesiones de Testing Unitario $\{S_1, S_2, S_3\}$

- **Sesión $S_1$ (Primer intento de ejecución unitaria):**
  - Se ejecuta el archivo sin modificar.
  - *Resultado:* Falla inmediata durante la etapa de parsing de Python por `IndentationError` y `SyntaxError`.
  - *Defectos computados:* **2 defectos.**
  - *Acción correctiva entre sesiones:* Se corrige la indentación del bloque `while` y del `if/else`, y se cierra el paréntesis del `print`.
- **Sesión $S_2$ (Segundo intento de ejecución unitaria):**
  - Se ejecuta la suite unitaria.
  - *Resultado:* Falla en runtime por `NameError: name 'j' is not defined` y retorno erróneo de tipo función en `return iter`.
  - *Defectos computados:* **2 defectos.**
  - *Acción correctiva entre sesiones:* Se sustituye `return iter` por `return iteraciones` y se parametriza correctamente la llamada a la función.
- **Sesión $S_3$ (Tercer intento de ejecución unitaria):**
  - Se ejecutan los casos $T_1, T_2, T_3, T_4, T_{11}, T_{12}$.
  - *Resultado:* **100% de casos unitarios exitosos.** 0 fallas observadas.

---

### 1.7. Ejecución de Sesiones de Testing Funcional $\{S_4, S_5\}$

- **Sesión $S_4$ (Primer intento de ejecución funcional):**
  - Se evalúan los casos funcionales $T_5$ a $T_{10}$.
  - *Resultado:* Fallan $T_8$ (acepta $n > 1999$), $T_9$ (admite números negativos o entra en bucle) y $T_{10}$ (rompe por `ValueError` sin atrapar excepción). Además, se detecta que el programa no pide datos por teclado.
  - *Defectos computados:* **1 defecto funcional mayor (lógica de validación de entrada por teclado y límites).**
  - *Acción correctiva:* Se implementa la función `solicitar_numero()` con bucle de validación, manejo de `ValueError`, mensajes claros y control de rango $[1, 1999]$.
- **Sesión $S_5$ (Segundo intento de ejecución funcional):**
  - Se ejecutan la totalidad de casos de prueba funcionales ($T_5$ a $T_{10}$).
  - *Resultado:* **100% de casos funcionales exitosos.** 0 fallas observadas.

---

### 1.8. Resumen Consolidado de Sesiones y Defectos

| Sesión | Tipo / Etapa | Defectos Detectados | Estado / Observaciones |
|---|---|:---:|---|
| **$S_1$** | Inspección Estática de Código | 4 | Errores de indentación, sintaxis, variables y retornos. |
| **$S_2$** | Inspección de Casos de Prueba | 2 | Omisiones de casos de frontera y excepciones. |
| **$S_3$** | Testing Unitario (Corrida 1 y 2) | 2 | Falla sintáctica inicial y posterior falla de ejecución. |
| **$S_4$** | Testing Unitario (Corrida 3) | 0 | 100% de tests unitarios exitosos. |
| **$S_5$** | Testing Funcional (Corrida 1) | 1 | Falla en validación de entrada por teclado y cota 1999. |
| **$S_6$** | Testing Funcional (Corrida 2) | 0 | 100% de tests funcionales exitosos. |
| **Total** | **Todas las sesiones** | **9** | **Condiciones de finalización verificadas al 100%.** |

#### Verificación de Condiciones de Cierre:
- [x] Todos los casos de prueba fueron exitosamente ejecutados al menos una vez.
- [x] No hubo caso de test que no se hubiera ejecutado.
- [x] No hay requerimiento (funcional o no funcional) que no se haya verificado.

---

## Ejercicio 2: Métricas de Fase, Contención (PCE) y Densidad de Defectos

### 2.1. Eficacia de Contención en Fase (Phase Containment Effectiveness - PCE)

De acuerdo con el modelo expuesto por el Dr. Colla (slide 9 de *Procesos de Calidad*), el PCE mide la capacidad de una fase para capturar y contener defectos antes de que escapen a las etapas subsiguientes:

$$PCE_k = \frac{\text{Defectos detectados en la fase } k}{\text{Defectos totales observados}} \times 100\%$$

Asumiendo como universo total el 100% de los defectos observados en el ciclo de vida del ejercicio ($D_{\text{total}} = 9$):

1. **Fase de Inspección (Sesiones $S_1$ y $S_2$):**
   - Defectos detectados: $4 + 2 = 6$ defectos.
   - $$PCE_{\text{Inspección}} = \frac{6}{9} \times 100\% = \mathbf{66.67\%}$$

2. **Fase de Test Unitario (Sesión $S_3$):**
   - Defectos detectados: $2$ defectos.
   - $$PCE_{\text{Unitario}} = \frac{2}{9} \times 100\% = \mathbf{22.22\%}$$

3. **Fase de Test Funcional (Sesión $S_5$):**
   - Defectos detectados: $1$ defecto.
   - $$PCE_{\text{Funcional}} = \frac{1}{9} \times 100\% = \mathbf{11.11\%}$$

*Conclusión del PCE:* La inspección estática temprana contuvo el **66.67%** de los defectos, corroborando la regla fundamental de calidad: *"remover defectos en etapas tempranas evita el multiplicador exponencial de costos en etapas posteriores"*.

---

### 2.2. Densidad de Defectos al Inicio del Test

- Tamaño original del programa: $S = 18 \text{ LOCs}$.
- Defectos totales detectados: $\mu_0 = 9 \text{ defectos}$.
- Densidad de defectos inicial ($\delta_0$):
  $$\delta_0 = \frac{\mu_0}{S} = \frac{9}{18} = \mathbf{0.50 \text{ defectos/LOC}} \quad (500 \text{ def/KLOC})$$

*Interpretación:* Una densidad de 0.50 def/LOC refleja un código preliminar con severos vicios de codificación inicial, justificando el proceso riguroso de V&V aplicado.

---

## Ejercicio 3: Metodología Kanban y el Parámetro TEP (Álvaro Ruiz de Mendarozqueta)

Con base en el tutorial *"Kanban para uso genérico"* (Marzo 2015) del **Ing. Álvaro Ruiz de Mendarozqueta**:

### 3.1. Significado del Parámetro TEP
El parámetro **TEP** significa **Trabajo En Progreso**, siendo la traducción y formalización al español del término estándar **WIP** (*Work In Progress*).  
En el marco de la metodología visual Kanban, el TEP representa la **cantidad de tareas o tarjetas de trabajo que se encuentran simultáneamente en ejecución activa** en un estado determinado del proceso (principalmente en la columna *"Trabajando"* o en cualquiera de los subprocesos de la cadena de valor).

---

### 3.2. Significado Crítico en su Utilización
El rol del TEP es el pilar operativo y matemático de Kanban, fundamentado formalmente en la **Ley de Little**:

$$\text{Plazo de ejecución (Lead Time)} = \frac{\text{Trabajo En Progreso (TEP)}}{\text{Rendimiento (Throughput)}}$$

$$\text{Lead Time} = \frac{\text{W.I.P.}}{\text{Throughput}}$$

La criticidad de fijar un **límite explícito al TEP** (ejemplo: $TEP = 2$) radica en los siguientes aspectos estructurales:
1. **Control Determinista del Tiempo de Entrega:** Como se desprende de la Ley de Little, si el trabajo en progreso se incrementa sin control, el plazo de ejecución (*Lead Time*) se alarga de forma directamente proporcional. Limitar el TEP es la única forma de garantizar tiempos de entrega cortos y predecibles.
2. **Transformación hacia un Sistema Pull:** Al establecer un límite de TEP en las columnas activas, las tareas nuevas sólo pueden ingresar cuando se libera cupo al completarse una tarea previa. Se elimina la sobreproducción y el inicio indiscriminado de actividades sin finalizar las anteriores (*"dejar de empezar y empezar a terminar"*).
3. **Evitar Multitarea y Procrastinación:** Reduce drásticamente la dispersión de esfuerzos, el costo de cambio de contexto y las tareas paralizadas a medio hacer.
4. **Visibilidad Inmediata de Cuellos de Botella:** Cuando una tarea se bloquea por factores internos o externos, el TEP de la etapa se satura rápidamente. Esto frena el flujo aguas arriba e impulsa a todo el equipo a concentrarse solidariamente en eliminar el impedimento para restablecer el ritmo de valor (mejora continua).

---

## Ejercicio 4: Modelos Dinámicos de Confiabilidad y Proyección de Defectos (Modelo de Musa)

### 4.1. Marco Teórico y Ecuaciones del Modelo

En el taller `Taller_Defectos.ipynb` del **Dr. Pedro E. Colla**, se analiza el Modelo Básico de Ejecución en el Tiempo de J. D. Musa (asimilable a modelos de Poisson no homogéneos - NHPP tipo Goel-Okumoto):

- **Tasa instantánea de aparición de defectos:**
  $$\lambda(t) = \lambda_0 e^{-\left(\frac{\lambda_0}{\mu_0}\right) t}$$
- **Defectos acumulados en función del tiempo de test continuo:**
  $$\mu(t) = \mu_0 \left(1 - e^{-\left(\frac{\lambda_0}{\mu_0}\right) t}\right)$$
- **Linealización para estimación de parámetros:**
  Tomando logaritmo natural sobre la tasa de defectos observados $d(t)$:
  $$\ln(d(t)) = \ln(\lambda_0) - \left(\frac{\lambda_0}{\mu_0}\right) t = b + m \cdot t$$
  donde:
  $$b = \ln(\lambda_0) \implies \lambda_0 = e^b$$
  $$m = -\frac{\lambda_0}{\mu_0} \implies \mu_0 = -\frac{\lambda_0}{m}$$

---

### 4.2. Calibración con el Dataset de la Guía (Días 0 a 6)

| Día ($t$) | Defectos Observados ($d$) | $\ln(d)$ | Defectos Acumulados |
|:---:|:---:|:---:|:---:|
| 0 | 9 | 2.1972 | 9 |
| 1 | 18 | 2.8904 | 27 |
| 2 | 5 | 1.6094 | 32 |
| 3 | 7 | 1.9459 | 39 |
| 4 | 23 | 3.1355 | 62 |
| 5 | 2 | 0.6931 | 64 |
| 6 | 8 | 2.0794 | 72 |

Aplicando regresión por mínimos cuadrados mediante `taller_defectos_collatz.py`:
- Pendiente de regresión ($m$): **$-0.115062$**
- Ordenada al origen ($b$): **$2.423905$**
- Intensidad de fallas inicial ($\lambda_0 = e^b$): **$11.2899 \text{ def/día}$**
- **Expectativa total de defectos ($\mu_0 = -\frac{\lambda_0}{m}$):** **$\mathbf{98.12 \text{ defectos}}$**
- Defectos observados a la fecha ($\sum \mu_i$): $72 \text{ defectos}$
- **Defectos remanentes latentes esperados:** $\mu_0 - 72 = \mathbf{26.12 \text{ defectos}}$

---

### 4.3. Calibración para el Software Collatz (Asimilando Día a Sesiones)

Tomando el dataset de sesiones de prueba de Collatz:
- Sesión 1: 4 defectos
- Sesión 2: 2 defectos
- Sesión 3: 2 defectos
- Sesión 4: 1 defecto
- Sesión 5: 1 defecto
- Total observado: $\sum \mu_i = 10 \text{ defectos}$

Resultados de la regresión de Musa:
- Pendiente ($m$): **$-0.346574$**
- Ordenada ($b$): **$1.594239$**
- Intensidad inicial ($\lambda_0$): **$4.9246 \text{ def/sesión}$**
- **Expectativa total de defectos ($\mu_0$):** **$\mathbf{14.21 \text{ defectos}}$**

#### Tamaño Final y Defectos Liberados:
- Tamaño final medido con comando equivalente a `cat collatz.py | wc -l`: **$82 \text{ LOCs}$**.
- Defectos "liberados" al finalizar el test ($\mu_r$):
  $$\mu_r = \mu_0 - \sum \mu_i = 14.21 - 10 = \mathbf{4.21 \text{ defectos}}$$
- Densidad final de defectos liberados en el código:
  $$\delta_{\text{final}} = \frac{\mu_r}{\text{LOCs}} = \frac{4.21}{82} = \mathbf{0.0513 \text{ def/LOC}} \quad (51.3 \text{ def/KLOC})$$

---

## Ejercicio 5: Marco para Evaluar Garantía y Efecto de Multas Contractuales

### 5.1. Comportamiento Cualitativo de Incrementar el PCE en el Tiempo Óptimo de Test

En el modelo de garantía de software expuesto por el Dr. Colla (slides 8 y 9 de *Garantía*):
- El costo total normalizado del ciclo de vida bajo garantía $C_t(\tau_r)$ es la suma del costo de testeo $C(\tau_r)$ y el costo esperado de atender las fallas durante el período de garantía contractual $\tau_w$, denotado $W(\tau_r)$:
  $$C_t(\tau_r) = C(\tau_r) + W(\tau_r)$$
  donde el resultado óptimo de liberación ocurre en:
  $$C_t = \min_{\tau_r} (C(\tau_r) + W(\tau_r)) \implies \frac{\partial C_t(\tau_r)}{\partial \tau_r} = 0$$

- **Comportamiento Cualitativo al Aumentar el PCE:**
  1. Un mayor PCE en las fases previas (requerimientos, análisis, arquitectura e inspección) incrementa la remoción temprana de defectos, lo que **disminuye la cantidad de defectos latentes que ingresan a la fase de prueba**.
  2. Al llegar menos defectos a la etapa de testeo, la curva de defectos acumulados se aplana y la intensidad de fallas $\lambda(t)$ disminuye con mayor celeridad.
  3. Para satisfacer una meta de confiabilidad dada y mitigar el costo de garantía en campo $W(\tau_r)$, **se requiere un tiempo total de testeo óptimo $(\tau_r^*)$ significativamente menor**.
  4. Como se aprecia en la lámina de sensibilidad $[\tau_r/\tau_0] = f(\tau_w, PCE)$, al pasar de $PCE = 0.5$ a $0.7$ y $0.9$, la curva de tiempo de test óptimo se desplaza hacia abajo: **a mayor PCE, menor es el tiempo y esfuerzo de testeo necesario para poder otorgar garantía con el mínimo costo total**.

---

### 5.2. Efecto de la Aplicación de una Multa al Punto de Equilibrio

De acuerdo a la lámina 10 de *Garantía* (*"Las multas incentivan a los proveedores a reducir los defectos pues encarece la garantía. Equivale a incrementar el costo de reparación"*):

- **Fundamentación Formal:**
  En el modelo de costos, el término de garantía $W(q)$ depende directamente del costo unitario de reparación de defectos en ambiente productivo ($C_3$):
  $$W(q) = C_3 \mu_0 \left[ (1 - e^{-\lambda_0 (\tau_r + \tau_w)}) - (1 - e^{-\lambda_0 \tau_r}) \right]$$
  La inclusión de una **multa o penalidad contractual** por falla en garantía equivale a sustituir $C_3$ por un costo incrementado $C_3' = C_3 + \text{Multa}$.

- **Desplazamiento del Punto de Equilibrio:**
  1. Al aumentar $C_3'$, la curva $W(\tau_r)$ se traslada hacia arriba y su pendiente negativa $-\frac{\partial W}{\partial \tau_r}$ se vuelve mucho más empinada para valores bajos y medios de $\tau_r$.
  2. En el balance marginal de costos:
     $$\frac{\partial C(\tau_r)}{\partial \tau_r} = -\frac{\partial W(\tau_r)}{\partial \tau_r}$$
     el costo marginal de continuar probando es contrarrestado por un ahorro marginal de garantía mucho más alto.
  3. Por consiguiente, la condición de mínimo costo total se satisface a un valor de tiempo de test **mayor**: **el punto de equilibrio óptimo $(\tau_r^*)$ se desplaza hacia la derecha**.
  4. La multa penaliza severamente la liberación prematura, obligando a la organización a prolongar el período de V&V en desarrollo para reducir los defectos escapados y proteger la viabilidad financiera del proyecto.

---

## Ejercicio 6: Línea de Base Organizacional y Dimensionamiento de V&V

### Premisas:
- Performance histórica organizacional: $PCE = 89\% = 0.89$.
- Densidad de defectos al momento de liberación: $\delta_r = 0.12 \text{ def/FP}$.
- Tamaño del proyecto recién construido: $S = 100 \text{ FP}$.

---

### 6.1. Expectativa de Defectos Totales ($\mu_0$)
Los defectos tolerables que escapan al momento de la entrega son:
$$D_r = S \times \delta_r = 100 \text{ FP} \times 0.12 \text{ def/FP} = 12 \text{ defectos}$$

Por definición de contención en fase, la fracción de defectos liberados corresponde a $(1 - PCE)$:
$$1 - PCE = \frac{D_r}{\mu_0} \implies \mu_0 = \frac{D_r}{1 - PCE} = \frac{S \times \delta_r}{1 - PCE}$$
$$\mu_0 = \frac{12}{1 - 0.89} = \frac{12}{0.11} = \mathbf{109.09 \text{ defectos} \approx 109 \text{ defectos}}$$

---

### 6.2. Densidad de Defectos al Finalizar Construcción ($\delta_0$)
$$\delta_0 = \frac{\mu_0}{S} = \frac{109.09 \text{ defectos}}{100 \text{ FP}} = \mathbf{1.0909 \text{ def/FP}}$$

---

### 6.3. Defectos a Planear Detectar Durante V&V
$$D_{V\&V} = \mu_0 \times PCE = 109.09 \times 0.89 = \mathbf{97.09 \text{ defectos} \approx 97 \text{ defectos}}$$
*(Comprobación: $D_{V\&V} = \mu_0 - D_r = 109.09 - 12 = 97.09$)*

---

### 6.4. Opinión Fundamentada ante la Detección de 60 Defectos en 3 Días

Si en los primeros 3 días de V&V se detectan **20 defectos diarios (60 defectos en total)**, esto representa el **$61.8\%$** de todos los defectos previstos para todo el ciclo de V&V ($60 / 97.09$).

**Fundamentación Técnica:**
1. **Comportamiento Anómalo respecto al Histórico:** El ritmo de detección inicial tan elevado indica que la densidad de defectos reales inyectados durante la construcción superó drásticamente la línea de base ($\delta_0 > 1.09$).
2. **Subestimación de $\mu_0$:** Si la curva de fallas aún se encuentra en su fase temprana (lejos de la asíntota de saturación), la expectativa real de defectos totales $\mu_0$ del proyecto es significativamente más alta que 109 defectos.
3. **Riesgo Inminente de Liberación:** Si se detiene el test al cumplir los días originalmente planificados, el número de defectos escapados superará con creces el límite contractual $\delta_r = 0.12$ def/FP, destruyendo el PCE.
4. **Decisión Gerencial Recomendada:** Es imperativo recalibrar de inmediato los parámetros del modelo dinámico de Musa con los datos observados de los días 1 a 3, aplicar una ventana de *Code Freeze*, y extender el calendario y recursos de V&V para capturar los defectos excedentes antes de autorizar el pase a producción.

---

## Ejercicio 7: Herramienta CLI `json2csv.py` y Marco de Integración Continua (CI/CD)

### 7.1. Características de Implementación de `json2csv.py`
El script [json2csv.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp11/json2csv.py) implementa una arquitectura modular de filtro:
- Invocación estándar: `python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}`.
- Si no se informa `-i`: lee fluidamente desde `sys.stdin`.
- Si no se informa `-o`: escribe en `sys.stdout`.
- Delimitador configurable con coma (`,`) por defecto.
- Gestión rigurosa de excepciones (`json.JSONDecodeError`, `ValueError`, `OSError`, `FileNotFoundError`).

### 7.2. Cumplimiento de Estándares de Calidad
- **Black & Ruff:** Formato automático consistente, sin errores de linting.
- **PEP8 y PEP257:** Nombres canónicos y docstrings completos validados con `pydocstyle` (0 observaciones).
- **Tipado Estático:** 0 errores en `mypy` y 0 errores en `pyright`.
- **Seguridad:** 0 observaciones de severidad en `bandit`.
- **Cobertura de Tests:** **$99\%$ de cobertura** con 20 pruebas automáticas en `test_json2csv.py`.

---

## Ejercicio 8: Deuda Técnica y Calidad en Ciclos Ágiles

Conforme a la presentación del Dr. Pedro Colla (*"Agile and software engineering, an invisible bond"*):

### 8.1. Factores Gestionados desde Calidad que Mejoran la Deuda Técnica
1. **Contención en Fase (PCE):** La calidad gobierna la generación de **deuda técnica involuntaria**. Un $PCE \ge 80\%$ previene que los defectos se escapen del sprint y se conviertan en deuda mandatoria con precedencia sobre las nuevas historias de usuario.
2. **Costo de Pobre Calidad (CoPQ):** El modelado de escenarios económicos demuestra que mantener el $CoPQ \le 18\%$ protege el valor operativo adicional (OPV) aportado por la agilidad.
3. **Capacidad Asignada a Refactoring ($r$):** La gestión de calidad exige reservar una fracción del sprint $R_k = r V_k$ que debe superar la frontera de bancarrota técnica:
   $$r > \frac{\alpha}{\alpha + 1 - \beta}$$
4. **Reducción de Tasas de Inyección ($\alpha$) y Retrabajo ($\beta$):** Prácticas preventivas (análisis estático, TDD, revisiones de pares) reducen la inyección de defectos sobre nuevas funciones ($\alpha$) y sobre las correcciones previas ($\beta$).

---

### 8.2. Por Qué Producen esa Mejora
En la realidad del desarrollo de software, la velocidad del equipo no es constante sino que se deteriora por el stock de deuda acumulada:

$$V_k = \frac{V_0}{1 + \gamma D_k}$$

Si no se gestiona el PCE y se omite el refactoring, la deuda técnica $D_k$ diverge. El equipo cae en una condición destructiva denominada **equilibrio de "trashing"**:
$$D = \frac{\alpha}{1 - \beta + \alpha} V$$
donde todo el tiempo del sprint se consume en apagar incendios y resolver defectos viejos, haciendo que la entrega de funcionalidad nueva se anule ($N_k \to 0$). La gestión formal de calidad preserva la velocidad efectiva, minimiza los sprints de estabilización ($S_{clean}$) y garantiza la viabilidad presupuestaria y temporal del proyecto.
