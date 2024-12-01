import random

class Proceso:
    def __init__(self, id, nombre, arrival, burst):
        self.id = id            # Identificador del proceso
        self.nombre = nombre    # Nombre del proceso
        self.burst = burst      # Ráfaga de CPU (tiempo de ejecución)
        self.arrival = arrival  # Tiempo de llegada del proceso
        self.burst_tmp = burst  # Copia del tiempo original de la ráfaga
        self.wait = 0           # Tiempo de espera
        self.return_ = 0        # Tiempo de retorno
        self.ending = 0         # Tiempo de finalización

    @classmethod
    def crear(cls, nombre, arrival, burst):
        """Método de clase para crear un proceso con valores específicos."""
        import random
        id = random.randint(1000, 9999)  # Generar un ID aleatorio para el proceso
        return cls(id, nombre, arrival, burst)

    @classmethod
    def eliminar_proceso(cls, id, lista_procesos):
        """Método de clase para eliminar un proceso de la lista dado un ID."""
        # Eliminar el proceso con el ID dado
        lista_procesos = [p for p in lista_procesos if p.id != id]
        print(f"Proceso con ID {id} eliminado.")
        return lista_procesos  # Retornar la lista actualizada de procesos

    def ejecutar(self):
        """Simula la ejecución del proceso"""
        print(f"Ejecutando el proceso {self.id} - {self.nombre}...")
        # Simula que el proceso se ejecuta y se termina después de su ráfaga
        self.ending = self.arrival + self.burst  # El proceso termina después de su ráfaga
        self.return_ = self.ending - self.arrival
        print(f"Proceso {self.id} ejecutado. Finaliza en el tiempo {self.ending}.")

    def __str__(self):
        """Representación del proceso para imprimir información"""
        return f"Proceso {self.id} - {self.nombre} (Llegada: {self.arrival}, Ráfaga: {self.burst})"

