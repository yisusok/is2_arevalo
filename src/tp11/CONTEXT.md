# CONTEXT.md: Registro de Contexto, Especificaciones y Prompts de Asistencia

**Proyecto:** json2csv / TP11 Gestión de Calidad  
**Asignatura:** Ingeniería de Software II  
**Institución:** Facultad de Ciencia y Tecnología (FCyT) - Universidad Autónoma de Entre Ríos (UADER)  
**Docente:** Dr. Pedro E. Colla  
**Autor:** Jesús Arévalo  

---

## 1. Contexto del Problema y Objetivos de Ingeniería

El objetivo del proyecto es el diseño, desarrollo, verificación y aseguramiento de la calidad de una herramienta utilitaria en lenguaje Python denominada `json2csv.py`. La herramienta implementa una estrategia de filtro (estilo tubería Unix), permitiendo convertir flujos de datos en formato JSON a tablas tabulares en formato CSV.

### Requerimientos Funcionales y de Ejecución:
- Formato de invocación por consola:
  ```bash
  python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
  ```
- Si no se especifica `-i`, la entrada se lee directamente desde la entrada estándar (`sys.stdin`).
- Si no se especifica `-o`, la salida se emite a través de la salida estándar (`sys.stdout`).
- El delimitador de campos es la coma (`,`) por defecto, a menos que se configure un carácter alternativo mediante el flag `-d`.
- Soporte para registros con estructuras anidadas (serialización canónica de diccionarios y listas internas).
- Soporte para diccionarios simples y listas de diccionarios con claves homogéneas o heterogéneas.

### Requerimientos de Calidad y Verificación:
- Ambiente virtual Python aislado (`venv`).
- Cobertura de tests unitarios y de integración con `pytest` y `pytest-cov` superior o igual al 85%.
- Formato y estilo: `ruff` (sin errores), `black` (formato consistente), cumplimiento estricto de PEP8.
- Documentación interna de código: Docstrings conforme a la convención PEP257 (`pydocstyle` sin observaciones).
- Tipado estático: Análisis con `mypy` y `pyright` sin errores ni advertencias.
- Seguridad estática: Evaluación con `bandit` sin hallazgos de vulnerabilidades.
- Exclusión deliberada de `Trufflehog` de acuerdo a la pauta de la cátedra.
- Integración Continua: Pipeline automatizado de GitHub Actions en `.github/workflows/ci.yml`.

---

## 2. Registro de Prompts y Diálogos con Herramientas de IA

De conformidad con el punto (c) de las consignas del Trabajo Práctico 11, se documenta la secuencia de directivas y prompts técnicos formulados para el diseño, depuración y validación del código:

### Prompt 1: Arquitectura del Filtro CLI y Manejo de Streams
> **Prompt:**  
> *"Diseña una herramienta en Python 3.14 llamada `json2csv.py` que funcione como un filtro estándar de consola. Debe aceptar argumentos opcionales `-i/--input`, `-o/--output` y `-d/--delimiter` (por defecto coma). Si no se informa `-i`, lee de `sys.stdin`. Si no se informa `-o`, escribe en `sys.stdout`. Asegura manejo robusto de excepciones para archivos inexistentes, JSON mal formado, delimitadores de más de un carácter y errores de E/S, devolviendo códigos de salida enteros diferenciados."*
>
> **Resultado Obtenido:**  
> Se generó la estructura modular con `argparse`, separando la lógica de lectura/escritura (`convertir_json_a_csv`) del punto de entrada CLI (`ejecutar_filtro`).

### Prompt 2: Tipado Estático y Docstrings PEP257
> **Prompt:**  
> *"Revisa `json2csv.py` para asegurar anotaciones de tipo completas compatibles con `mypy` y `pyright`. Agrega docstrings en formato PEP257 para el módulo y todas las funciones públicas y privadas, garantizando que `pydocstyle` y `ruff` no reporten ninguna observación."*
>
> **Resultado Obtenido:**  
> Se añadieron anotaciones de tipo (`TextIO`, `Sequence[str] | None`, `tuple[list[str], list[dict[str, Any]]]`) y docstrings con descripción de argumentos, retornos y excepciones lanzadas.

### Prompt 3: Suite de Pruebas Unitarias con Pytest y Cobertura
> **Prompt:**  
> *"Crea una suite de pruebas con `pytest` en `test_json2csv.py` que valide casos nominales, conversión de diccionarios individuales, listas de objetos, registros anidados, delimitadores personalizados (ej. ';', '|'), manejo de JSON inválido, archivos inexistentes, buffers vacíos y llamadas a `sys.stdin`/`sys.stdout` usando mocks de `unittest.mock`. La cobertura de código debe superar holgadamente el 85%."*
>
> **Resultado Obtenido:**  
> Se implementaron 20 tests unitarios y de integración, logrando una cobertura del 99% en `json2csv.py`.

### Prompt 4: Configuración de CI/CD para GitHub Actions
> **Prompt:**  
> *"Genera el archivo `.github/workflows/ci.yml` para GitHub Actions que automatice en cada push y pull request: checkout, configuración de Python, instalación de dependencias, ejecución de `ruff`, `black --check`, `mypy`, `pyright`, `pydocstyle`, `bandit` y `pytest --cov`."*
>
> **Resultado Obtenido:**  
> Se definió el workflow completo en YAML garantizando la ejecución de todos los chequeos de calidad solicitados.
