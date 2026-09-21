"""
Ejercicio 2: Evaluación de Escenarios Financieros y Equilibrio Negociado
Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Estudiante de Ingeniería de Software

Este script evalúa la neutralidad financiera entre el cliente y el proveedor para el Ejercicio 2.
"""

def calcular_ejercicio_2():
    r = 0.01  # Costo de oportunidad mensual 1%
    costo_mensual = 1000.0
    pago_acordado_12 = 14000.0

    print("=" * 70)
    print("EJERCICIO 2: EVALUACIÓN DE ESCENARIOS Y EQUILIBRIO FINANCIERO")
    print("=" * 70)

    # Línea de base contractual (12 meses, pago $14000 en mes 12)
    pv_costos_base = sum(costo_mensual / ((1 + r)**t) for t in range(1, 13))
    pv_ingreso_base = pago_acordado_12 / ((1 + r)**12)
    npv_proveedor_base = pv_ingreso_base - pv_costos_base

    print("\nLÍNEA DE BASE CONTRACTUAL (12 Meses):")
    print(f"   - PV de Costos del Proveedor: ${pv_costos_base:.2f}")
    print(f"   - PV de Ingresos del Proveedor: ${pv_ingreso_base:.2f}")
    print(f"   - Beneficio Neto Presente del Proveedor (NPV_base): ${npv_proveedor_base:.2f}")

    # Escenario a: Pago diferido a mes 14 (sin costo adicional de equipos)
    # Neutralidad financiera al proveedor => Mismo PV de ingreso a t=0
    pago_mes_14 = pv_ingreso_base * ((1 + r)**14)
    # Alternativamente pago_acordado_12 * (1+r)^2 = 14000 * (1.01)^2 = 14281.40
    print("\nEscenario a. Pago diferido 2 meses después de entrega (Mes 14):")
    print("   - Costo del proveedor: Se mantiene igual (12 meses de trabajo).")
    print(f"   - Pago requerido en Mes 14 para neutralidad financiera: ${pago_mes_14:.2f}")
    print(f"   - Compensación de intereses por diferimiento (2 meses al 1%): ${pago_mes_14 - pago_acordado_12:.2f}")

    # Escenario b: Entrega anticipada en mes 6, pago en mes 12
    pv_costos_6meses = sum(costo_mensual / ((1 + r)**t) for t in range(1, 7))
    # Para mantener el mismo NPV del proveedor ($1169.21 en t=0):
    pv_ingreso_requerido_b = pv_costos_6meses + npv_proveedor_base
    pago_mes_12_b = pv_ingreso_requerido_b * ((1 + r)**12)

    print("\nEscenario b. Entrega acelerada en Mes 6, Pago mantenido en Mes 12:")
    print(f"   - PV de Costos reducidos del proveedor (6 meses): ${pv_costos_6meses:.2f}")
    print(f"   - PV de Ingreso necesario a t=0 para conservar NPV_base: ${pv_ingreso_requerido_b:.2f}")
    print(f"   - Pago ajustado a realizar en Mes 12: ${pago_mes_12_b:.2f}")
    print(f"   - Descuento a favor del patrocinante por menor esfuerzo: ${pago_acordado_12 - pago_mes_12_b:.2f}")

    # Escenario c: Entrega en mes 6 y Pago en mes 6
    pago_mes_6_c = pv_ingreso_requerido_b * ((1 + r)**6)

    print("\nEscenario c. Entrega en Mes 6 y Pago en Mes 6:")
    print(f"   - PV de Ingreso necesario a t=0 para conservar NPV_base: ${pv_ingreso_requerido_b:.2f}")
    print(f"   - Pago ajustado a realizar en Mes 6: ${pago_mes_6_c:.2f}")
    print(f"   - Diferencia respecto al pago original de $14000: ${pago_acordado_12 - pago_mes_6_c:.2f}")
    print("=" * 70)

if __name__ == "__main__":
    calcular_ejercicio_2()
