"""
TP9 - Ejercicio 5: Priorización de Backlog y Evaluación de Capacidad
Datos:
    Funciones, Story Points (SP) y Frecuencia mensual de uso (Hits).
    Velocidad histórica del equipo = 5 SP/sprint (Sprint = 2 semanas).
"""

from itertools import combinations
from typing import List, Dict


def evaluar_combinaciones(backlog: List[Dict], capacidad_max: float) -> List[Dict]:
    """Evalúa todas las combinaciones posibles de items dentro de la capacidad disponible."""
    mejores_opciones = []
    n = len(backlog)

    for r in range(1, n + 1):
        for combo in combinations(backlog, r):
            total_sp = sum(item['sp'] for item in combo)
            total_hits = sum(item['hits'] for item in combo)

            if total_sp <= capacidad_max:
                mejores_opciones.append({
                    'items': [item['nombre'] for item in combo],
                    'sp': total_sp,
                    'hits': total_hits,
                    'densidad_media': total_hits / total_sp
                })

    # Ordenar por total de hits (descendente) y luego por menor SP
    mejores_opciones.sort(key=lambda x: (x['hits'], -x['sp']), reverse=True)
    return mejores_opciones


def main():
    backlog = [
        {'nombre': 'Función A', 'sp': 2, 'hits': 1104},
        {'nombre': 'Función B', 'sp': 3, 'hits': 1762},
        {'nombre': 'Función C', 'sp': 8, 'hits': 6602},
        {'nombre': 'Función D', 'sp': 5, 'hits': 1565},
        {'nombre': 'Función F', 'sp': 2, 'hits': 2179},
        {'nombre': 'Función G', 'sp': 13, 'hits': 8030},
    ]

    print("=== Ejercicio 5: Análisis y Selección de Scope en Backlog ===\n")
    print("Backlog Original:")
    print(f"{'Función':<12} | {'Story Points':<12} | {'Hits Mensuales':<15} | {'Densidad (Hits/SP)':<20}")
    print("-" * 65)
    for item in backlog:
        densidad = item['hits'] / item['sp']
        print(f"{item['nombre']:<12} | {item['sp']:<12} | {item['hits']:<15} | {densidad:<20.2f}")

    # Escenario 1: Presupuesto 6 semanas (3 sprints) @ 5 SP/sprint -> 15 SP
    print("\n" + "=" * 65)
    print("1. Alcance para 6 semanas (3 Sprints = 15 SP):")
    opciones_15 = evaluar_combinaciones(backlog, 15)
    top_15 = opciones_15[0]
    print(f"   Funciones Recomendadas: {', '.join(top_15['items'])}")
    print(f"   Total Story Points: {top_15['sp']} / 15 SP")
    print(f"   Total Hits Atendidos: {top_15['hits']} hits/mes")

    # Escenario 2: Presupuesto a la mitad (3 semanas = 7.5 SP max)
    print("\n" + "=" * 65)
    print("2. Alcance con Presupuesto Reducido a la Mitad (3 semanas = 7.5 SP / ~7 SP):")
    opciones_7 = evaluar_combinaciones(backlog, 7.5)
    top_7 = opciones_7[0]
    print(f"   Funciones Mantenidas: {', '.join(top_7['items'])}")
    print(f"   Total Story Points: {top_7['sp']} SP")
    print(f"   Total Hits Atendidos: {top_7['hits']} hits/mes")
    eliminadas_7 = [item['nombre'] for item in backlog if item['nombre'] not in top_7['items']]
    print(f"   Funciones Eliminadas: {', '.join(eliminadas_7)}")

    # Escenario 3: Presupuesto extendido a 7 semanas (3.5 Sprints = 17.5 SP max)
    print("\n" + "=" * 65)
    print("3. Alcance con Presupuesto de 7 semanas (3.5 Sprints = 17.5 SP):")
    opciones_17 = evaluar_combinaciones(backlog, 17.5)
    top_17 = opciones_17[0]
    print(f"   Funciones Incluidas: {', '.join(top_17['items'])}")
    print(f"   Total Story Points: {top_17['sp']} / 17.5 SP")
    print(f"   Total Hits Atendidos: {top_17['hits']} hits/mes")

    # Escenario 4: Priorización de Función D (Arquitectura)
    print("\n" + "=" * 65)
    print("4. Priorización de Función D (Recomendación Arquitectónica):")
    print("   Aunque D posee menor densidad de hits (313.0 hits/SP), su valor de arquitectura")
    print("   la convierte en una función habilitadora (Enabler). Se recomienda asignarle prioridad")
    print("   alta (Must Have / Sprint 1) para evitar sobrecostos por deuda de diseño.")

    # Escenario 5: Velocidad de Deuda Técnica = 1 SP/sprint
    print("\n" + "=" * 65)
    print("5. Efecto de Deuda Técnica (1 SP/sprint dedicado a refactor/deuda):")
    print("   Velocidad efectiva para nuevas funciones = 5 - 1 = 4 SP/sprint.")
    print("   Capacidad en 6 semanas (3 sprints) = 3 * 4 = 12 SP.")
    opciones_12 = evaluar_combinaciones(backlog, 12)
    top_12 = opciones_12[0]
    print(f"   Funciones Recomendadas con Deuda Técnica: {', '.join(top_12['items'])}")
    print(f"   Total Story Points: {top_12['sp']} / 12 SP")
    print(f"   Total Hits Atendidos: {top_12['hits']} hits/mes")


if __name__ == '__main__':
    main()
