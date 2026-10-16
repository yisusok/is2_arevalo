"""Suite de pruebas unitarias y de integración para json2csv.py.

Verifica la cobertura funcional, manejo de excepciones y estrategia de filtro.
Objetivo de cobertura: >= 85%.
"""

from __future__ import annotations

import io
import json
from unittest.mock import patch

import pytest

from src.tp11.json2csv import (
    aplanar_valor,
    convertir_json_a_csv,
    ejecutar_filtro,
    obtener_version,
    transformar_json_a_filas,
)

# ==============================================================================
# PRUEBAS DE FUNCIONES AUXILIARES Y TRANSFORMACIÓN
# ==============================================================================


def test_obtener_version():
    """Valida que la versión sea una cadena semántica válida."""
    ver = obtener_version()
    assert isinstance(ver, str)
    assert len(ver.split(".")) == 3


def test_aplanar_valor_tipos_basicos():
    """Valida el aplanado de valores simples."""
    assert aplanar_valor(None) == ""
    assert aplanar_valor("texto") == "texto"
    assert aplanar_valor(123) == 123
    assert aplanar_valor(45.67) == 45.67
    assert aplanar_valor(True) is True


def test_aplanar_valor_estructuras_anidadas():
    """Valida la serialización de listas y diccionarios anidados."""
    obj = {"sub": 1}
    lista = [1, 2, "a"]
    assert aplanar_valor(obj) == '{"sub": 1}'
    assert aplanar_valor(lista) == '[1, 2, "a"]'


def test_transformar_json_a_filas_diccionario_simple():
    """Valida la transformación de un único objeto JSON."""
    datos = {"id": 1, "nombre": "Alice"}
    encabezados, filas = transformar_json_a_filas(datos)
    assert encabezados == ["id", "nombre"]
    assert filas == [datos]


def test_transformar_json_a_filas_lista_objetos():
    """Valida la transformación de una lista de objetos JSON con claves disjuntas."""
    datos = [
        {"id": 1, "nombre": "Alice"},
        {"id": 2, "nombre": "Bob", "email": "bob@example.com"},
    ]
    encabezados, filas = transformar_json_a_filas(datos)
    assert encabezados == ["id", "nombre", "email"]
    assert len(filas) == 2


def test_transformar_json_a_filas_vacio():
    """Valida el manejo de una lista vacía."""
    encabezados, filas = transformar_json_a_filas([])
    assert encabezados == []
    assert filas == []


def test_transformar_json_a_filas_tipo_invalido():
    """Valida que tipos primitivos disparen ValueError."""
    with pytest.raises(ValueError, match="objeto o una lista de objetos"):
        transformar_json_a_filas("no es dict ni lista")

    with pytest.raises(ValueError, match="únicamente objetos"):
        transformar_json_a_filas([1, 2, 3])


# ==============================================================================
# PRUEBAS DE CONVERSIÓN DE FLUJOS (convertir_json_a_csv)
# ==============================================================================


def test_convertir_json_a_csv_nominal():
    """Valida la conversión completa con delimitador por defecto (coma)."""
    contenido_json = json.dumps(
        [
            {"id": 1, "nombre": "Carlos", "ciudad": "Paraná"},
            {"id": 2, "nombre": "Diana", "ciudad": "Concordia"},
        ]
    )
    flujo_in = io.StringIO(contenido_json)
    flujo_out = io.StringIO()

    filas_procesadas = convertir_json_a_csv(flujo_in, flujo_out)
    assert filas_procesadas == 2

    resultado = flujo_out.getvalue().splitlines()
    assert resultado[0] == "id,nombre,ciudad"
    assert resultado[1] == "1,Carlos,Paraná"
    assert resultado[2] == "2,Diana,Concordia"


def test_convertir_json_a_csv_delimitador_personalizado():
    """Valida la conversión con delimitador personalizado (punto y coma)."""
    contenido_json = json.dumps([{"colA": "val1", "colB": "val2"}])
    flujo_in = io.StringIO(contenido_json)
    flujo_out = io.StringIO()

    convertir_json_a_csv(flujo_in, flujo_out, delimitador=";")
    lineas = flujo_out.getvalue().splitlines()
    assert lineas[0] == "colA;colB"
    assert lineas[1] == "val1;val2"


def test_convertir_json_a_csv_delimitador_invalido():
    """Valida que un delimitador de longitud distinta a 1 lance ValueError."""
    flujo_in = io.StringIO('{"a": 1}')
    flujo_out = io.StringIO()
    with pytest.raises(ValueError, match="único carácter"):
        convertir_json_a_csv(flujo_in, flujo_out, delimitador=",,")


