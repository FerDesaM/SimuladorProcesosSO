from scheduler import *

class CPU:
    def __init__(self, id_cpu, procesos=None):
        self.id_cpu = id_cpu
        self.proceso_actual = None
        
        if procesos is None:
            self.procesos = []
        else:
            self.procesos = procesos  # Lista de procesos asignados a esta CPU

    def asignar_proceso(self, proceso):
        self.procesos.append(proceso)
        self.proceso_actual = proceso

    def planificar(self):
        """Llama al algoritmo de planificación Round Robin (Turno Rotatorio)"""
        print(f"\n🚀 Planificando los procesos de la CPU {self.id_cpu}")
        RR(self.procesos)  # Pasamos los procesos directamente al inicializador de RR
    
    def mostrar_tiempos(self):
        """Muestra los tiempos de llegada y ejecución de todos los procesos asignados a la CPU."""
        for proceso in self.procesos:
            print(f"    Proceso {proceso.nombre} - Llegada: {proceso.arrival}, Ráfaga: {proceso.burst}")

    def planificarSJF(self):
        """Llama al algoritmo de planificación Round Robin (Turno Rotatorio)"""
        print(f"\n🚀 Planificando los procesos de la CPU {self.id_cpu}")
        sjf = SJF(self.procesos)  # Creamos una instancia de Scheduler dentro de la CPU
        sjf.ejecutar()
       
    
    def planificarFCFS(self):
        """Llama al algoritmo de planificación Round Robin (Turno Rotatorio)"""
        print(f"\n🚀 Planificando los procesos de la CPU {self.id_cpu}")
        fcfs = FCFS(self.procesos)  # Creamos una instancia de Scheduler dentro de la CPU
        fcfs.ejecutar()
      

