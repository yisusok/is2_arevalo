"""
Módulo de calculadora RPN para Ingeniería de Software II - UADER.

Este programa implementa una calculadora de Notación Polaca Inversa (RPN)
que utiliza una pila para el procesamiento de operandos y operadores.
Incluye soporte para funciones trigonométricas, registros de memoria
y constantes matemáticas, cumpliendo con los requisitos del TP2.
"""
import math
import sys


class RPNError(Exception):
    """
    Excepción personalizada para errores lógicos de la calculadora RPN.
    Se dispara ante errores de pila vacía, tokens inválidos o división por cero.
    """


def _rad(grados):
    """Convierte grados a radianes para compatibilidad con la librería math."""
    return math.radians(grados)


def _deg(radianes):
    """Convierte radianes a grados para presentar resultados al usuario."""
    return math.degrees(radianes)


class RPNCalculator:
    """
    Clase principal que gestiona el estado de la pila y las operaciones.
    Utiliza un diccionario de despacho para reducir la complejidad ciclomática.
    """

    def __init__(self):
        """Inicializa la pila, registros de memoria y tabla de constantes."""
        # Punto 1: Implementación de la pila mediante lista.
        self.stack = []
        # Punto 10: 10 registros de memoria inicializados en 0.0.
        self.memory = [0.0] * 10
        # Punto 6: Constantes matemáticas requeridas por consigna.
        self.constants = {
            "pi": math.pi,
            "e": math.e,
            "phi": (1 + 5 ** 0.5) / 2,
        }
        # Despacho de operaciones para evitar estructuras if/elif extensas.
        self.ops = {
            "+": self._add, "-": self._sub, "*": self._mul, "/": self._div,
            "sqrt": self._sqrt, "log": self._log, "ln": self._ln, "ex": self._exp,
            "10x": self._pow10, "yx": self._powyx, "1/x": self._inv, "chs": self._chs,
            "sin": self._sin, "cos": self._cos, "tg": self._tg,
            "asin": self._asin, "acos": self._acos, "atg": self._atg,
            "dup": self._dup, "swap": self._swap, "drop": self._drop,
            "clear": self._clear,
        }

    def _pop(self):
        """Extrae el último elemento de la pila con validación de existencia."""
        if not self.stack:
            raise RPNError("Pila insuficiente para operar")
        return self.stack.pop()

    def _pop2(self):
        """Extrae los dos últimos elementos asegurando el orden de operación."""
        if len(self.stack) < 2:
            raise RPNError("Pila insuficiente para operar")
        val_b = self.stack.pop()
        val_a = self.stack.pop()
        return val_a, val_b

    def _push(self, val):
        """Agrega un valor numérico al tope de la pila de trabajo."""
        self.stack.append(val)

    def _add(self):
        """Suma los dos valores superiores de la pila."""
        val_a, val_b = self._pop2()
        self._push(val_a + val_b)

    def _sub(self):
        """Resta el valor superior al valor penúltimo."""
        val_a, val_b = self._pop2()
        self._push(val_a - val_b)

    def _mul(self):
        """Multiplica los dos valores superiores de la pila."""
        val_a, val_b = self._pop2()
        self._push(val_a * val_b)

    def _div(self):
        """Divide el penúltimo por el último con validación de divisor nulo."""
        val_a, val_b = self._pop2()
        if val_b == 0:
            raise RPNError("división por cero")
        self._push(val_a / val_b)

    def _sqrt(self):
        """Calcula la raíz cuadrada del tope de la pila."""
        self._push(math.sqrt(self._pop()))

    def _log(self):
        """Calcula el logaritmo en base 10 del tope de la pila."""
        self._push(math.log10(self._pop()))

    def _ln(self):
        """Calcula el logaritmo natural (base e) del tope de la pila."""
        self._push(math.log(self._pop()))

    def _exp(self):
        """Calcula la función exponencial e^x del tope de la pila."""
        self._push(math.exp(self._pop()))

    def _pow10(self):
        """Calcula la potencia de base 10 (10^x) del tope de la pila."""
        self._push(10 ** self._pop())

    def _powyx(self):
        """Calcula la potencia de base y elevada al exponente x."""
        val_a, val_b = self._pop2()
        self._push(pow(val_a, val_b))

    def _inv(self):
        """Calcula el inverso multiplicativo (1/x) con validación de cero."""
        val_v = self._pop()
        if val_v == 0:
            raise RPNError("división por cero")
        self._push(1 / val_v)

    def _chs(self):
        """Invierte el signo algebraico del elemento superior (change sign)."""
        self._push(-self._pop())

    def _sin(self):
        """Seno trigonométrico asumiendo entrada en grados decimales."""
        self._push(math.sin(_rad(self._pop())))

    def _cos(self):
        """Coseno trigonométrico asumiendo entrada en grados decimales."""
        self._push(math.cos(_rad(self._pop())))

    def _tg(self):
        """Tangente trigonométrica asumiendo entrada en grados decimales."""
        self._push(math.tan(_rad(self._pop())))

    def _asin(self):
        """Arcoseno con resultado convertido a grados decimales."""
        self._push(_deg(math.asin(self._pop())))

    def _acos(self):
        """Arcocoseno con resultado convertido a grados decimales."""
        self._push(_deg(math.acos(self._pop())))

    def _atg(self):
        """Arcotangente con resultado convertido a grados decimales."""
        self._push(_deg(math.atan(self._pop())))

    def _dup(self):
        """Punto 5: Duplica el último elemento presente en la pila."""
        val_v = self._pop()
        self.stack.extend([val_v, val_v])

    def _swap(self):
        """Punto 5: Intercambia la posición de los dos elementos superiores."""
        val_a, val_b = self._pop2()
        self.stack.extend([val_b, val_a])

    def _drop(self):
        """Punto 5: Elimina el elemento superior de la pila sin retornarlo."""
        self._pop()

    def _clear(self):
        """Punto 5: Vacía completamente la pila de trabajo."""
        self.stack.clear()

    def _mem_sto(self, idx):
        """Guarda el tope de la pila en memoria sin consumirlo de la pila."""
        val_v = self._pop()
        self.memory[idx] = val_v
        self._push(val_v)

    def _dispatch_mem(self, token):
        """Procesa comandos STO/RCL validando el índice de memoria (0-9)."""
        idx_raw = token[3:]
        if not idx_raw.isdigit():
            raise RPNError(f"token inválido: {token}")
        idx = int(idx_raw)
        if not 0 <= idx <= 9:
            raise RPNError("Memoria fuera de rango")
        if token.startswith("sto"):
            self._mem_sto(idx)
        else:
            self._push(self.memory[idx])

    def _try_push_number(self, token):
        """Intenta interpretar el token como número flotante y apilarlo."""
        try:
            self._push(float(token))
            return True
        except ValueError:
            return False

    def evaluate(self, expression):
        """
        Punto 2 y 11: Procesa una expresión RPN completa.
        Limpia la pila al inicio para asegurar independencia entre ejecuciones.
        """
        self.stack.clear()
        # Normalización de entrada: reemplazo de comas por puntos decimales.
        for token in expression.replace(",", ".").split():
            t_low = token.lower()
            if self._try_push_number(t_low):
                continue
            if t_low in self.ops:
                self.ops[t_low]()
            elif t_low in self.constants:
                self._push(self.constants[t_low])
            elif (t_low.startswith("sto") or t_low.startswith("rcl")) and len(t_low) > 3:
                self._dispatch_mem(t_low)
            else:
                raise RPNError(f"token inválido: {token}")

        # Punto 4d y 13: Verificación de que solo quede el resultado final.
        if len(self.stack) != 1:
            raise RPNError(f"pila inválida (quedan {len(self.stack)} elementos)")
        return self.stack[0]


def main():
    """
    Punto 14: Entrada principal. Soporta argumentos de consola o stdin.
    Punto 15: Utiliza exclusivamente las librerías sys y math.
    """
    calc = RPNCalculator()
    # Captura de argumentos o lectura de tubería (pipe).
    args = sys.argv[1:]
    expr = " ".join(args) if args else sys.stdin.read()
    if not expr.strip():
        return
    try:
        # Formateo de salida según Punto 11.
        print(calc.evaluate(expr))
    except RPNError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()