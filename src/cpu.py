# cpu.py
from scheduler import Scheduler  # Importamos la clase Scheduler

class CPU:
    def __init__(self, id_cpu, procesos=None):
        self.id_cpu = id_cpu
        self.proceso_actual = None
        
        # Si no se pasa una lista de procesos, inicializamos con una lista vacía
        if procesos is None:
            self.procesos = []
        else:
            self.procesos = procesos  # Lista de procesos asignados a esta CPU

    def asignar_proceso(self, proceso):
        # Asignamos un proceso a esta CPU
        self.procesos.append(proceso)
        self.proceso_actual = proceso  # Opcional: si solo hay un proceso activo

    def planificar(self):
        """Llama al algoritmo de planificación Round Robin (Turno Rotatorio)"""
        print(f"\n🚀 Planificando los procesos de la CPU {self.id_cpu}")
        scheduler = Scheduler()  # Creamos una instancia de Scheduler dentro de la CPU
        scheduler.planificar(self.procesos)  # Pasa los procesos de esta CPU al planificador
    
    def mostrar_tiempos(self):
        """Muestra los tiempos de llegada y ejecución de todos los procesos asignados a la CPU."""
        for proceso in self.procesos:
            print(f"    Proceso {proceso.nombre} - Llegada: {proceso.arrival}, Ráfaga: {proceso.burst}")
