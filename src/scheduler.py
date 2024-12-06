from proceso import Proceso

class SJF:
    def __init__(self, procesos):
        """
        Inicializa el planificador SJF con una lista de objetos de tipo Proceso.
        :param procesos: Lista de objetos Proceso
        """
        self.procesos = procesos

    def ejecutar(self):
        """
        Ejecuta la planificación de los procesos usando el algoritmo SJF (Shortest Job First).
        """
        tiempo_actual = 0
        finalizado = 0
        n = len(self.procesos)

        while finalizado < n:
            proceso_elegido = None
            menor_burst = float('inf')

            # Encontrar el proceso con el menor tiempo de ráfaga que ya haya llegado
            for proceso in self.procesos:
                if proceso.arrival <= tiempo_actual and proceso.burst_tmp < menor_burst and proceso.ending == 0:
                    menor_burst = proceso.burst_tmp
                    proceso_elegido = proceso

            if proceso_elegido:
                # Ejecutar el proceso seleccionado
                tiempo_actual += proceso_elegido.burst
                proceso_elegido.ending = tiempo_actual  # Tiempo de finalización es el tiempo actual
                proceso_elegido.return_ = proceso_elegido.ending - proceso_elegido.arrival  # Calcular TAT
                proceso_elegido.wait = proceso_elegido.return_ - proceso_elegido.burst  # Calcular el tiempo de espera
                finalizado += 1
            else:
                # No hay procesos listos, avanzar el tiempo
                tiempo_actual += 1

    def imprimir_tabla(self):
        """
        Imprime la tabla de llegada y ráfaga de los procesos.
        """
        print("\nTabla de Procesos:")
        print("Proceso\tTiempo de Llegada\tTiempo de Servicio")
        print("-------\t-----------------\t------------------")
        for proceso in self.procesos:
            print(f"  {proceso.nombre}\t\t{proceso.arrival}\t\t\t{proceso.burst}")


    def imprimir_resultados(self):
        """
        Imprime los resultados de los tiempos de espera y retorno de los procesos.
        """
        print("\nProceso\tTiempo de Espera\tTiempo de Retorno\tTiempo de finalizacion")
        print("-------\t-----------------\t------------------")
        total_espera = 0
        total_retorno = 0
        total_finalizacion = 0
        for proceso in self.procesos:
            print(f"  {proceso.nombre}\t\t{proceso.wait}\t\t\t{proceso.return_}\t\t\t{proceso.ending}")
            total_espera += proceso.wait
            total_retorno += proceso.return_
            total_finalizacion += proceso.ending
        print(f"\nTiempo total de espera: {total_espera}")
        print(f"Tiempo total de retorno: {total_retorno}")
        print(f"Tiempo promedio de espera: {total_espera / len(self.procesos):.2f}")
        print(f"Tiempo promedio de retorno: {total_retorno / len(self.procesos):.2f}")
        print(f"Tiempo promedio de finalización: {total_finalizacion / len(self.procesos):.2f}")
    


class RR:
    def __init__(self, process_list):
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

        # Abrir archivo para registrar tiempos de ejecución
        log_file = open("execution_log.txt", "w")
        
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
                            log_file.write(f"Tiempo {time}, Proceso {currently_execution_proccess.id}\n")  # Registro
                            time += quantum
                            print(f'💡 Se aumenta {quantum} al tiempo')
                        else:
                            log_file.write(f"Tiempo {time}, Proceso {currently_execution_proccess.id}\n")  # Registro
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
        
        # Cerrar el archivo después de escribir
        log_file.close()
