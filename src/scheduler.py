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