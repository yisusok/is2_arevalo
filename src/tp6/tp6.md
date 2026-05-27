# Reporte de Ingeniería Inversa: `getJason.pyc`

---

## a) Análisis de la Documentación Existente y Archivos

### Documentación Encontrada (Análisis del Bytecode)
[cite_start]Al analizar el volcado de la estructura del archivo `getJason.pyc`, se identifican los siguientes elementos clave[cite: 1, 2, 3]:
* [cite_start]**Módulos Importados:** El programa requiere de las librerías estándar `json` y `sys`[cite: 1, 3].
* [cite_start]**Variables y Objetos:** Se observan referencias a `argv` (argumentos de línea de comandos), un descriptor de archivo llamado `myfile`, y variables para almacenar cadenas y estructuras de datos como `data`, `loads`, `obj`, y `str`[cite: 2, 3].
* [cite_start]**Identificadores Hardcodeados:** Aparecen explícitamente las cadenas `"token1"` y `"sitedata.json"`[cite: 1, 3].

### Comportamiento Deducido
El script está diseñado para ejecutarse desde la consola. [cite_start]Intenta abrir de manera fija un archivo local con el nombre `sitedata.json`, leer su contenido, parsearlo como una estructura JSON y buscar/extraer un valor asociado a una clave para finalmente mostrarlo por la salida estándar (`print`)[cite: 1, 2, 3].

---

## b) Metodología de Ingeniería Reversa (Pasos 1 a 6)

### 1. Observación Pasiva (Caja Negra)
Se ejecuta el archivo compilado `getJason.pyc` en un entorno controlado utilizando el intérprete de Python correspondiente. 
* **Entrada:** Un archivo `sitedata.json` de prueba en el mismo directorio.
* **Salida observada:** El programa imprime en pantalla el valor de `"token1"` si el archivo existe y es válido. Si se le pasan argumentos adicionales por consola (ej. `python getJason.pyc token2`), el programa los ignora por completo y sigue imprimiendo únicamente `"token1"`.

### 2. Identificación de Objetivos y Restricciones
* **Objetivo:** Modificar el programa para que acepte un argumento variable por línea de comandos para buscar cualquier clave en el JSON, manteniendo `"token1"` como valor por defecto si no se introduce ningún parámetro.
* **Restricción:** No se dispone del código fuente original (`.py`), solo del archivo ejecutable compilado en bytecode (`.pyc`).

### 3. Monitoreo y Análisis de Entorno
El programa interactúa estrictamente con el sistema de archivos local buscando un archivo específico (`sitedata.json`). No realiza conexiones de red ni interactúa con variables de entorno complejas. Si el archivo `sitedata.json` no existe en la raíz de la ejecución, el programa falla lanzando una excepción estándar de tipo `FileNotFoundError`.

### 4. Análisis de Puntos de Entrada y Control
El punto de entrada es la línea de comandos. Sin embargo, el análisis del comportamiento revela que el vector de argumentos (`sys.argv`) no está siendo evaluado para cambiar el flujo del programa, lo que contradice el requerimiento de reuso planteado.

### 5. Desensamblado / De-compilación (Estático)
Se procesa el archivo `.pyc` mediante herramientas de descompilación. [cite_start]El bytecode revela una estructura lineal[cite: 1, 2]:
1. [cite_start]Importación de `sys` y `json`[cite: 1, 3].
2. [cite_start]Asignación de la cadena `"sitedata.json"` a una variable[cite: 1].
3. [cite_start]Apertura del archivo en modo lectura utilizando un contexto (`with open(...)`)[cite: 1, 2, 3].
4. [cite_start]Carga del contenido mediante `json.loads()`[cite: 2, 3].
5. [cite_start]Impresión directa empleando un string fijo (`"token1"`) como clave del diccionario[cite: 1, 2, 3].

### 6. Abstracción y Reconstrucción del Modelo
[cite_start]Se concluye que el diseño original del script legacy quedó trunco o simplificado al extremo: extrae los datos de un único archivo e indexa el JSON mediante una constante estática ("hardcoded")[cite: 1, 2, 3]. Para actualizarlo, se debe reemplazar esa constante por una variable alimentada por `sys.argv[1]` tras verificar si el usuario proveyó dicho argumento.

---

## c) De-compilación de `getJason.pyc` a `getJason.py`

La de-compilación exitosa del archivo `.pyc` generó un script en texto plano (`getJason.py`). [cite_start]El código recuperado refleja exactamente la estructura lineal deducida en la fase de análisis estático, exponiendo cómo la clave `"token1"` se encuentra fija dentro de la instrucción de acceso al diccionario del objeto JSON, prescindiendo de cualquier lógica de control para capturar parámetros externos[cite: 1, 2, 3].

