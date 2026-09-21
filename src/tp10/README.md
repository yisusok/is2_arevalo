# TP10: Administración de Proyectos (Gestión)

**Asignatura:** Ingeniería de Software II  
**Docente:** Dr. Pedro E. Colla  
**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  
**Ubicación de Resolución y Documentación:** `src/tp10/`

> **Nota de Alineación Académica:** Las respuestas, derivaciones matemáticas y análisis conceptuales presentados en este documento han sido elaborados conforme al marco teórico, modelos sistémicos, formulaciones y láminas de las clases dictadas por el **Dr. Pedro E. Colla** (*"Monitoreo y Control"*, *"Gestión de Configuración"*, *"Fábrica de Software"*, *"Calendarización y Gestión de Riesgos"*, y *"Planeamiento Financiero"*).

---

## Tabla de Contenidos

1. [Ejercicio 1: Ingeniería Financiera de un Proyecto de Software](#ejercicio-1-ingeniería-financiera-de-un-proyecto-de-software)
2. [Ejercicio 2: Desafíos de Negocio y Equilibrio Financiero](#ejercicio-2-desafíos-de-negocio-y-equilibrio-financiero)
3. [Ejercicio 3: Análisis de la Fórmula de Calendarización Unipersonal](#ejercicio-3-análisis-de-la-fórmula-de-calendarización-unipersonal)
4. [Ejercicio 4: Estimación de Duración en Estructuras Secuenciales Monótonas](#ejercicio-4-estimación-de-duración-en-estructuras-secuenciales-monótonas)
5. [Ejercicio 5: Retraso Inexorable en Tareas del Camino Crítico](#ejercicio-5-retraso-inexorable-en-tareas-del-camino-crítico)
6. [Ejercicio 6: Inconveniencia de Acelerar Actividades con Margen $\neq 0$](#ejercicio-6-inconveniencia-de-acelerar-actividades-con-margen-neq-0)
7. [Ejercicio 7: Inviabilidad de Reducción del 50% mediante Clocking](#ejercicio-7-inviabilidad-de-reducción-del-50-mediante-clocking)
8. [Ejercicio 8: Imposibilidad de la Consigna "Cero Cambios"](#ejercicio-8-imposibilidad-de-la-consigna-cero-cambios)
9. [Ejercicio 9: Evaluación de Plan de Contingencia por Riesgo Sísmico en UADER](#ejercicio-9-evaluación-de-plan-de-contingencia-por-riesgo-sísmico-en-uader)
10. [Ejercicio 10: Razón Principal para la Transferencia de Riesgos](#ejercicio-10-razón-principal-para-la-transferencia-de-riesgos)
11. [Ejercicio 11: Control del Trabajo vs. Control de Trabajadores Individuales](#ejercicio-11-control-del-trabajo-vs-control-de-trabajadores-individuales)
12. [Ejercicio 12: Evaluación de GitHub para la Gestión de Configuración](#ejercicio-12-evaluación-de-github-para-la-gestión-de-configuración)
13. [Ejercicio 13: Fábrica de Software vs. Equipo Convencional de Desarrollo](#ejercicio-13-fábrica-de-software-vs-equipo-convencional-de-desarrollo)
14. [Ejercicio 14: Partición de Actividades, PERT/CPM y Nivelación de Recursos](#ejercicio-14-partición-de-actividades-pertcpm-y-nivelación-de-recursos)

---

## Archivos de Código y Notebook Asociados

Para la resolución automatizada, simulación numérica y generación de gráficos interactivos de este trabajo práctico, se crearon los siguientes archivos ejecutables dentro de `src/tp10/`:

- [ejercicio1_finanzas.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp10/ejercicio1_finanzas.py): Script en Python para la resolución analítica completa de las partes a, b, c, d, e, f del Ejercicio 1.
- [ejercicio2_escenarios.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp10/ejercicio2_escenarios.py): Script en Python para el cálculo de neutralidad financiera y flujos en los escenarios del Ejercicio 2.
- [ejercicio14_caminocritico.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp10/ejercicio14_caminocritico.py): Script en Python que ejecuta el método CPM (forward/backward pass) y la nivelación de recursos para 2 personas del Ejercicio 14.
- [create_notebook.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp10/create_notebook.py): Script para la generación programática del cuaderno Jupyter Notebook.
- [TP10_Gestion.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp10/TP10_Gestion.ipynb): Jupyter Notebook interactivo con explicaciones, código ejecutable y visualizaciones (curvas de NPV y diagrama Gantt comparativo).

---

## Ejercicio 1: Ingeniería Financiera de un Proyecto de Software

### Premisa:
- Inversión requerida: $\$1000$ por mes durante 12 meses (pago mensual vencido).
- Retorno de activos subyacentes: Al mes 12 finaliza el proyecto y genera un flujo cuyo Valor Presente en dicho momento es $PV_{12} = \$18,000$.
- Tasa de descuento: Tasa efectiva mensual $r = 1\% = 0.01$.

---

### a. Valor Presente Neto (NPV) en Ejecución Nominal (12 Meses)

#### Modelo Matemático de Flujo Descontado de Caja (DCF):
El Valor Presente de los Costos ($PV_{\text{costos}}$) para 12 egresos mensuales vencidos de $\$1000$ se calcula como:
$$PV_{\text{costos}} = \sum_{t=1}^{12} \frac{1000}{(1+0.01)^t} = 1000 \times \frac{1 - (1.01)^{-12}}{0.01} = 1000 \times 11.255078 = \$11,255.08$$

El Valor Presente de los Beneficios ($PV_{\text{beneficio}}$) descontado al momento actual ($t=0$) es:
$$PV_{\text{beneficio}} = \frac{18,000}{(1.01)^{12}} = 18,000 \times 0.887449 = \$15,974.09$$

El Valor Presente Neto ($NPV$) del proyecto planificado resulta:
$$NPV_{\text{plan}} = PV_{\text{beneficio}} - PV_{\text{costos}} = 15,974.09 - 11,255.08 = \mathbf{\$4,719.01}$$

---

### b. NPV en Escenario Retrasado 3 Meses (Total 15 Meses)

Si la ejecución se extiende 3 meses manteniendo el costo mensual de $\$1000$:
$$PV_{\text{costos, 15m}} = \sum_{t=1}^{15} \frac{1000}{(1.01)^t} = 1000 \times \frac{1 - (1.01)^{-15}}{0.01} = 1000 \times 13.865053 = \$13,865.05$$

Los beneficios subyacentes se reciben recién en el mes 15:
$$PV_{\text{beneficio, 15m}} = \frac{18,000}{(1.01)^{15}} = 18,000 \times 0.861349 = \$15,504.28$$

El nuevo NPV es:
$$NPV_{\text{15m}} = 15,504.28 - 13,865.05 = \mathbf{\$1,639.24}$$

---

### c. Análisis de Rentabilidad

De acuerdo con la consigna, la rentabilidad se calcula como $\text{Rentabilidad} = \frac{NPV}{PV_{\text{costos}}}$:

1. **Caso Planificado (12 meses):**
   $$\text{Rentabilidad}_{\text{plan}} = \frac{4,719.01}{11,255.08} = 0.419279 \implies \mathbf{41.93\%}$$

2. **Caso Retrasado (15 meses):**
   $$\text{Rentabilidad}_{\text{15m}} = \frac{1,639.24}{13,865.05} = 0.118228 \implies \mathbf{11.82\%}$$

**Conclusión:** Un retraso del $25\%$ en el plazo calendario (de 12 a 15 meses) provoca una caída drástica de la rentabilidad de **30.11 puntos porcentuales** (una reducción relativa del $71.8\%$).

---

### d. Impacto Financiero de un Retraso de 6 Meses (Total 18 Meses)

Si la entrega del proyecto se retrasa 6 meses:
- $PV_{\text{costos, 18m}} = 1000 \times \frac{1 - (1.01)^{-18}}{0.01} = 1000 \times 16.398268 = \$16,398.27$
- $PV_{\text{beneficio, 18m}} = \frac{18,000}{(1.01)^{18}} = 18,000 \times 0.836017 = \$15,048.31$
- $NPV_{\text{18m}} = 15,048.31 - 16,398.27 = \mathbf{-\$1,349.96}$
- $\text{Rentabilidad}_{\text{18m}} = \frac{-1,349.96}{16,398.27} = \mathbf{-8.23\%}$

**Análisis de Impacto:**  
Un retraso de 6 meses **destruye completamente el valor del proyecto**, transformando un proyecto altamente rentable ($NPV = +\$4,719.01$) en un proyecto con **pérdida neta destructora de capital ($NPV < 0$)**. La pérdida absoluta de valor en comparación con el plan original asciende a **$\$6,068.97$**.

---

### e. Análisis Financiero de la Gestión Profesional del Proyecto

Suponga que se contrata un Project Manager (PM) certificado que garantiza el cumplimiento estricto del calendario de 12 meses agregando un sobrecosto del $5\%$ mensual ($\$1050$/mes):

- Nuevo $PV_{\text{costos, PM}} = 1050 \times 11.255078 = \$11,817.83$
- $PV_{\text{beneficio}} = \$15,974.09$
- $NPV_{\text{PM}} = 15,974.09 - 11,817.83 = \mathbf{\$4,156.25}$
- $\text{Rentabilidad}_{\text{PM}} = \frac{4,156.25}{11,817.83} = \mathbf{35.17\%}$

#### Comparación de Conveniencia Financiera:
- **Sin PM certificado (retardado a 15 meses por desvío típico):** $NPV = \$1,639.24$.
- **Con PM certificado (garantiza 12 meses):** $NPV = \$4,156.25$.
- **Beneficio Neto de Contratar Gestión Profesional:**  
  $$\Delta NPV = 4,156.25 - 1,639.24 = \mathbf{+\$2,517.01}$$

**Dictamen Financiero:**  
Es **ALTAMENTE CONVENIENTE** implementar una gestión profesional del proyecto. La compra de "certeza de calendario" por un costo adicional de $\$562.75$ en $PV$ evita una pérdida por valor del tiempo y sobrecostos de $\$3,079.77$ producida por un retraso de 3 meses.

---

### f. [Desafío] Máximo Costo Mensual Aceptable para 15 Meses conservando el NPV Objetivo

Si resulta inevitable extender el proyecto a 15 meses, pero el inversor exige conservar el NPV originalmente planeado ($NPV_{\text{objetivo}} = \$4,719.01$):

El $PV$ de beneficios a 15 meses es $PV_{\text{beneficio, 15m}} = \$15,504.28$.  
El $PV$ máximo de costos permitido es:
$$PV_{\text{costos, máximo}} = PV_{\text{beneficio, 15m}} - NPV_{\text{objetivo}} = 15,504.28 - 4,719.01 = \$10,785.27$$

Dado que el factor de descuento acumulado para 15 meses al $1\%$ es $\sum_{t=1}^{15} (1.01)^{-t} = 13.865053$:
$$C_{\text{máx}} = \frac{10,785.27}{13.865053} = \mathbf{\$777.88 / \text{mes}}$$

**Conclusión:**  
Para neutralizar la pérdida financiera por el retraso de 3 meses y mantener la utilidad del plan original, el costo mensual del proyecto debe reducirse de $\$1000$ a **$\$777.88$** (un recorte presupuestario del **$22.21\%$**).

---

## Ejercicio 2: Desafíos de Negocio y Equilibrio Financiero

### Datos Base:
- Plazo técnico de construcción: 12 meses. Staff técnico: $\$1000$/mes.
- Costo de oportunidad ($r$): $1\%$ TEM (tanto para proveedor como patrocinante).
- Pago contractual acordado a la entrega ($t=12$): $\$14,000$.

#### Línea de Base Financiera del Proveedor:
- $PV_{\text{costos, base}} = 1000 \times \frac{1 - (1.01)^{-12}}{0.01} = \$11,255.08$
- $PV_{\text{ingresos, base}} = \frac{14,000}{(1.01)^{12}} = \$12,424.29$
- **Ganancia Neta Presente del Proveedor ($NPV_{\text{prov, base}}$):**  
  $$NPV_{\text{prov, base}} = 12,424.29 - 11,255.08 = \mathbf{\$1,169.21}$$

---

### a. Pago Diferido a Mes 14 (Retraso de Caja del Patrocinante)

- El proveedor mantiene el equipo 12 meses (costo total constante).
- Para que el cambio sea **financieramente neutro** para el proveedor, el Valor Presente del pago en el mes 14 debe ser exactamente igual al Valor Presente del ingreso de la línea de base ($PV = \$12,424.29$):
  $$P_{14} = PV_{\text{ingresos, base}} \times (1.01)^{14} = 14,000 \times (1.01)^2 = 14,000 \times 1.0201 = \mathbf{\$14,281.40}$$

**Respuesta:** El patrocinante deberá pagar **$\$14,281.40$** en el mes 14 para compensar el costo financiero de 2 meses de diferimiento al $1\%$ TEM.

---

### b. Entrega Acelerada en Mes 6 con Pago Mantenido en Mes 12

- El proveedor trabaja únicamente durante 6 meses:
  $$PV_{\text{costos, 6m}} = sum_{t=1}^6 \frac{1000}{(1.01)^t} = 1000 \times \frac{1 - (1.01)^{-6}}{0.01} = \$5,795.48$$
- Para mantener la neutralidad financiera (misma ganancia neta en $t=0$, $NPV = \$1,169.21$), el Valor Presente que debe recibir el proveedor es:
  $$PV_{\text{ingreso requerido}} = 5,795.48 + 1,169.21 = \$6,964.69$$
- Llevado al mes 12:
  $$P_{12, \text{ajustado}} = 6,964.69 \times (1.01)^{12} = \mathbf{\$7,847.98}$$

**Respuesta:** El patrocinante deberá pagar **$\$7,847.98$** en el mes 12. Esto representa un descuento de $\$6,152.02$ a favor del patrocinante debido a la reducción del esfuerzo del equipo de 12 a 6 meses.

---

### c. Entrega en Mes 6 con Pago en Mes 6

- Manteniendo la neutralidad financiera ($PV_{\text{ingreso requerido}} = \$6,964.69$ a $t=0$):
- Llevado al mes 6:
  $$P_{6} = 6,964.69 \times (1.01)^6 = \mathbf{\$7,393.16}$$

**Respuesta:** En caso de abonarse inmediatamente a la entrega en el mes 6, el patrocinante deberá desembolsar **$\$7,393.16$**.

---

## Ejercicio 3: Análisis de la Fórmula de Calendarización Unipersonal

### Consigna:
¿Por qué la relación de calendarización siguiente es sólo válida para un equipo unipersonal?
$$D(\text{días}) = \frac{\text{Esfuerzo}(\text{Staff-Horas})}{\text{Horas-Día / Persona}} \times \frac{1}{\text{Staff}}$$

### Resolución y Justificación Teórica:
Esta fórmula asume una **escalabilidad perfectamente lineal** de la productividad del trabajo respecto de la cantidad de personas agregadas.

De acuerdo con el marco teórico del Dr. Pedro E. Colla (Lámina 19 de *Calendarización y Gestión de Riesgos*) y la **Ley de Brooks** (*"Agregar personas a un proyecto de software retrasado lo retrasa más"*):

1. **Fricción de Comunicación:** En equipos multipersona ($N > 1$), se generan canales interpersonales de comunicación que crecen según la relación combinatoria $C = \frac{N(N-1)}{2}$. El tiempo invertido en reuniones, sincronización y traspaso de información no produce código directamente.
2. **Indivisibilidad de Tareas:** Las actividades de desarrollo poseen dependencias y cotas de paralelismo técnico que impiden subdividirlas infinitamente entre más desarrolladores.
3. **Pérdidas por Coordinación e Inducción:** El esfuerzo consumido en incorporar y alinear personal dispersa la productividad promedio por persona.

Por lo tanto, la ecuación $D = \frac{E}{H} \cdot \frac{1}{\text{Staff}}$ ignora por completo el sobrecosto de comunicación y coordinación, siendo **matemáticamente válida únicamente cuando $\text{Staff} = 1$**.

---

## Ejercicio 4: Estimación de Duración en Estructuras Secuenciales Monótonas

### Consigna:
¿Por qué la estimación de duración para proyectos dada por la fórmula $\tau_{\text{proyecto}} = \sum_{i=1}^N \tau_i$ es sólo válida en proyectos triviales cuya estructura de tareas es secuencial monótona?

### Resolución conforme a la teoría del Dr. Pedro E. Colla:
En las láminas del curso (Lámina 21 de *Calendarización*):
- La suma aritmética lineal $\sum_{i=1}^N \tau_i$ asume que la red de actividades posee una **topología estrictamente serial** ($A_1 \to A_2 \to \dots \to A_N$), donde la tarea $i+1$ comienza indefectiblemente cuando finaliza la tarea $i$, sin concurrencia ni ramificaciones.

En proyectos reales de software:
1. Las tareas se ejecutan en **redes complejas de actividades** (diagramas de precedencia PERT/CPM) con caminos paralelos y holguras dispares.
2. La duración real del proyecto no depende de la suma de todas las tareas, sino exclusivamente del **Camino Crítico**:
   $$\tau_{\text{proyecto}} = \max_k \left( \sum_{i \in \text{Camino}_k} \tau_i \right)$$
3. Sumar aritméticamente todas las tareas sobreestima groseramente la duración real, ya que ignora el trabajo ejecutado simultáneamente en ramificaciones paralelas.

---

## Ejercicio 5: Retraso Inexorable en Tareas del Camino Crítico

### Consigna:
Elabore conceptualmente en la razón por la cual retrasar una tarea del camino crítico de un proyecto (tareas con margen $= 0$) retrasa al mismo inexorablemente.

### Resolución Teórica:
El **Camino Crítico** se define como el camino continuo más largo a través de la red de actividades que conecta el inicio con el fin del proyecto (Láminas 29 y 30 de *Calendarización*).

- Las tareas que pertenecen al camino crítico poseen **Holgura o Margen nulo** ($\text{Margen} = LS - ES = LF - EF = 0$).
- La holgura representa el tiempo máximo que una tarea puede deslizarse sin alterar la fecha final de entrega.
- Al tener $\text{Margen} = 0$, **no existe colchón ni amortiguador temporal** que pueda absorber una desviación.

Por lo tanto, cualquier demora $\Delta t > 0$ sufrida en una tarea crítica desplaza la fecha de inicio temprano ($ES$) de todas las tareas subsiguientes en ese camino, trasladando íntegramente la demora $\Delta t$ al hito de finalización del proyecto.

---

## Ejercicio 6: Inconveniencia de Acelerar Actividades con Margen $\neq 0$

### Consigna:
¿Cuál es la razón por la cual no es conveniente agregar recursos para acelerar una actividad en un proyecto si la misma tiene un margen $\neq 0$?

### Resolución Teórica:
Siguiendo las premisas de gestión (Láminas 29 a 31 de *Calendarización*):
1. **Falta de Impacto en la Duración Total:** Las actividades no críticas poseen holgura ($\text{Margen} > 0$). Reducir la duración de una tarea no crítica consume recursos pero **no comprime el camino crítico**, por lo que la fecha de finalización del proyecto permanece inalterada.
2. **Sobrecosto e Ineficiencia Financiera:** Asignar desarrolladores adicionales o pagar horas extras en caminos no críticos destruye valor económico al incurrir en gastos que no agregan reducción de plazo.
3. **Incremento Innecesario de Fricción:** Aumenta la complejidad de coordinación y comunicación del equipo sin beneficio de calendario.

**Conclusión:** Los esfuerzos y recursos de aceleración deben enfocarse **exclusivamente en las tareas del camino crítico**.

---

## Ejercicio 7: Inviabilidad de Reducción del 50% mediante Clocking

### Consigna:
Si le sugirieran reducir el calendario de un proyecto en un 50% utilizando únicamente la técnica de clocking, ¿cree que es viable? Justifique.

### Resolución conforme a la teoría del Dr. Pedro E. Colla:
De acuerdo con las láminas de la materia (Lámina 20 de *Calendarización*):
- **Clocking** se define como la alteración del ritmo de trabajo imponiendo jornadas extendidas, sobretiempos y trabajo en fines de semana.

**Respuesta: NO ES VIABLE.** Justificación teórico-empírica:

1. **Efecto Corto Plazo vs. Desvío Sistémico:** El *clocking* solo es efectivo como medida táctica puntual en "épicas cortas" o cierres de sprint (*crunch time*). No puede sostenerse durante el desarrollo regular.
2. **Degradación Exponencial de Productividad:** La sobrecarga prolongada provoca fatiga extrema, *burnout* y un incremento exponencial en la tasa de errores (Costo de Mala Calidad - $CoPQ$). El tiempo ganado en horas extras se pierde completamente corrigiendo defectos y retrabajos.
3. **Límites Físicos de Compresión (Zona Imposible de Boehm):** Las investigaciones empíricas en ingeniería de software demuestran que la compresión máxima alcanzable por aceleración de ritmo está acotada a un **$\sim 20\text{-}25\%$**. Exigir un $50\%$ mediante *clocking* conduce al colapso del proyecto y a la renuncia del personal.

---

## Ejercicio 8: Imposibilidad de la Consigna "Cero Cambios"

### Consigna:
Un proyecto que tiene fuertes restricciones financieras que se traducen en un calendario objetivo muy agresivo y estricto ¿puede apelar a la implementación de una consigna de “cero cambios”? Justifique.

### Resolución Teórica:
Conforme a las láminas de la materia (Lámina 36 de *Control de Cambios* y Lámina 3 de *Monitoreo y Control*):

> *"Un proyecto típico experimenta entre un 20% y un 40% de cambios en requerimientos debido a la volatilidad de negocios, comprensión del proceso y evolución tecnológica."*
> *"Lo que no se gestione ocurrirá de todas formas, solo que con impactos negativos."*

**Respuesta: NO PUEDE APELAR A "CERO CAMBIOS".** Justificación:
1. **Ineludibilidad del Cambio:** Los cambios en el software son sistémicos. Prohibirlos no evita su aparición; solo provoca que las desviaciones emerjan clandestinamente como **deuda técnica, defectos no documentados o productos desalineados** que fracasan en las pruebas de aceptación.
2. **Destrucción de Valor:** Un producto congelado arbitrariamente que no satisface las necesidades reales del negocio carece de valor financiero ($NPV < 0$).
3. **Mecanismo Correcto:** Ante calendarios y presupuestos estrictos, no se impone "cero cambios", sino un estricto **Comité de Control de Cambios (CCB)** y la técnica de **intercambio de alcance** en backlog (re-priorización ágil: ingresar un cambio requiere retirar una funcionalidad de equivalente esfuerzo).

---

## Ejercicio 9: Evaluación de Plan de Contingencia por Riesgo Sísmico en UADER

### Consigna:
Cuando esté planeando un proyecto a ejecutar en la sede Concepción del Uruguay de UADER. ¿Consideraría un plan de contingencia para recuperación de días perdidos en un proyecto debido a actividad sísmica? Justifique utilizando el marco teórico, no usando creencias o percepciones subjetivas.

### Resolución conforme a la teoría del Dr. Pedro E. Colla:
En la teoría de Gestión Formal de Riesgos (Láminas 4 a 8 de *Gestión de Riesgos*):

- El impacto esperado de un riesgo se modela formalmente como:
  $$V(x) = \mathcal{E}[\Delta V] = \sum_{i=1}^N I(x_i) \cdot P(x_i)$$
- Criterio de Selección de Riesgos (Lámina 6): *"Solo deben considerarse riesgos cuya magnitud de impacto sea significativo ($V(x) \gg 0$)."*
- Principio de Conservación de Valor (Lámina 8): *"Todo gasto emergente en gestionar un riesgo destruye valor por su parte."*

#### Análisis Científico-Geográfico:
La sede Concepción del Uruguay (Provincia de Entre Ríos, Argentina) está clasificada por el Instituto Nacional de Prevención Sísmica (INPRES) en la **Zona 0 (Sismicidad Muy Baja / Despreciable)**. La probabilidad de ocurrencia de un terremoto destructivo es prácticamente nula ($P(x) \approx 0$).

Por consiguiente, $V(x) = I(x) \cdot P(x) \approx 0$. 

**Dictamen:** Asignar fondos presupuestarios o días de contingencia para este evento destruye valor del proyecto de forma inútil. La estrategia metodológica correcta es **Aceptar / Ignorar el riesgo**.

---

## Ejercicio 10: Razón Principal para la Transferencia de Riesgos

### Consigna:
¿Cuál cree es la principal razón que hace deseable transferir un riesgo en vez de intentar solucionarlo o mitigarlo?

### Resolución Teórica:
Siguiendo los principios de Gestión Financiera de Riesgos (Láminas 6 a 8 de *Gestión de Riesgos*):

- **Razón Principal:** Transferir un riesgo (vía seguros, contratos a precio fijo o subcontratación con SLAs) es deseable cuando el **costo interno de mitigarlo o solucionarlo supera el costo de la prima de transferencia**, o cuando el impacto del riesgo es muy alto pero escapa al control operativo del equipo de proyecto.
- **Ventaja de Negocio:** La transferencia acota la responsabilidad financiera máxima a un monto fijo conocido (la prima o tarifa del tercero), eliminando la volatilidad del peor escenario y preservando el perfil de riesgo aceptable del proyecto.

---

## Ejercicio 11: Control del Trabajo vs. Control de Trabajadores Individuales

### Consigna:
¿Cuál es la razón, conceptual, detrás de la consigna de control de proyectos mediante la cual se debe controlar el trabajo del equipo y no a los trabajadores individuales?

### Resolución conforme a la teoría del Dr. Pedro E. Colla:
Lámina 4 de *Monitoreo y Control*:

> *"Principios Fundamentales: Lo que se controla es el trabajo, no los trabajadores. Utilizar control personal distorsiona las métricas. El control se debe basar en trabajos terminados y entregables concretos."*

### Razón Conceptual:
1. **Evitar la Distorsión de Métricas:** El control sobre trabajadores individuales induce la manipulación de reportes (efecto "90-90", donde una tarea está al 90% durante el 90% del tiempo) y fomenta comportamientos defensivos u optimizaciones locales engañosas (ej. inflar horas o líneas de código).
2. **Naturaleza Colaborativa del Software:** El desarrollo es un proceso cognitivo complejo y colectivo. El progreso real solo se verifica mediante la entrega de **entregables concretos y finalizados** (*Definition of Done*).
3. **Métrica Objetiva de Valor:** Centrarse en el trabajo finalizado permite medir métricas cuantitativas no distorsionadas (Velocidad, *Throughput*, *Burn-down*), alineando el monitoreo con el valor real entregado al proyecto.

---

## Ejercicio 12: Evaluación de GitHub para la Gestión de Configuración

### Consigna:
Evalúe si las funciones que ofrece GitHub satisfacen las necesidades requeridas para la gestión de configuración. Tabule y justifique.

### Evaluación Tabulada:

| Función de Gestión de Configuración (CM) | Herramienta / Función de GitHub | Grado de Cumplimiento | Justificación Teórica |
| :--- | :--- | :--- | :--- |
| **Identificación de Elementos (CI)** | Repositorios, Rutas de archivos, Git Hashing (SHA-1/256). | **Satisface Totalmente** | Permite identificar de forma unívoca cada elemento fuente (*source item*) y su árbol de dependencias mediante hashes criptográficos. |
| **Control de Versiones y Ramas** | Git Branching, Pull Requests (PR), Merge Strategies. | **Satisface Totalmente** | Soporta el aislamiento de cambios en ramas separadas, gestión de conflictos y fusión controlada (*branch & merge*). |
| **Líneas de Base (Baselines)** | Git Tags, GitHub Releases, Protected Branches. | **Satisface Totalmente** | Permite congelar versiones estables, marcar liberaciones de software e impedir modificaciones no autorizadas en ramas principales. |
| **Control de Cambios y Revisión** | PR Reviews, Code Owners, Branch Protection Rules. | **Satisface Totalmente** | Ofrece aprobación obligatoria por pares, análisis de impacto y trazabilidad formal previa a la integración del código. |
| **Reporte de Status y Auditoría** | Commit History, PR Traceability, Audit Logs, GitHub Insights. | **Satisface Totalmente** | Proporciona un registro inmutable de quién, cuándo y por qué modificó cada componente, satisfaciendo los requisitos de auditabilidad. |
| **Gestión de Construcción (Build)** | GitHub Actions (CI/CD Pipelines). | **Satisface Totalmente** | Automatiza la compilación, ejecución de tests unitarios, empaquetado y validación de criterios de salida del componente. |

**Conclusión:** GitHub satisface **de manera integral** los pilares requeridos por la disciplina formal de Gestión de Configuración (Láminas 37 a 41 de *Gestión de Configuración*).

---

## Ejercicio 13: Fábrica de Software vs. Equipo Convencional de Desarrollo

### Consigna:
¿En qué se diferencia un equipo de desarrollo operando bajo modalidad fábrica de software de un equipo convencional de desarrolladores participando en un proyecto?

### Cuadro Comparativo conforme a la teoría del Dr. Pedro E. Colla:
*(Basado en Láminas 47 a 51 de Fábrica de Software)*

| Dimensión de Análisis | Equipo bajo Modalidad Fábrica de Software | Equipo Convencional de Proyecto |
| :--- | :--- | :--- |
| **Alcance y Orientación** | Especializado en la **construcción masiva de componentes** de software estandarizados a partir de especificaciones técnicas rígidas. | Orientado de punta a punta al **producto y dominio del negocio** (requerimientos, diseño, desarrollo, despliegue). |
| **Insumos y Entregables** | Entradas: Especificaciones técnicas completas y arquitectura. Salidas: Código desarrollado con **Test Unitario estandarizado** y notas de instalación. | Entradas: Problemas de negocio e historias de usuario vagas. Salidas: Sistema funcional integral y valor de negocio. |
| **Estandarización de Procesos** | Procesos altamente formalizados y repetibles, acreditados bajo marcos rígidos (**ISO 9001/20000, CMMI**). | Procesos adaptables, frecuentemente ágiles (Scrum, Kanban) con alta flexibilidad de equipo. |
| **Estructura y Escala** | Estructuras permanentes con **gestión de banca (*bench*)** y capacidad de rampas de incorporación muy agresivas. | Equipo temporal armado *ad-hoc* para la duración específica del proyecto; se disuelve al finalizar. |
| **Ubicación y Modelo Operativo** | Frecuentemente externo, distribuido geográficamente (*Off-shore*, *Follow-the-sun*) para reducir costos. | Típicamente integrado, coubicado o en interacción directa con los *stakeholders* del proyecto. |

---

## Ejercicio 14: Partición de Actividades, PERT/CPM y Nivelación de Recursos

### Red de Actividades del Proyecto:

| Tarea ID | Tipo / Nombre | Duración ($\tau_i$) | Requisitos (Predecesoras) |
| :---: | :--- | :---: | :---: |
| **A** | Requerimientos | 5 días | Ninguno |
| **B** | Arquitectura | 3 días | A |
| **C** | Diseño | 10 días | A |
| **D** | Test cases | 20 días | A |
| **E** | Programa 1 | 5 días | B, C |
| **F** | Programa 2 | 6 días | B, C |
| **G** | Programa 3 | 7 días | B, C |
| **H** | Test F1 | 10 días | E, F, D |
| **I** | Test F2 | 9 días | G, D |
| **J** | System Test | 12 días | H, I |

---

### a. Análisis CPM con Recursos Infinitos

Ejecutando las pasadas adelante (*Forward Pass*) y atrás (*Backward Pass*) mediante el script [ejercicio14_caminocritico.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp10/ejercicio14_caminocritico.py):

#### Tabla de Tiempos y Holguras:

| Tarea ID | Duración | $ES$ (Inicio Temprano) | $EF$ (Fin Temprano) | $LS$ (Inicio Tardío) | $LF$ (Fin Tardío) | Holgura ($LS - ES$) | ¿En Camino Crítico? |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **A** | 5 | 0 | 5 | 0 | 5 | **0** | **SÍ** |
| **B** | 3 | 5 | 8 | 16 | 19 | 11 | No |
| **C** | 10 | 5 | 15 | 9 | 19 | 4 | No |
| **D** | 20 | 5 | 25 | 5 | 25 | **0** | **SÍ** |
| **E** | 5 | 15 | 20 | 20 | 25 | 5 | No |
| **F** | 6 | 15 | 21 | 19 | 25 | 4 | No |
| **G** | 7 | 15 | 22 | 19 | 26 | 4 | No |
| **H** | 10 | 25 | 35 | 25 | 35 | **0** | **SÍ** |
| **I** | 9 | 25 | 34 | 26 | 35 | 1 | No |
| **J** | 12 | 35 | 47 | 35 | 47 | **0** | **SÍ** |

#### Resultados (Recursos Infinitos):
- **Duración Total del Proyecto:** **47 días**
- **Camino Crítico (Holgura = 0):** **$A \to D \to H \to J$**  
  *(Verificación: $5 + 20 + 10 + 12 = 47$ días).*

---

### b. Nivelación de Recursos con Staff de 2 Personas

Asumiendo que se dispone de únicamente **2 personas** en el staff, que cada tarea requiere 1 persona y es indivisible:

#### Algoritmo de Nivelación Aplicado:
Se resuelven los conflictos de recursos en cada día $t$ priorizando tareas elegibles por:
1. Menor fecha de Inicio Tardío ($LS$).
2. Menor Holgura.

#### Cronograma Nivelado Resultante:

| Tarea ID | Duración | Inicio ($ST$) | Fin ($ET$) | Asignación de Recurso |
| :---: | :---: | :---: | :---: | :--- |
| **A** | 5 | 0 | 5 | Trabajador 1 |
| **D** | 20 | 5 | 25 | Trabajador 1 |
| **C** | 10 | 5 | 15 | Trabajador 2 |
| **B** | 3 | 15 | 18 | Trabajador 2 |
| **F** | 6 | 18 | 24 | Trabajador 2 |
| **G** | 7 | 24 | 31 | Trabajador 2 |
| **E** | 5 | 25 | 30 | Trabajador 1 |
| **H** | 10 | 30 | 40 | Trabajador 1 |
| **I** | 9 | 31 | 40 | Trabajador 2 |
| **J** | 12 | 40 | 52 | Trabajador 1 |

#### Resultados (Staff = 2 Personas):
- **Nueva Duración Total del Proyecto:** **52 días** (Retraso forzado por restricción de recursos de **+5 días** respecto del caso infinito).
- **Nuevo Camino Crítico Nivelado (Secuencia Restrictiva):**  
  $$\mathbf{A (0\text{-}5) \to C (5\text{-}15) \to B (15\text{-}18) \to F (18\text{-}24) \to E (25\text{-}30) \to H (30\text{-}40) \to J (40\text{-}52)}$$
  *(Las tareas D y G se ejecutan en paralelo aprovechando la capacidad del segundo recurso sin demorar la entrega final).*

---
