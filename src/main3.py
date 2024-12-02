from proceso import Proceso
from scheduler import SJF
procesos = [
    Proceso.crear("P1", 0, 6),
    Proceso.crear("P2", 1, 8),
    Proceso.crear("P3", 2, 7),
    Proceso.crear("P4", 3, 3),
]

# Crear instancia de SJF y ejecutar
planificador = SJF(procesos)
planificador.imprimir_tabla()  # Muestra la tabla inicial de llegada y ráfaga
planificador.ejecutar()        # Ejecuta el algoritmo
planificador.imprimir_resultados()  # Muestra los resultados de espera y retorno