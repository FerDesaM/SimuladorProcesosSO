# proceso.py
import random

class Proceso:
    def __init__(self, pid, nombre, tiempo_llegada, tiempo_ejecucion):
        self.pid = pid
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.tiempo_restante = tiempo_ejecucion  # Tiempo restante para completar el proceso
        self.estado = "Nuevo"  # Estado del proceso (Nuevo, Ejecutando, Terminando)
    
    def ejecutar(self, quantum=None):
        """Simula la ejecución del proceso."""
        if self.tiempo_restante > 0:
            if quantum and self.tiempo_restante > quantum:
                self.tiempo_restante -= quantum
                self.estado = "Ejecutando"
            else:
                self.tiempo_restante = 0
                self.estado = "Terminado"
            return True
        return False
    
    def reiniciar(self):
        """Reinicia el proceso con su tiempo de ejecución original."""
        self.tiempo_restante = self.tiempo_ejecucion
        self.estado = "Nuevo"
    
    @classmethod
    def crear_proceso(cls, nombre):
        """Método de clase para crear un proceso con valores aleatorios."""
        pid = random.randint(1000, 9999)
        tiempo_llegada = random.randint(0, 10)
        tiempo_ejecucion = random.randint(1, 5)
        return cls(pid, nombre, tiempo_llegada, tiempo_ejecucion)
    
    @classmethod
    def eliminar_proceso(cls, pid, lista_procesos):
        """Método de clase para eliminar un proceso de la lista dado un PID."""
        lista_procesos = [p for p in lista_procesos if p.pid != pid]
        return lista_procesos

    def __str__(self):
        return f"Proceso {self.pid} - {self.nombre}: Llega a {self.tiempo_llegada}, Ejecuta por {self.tiempo_ejecucion} unidades de tiempo."
