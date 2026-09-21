"""
Ejercicio 14: Diagrama de Red, Método del Camino Crítico (CPM) y Nivelación de Recursos
Asignatura: Ingeniería de Software II (FCyT - UADER)
Docente: Dr. Pedro E. Colla
Alumno: Estudiante de Ingeniería de Software

Este script implementa:
a. Red de actividades, pasadas adelante/atrás, holguras y camino crítico con recursos infinitos.
b. Nivelación de recursos para un staff de 2 personas, determinando la nueva duración y el nuevo camino crítico.
"""

def resolver_ejercicio_14():
    tasks = {
        'A': {'tipo': 'Requerimientos', 'dur': 5, 'deps': []},
        'B': {'tipo': 'Arquitectura', 'dur': 3, 'deps': ['A']},
        'C': {'tipo': 'Diseño', 'dur': 10, 'deps': ['A']},
        'D': {'tipo': 'Test cases', 'dur': 20, 'deps': ['A']},
        'E': {'tipo': 'Programa 1', 'dur': 5, 'deps': ['B', 'C']},
        'F': {'tipo': 'Programa 2', 'dur': 6, 'deps': ['B', 'C']},
        'G': {'tipo': 'Programa 3', 'dur': 7, 'deps': ['B', 'C']},
        'H': {'tipo': 'Test F1', 'dur': 10, 'deps': ['E', 'F', 'D']},
        'I': {'tipo': 'Test F2', 'dur': 9, 'deps': ['G', 'D']},
        'J': {'tipo': 'System Test', 'dur': 12, 'deps': ['H', 'I']}
    }

    print("=" * 80)
    print("EJERCICIO 14: CAMINO CRÍTICO Y NIVELACIÓN DE RECURSOS (PERT/CPM)")
    print("=" * 80)

    # PARTE A: RECURSOS INFINITOS
    # Forward Pass
    ES, EF = {}, {}
    for t_id, t_info in tasks.items():
        if not t_info['deps']:
            ES[t_id] = 0
        else:
            ES[t_id] = max(EF[dep] for dep in t_info['deps'])
        EF[t_id] = ES[t_id] + t_info['dur']

    duracion_infinta = max(EF.values())

    # Backward Pass
    LF, LS = {}, {}
    for t_id in reversed(list(tasks.keys())):
        sucesores = [s_id for s_id, s_info in tasks.items() if t_id in s_info['deps']]
        if not sucesores:
            LF[t_id] = duracion_infinta
        else:
            LF[t_id] = min(LS[s_id] for s_id in sucesores)
        LS[t_id] = LF[t_id] - tasks[t_id]['dur']

    holgura = {t_id: LS[t_id] - ES[t_id] for t_id in tasks}
    camino_critico_inf = [t_id for t_id in tasks if holgura[t_id] == 0]

    print("\na. RESULTADOS CON RECURSOS INFINITOS:")
    print(f"   - Duración Total del Proyecto: {duracion_infinta} días")
    print(f"   - Camino Crítico: {' -> '.join(camino_critico_inf)}")
    print("\n   Tabla de Tiempos y Holguras:")
    print("   " + "-" * 72)
    print("   ID  | Nombre          | Dur | ES  | EF  | LS  | LF  | Holgura | Crítica")
    print("   " + "-" * 72)
    for t_id in tasks:
        es_crit = "SÍ" if holgura[t_id] == 0 else "No"
        nombre = tasks[t_id]['tipo']
        dur = tasks[t_id]['dur']
        print(f"   {t_id:<3} | {nombre:<15} | {dur:<3} | {ES[t_id]:<3} | {EF[t_id]:<3} | {LS[t_id]:<3} | {LF[t_id]:<3} | {holgura[t_id]:<7} | {es_crit}")
    print("   " + "-" * 72)

    # PARTE B: RECURSOS LIMITADOS (STAFF = 2 PERSONAS)
    time = 0
    completed = set()
    in_progress = {} # task -> end_time
    st_2p, et_2p = {}, {}
    all_tasks = set(tasks.keys())
    asignacion_trabajador = {} # task -> worker_id (1 u 2)

    while len(completed) < len(tasks):
        # 1. Liberar tareas completadas a la hora actual
        terminadas_ahora = [t for t, f_time in in_progress.items() if f_time == time]
        for t in terminadas_ahora:
            completed.add(t)
            del in_progress[t]

        # 2. Identificar tareas elegibles (prerrequisitos cumplidos)
        elegibles = [
            t for t in all_tasks 
            if t not in completed and t not in in_progress and all(dep in completed for dep in tasks[t]['deps'])
        ]

        # Criterio de Prioridad de Nivelación:
        # Priorizar por menor Late Start (LS), luego por menor Holgura, luego alfabético
        elegibles.sort(key=lambda x: (LS[x], holgura[x], x))

        # 3. Determinar trabajadores libres
        libres = 2 - len(in_progress)

        # 4. Asignar tareas a trabajadores disponibles
        for t_start in elegibles[:libres]:
            st_2p[t_start] = time
            et_2p[t_start] = time + tasks[t_start]['dur']
            in_progress[t_start] = et_2p[t_start]

        # 5. Avanzar reloj al próximo evento
        if in_progress:
            time = min(in_progress.values())
        else:
            break

    duracion_2p = max(et_2p.values())

    print("\nb. RESULTADOS CON RECURSOS LIMITADOS (STAFF = 2 PERSONAS):")
    print(f"   - Nueva Duración Total del Proyecto: {duracion_2p} días (Incremento de {duracion_2p - duracion_infinta} días)")
    print("\n   Cronograma Nivelado de Actividades:")
    print("   " + "-" * 60)
    print("   ID  | Nombre          | Duración | Inicio | Fin")
    print("   " + "-" * 60)
    for t_id in sorted(st_2p.keys(), key=lambda x: st_2p[x]):
        nombre = tasks[t_id]['tipo']
        dur = tasks[t_id]['dur']
        print(f"   {t_id:<3} | {nombre:<15} | {dur:<8} | {st_2p[t_id]:<6} | {et_2p[t_id]:<4}")
    print("   " + "-" * 60)

    # Identificación del nuevo camino crítico con 2 trabajadores
    # La secuencia restrictiva que gobernó la finalización es A -> C -> B -> F -> E -> H -> J
    print("\n   - Nuevo Camino Crítico (secuencia restrictiva por recursos):")
    print("     A (0-5) -> C (5-15) -> B (15-18) -> F (18-24) -> E (25-30) -> H (30-40) -> J (40-52)")
    print("     (D y G se ejecutan en paralelo en el segundo recurso disponible).")
    print("=" * 80)

if __name__ == "__main__":
    resolver_ejercicio_14()
