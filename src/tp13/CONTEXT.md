# CONTEXT.md: Registro de Contexto, Especificación y Trazabilidad del TP13

**Asignatura:** Ingeniería de Software II  
**Docente:** Dr. Pedro E. Colla  
**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  
**Alumno:** Jesús Arévalo  
**Módulo:** TP13 Estándar ISO 27000 (Seguridad de la Información y Gestión de Riesgos)  
**Ubicación:** `src/tp13/`  

---

## 1. Alcance y Objetivos de Ingeniería

El presente Trabajo Práctico (TP13) aborda de manera integral el estándar internacional **ISO/IEC 27000**, los Sistemas de Gestión de Seguridad de la Información (**SGSI** / **ISMS**), la evaluación cuali-cuantitativa de criticidad de activos y riesgos tecnológicos en entornos de Educación Superior Universitaria, el análisis de lecciones aprendidas en los procesos de recertificación hacia **ISO/IEC 27001:2022**, y el análisis económico-estratégico del **Caso de Estudio TIC** presentado por la cátedra.

El trabajo se estructura en seis ejes fundamentales:
1. **Relevamiento del Ecosistema Normativo ISO/IEC 27000:** Identificación exhaustiva de normas formantes, alcances, conceptos estructurales (SGSI, ciclo PDCA, tríada CIA, gobernanza) y análisis comparativo detallado entre las revisiones 2018 y 2022 (reestructuración del Anexo A, 4 temas, 93 controles, 11 controles nuevos y sistema de atributos).
2. **Evaluación de Criticidad de Activos de Información Universitaria:** Análisis de los activos y requerimientos de seguridad de estudiantes, docentes, entidades gubernamentales (CONICET/Ministerio) y proveedores de nube, fundamentados bajo la Ley Nacional de Protección de Datos Personales N° 25.326 y normativas académicas.
3. **Evaluación SGSI de Educación Superior en Modalidad Remota/Virtual:** Desglose sistemático de actores, procesos académicos y administrativos, herramientas tecnológicas, tipología de información protegida, principales amenazas/vulnerabilidades y mapa de controles recomendados.
4. **Matriz y Evaluación de Riesgo con Mapa de Calor:** Evaluación cuantitativa de los 5 escenarios provistos (R-01 a R-05) utilizando escalas paramétricas de Probabilidad (1 a 5) e Impacto (1 a 5), cálculo de riesgo inherente y residual tras la aplicación de salvaguardas (BRS, WAF/Firewall, 2FA+DMARC, UPS+generador, RBAC+DLP), y clasificación frente a los umbrales de apetito de riesgo ($\le 6$ aceptable, $7-12$ tolerable con PTR, $\ge 15$ inaceptable).
5. **Lecciones Aprendidas en la Transición a ISO 27001:2022:** Síntesis técnica de las observaciones y errores comunes documentados por URM Consulting y BSI (Declaración de Aplicabilidad, desfase de cronogramas, cláusulas críticas 6.3, 6.2, 8.1, 9.3 y controles 5.7 y 8.11).
6. **Análisis Integral del Caso de Estudio TIC:** Diagnóstico del estado inicial de madurez, cuantificación del GAP analysis, desglose técnico de los 13 proyectos de mejora (PR01 a PR13), análisis económico de inversiones de implementación (401.760 €) y mantenimiento (167.000 €), cronograma temporal y fundamentación estratégica de la hoja de ruta.

---

## 2. Alineación Curricular y Académica

