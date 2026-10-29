"""Script para generar programáticamente el Jupyter Notebook 'TP13_ISO27000.ipynb'.

Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Jesús Arévalo
Ubicación: src/tp13/
"""

import json
import os


def build_notebook() -> None:
    """Construye y serializa el cuaderno Jupyter con todas las consignas resueltas."""
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    # Celda 1: Portada
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# TP13: Estándar ISO/IEC 27000 y Gestión de Seguridad de la Información (SGSI)\n",
                "\n",
                "**Asignatura:** Ingeniería de Software II  \n",
                "**Docente:** Dr. Pedro E. Colla  \n",
                "**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  \n",
                "**Alumno:** Jesús Arévalo  \n",
                "**Ubicación de Código y Reportes:** `src/tp13/`  \n",
                "\n",
                "> **Resumen del Trabajo Práctico:** El presente cuaderno aborda el ecosistema normativo **ISO/IEC 27000**, la evaluación sistemática de criticidad de activos en una universidad, el modelado SGSI del dictado de clases virtual/remoto, la cuantificación del riesgo con mapa de calor para cinco amenazas críticas (R-01 a R-05), el análisis de las lecciones aprendidas en los procesos de recertificación hacia **ISO/IEC 27001:2022** (publicadas por URM Consulting / BSI), y la evaluación económica y estratégica del **Caso de Estudio TIC** expuesto en las clases del Dr. Pedro E. Colla.\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 2: Punto 1 - Ecosistema Normativo ISO 27000
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Ecosistema Normativo ISO/IEC 27000 y Evolución 2018 vs 2022\n",
                "\n",
                "### 1.1. Fundamentos y Normas Formantes del Ecosistema\n",
                "El estándar **ISO/IEC 27000:2018** (*Information technology - Security techniques - Information security management systems - Overview and vocabulary*) define la visión general y los términos nucleares del Sistema de Gestión de Seguridad de la Información (**SGSI** / **ISMS**).\n",
                "\n",
                "El ecosistema se subdivide en tres grupos de normas:\n",
                "1. **Normas de Requisitos Mandatorios (Certificables):**\n",
                "   - **ISO/IEC 27001:** Requisitos para el establecimiento, implementación, operación, monitoreo, revisión y mejora continua del SGSI. Es la única norma certificable mediante auditoría externa de tercera parte.\n",
                "   - **ISO/IEC 27006:** Requisitos para organismos que efectúan auditorías y certificación de SGSI.\n",
                "2. **Normas de Directrices Generales y Soporte Metodológico:**\n",
                "   - **ISO/IEC 27000:** Vocabulario estandarizado y principios fundamentales.\n",
                "   - **ISO/IEC 27002:** Código de prácticas y catálogo detallado de controles de seguridad de la información (guía técnica de implementación de los controles listados en el Anexo A de ISO 27001).\n",
                "   - **ISO/IEC 27003:** Guía paso a paso para el diseño y despliegue del SGSI.\n",
                "   - **ISO/IEC 27004:** Métricas, monitoreo, análisis y evaluación de la efectividad del SGSI.\n",
                "   - **ISO/IEC 27005:** Directrices para la gestión integral de riesgos de seguridad de la información.\n",
                "   - **ISO/IEC 27007:** Guía para la auditoría de sistemas de gestión de la seguridad de la información.\n",
                "   - **ISO/IEC 27008:** Guía para la evaluación técnica de los controles de seguridad de la información.\n",
                "3. **Normas Sectoriales y de Tecnologías Específicas:**\n",
                "   - **ISO/IEC 27017:** Controles de seguridad de la información para servicios de Computación en la Nube (*Cloud Computing*).\n",
                "   - **ISO/IEC 27018:** Protección de Información de Identificación Personal (*PII*) en nubes públicas que actúan como procesadores de datos.\n",
                "   - **ISO/IEC 27019:** Seguridad de la información para sistemas de control de procesos en la industria energética.\n",
                "   - **ISO/IEC 27031:** Preparación de tecnologías de información y comunicaciones para la continuidad del negocio (*ICT Readiness*).\n",
                "   - **ISO/IEC 27032:** Directrices para la ciberseguridad y resiliencia ante amenazas en el ciberespacio.\n",
                "   - **ISO/IEC 27033:** Seguridad de redes de datos (partes 1 a 6).\n",
                "   - **ISO/IEC 27034:** Seguridad en el ciclo de vida del desarrollo de aplicaciones (*Secure SDLC*).\n",
                "   - **ISO/IEC 27035:** Gestión de incidentes de seguridad de la información.\n",
                "   - **ISO/IEC 27036:** Seguridad en las relaciones con proveedores y cadenas de suministro.\n",
                "   - **ISO/IEC 27701:** Extensión de ISO 27001/27002 para la Gestión de la Privacidad de la Información (*PIMS*).\n",
                "\n",
                "### 1.2. Principales Conceptos Abordados\n",
                "- **Tríada CIA:** Confidencialidad (acceso solo a autorizados), Integridad (exactitud y no alteración indebida), Disponibilidad (acceso oportuno en el momento requerido).\n",
                "- **Principios Deseables Complementarios:** No Repudio (imposibilidad de negar emisión o recepción) y Autenticación (verificación fehaciente de la identidad invocada).\n",
                "- **Enfoque Basado en Riesgo:** Determinación sistemática del riesgo inherente y residual considerando el inventario de activos, amenazas activas/pasivas y vulnerabilidades técnicas/humanas.\n",
                "- **Declaración de Aplicabilidad (SoA - Statement of Applicability):** Documento formal que justifica la inclusión o exclusión de cada control de seguridad.\n",
                "- **Ciclo Deming (PDCA):** Planificar (Plan), Hacer (Do), Verificar (Check), Actuar (Act) como motor de mejora continua del SGSI.\n",
                "\n",
                "### 1.3. Principales Diferencias entre la Versión 2018 (con ISO 27001:2013) y la Versión 2022\n",
                "| Aspecto | Versión 2018 (ISO 27000:2018 / 27001:2013) | Versión 2022 (ISO 27001:2022 / 27002:2022) |\n",
                "| :--- | :--- | :--- |\n",
                "| **Título de la Norma** | *Information technology - Security techniques* | *Information security, cybersecurity and privacy protection* |\n",
                "| **Estructura del Anexo A** | 14 dominios rígidos (A.5 a A.18) y 35 objetivos de control | 4 temas modulares: Organizacional (37), Personas (8), Físico (14) y Tecnológico (34) |\n",
                "| **Cantidad de Controles** | 114 controles | 93 controles (57 fusionados, 35 conservados, 1 eliminado, 11 creados) |\n",
                "| **Nuevos Controles Contemporáneos** | Ausentes formalmente | 11 nuevos controles: Inteligencia de Amenazas (5.7), Seguridad en la Nube (5.23), Preparación TIC (5.30), Monitoreo Físico (7.4), Gestión de Configuraciones (8.9), Eliminación de Información (8.10), Enmascaramiento de Datos (8.11), Prevención de Fuga DLP (8.12), Monitoreo de Actividades (8.16), Filtrado Web (8.23), Codificación Segura (8.28) |\n",
                "| **Sistema de Atributos** | No existía metadato estandarizado | 5 atributos por control: Tipo de control, Propiedades CIA, Conceptos de Ciberseguridad (NIST CSF), Capacidades Operativas y Dominios de Seguridad |\n",
                "| **Cuerpo Principal (Cláusulas)** | Estructura tradicional de alto nivel | Adopción formal de la Estructura Armonizada ISO (Annex SL) con Cláusula 6.3 (Planificación de cambios), Cláusula 6.2 (Monitoreo de objetivos) y Cláusula 8.1 (Criterios y procesos de control) |\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 3: Punto 2 - Grado de Criticidad de Activos Universitarios
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Grado de Criticidad de Activos de Información en Educación Superior\n",
                "\n",
                "En el marco de una organización universitaria (proveedora de educación superior, ej. FCyT - UADER), se evalúa la criticidad de los activos asociados a las partes interesadas:\n",
                "\n",
                "| Parte Interesada | Requisito de Seguridad | Fuente Normativa/Legal | Grado de Criticidad | Justificación y Dimensiones CIA Involucradas |\n",
                "| :--- | :--- | :--- | :--- | :--- |\n",
                "| **Estudiantes** | Protección de Datos Personales (PII) y acceso a LMS (Campus Virtual) 24x7 | Ley Nacional 25.326 / Contratos nube (SaaS/IaaS) | **CRÍTICA (Muy Alta)** | **Confidencialidad, Privacidad y Disponibilidad:** La universidad custodia información personal sensible (DNI, domicilios, legajos, situaciones socioeconómicas y datos biométricos). Su filtración acarrea sanciones directas de la Agencia de Acceso a la Información Pública (AAIP) bajo la Ley 25.326. La indisponibilidad del LMS en períodos de cursado/exámenes paraliza la misión académica esencial de la institución. |\n",
                "| **Docentes** | Integridad de calificaciones y disponibilidad de actas | Normativa académica interna / Reglamentos de cátedra | **CRÍTICA (Muy Alta)** | **Integridad y No Repudio:** Las calificaciones y actas de examen constituyen instrumentos públicos con validez jurídica y fehaciente. La alteración no autorizada de una nota destruye la fe pública de los títulos emitidos. Asimismo, la indisponibilidad en fechas de cierre de actas colapsa el calendario académico y administrativo. |\n",
                "| **Ministerio / CONICET** | Confidencialidad de líneas de investigación, patentes y convenios | Convenios interinstitucionales / Ley de Propiedad Intelectual 11.723 | **ALTA** | **Confidencialidad e Integridad:** Los proyectos de I+D, desarrollos biotecnológicos, algoritmos propietarios y papers antes de su publicación internacional están sujetos a acuerdos de estricta confidencialidad (NDAs). La exfiltración de propiedad intelectual puede invalidar patentes y anular financiamientos millonarios con organismos estatales o internacionales. |\n",
                "| **Proveedores Nube** | Garantía de SLA (disponibilidad), cifrado (reposo/tránsito) y trazabilidad de logs | Contratos de Servicio / Acuerdos de Nivel de Servicio (SLA) | **ALTA** | **Disponibilidad, Trazabilidad y Seguridad Lógica:** La infraestructura en la nube aloja sistemas nodales (LMS, SIU, correo). Si el proveedor no garantiza un SLA ≥ 99.9%, cifrado robusto (AES-256 / TLS 1.3) y retención inmutable de logs de auditoría, la universidad queda ciega ante ciberataques y sufre responsabilidades contractuales solidarias. |\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 4: Punto 3 - Evaluación SGSI del Dictado Virtual/Remoto
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Evaluación Detallada del SGSI en Educación Superior Remota/Virtual\n",
                "\n",
                "Desde la perspectiva de un **SGSI basado en ISO/IEC 27001**, el dictado de educación superior en formato virtual desagrega los siguientes componentes sistémicos:\n",
                "\n",
                "### 3.1. Actores (Stakeholders del Sistema)\n",
                "- **Estudiantes:** Usuarios finales que acceden desde redes residenciales inseguras y dispositivos personales no gestionados (*BYOD*).\n",
                "- **Cuerpo Docente:** Creadores de contenido pedagógico y evaluadores que administran calificaciones y exámenes.\n",
                "- **Administradores de TI / SysAdmins:** Responsables de la infraestructura de servidores, bases de datos, redes y asignación de privilegios de acceso.\n",
                "- **Secretaría Académica y Bedelía:** Responsables de la custodia y formalización de actas, matrículas y certificaciones académicas.\n",
                "- **Proveedores Cloud Terceros:** Empresas proveedoras de software como servicio (MoodleCloud, Google Workspace, Microsoft 365, AWS).\n",
                "\n",
                "### 3.2. Procesos Críticos\n",
                "- **Autenticación y Gestión de Identidades (IAM):** Matriculación, asignación de credenciales y federación de identidades (*Single Sign-On*).\n",
                "- **Dictado Sincrónico y Asincrónico:** Transmisión de clases en vivo por videoconferencia y publicación de materiales de estudio.\n",
                "- **Evaluación en Línea y Rúbricas:** Creación de cuestionarios con límite temporal, entrega de trabajos prácticos y exámenes finales virtuales.\n",
                "- **Asentamiento y Cierre de Calificaciones:** Carga de notas en SIU Guaraní y firma digital/electrónica de actas.\n",
                "- **Gestión de Continuidad Operativa y Respaldo:** Ejecución de backups periódicos (política 3-2-1) y pruebas de recuperación ante desastres (*DRP*).\n",
                "\n",
                "### 3.3. Herramientas y Plataformas Tecnológicas\n",
                "- **Learning Management System (LMS):** Plataforma Moodle institucional accesible mediante interfaz web y aplicación móvil.\n",
                "- **Sistema de Gestión Académica:** Plataforma SIU Guaraní para el registro formal de historial académico.\n",
                "- **Plataformas de Comunicación y Videoconferencia:** Google Meet, Zoom Institucional, Microsoft Teams.\n",
                "- **Infraestructura de Red:** Firewalls perimetrales, Web Application Firewall (WAF), túneles VPN SSL para administradores.\n",
                "\n",
                "### 3.4. Tipología de Información y Activos de Datos\n",
                "- **Datos Personales e Identificatorios (PII):** DNI, CUIL, fotografías, teléfonos, domicilios y registros de regularidad.\n",
                "- **Instrumentos de Evaluación:** Enunciados de exámenes antes de su publicación, soluciones modelo y bancos de preguntas.\n",
                "- **Propiedad Intelectual Docente:** Clases grabadas, manuales de cátedra, artículos científicos no publicados y código fuente.\n",
                "- **Registros de Auditoría y Telemetría:** Logs de acceso HTTP, direcciones IP de conexión, marcas de tiempo y auditorías de base de datos.\n",
                "\n",
                "### 3.5. Mapeo de Controles ISO 27002 Recomendados\n",
                "- **Control 5.15 & 5.18 (Control de Acceso y Derechos de Acceso):** Autenticación Multifactorial (MFA) obligatoria y principio de menor privilegio.\n",
                "- **Control 6.7 (Teletrabajo / Trabajo Remoto):** Políticas de seguridad para dispositivos remotos y conexiones mediante VPN cifrada.\n",
                "- **Control 8.24 (Uso de Criptografía):** Encriptación obligatoria en tránsito (TLS 1.3) y en reposo (AES-256) en bases de datos estudiantiles.\n",
                "- **Control 8.12 (Prevención de Fuga de Datos - DLP):** Bloqueo de descargas masivas no autorizadas de padrones y legajos.\n",
                "- **Control 8.16 (Monitoreo de Actividades):** Detección de accesos concurrentes anómalos o intentos masivos de inicio de sesión (*brute-force*).\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 5: Punto 4 - Evaluación de Riesgos y Mapa de Calor
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Evaluación Cuantitativa de Riesgo y Mapa de Calor (5x5)\n",
                "\n",
                "### 4.1. Escalas Paramétricas Definidas en la Consigna\n",
                "- **Probabilidad (P) [1 a 5]:**\n",
                "  - $1$: Muy baja ($\\le 1$ vez cada 5 años)\n",
                "  - $2$: Baja (1 vez cada 2 a 3 años)\n",
                "  - $3$: Media (1 vez al año)\n",
                "  - $4$: Alta (1 vez por trimestre)\n",
                "  - $5$: Crítica ($\\ge 1$ vez al mes)\n",
                "\n",
                "- **Impacto (I) [1 a 5]:**\n",
                "  - $1$: Menor (Sin impacto apreciable / horas)\n",
                "  - $2$: Bajo (Menor, indisponibilidad $< 1$ día)\n",
                "  - $3$: Moderado (Afectación local, 1 a 2 días)\n",
                "  - $4$: Mayor (Impacto grave, 3 a 6 días)\n",
                "  - $5$: Catastrófico (Masivo, interrupción $\\ge 1$ semana)\n",
                "\n",
                "- **Perfil de Apetito de Riesgo:**\n",
                "  - **Riesgo Aceptable:** $R = P \\times I \\le 6$ (Zona Verde)\n",
                "  - **Riesgo Tolerable:** $7 \\le R \\le 12$ con Plan de Tratamiento de Riesgos (PTR) (Zona Amarilla/Naranja)\n",
                "  - **Riesgo Inaceptable:** $R \\ge 15$ con Requerimiento de Accionar Inmediato (Zona Roja)\n",
                "\n",
                "> **Propiedad Matemática:** En el espacio discreto de la matriz de productos $\\{P \\times I \\mid P, I \\in \\{1,2,3,4,5\\}\\}$, los valores posibles son $\\{1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20, 25\\}$. Nótese que los valores 13 y 14 son matemáticamente imposibles como producto de enteros en dicho intervalo. Por lo tanto, los umbrales de la cátedra constituyen una partición disjunta y exhaustiva de todo el espacio de riesgos.\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 6: Código Python de Evaluación de Riesgos y Mapa de Calor
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from src.tp13.evaluacion_riesgo import MatrizRiesgo\n",
                "\n",
                "# Instanciación de los riesgos provistos en la consigna\n",
                "matriz = MatrizRiesgo.obtener_riesgos_consigna()\n",
                "\n",
                "# Presentación de la tabla comparativa de riesgos Inherentes vs. Residuales\n",
                "print(matriz.generar_reporte_texto())\n",
                "\n",
                "# Exportación y visualización del mapa de calor\n",
                "archivo_grafico = matriz.exportar_mapa_calor(\"src/tp13/mapa_calor_riesgos.png\")\n",
                "print(f\"\\n[OK] Gráfico generado: {archivo_grafico}\")\n",
                "\n",
                "# Mostrar la imagen en el cuaderno\n",
                "from IPython.display import Image\n",
                "Image(filename=\"src/tp13/mapa_calor_riesgos.png\")\n",
            ],
        }
    )

    # Celda 7: Punto 5 - Lecciones Aprendidas (URM Consulting / BSI)
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Lecciones Aprendidas en la Transición y Recertificación ISO 27001:2022\n",
                "\n",
                "Con base en el análisis empírico publicado por **URM Consulting** en colaboración con **BSI (British Standards Institution)** (*\"Lessons Learnt from Early ISO 27001:2022 Transitions\"*, 2024), se identifican los principales errores y desafíos observados en auditorías reales:\n",
                "\n",
                "1. **No Actualizar la Declaración de Aplicabilidad (SoA) ni la Documentación Operativa:**\n",
                "   - El SoA es lo primero que audita la entidad certificadora. En ISO 27001:2022, cada control individual posee un *propósito explícito* (reemplazando los objetivos de sección). Si los números de control y referencias normativas no se actualizan en los procedimientos internos, matrices de riesgo y guías operativas, la auditoría detecta no conformidades inmediatas.\n",
                "2. **Confusión en los Cronogramas y Fechas Límite (Transition Timeline):**\n",
                "   - Muchas organizaciones asumen erróneamente que cuentan con plazo hasta el 31 de octubre de 2025 (fecha de expiración definitiva de la versión 2013). Sin embargo, las directivas internacionales establecieron que **a partir del 1 de mayo de 2024 todas las auditorías iniciales y de recertificación deben realizarse obligatoriamente contra ISO/IEC 27001:2022**.\n",
                "3. **Abandono Prematuro de la Conformidad con la Versión 2013:**\n",
                "   - Se observaron empresas que descartaron su SoA 2013 antes de aprobar la auditoría de transición. Mientras no se emita el nuevo certificado, la empresa está legalmente obligada a mantener la conformidad con ISO 27001:2013. La mejor práctica recomendada es mantener un **SoA con doble columna de mapeo** cruzado hasta la aprobación formal.\n",
                "4. **Subestimación de Pequeños Cambios en la Redacción de Cláusulas y Controles:**\n",
                "   - La adición o modificación de unas pocas palabras en una cláusula a menudo introduce requisitos operacionales estrictos. En los controles fusionados, el alcance agregado exige nuevas evidencias de cumplimiento que no deben darse por sobreentendidas.\n",
                "5. **Desactualización en las Competencias de Auditores e Implementadores:**\n",
                "   - No basta con capacitar a los auditores internos en la norma de requisitos ISO 27001; es indispensable que dominen la guía de buenas prácticas **ISO/IEC 27002:2022** para auditar contra el estado del arte contemporáneo.\n",
                "6. **Cuello de Botella en la Reserva de Fechas de Auditoría Externa:**\n",
                "   - La alta demanda de recertificación satura la disponibilidad de los auditores acreditados por BSI/IRCA. No reservar las fechas con suficiente antelación pone en riesgo la continuidad de la certificación.\n",
                "7. **Cláusulas del Cuerpo Principal más Desafiantes:**\n",
                "   - **Cláusula 6.3 (Planificación de cambios):** Exige demostrar formalmente la gestión del cambio dentro del propio SGSI (minutas de revisión directiva, autorizaciones formales y análisis de impacto).\n",
                "   - **Cláusula 6.2 (Objetivos de seguridad):** Requiere procesos explícitos de monitoreo continuo del grado de avance de cada objetivo.\n",
                "   - **Cláusula 8.1 (Control operacional):** Obliga a fijar criterios verificables para la ejecución de las acciones derivadas de la gestión del riesgo.\n",
                "   - **Cláusula 9.3.2 (Entradas de la revisión directiva):** Exige identificar proactivamente cambios en las expectativas de partes interesadas.\n",
                "8. **Controles del Anexo A más Críticos:**\n",
                "   - **Control 5.7 (Threat Intelligence):** Demanda la incorporación de feeds y procesos dinámicos de inteligencia ante ciberamenazas emergentes.\n",
                "   - **Control 8.11 (Data Masking):** Obliga a desplegar técnicas formales de anonimización, seudonimización y enmascaramiento de datos.\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 8: Punto 6 - Caso de Estudio TIC
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Caso de Estudio TIC: Análisis Económico, Cronograma y Hoja de Ruta\n",
                "\n",
                "A partir del **Caso de Estudio TIC** expuesto en las diapositivas de cátedra del Dr. Pedro E. Colla, se evalúa la transformación de una empresa de tecnología que implementa ISO 27001:\n",
                "\n",
                "### 6.1. Diagnóstico Inicial y Análisis Diferencial (GAP Analysis)\n",
                "- **Nivel de Madurez Inicial:** Nivel L1 (Inicial / Ad-hoc, efectividad estimada ~10%) con áreas en L0 (Inexistente).\n",
                "- **Conformidad con ISO 27001:2013:** Valores críticos en cláusulas organizacionales (Contexto 5%, Liderazgo 1%, Planificación 0%, Soporte 10%, Funcionamiento 0%, Evaluación 5%, Mejora 0%) totalizando **101 No Conformidades Mayores**.\n",
                "- **Conformidad con ISO 27002:2013:** Promedio inicial global del 17%. Pese a contar con relativo desarrollo en A.14 (Desarrollo y adquisición de software ~70% por su perfil tecnológico), presentaba vacíos críticos en Criptografía (A.10 ~5%), Incidentes (A.16 ~5%) y Continuidad de Negocio (A.17 ~2%).\n",
                "\n",
                "### 6.2. Cartera de Proyectos del Plan de Mejora (PR01 a PR13)\n",
                "La organización articuló 13 proyectos de salvaguardas desplegados en un horizonte de dos años (2016 - 2018):\n",
                "- **CAPEX Total de Implementación:** **401.760,00 €**\n",
                "- **OPEX Total de Mantenimiento Anual:** **167.000,00 €**\n",
                "- **Proyecto Dominante:** **PR10 (Gestión de Incidentes, SIEM, Logs e Inteligencia de Amenazas)** con una inversión de 251.000 € (62,48% del CAPEX total) y 69.600 € anuales de soporte (41,68% del OPEX).\n",
                "\n",
                "### 6.3. Motivaciones Estratégicas y Hoja de Ruta\n",
                "- **Protección de la Cadena de Valor:** La información y los sistemas de software constituyen el corazón de los servicios ofrecidos. Un incidente de ransomware o filtración de código destruye el activo subyacente de la compañía.\n",
                "- **Habilitador de Negocio y Confianza B2B:** En el mercado tecnológico global, la certificación ISO 27001 es un requisito contractual excluyente para acceder a licitaciones corporativas y contratos internacionales.\n",
                "- **Racionalidad Económica:** Los 401.760 € invertidos son plenamente consistentes frente a las pérdidas catastróficas que provocaría un incidente de seguridad (rescates millonarios, multas por protección de datos y pérdida de clientes).\n",
                "\n",
                "---",
            ],
        }
    )

    # Celda 9: Código Python para Caso TIC (Costes y Radar)
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from src.tp13.caso_estudio_tic import CasoEstudioTIC\n",
                "\n",
                "caso = CasoEstudioTIC()\n",
                "\n",
                "# Visualizar tabla financiera de los 13 proyectos\n",
                "print(caso.generar_reporte_proyectos())\n",
                "\n",
                "# Exportar gráficos\n",
                "img_costes = caso.exportar_grafico_costes(\"src/tp13/costes_proyectos_tic.png\")\n",
                "img_radar = caso.exportar_grafico_radar(\"src/tp13/radar_cumplimiento_tic.png\")\n",
                "print(f\"\\n[OK] Gráfico de Costes exportado: {img_costes}\")\n",
                "print(f\"[OK] Gráfico Radar exportado: {img_radar}\")\n",
                "\n",
                "# Mostrar gráficos en el cuaderno\n",
                "from IPython.display import Image, display\n",
                "display(Image(filename=\"src/tp13/costes_proyectos_tic.png\"))\n",
                "display(Image(filename=\"src/tp13/radar_cumplimiento_tic.png\"))\n",
            ],
        }
    )

    # Celda 10: Conclusiones
    nb["cells"].append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Conclusiones y Consideraciones Finales\n",
                "\n",
                "1. **El SGSI como Enfoque Holístico:** La seguridad de la información trasciende la mera seguridad informática; abarca políticas, concientización humana, marcos normativos, gobernanza y resiliencia operativa.\n",
                "2. **Evolución Dinámica en ISO 27001:2022:** La transición hacia controles contemporáneos (Threat Intelligence, Cloud Security, DLP y Enmascaramiento de Datos) refleja la sofisticación del ecosistema de ciberamenazas actuales.\n",
                "3. **Gestión Universitaria Proactiva:** En el ámbito universitario, la protección de PII de estudiantes (Ley 25.326), la integridad innegociable de calificaciones y la custodia de investigaciones de CONICET demandan salvaguardas robustas y monitoreo continuo.\n",
                "4. **Efectividad Comprobada de las Salvaguardas:** La evaluación de riesgos demostró cómo la aplicación de controles formales (planes BRS, WAF, 2FA, UPS redundante y RBAC/DLP) reduce los riesgos inherentes inaceptables ($R \\ge 15$) a niveles plenamente tolerables y aceptables dentro del apetito institucional ($R \\le 6$).\n",
                "5. **Alineación Económica de la Seguridad:** Como demostró el Caso TIC, la seguridad de la información requiere una inversión calibrada con el valor de los activos protegidos, garantizando la sostenibilidad y continuidad de la organización.\n",
                "\n",
                "---",
            ],
        }
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_nb = os.path.join(base_dir, "TP13_ISO27000.ipynb")
    with open(target_nb, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    print(f"[OK] Notebook generado exitosamente en: {target_nb}")


if __name__ == "__main__":
    build_notebook()