def test_convertir_json_a_csv_contenido_blanco():
    """Valida el manejo de streams vacíos o solo espacios."""
    flujo_in = io.StringIO("   \n  ")
    flujo_out = io.StringIO()
    assert convertir_json_a_csv(flujo_in, flujo_out) == 0
    assert flujo_out.getvalue() == ""


def test_convertir_json_a_csv_lista_vacia():
    """Valida el manejo de JSON con lista vacía '[]'."""
    flujo_in = io.StringIO("[]")
    flujo_out = io.StringIO()
    assert convertir_json_a_csv(flujo_in, flujo_out) == 0
    assert flujo_out.getvalue() == ""


def test_convertir_json_a_csv_json_invalido():
    """Valida que JSON mal formado dispare json.JSONDecodeError."""
    flujo_in = io.StringIO("{este json no es valido")
    flujo_out = io.StringIO()
    with pytest.raises(json.JSONDecodeError):
        convertir_json_a_csv(flujo_in, flujo_out)


# ==============================================================================
# PRUEBAS DE INTEGRACIÓN CLI (ejecutar_filtro)
# ==============================================================================


def test_ejecutar_filtro_archivos_io(tmp_path):
    """Valida la ejecución con argumentos -i y -o."""
    archivo_in = tmp_path / "datos.json"
    archivo_out = tmp_path / "salida.csv"

    datos = [
        {"codigo": 101, "item": "Teclado"},
        {"codigo": 102, "item": "Mouse"},
    ]
    archivo_in.write_text(json.dumps(datos), encoding="utf-8")

    codigo_retorno = ejecutar_filtro(
        ["-i", str(archivo_in), "-o", str(archivo_out), "-d", ","]
    )
    assert codigo_retorno == 0

    contenido_salida = archivo_out.read_text(encoding="utf-8").splitlines()
    assert contenido_salida[0] == "codigo,item"
    assert contenido_salida[1] == "101,Teclado"
    assert contenido_salida[2] == "102,Mouse"


def test_ejecutar_filtro_stdin_stdout(capsys):
    """Valida la estrategia de filtro usando stdin y stdout."""
    datos = [{"usuario": "pedro", "rol": "docente"}]
    texto_json = json.dumps(datos)

    with patch("sys.stdin", io.StringIO(texto_json)):
        codigo_retorno = ejecutar_filtro([])
        assert codigo_retorno == 0

    capturado = capsys.readouterr()
    lineas = capturado.out.splitlines()
    assert lineas[0] == "usuario,rol"
    assert lineas[1] == "pedro,docente"


def test_ejecutar_filtro_archivo_inexistente(capsys):
    """Valida el manejo de error cuando el archivo de entrada no existe (código 1)."""
    codigo = ejecutar_filtro(["-i", "archivo_que_no_existe_12345.json"])
    assert codigo == 1
    capturado = capsys.readouterr()
    assert "no existe" in capturado.err


def test_ejecutar_filtro_json_malformado(tmp_path, capsys):
    """Valida el código de error ante JSON sintácticamente incorrecto (código 2)."""
    archivo_malo = tmp_path / "invalido.json"
    archivo_malo.write_text("{clave_sin_cerrar", encoding="utf-8")

    codigo = ejecutar_filtro(["-i", str(archivo_malo)])
    assert codigo == 2
    capturado = capsys.readouterr()
    assert "Error de formato JSON" in capturado.err


def test_ejecutar_filtro_delimitador_largo(tmp_path, capsys):
    """Valida el código de error ante delimitador inválido (código 3)."""
    archivo_in = tmp_path / "valid.json"
    archivo_in.write_text('{"a": 1}', encoding="utf-8")

    codigo = ejecutar_filtro(["-i", str(archivo_in), "-d", "DELIM"])
    assert codigo == 3
    capturado = capsys.readouterr()
    assert "Error de validación" in capturado.err


def test_ejecutar_filtro_error_io(tmp_path, capsys):
    """Valida el código de error ante fallas de entrada/salida (código 4)."""
    archivo_in = tmp_path / "in.json"
    archivo_in.write_text('{"x": 1}', encoding="utf-8")

    # Intentar escribir en un directorio como si fuera archivo
    directorio_como_archivo = tmp_path / "un_directorio"
    directorio_como_archivo.mkdir()

    codigo = ejecutar_filtro(
        ["-i", str(archivo_in), "-o", str(directorio_como_archivo)]
    )
    assert codigo == 4
    capturado = capsys.readouterr()
    assert "Error de entrada/salida" in capturado.err


def test_main_cli_invocacion():
    """Valida que main() invoque sys.exit correctamente."""
    from src.tp11.json2csv import main

    with patch("sys.argv", ["json2csv", "-i", "archivo_inexistente.json"]):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