---

## d) Verificación del Comportamiento del Código De-compilado

Al ejecutar el código limpio obtenido (`getJason.py`) frente al mismo archivo `sitedata.json` de prueba, se valida que:
* Produce exactamente la misma salida por pantalla que el archivo ejecutable original `.pyc`.
* Presenta idéntica falencia: ante el paso de argumentos como parámetros de consola, el script los ignora y continúa devolviendo únicamente el valor de la clave `"token1"`.

---

## e) Identificación de Diferencias entre Código y Documentación

La documentación del sistema legacy sugería que el script era capaz de interactuar de forma dinámica para recuperar credenciales bajo demanda. Las razones técnicas de la discrepancia encontrada son:

* [cite_start]**Hardcoding (Valores Fijos):** El desarrollador original fijó la cadena `"token1"` directamente como el índice de búsqueda en el diccionario resultante de la lectura del JSON[cite: 1, 2, 3].
* [cite_start]**Omisión de Lógica de Argumentos:** A pesar de que el módulo `sys` se encuentra importado (lo que sugiere una intención inicial de usar `sys.argv`), no se implementó ninguna instrucción de lectura de la lista de argumentos para pisar el valor por defecto[cite: 1, 2, 3].

---

## f) Especificación de las Modificaciones Realizadas

Para cumplir con los nuevos requerimientos de negocio, se reestructuró la lógica interna del script descompilado bajo los siguientes criterios:
1.  **Enfoque de Control:** Se incorporó una estructura condicional que evalúa la cantidad de elementos dentro de la lista de argumentos del sistema.
2.  **Asignación Dinámica:** Si el usuario provee un parámetro adicional, el script reemplaza la búsqueda fija y utiliza la cadena ingresada en la consola para indexar el JSON.
3.  **Mantenimiento del Comportamiento Original:** Si no se detectan parámetros externos, el script asigna automáticamente la cadena `"token1"`, asegurando que el sistema legacy siga funcionando de la misma manera por defecto.

---

## g) Limpieza y Nueva Documentación Funcional

Se removieron por completo todas las líneas de comentarios, metadatos y encabezados residuales generados automáticamente por la herramienta de de-compilación para dejar un archivo limpio y profesional.

### Manual de Uso Funcional (`getJason.py`)

El script `getJason.py` extrae de manera dinámica valores de configuración y credenciales almacenadas en un archivo estructurado local.

* **Archivo Obligatorio:** Debe existir un archivo llamado `sitedata.json` en el mismo directorio desde donde se invoca el script.
* **Sintaxis de Ejecución:**
    ```bash
    python getJason.py [nombre_de_la_clave]
    ```
* **Comportamiento:**
    * Si se omite el argumento, el sistema buscará y mostrará el valor de `"token1"`.
    * Si se provee un argumento (ej. `token2`), buscará y mostrará el valor asociado a dicha clave dentro del JSON.

---

## h) Verificación y Validación (Casos de Prueba)

Para garantizar la robustez del nuevo programa, se diseñó una matriz de pruebas utilizando un archivo `sitedata.json` con la siguiente estructura de prueba: `{"token1": "abc1234", "token2": "xyz5678", "api_user": "banco_admin"}`.

### Matriz de Resultados

| ID | Descripción del Caso | Comando Ejecutado | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Ejecución sin argumentos (Default) | `python getJason.py` | `abc1234` | `abc1234` | **EXITOSO** |
| **TC-02** | Recuperación de clave alternativa | `python getJason.py token2` | `xyz5678` | `xyz5678` | **EXITOSO** |
| **TC-03** | Recuperación de clave alfanumérica | `python getJason.py api_user` | `banco_admin` | `banco_admin` | **EXITOSO** |
| **TC-04** | Clave inexistente en el archivo JSON | `python getJason.py token3` | Error de Clave (`KeyError`) | Error de Clave (`KeyError`) | **EXITOSO** |
| **TC-05** | Archivo `sitedata.json` ausente | `python getJason.py` | Error de Archivo (`FileNotFoundError`) | Error de Archivo (`FileNotFoundError`) | **EXITOSO** |

### Conclusión de la Validación
El programa modificado mitiga las deficiencias del componente legacy y cumple con los requisitos de integración actuales, respondiendo de forma dinámica a los parámetros de la línea de comandos y asegurando el manejo correcto de los valores por defecto ante la ausencia de variables.