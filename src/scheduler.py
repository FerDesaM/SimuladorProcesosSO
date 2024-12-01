from proceso import Proceso

class PlanificadorSJF:
    def __init__(self):
        self.procesos = []
        self.tiempo_actual = 0
        self.proceso_actual = None

    def agregar_proceso(self, proceso):
        """Añade un proceso a la lista."""
        self.procesos.append(proceso)
        self.procesos.sort(key=lambda p: p.tiempo_llegada)  # Ordenar por tiempo de llegada

    def seleccionar_proceso_mas_corto(self):
        """Selecciona el proceso con menor tiempo de ejecución disponible."""
        procesos_disponibles = [
            p for p in self.procesos if p.tiempo_llegada <= self.tiempo_actual and p.tiempo_restante > 0
        ]
        if procesos_disponibles:
            return min(procesos_disponibles, key=lambda p: p.tiempo_ejecucion)
        return None

    def avanzar_tiempo(self):
        """Avanza un paso en el tiempo simulando la ejecución."""
        if self.proceso_actual is None:
            self.proceso_actual = self.seleccionar_proceso_mas_corto()
            if not self.proceso_actual:
                self.tiempo_actual += 1
                return

        # Reducir tiempo restante del proceso actual
        self.proceso_actual.tiempo_restante -= 1
        if self.proceso_actual.tiempo_restante == 0:
            self.proceso_actual.tiempo_retorno = self.tiempo_actual - self.proceso_actual.tiempo_llegada + 1
            self.procesos.remove(self.proceso_actual)
            self.proceso_actual = None

        self.tiempo_actual += 1

    def obtener_estado_procesos(self):
        """Devuelve una lista con el estado de todos los procesos."""
        return [
            {
                "id": p.id,
                "llegada": p.tiempo_llegada,
                "ejecucion": p.tiempo_ejecucion,
                "espera": p.tiempo_espera,
                "retorno": p.tiempo_retorno,
                "restante": p.tiempo_restante
            }
            for p in self.procesos
        ]
    

class Scheduler:
    def planificar(self, process_list):
        quantum = 0
        while quantum < 1:
            quantum = int(input('Ingrese el Quantum: '))
        quantum_tmp = quantum

        # FUNCIÓN PARA CALCULAR EL ORDEN DE LOS PROCESOS SEGÚN EL TIEMPO DE LLEGADA
        def orderProcessForTimeArrival(list):
            for proc in range(1, len(list)):
                item = proc
                while item > 0 and list[item].arrival < list[item - 1].arrival:
                    list[item], list[item - 1] = list[item - 1], list[item]
                    item = item - 1
            return list
        
        process_list = orderProcessForTimeArrival(process_list)  # se ordena por tiempo de llegada
        mirror_process = len(process_list)
        time = 0
        tail_processes = []
        currently_execution_proccess = None  # proceso actualmente en ejecución
        next_process = 0
        print('💡 Se activa el algoritmo Round Robin (turno rotatorio) 😁')
        print()

        control = True
        while mirror_process > 0:
            print(f' *************************** Tiempo: {time} ************************')
            if len(process_list) > next_process and time >= process_list[next_process].arrival:
                print(f'💡 El proceso {process_list[next_process].id} se ingreso a la cola de listos')
                tail_processes.append(process_list[next_process])
                next_process += 1
            else:
                if next_process > 0 or len(tail_processes) > 0:
                    if currently_execution_proccess is None:
                        currently_execution_proccess = tail_processes.pop(0)
                        control = True
                        print(f'💡 Se saca el proceso {currently_execution_proccess.id} de la cola y se ejecuta.')

                    if control:
                        if currently_execution_proccess.burst_tmp >= quantum:
                            currently_execution_proccess.burst_tmp -= quantum
                            print(f'💡 Se resta {quantum} a la ráfaga del proceso {currently_execution_proccess.id}')
                            time += quantum
                            print(f'💡 Se aumenta {quantum} al tiempo')
                        else:
                            time += currently_execution_proccess.burst_tmp
                            print(f'💡 Se aumenta {currently_execution_proccess.burst_tmp} al tiempo')
                            print(f'💡 Se resta {currently_execution_proccess.burst_tmp} a la ráfaga del proceso {currently_execution_proccess.id}')
                            currently_execution_proccess.burst_tmp = 0

                        if currently_execution_proccess.burst_tmp < 1:
                            print(f' *************************** Tiempo: {time} ************************')
                            print(f'💡 El Proceso {currently_execution_proccess.id} finalizó.')
                            currently_execution_proccess.ending = time
                            currently_execution_proccess.return_ = currently_execution_proccess.ending - currently_execution_proccess.arrival
                            currently_execution_proccess.wait = currently_execution_proccess.return_ - currently_execution_proccess.burst
                            mirror_process -= 1
                            currently_execution_proccess = None
                        else:
                            control = False
                    else:
                        tail_processes.append(currently_execution_proccess)
                        print(f'💡 Se agrega el proceso {currently_execution_proccess.id} que estaba en ejecución a la cola de listos')
                        currently_execution_proccess = None
                else:
                    time += 1
        
        print('💻💻💻💻💻 Algoritmo finalizado 💻💻💻💻💻')
        print('\n\n\n')
        print('✅✅✅✅✅ RESULTADOS ✅✅✅✅✅')
        total_return = 0
        total_wait = 0
        for process in process_list:
            print(f'Proceso #{process.id}, finalizó: {process.ending}, tiempo de espera: {process.wait}, retorno: {process.return_}')
            total_return += process.return_
            total_wait += process.wait
            print(f'Promedio de retorno: {total_return / len(process_list)}')
            print(f'Promedio de espera: {total_wait / len(process_list)}')
            print()
