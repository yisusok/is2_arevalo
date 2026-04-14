import unittest
import math
from tp2 import RPNCalculator, RPNError

class TestRPNCalculator(unittest.TestCase):
    """
    Punto 2: Suite de tests para alcanzar >90% de cobertura.
    Cubre todas las funciones matemáticas, comandos de pila y errores.
    """

    def setUp(self):
        self.calc = RPNCalculator()

    def test_operaciones_exito(self):
        """Prueba las operaciones básicas y expresiones del Punto 4.e."""
        self.assertEqual(self.calc.evaluate("3 4 +"), 7.0)
        self.assertEqual(self.calc.evaluate("5 1 2 + 4 * + 3 -"), 14.0)
        self.assertEqual(self.calc.evaluate("2 3 4 * +"), 14.0)

    def test_funciones_matematicas_y_potencias(self):
        """Cubre las líneas Missing de funciones (sqrt, log, ln, ex, 10x, yx, 1/x)."""
        self.assertAlmostEqual(self.calc.evaluate("4 sqrt"), 2.0)
        self.assertAlmostEqual(self.calc.evaluate("100 log"), 2.0)
        self.assertAlmostEqual(self.calc.evaluate("1 ln"), 0.0)
        self.assertAlmostEqual(self.calc.evaluate("1 ex"), math.e)
        self.assertEqual(self.calc.evaluate("2 10x"), 100.0)
        self.assertEqual(self.calc.evaluate("2 3 yx"), 8.0)
        self.assertEqual(self.calc.evaluate("0.5 1/x"), 2.0)
        self.assertEqual(self.calc.evaluate("5 chs"), -5.0)

    def test_trigonometria_completa(self):
        """Cubre sin, cos, tg y sus inversas (Punto 9)."""
        self.assertAlmostEqual(self.calc.evaluate("90 sin"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("0 cos"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("45 tg"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("1 asin"), 90.0)
        self.assertAlmostEqual(self.calc.evaluate("1 acos"), 0.0)
        self.assertAlmostEqual(self.calc.evaluate("1 atg"), 45.0)

    def test_comandos_pila(self):
        """Cubre dup, swap, drop, clear (Punto 5)."""
        self.assertEqual(self.calc.evaluate("5 dup +"), 10.0)
        self.assertEqual(self.calc.evaluate("10 5 swap -"), -5.0)
        self.assertEqual(self.calc.evaluate("1 2 drop"), 1.0)
        # Para probar clear, usamos un caso que falle si no se limpia
        with self.assertRaises(RPNError):
            self.calc.evaluate("1 2 clear")

    def test_memoria_y_constantes(self):
        """Prueba constantes y almacenamiento (Punto 6 y 10)."""
        self.assertAlmostEqual(self.calc.evaluate("pi"), math.pi)
        self.assertAlmostEqual(self.calc.evaluate("e"), math.e)
        self.assertAlmostEqual(self.calc.evaluate("phi"), (1 + 5**0.5) / 2)
        self.calc.evaluate("42 sto5")
        self.assertEqual(self.calc.evaluate("rcl5"), 42.0)

    def test_errores_try_except(self):
        """Cubre las excepciones RPNError y manejo de errores (Punto 4 y 12)."""
        # División por cero (Punto 4c)
        with self.assertRaises(RPNError): self.calc.evaluate("3 0 /")
        with self.assertRaises(RPNError): self.calc.evaluate("0 1/x")
        # Token inválido (Punto 4a)
        with self.assertRaises(RPNError): self.calc.evaluate("abc")
        # Pila insuficiente (Punto 4b)
        with self.assertRaises(RPNError): self.calc.evaluate("+")
        # Memoria fuera de rango
        with self.assertRaises(RPNError): self.calc.evaluate("42 sto15")

if __name__ == "__main__":
    unittest.main()