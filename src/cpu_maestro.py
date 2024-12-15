from cpu import CPU  # Importa la clase CPU desde cpu.py
from proceso import Proceso  # Importa la clase Proceso desde proceso.py
import random

class CpuMaestro:
    def __init__(self, num_cpus, num_procesos):
        self.procesos = []  # Arreglo de procesos
        self.cpus = [CPU(i) for i in range(num_cpus)]  # Arreglo de CPUs
        
        # Crear procesos para todos los CPUs
        for i in range(num_cpus):
            for j in range(num_procesos):
                nombre_proceso = f"Proceso_{i}_{j}"
                proceso = Proceso.crear(nombre_proceso, random.randint(0, 5), random.randint(1, 6))
                #self.cpus[i].procesos.append(proceso)
                
                # Agregar estos procesos también a self.procesos
                self.procesos.append(proceso)

    def generar_proceso(self):
        """
        Función para generar un proceso sin parámetros.
        Los valores de prioridad y tiempo de ejecución se generan aleatoriamente.

        :return: Un objeto de tipo Proceso.
        """
        nombre_proceso = f"Proceso_{len(self.procesos)}"  # Nombre único basado en la cantidad de procesos
        prioridad = random.randint(0, 5)  # Prioridad aleatoria entre 0 y 5
        tiempo_ejecucion = random.randint(1, 6)  # Tiempo de ejecución aleatorio entre 1 y 6

        # Crear un nuevo proceso con los valores generados
        proceso = Proceso.crear(nombre_proceso, prioridad, tiempo_ejecucion)

        # Agregar el nuevo proceso al listado de procesos
        self.procesos.append(proceso)

        return proceso  # Retornar el nuevo proceso creado

    def despachador(self):
        """Método para asignar los procesos a las CPUs según el número de procesos que tienen asignados."""
        while self.procesos:
            # Encontramos la CPU con menos procesos asignados
            cpu_con_menos_procesos = min(self.cpus, key=lambda cpu: len(cpu.procesos))
            
            # Tomamos el siguiente proceso disponible
            proceso_a_asignar = self.procesos.pop(0)
            
            # Asignamos el proceso a la CPU con menos procesos
            cpu_con_menos_procesos.asignar_proceso(proceso_a_asignar)
            print(f"Proceso {proceso_a_asignar.nombre} asignado a CPU {cpu_con_menos_procesos.id_cpu}")
            print(f"  Tiempo de llegada: {proceso_a_asignar.arrival}, Tiempo de ejecución: {proceso_a_asignar.burst}")
    
    def mostrar_tiempos(self):
        """Muestra los tiempos de llegada y ejecución de todos los procesos asignados a la CPU."""
        for cpu in self.cpus:
            print(f"\n💻 CPU {cpu.id_cpu}:")
            for proceso in cpu.procesos:
                print(f"  Proceso {proceso.nombre} - Llegada: {proceso.arrival}, Ráfaga: {proceso.burst}")
    
    def modificar_tiempos(self):
        """
        Permite que el usuario ingrese los tiempos de llegada y ejecución (ráfaga) para cada proceso 
        en una CPU seleccionada. El usuario debe elegir qué CPU quiere modificar y luego ingresar los tiempos por proceso.
        """
        # Pedir al usuario que elija una CPU
        while True:
            try:
                num_cpu = int(input(f"Seleccione el número de CPU (0-{len(self.cpus) - 1}): "))
                if 0 <= num_cpu < len(self.cpus):
                    break  # CPU válida
                else:
                    print(f"Por favor, ingrese un número de CPU válido entre 0 y {len(self.cpus) - 1}.")
            except ValueError:
                print("Por favor, ingrese un número entero válido.")
        
        # Obtener la CPU seleccionada
        cpu_seleccionada = self.cpus[num_cpu]
        
        # Mostrar en qué CPU estamos trabajando
        print(f"\nModificando procesos en la CPU {cpu_seleccionada.id_cpu}:")
        
        # Recorrer los procesos de la CPU seleccionada
        for proceso in cpu_seleccionada.procesos:
            print(f"\n  Modificando tiempos del proceso {proceso.nombre} en la CPU {cpu_seleccionada.id_cpu}:")
            
            # Pedir tiempo de llegada
            nuevo_arrival = int(input(f"    Ingrese el nuevo tiempo de llegada para {proceso.nombre}: "))
            
            # Pedir tiempo de ráfaga (ejecución)
            nuevo_burst = int(input(f"    Ingrese el nuevo tiempo de ejecución para {proceso.nombre}: "))
            
            # Actualizar los tiempos del proceso
            proceso.arrival = nuevo_arrival
            proceso.burst = nuevo_burst
            proceso.burst_tmp = nuevo_burst  # Actualizamos la ráfaga temporal también
            
            # Confirmar que el proceso ha sido actualizado
            print(f"    Proceso {proceso.nombre} actualizado:")
            print(f"      Nuevo tiempo de llegada: {nuevo_arrival}, Nuevo tiempo de ejecución: {nuevo_burst}")



    def ejecutar_planificacion_RR(self):
        """Método para ejecutar la planificación de los procesos en todos los CPUs."""
        for cpu in self.cpus:
            print(f"Ejecutando planificación en la CPU {cpu.id_cpu}")
            # Pasamos la lista de procesos de la CPU al planificador sin necesidad de modificar la firma de la función
            cpu.planificar()