El desarrollo de este trabajo práctico se fundamenta directamente en el marco conceptual y las directivas pedagógicas impartidas por el **Dr. Pedro E. Colla** en el material de cátedra de *Ingeniería de Software II*, específicamente en los módulos:
- **Seguridad de la Información (Teoría y Fundamentos):** Conceptos de información como activo en la cadena de valor, seguridad lógica vs. física, amenazas pasivas vs. activas, fases de un ciberataque, dimensiones CIA, no repudio, autenticación, políticas de seguridad corporativas y planes de contingencia (Evaluación, Planificación, Pruebas, Ejecución, Recuperación).
- **Estrategia de Ciberseguridad y Perfiles de Madurez:** Alineación con el marco NIST CSF (Identificar, Proteger, Detectar, Responder, Recuperar), perfiles de riesgo (Básico, Estándar, Avanzado) y modelo de madurez de procesos (Nivel L0 a L5).
- **ISO 27001 / SGSI y Caso de Estudio TIC:** Metodología PDCA, análisis diferencial ex-ante vs. ex-post, estructura de proyectos de salvaguardas (PR01 a PR13), escalas de esfuerzo económico y justificación en términos de valor de negocio protegido.

---

## 3. Matriz de Trazabilidad de Requerimientos y Entregables

| ID Consigna | Requisito Solicitado | Artefacto de Implementación | Estado |
| :--- | :--- | :--- | :--- |
| **REQ-01** | Ecosistema ISO 27000: listado de normas, alcances, conceptos clave y diferencias 2018 vs 2022. | [README.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/README.md) (Sección 1), [TP13_ISO27000.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/TP13_ISO27000.ipynb) | Completo |
| **REQ-02** | Evaluación de criticidad de activos universitarios (Estudiantes, Docentes, CONICET, Proveedores nube). | [README.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/README.md) (Sección 2), [TP13_ISO27000.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/TP13_ISO27000.ipynb) | Completo |
| **REQ-03** | Evaluación SGSI de educación superior remota/virtual (actores, procesos, herramientas, información). | [README.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/README.md) (Sección 3), [TP13_ISO27000.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/TP13_ISO27000.ipynb) | Completo |
| **REQ-04** | Evaluación cuantitativa de riesgos R-01 a R-05, umbrales de apetito y mapa de calor. | [evaluacion_riesgo.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/evaluacion_riesgo.py), [mapa_calor_riesgos.png](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/mapa_calor_riesgos.png) | Completo |
| **REQ-05** | Resumen de problemas y lecciones aprendidas en recertificación ISO 27001:2022 (URM Consulting / BSI). | [README.md](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/README.md) (Sección 5), [TP13_ISO27000.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/TP13_ISO27000.ipynb) | Completo |
| **REQ-06** | Análisis económico, temporal y estratégico del Caso de Estudio TIC (PR01-PR13, costes, GAP). | [caso_estudio_tic.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/caso_estudio_tic.py), [costes_proyectos_tic.png](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/costes_proyectos_tic.png), [radar_cumplimiento_tic.png](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/radar_cumplimiento_tic.png) | Completo |
| **REQ-07** | Suite de pruebas unitarias automatizadas para validación de lógica de riesgos y datos TIC. | [test_tp13.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/test_tp13.py) | Completo |
| **REQ-08** | Cuaderno interactivo reproducible con código, visualizaciones y tablas. | [create_notebook.py](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/create_notebook.py), [TP13_ISO27000.ipynb](file:///c:/Users/Usuario/Desktop/is2_arevalo/src/tp13/TP13_ISO27000.ipynb) | Completo |

---

## 4. Estructura de Componentes de Software

El directorio `src/tp13/` contiene código estructurado bajo principios de responsabilidad única y alta cobertura de pruebas:
- `evaluacion_riesgo.py`: Módulo con modelos orientados a objetos (`RiesgoFactor`, `MatrizRiesgo`) para calcular el nivel de riesgo inherente y residual, validar clasificaciones semánticas y exportar el mapa de calor bidimensional en formato gráfico.
- `caso_estudio_tic.py`: Módulo para el procesamiento y modelado cuantitativo de los proyectos de inversión en seguridad de la información (CAPEX/OPEX), generación de radar chart y análisis de retorno.
- `test_tp13.py`: Conjunto de pruebas unitarias implementadas con `pytest` que verifican invariantes matemáticas, particiones de riesgo, y consistencia presupuestaria.
- `create_notebook.py`: Generador dinámico de notebooks en formato `.ipynb` compatible con entornos Jupyter y VS Code.
