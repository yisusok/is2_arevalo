"""
Tests unitarios y funcionales para la conjetura de Collatz (TP11).

Clasificación de casos de prueba:
- Unitarios (Caja Blanca): T1, T2, T3, T4, T11, T12
- Funcionales (Caja Negra): T5, T6, T7, T8, T9, T10
"""

import pytest
from src.tp11.collatz import collatz, solicitar_numero
from unittest.mock import patch

# ==============================================================================
# TESTS UNITARIOS (CAJA BLANCA)
# ==============================================================================


def test_t1_unitario_n1():
    """T1 (Caja Blanca): n=1 debe retornar 0 iteraciones (no entra al bucle)."""
    assert collatz(1) == 0


def test_t2_unitario_n2():
    """T2 (Caja Blanca): n=2 rama par simple (2 -> 1), retorna 1 iteración."""
    assert collatz(2) == 1


def test_t3_unitario_n3():
    """T3 (Caja Blanca): n=3 rama impar e impar/par combinada, retorna 7 iteraciones."""
    assert collatz(3) == 7


def test_t4_unitario_n4():
    """T4 (Caja Blanca): n=4 potencias de 2 (4 -> 2 -> 1), retorna 2 iteraciones."""
    assert collatz(4) == 2


def test_t11_unitario_excepcion_cero():
    """T11 (Caja Blanca): n=0 debe disparar ValueError."""
    with pytest.raises(ValueError):
        collatz(0)


def test_t12_unitario_excepcion_negativo():
    """T12 (Caja Blanca): n=-5 debe disparar ValueError."""
    with pytest.raises(ValueError):
        collatz(-5)


# ==============================================================================
# TESTS FUNCIONALES (CAJA NEGRA)
# ==============================================================================


def test_t5_funcional_nominal_20():
    """T5 (Caja Negra): Caso nominal n=20 solicitado por requerimiento."""
    assert collatz(20) == 7


def test_t6_funcional_limite_inferior():
    """T6 (Caja Negra): Límite inferior válido n=1."""
    assert collatz(1) == 0


def test_t7_funcional_limite_superior_1999():
    """T7 (Caja Negra): Límite superior válido permitido n=1999."""
    assert collatz(1999) == 50


def test_t8_funcional_entrada_fuera_rango():
    """T8 (Caja Negra): Entrada > 1999 debe ser rechazada por la función de teclado."""
    # Simula ingreso 2000 seguido de 1999 válido
    with patch("builtins.input", side_effect=["2000", "1999"]):
        valor = solicitar_numero()
        assert valor == 1999


def test_t9_funcional_entrada_no_positiva():
    """T9 (Caja Negra): Entrada <= 0 debe ser rechazada."""
    # Simula ingreso -10, 0, y luego 20 válido
    with patch("builtins.input", side_effect=["-10", "0", "20"]):
        valor = solicitar_numero()
        assert valor == 20


def test_t10_funcional_entrada_no_numerica():
    """T10 (Caja Negra): Entrada alfanumérica debe manejarse con reintento."""
    # Simula ingreso 'abc', '12.5', y luego 5 válido
    with patch("builtins.input", side_effect=["abc", "12.5", "5"]):
        valor = solicitar_numero()
        assert valor == 5


def test_main_ejecucion(capsys):
    """Prueba la ejecución de main() con salida estándar capturada."""
    from src.tp11.collatz import main

    with patch("builtins.input", return_value="20"):
        main()
    captured = capsys.readouterr()
    assert "Número de partida: 20" in captured.out
    assert "Número de iteraciones necesarias para alcanzar 1: 7" in captured.out
